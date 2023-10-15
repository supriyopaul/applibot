import datetime
from fastapi import Query

from applibot.utils.misc import compute_sha256, extract_output_block
from langchain.prompts import PromptTemplate

INFO_FORMATTING_TEMPLATE = """
From the given user information input, which may be poorly formatted, empty, or partially filled out:
=====Input start=====
{unformatted_info}
=====Input end=====
Reformat the information and values to adhere to the specified format: <Field: Value>.
Value any field not found in the above given information should be filled as "Not sure!".
Your output should strictly follow the example provided below:
=====Output start=====
Name: John Doe
Total experience in years: 6
Highest Level of Education: Bachelor's Degree
Skills: Project Management, Agile Methodologies, Scrum
Previous Employer: TechCorp
Email: john.doe@example.com
Passport: Not sure!
...
=====Output end=====
"""

QUESTION_RESPONSE_TEMPLATE = """
Given the set of questions and user-provided information, extract and format the answers to the questions using the user's information:
=====Questions start=====
{questions}
=====Questions end=====
From the user's information:
=====Input start=====
{info_text}
=====Input end=====
Format the answers to the questions in the format: <Question: Answer>. If an answer to a question is not found in the user's information, fill it as "Not sure!".
Your output should strictly follow the example provided below:
=====Output start=====
What is your name?: John Doe
How many years of experience do you have?: 6
What's your highest level of education?: Bachelor's Degree
List some of your skills: Project Management, Agile Methodologies, Scrum
Who was your previous employer?: TechCorp
What's your email address?: john.doe@example.com
Do you have a passport?: Not sure!
...
=====Output end=====
"""

QUESTION_EXTRACTION_TEMPLATE = """
From the provided unformatted information:
=====Input start=====
{unformatted_info}
=====Input end=====
Extract key details and frame them as empty questions. Your output should help in understanding what kind of details can be extracted from the given unformatted information. Present the questions in a list format.
=====Output start=====
- What is the name?
- How many years of experience does the individual have?
- What is the highest level of education achieved?
- Can you list some of the skills?
...
=====Output end=====
"""



class Applibot:
    def __init__(self, config):
        self.embedding = config.objects.embedding
        self.llm = config.objects.llm
        self.resume_store = config.objects.resume_store
        self.info_store = config.objects.info_store

    async def post_resume(self, resume_text: str):
        """API to post a resume text."""
        data = {
            "vector": self.embedding.embed_query(resume_text),
            "text": resume_text,
            "id": compute_sha256(resume_text),
            "timestamp": int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
        }
        self.resume_store.table.add([data])
        resumes = self.resume_store.table.to_pandas().sort_values(by='timestamp')
        latest_resume = resumes.iloc[-1]
        latest_resume = latest_resume.to_dict()
        latest_resume.pop('vector')
        return latest_resume

    async def get_resumes(self, limit: int = Query(10, description="Limit to get the last n uploaded resumes")):
        """API to get the last n uploaded resumes."""
        resumes_df = self.resume_store.table.to_pandas()
        latest_resumes = resumes_df.sort_values(by='timestamp', ascending=False).head(limit)
        return latest_resumes.drop(columns=['vector']).to_dict(orient='records')
    
    async def delete_resume(self, resume_id: str):
        """Delete a resume based on its id."""
        self.resume_store.table.delete(f'id = "{resume_id}"')
        return {"status": "Resume deleted successfully"}

    async def format_info(self, info_text: str):
        """API to format info"""
        form_formatting_template = PromptTemplate.from_template(INFO_FORMATTING_TEMPLATE)
        form_formatting_template = form_formatting_template.format(unformatted_info=info_text)
        formatted_form_text = self.llm.predict(form_formatting_template)
        return extract_output_block(formatted_form_text)
    
    async def post_info(self, info_text: str):
        """API to post an info text."""
        info_id = compute_sha256(info_text)
        data = {
            "text": info_text,
            "id": info_id,
            "vector": self.embedding.embed_query(info_text),
        }
        self.info_store.table.add([data])
        infos = self.info_store.table.to_pandas().drop(columns=['vector'])
        matching_info = infos[infos['id'] == info_id].iloc[0]
        return matching_info.to_dict()

    async def post_questions(self, question_text: str, limit: int = Query(5, description="Limit to get the nearest k info docs")):
        """API to retrieve info based on a query string."""
        query_vector = self.embedding.embed_query(question_text)
        results = self.info_store.table.search(query_vector).limit(limit).to_df().drop(columns=['vector']).to_dict(orient='records')
        return results

    async def delete_info(self, info_id: str):
        """Delete an info based on its id."""
        self.info_store.table.delete(f'id = "{info_id}"')
        return {"status": "Info deleted successfully"}