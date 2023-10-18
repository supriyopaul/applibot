import datetime
import asyncio

from fastapi import Query
from langchain.prompts import PromptTemplate
from applibot.utils.misc import compute_sha256, extract_output_block, check_formatted_info
from applibot.templates import QUESTION_EXTRACTION_TEMPLATE, QUESTION_RESPONSE_TEMPLATE, COVER_LETTER_TEMPLATE, COVER_LETTER_FILL_TEMPLATE, DM_REPLY_TEMPLATE, EXPRESSION_OF_INTEREST_TEMPLATE, EOI_FILL_TEMPLATE, INFO_FORMATTING_TEMPLATE

def run(coro): return asyncio.get_event_loop().run_until_complete(coro)

class Applibot:
    INFO_LIMIT = 5

    def __init__(self, config):
        self.embedding = config.objects.embedding
        self.llm = config.objects.llm
        self.resume_store = config.objects.resume_store
        self.info_store = config.objects.info_store

        self.question_extraction_template = PromptTemplate(input_variables=["unformatted_info"], template=QUESTION_EXTRACTION_TEMPLATE)
        self.question_response_template = PromptTemplate(input_variables=["questions", "resume", "info_text"], template=QUESTION_RESPONSE_TEMPLATE)
        self.cover_letter_template = PromptTemplate(input_variables=["job_description"], template=COVER_LETTER_TEMPLATE)
        self.cover_letter_fill_template = PromptTemplate(input_variables=["cover_template", "resume", "info_text"], template=COVER_LETTER_FILL_TEMPLATE)
        self.dm_reply_template = PromptTemplate(input_variables=["dm"], template=DM_REPLY_TEMPLATE)
        self.expression_of_interest_template = PromptTemplate(input_variables=["details"], template=EXPRESSION_OF_INTEREST_TEMPLATE)
        self.eoi_fill_template = PromptTemplate(input_variables=["eoi_template", "resume", "info_text"], template=EOI_FILL_TEMPLATE)
        self.info_formatting_template = PromptTemplate(input_variables=["unformatted_info"], template=INFO_FORMATTING_TEMPLATE)

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
        formatted_prompt = form_formatting_template.format(unformatted_info=info_text)
        print("Formatted Prompt for INFO_FORMATTING_TEMPLATE:\n", formatted_prompt)
        formatted_form_text = self.llm.predict(formatted_prompt)
        print("LLM Prediction for INFO_FORMATTING_TEMPLATE:\n", formatted_form_text)
        return extract_output_block(formatted_form_text)
    
    async def post_info(self, info_text: str):
        """API to post an info text."""
        #formatted, reason = check_formatted_info(text=info_text)
        #if not formatted:
            #print(reason)
            #info_text = await self.format_info(info_text=info_text)
        info_text = await self.format_info(info_text=info_text)
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

    async def post_questions(self, question_text: str):
        """API to retrieve info based on a query string."""
        resumes_df = self.resume_store.table.to_pandas()
        latest_resume = resumes_df.sort_values(by='timestamp', ascending=False).loc[0, 'text']

        question_extraction_prompt = self.question_extraction_template.format(unformatted_info=question_text)
        print("Formatted Prompt for QUESTION_EXTRACTION_TEMPLATE:\n", question_extraction_prompt)
        extracted_questions = extract_output_block(self.llm.predict(question_extraction_prompt))
        print("LLM Prediction for QUESTION_EXTRACTION_TEMPLATE:\n", extracted_questions)
        query_vector = self.embedding.embed_query(extracted_questions)
        relevant_info_df = self.info_store.table.search(query_vector).limit(self.INFO_LIMIT).to_df()
        relevant_info_texts = '\n'.join(relevant_info_df['text'].tolist())
        question_response_prompt = self.question_response_template.format(questions=extracted_questions, resume=latest_resume, info_text=relevant_info_texts)
        print("Formatted Prompt for QUESTION_RESPONSE_TEMPLATE:\n", question_response_prompt)
        answers = self.llm.predict(question_response_prompt)
        print("LLM Prediction for QUESTION_RESPONSE_TEMPLATE:\n", answers)
        return extract_output_block(answers)

    async def delete_info(self, info_id: str):
        """Delete an info based on its id."""
        self.info_store.table.delete(f'id = "{info_id}"')
        return {"status": "Info deleted successfully"}
    
    async def get_all_info(self):
        """API to get all the info from the info table."""
        infos_df = self.info_store.table.to_pandas()
        return infos_df.drop(columns=['vector']).to_dict(orient='records')
    
    async def generate_cover_letter(self, job_description: str):
        """API to generate a cover letter based on a job description."""
        resumes_df = self.resume_store.table.to_pandas()
        latest_resume = resumes_df.sort_values(by='timestamp', ascending=False).loc[0, 'text']
    
        cover_letter_prompt = self.cover_letter_template.format(job_description=job_description)
        print("Formatted Prompt for COVER_LETTER_TEMPLATE:\n", cover_letter_prompt)
        cover_letter_template = extract_output_block(self.llm.predict(cover_letter_prompt))
        print("LLM Prediction for COVER_LETTER_TEMPLATE:\n", cover_letter_template)
        query_vector = self.embedding.embed_query(cover_letter_template)
        relevant_info_df = self.info_store.table.search(query_vector).limit(self.INFO_LIMIT).to_df()
        relevant_info_texts = '\n'.join(relevant_info_df['text'].tolist())
        cover_letter_fill_prompt = self.cover_letter_fill_template.format(cover_template=cover_letter_template, resume=latest_resume, info_text=relevant_info_texts)
        print("Formatted Prompt for COVER_FILL_TEMPLATE:\n", cover_letter_fill_prompt)
        cover_letter = self.llm.predict(cover_letter_fill_prompt)
        print("LLM Prediction for COVER_FILL_TEMPLATE:\n", cover_letter)
        return extract_output_block(cover_letter)
    
    async def reply_to_dm(self, dm: str, job_description: str):
        """API to generate a response based on the recruiter's DM and job description."""
        resumes_df = self.resume_store.table.to_pandas()
        latest_resume = resumes_df.sort_values(by='timestamp', ascending=False).loc[0, 'text']
    
        dm_reply_prompt = self.dm_reply_template.format(dm=dm)
        print("Formatted Prompt for DM_REPLY_TEMPLATE:\n", dm_reply_prompt)
        dm_response_template = extract_output_block(self.llm.predict(dm_reply_prompt))
        print("LLM Prediction for DM_REPLY_TEMPLATE:\n", dm_response_template)
        query_vector = self.embedding.embed_query(dm_response_template)
        relevant_info_df = self.info_store.table.search(query_vector).limit(self.INFO_LIMIT).to_df()
        relevant_info_texts = '\n'.join(relevant_info_df['text'].tolist())
        cover_letter_fill_prompt = self.cover_letter_fill_template.format(cover_template=dm_response_template, resume=latest_resume, info_text=relevant_info_texts)
        print("Formatted Prompt for COVER_FILL_TEMPLATE:\n", cover_letter_fill_prompt)
        dm_response = self.llm.predict(cover_letter_fill_prompt)
        print("LLM Prediction for COVER_FILL_TEMPLATE:\n", dm_response)
        return extract_output_block(dm_response)
    
    async def generate_eoi(self, details: str):
        """API to generate an Expression of Interest letter based on company/field details."""
        resumes_df = self.resume_store.table.to_pandas()
        latest_resume = resumes_df.sort_values(by='timestamp', ascending=False).loc[0, 'text']
    
        eoi_prompt = self.expression_of_interest_template.format(details=details)
        print("Formatted Prompt for EXPRESSION_OF_INTEREST_TEMPLATE:\n", eoi_prompt)
        eoi_template = extract_output_block(self.llm.predict(eoi_prompt))
        print("LLM Prediction for EXPRESSION_OF_INTEREST_TEMPLATE:\n", eoi_template)
        query_vector = self.embedding.embed_query(eoi_template)
        relevant_info_df = self.info_store.table.search(query_vector).limit(self.INFO_LIMIT).to_df()
        relevant_info_texts = '\n'.join(relevant_info_df['text'].tolist())
        eoi_fill_prompt = self.eoi_fill_template.format(eoi_template=eoi_template, resume=latest_resume, info_text=relevant_info_texts)
        print("Formatted Prompt for EOI_FILL_TEMPLATE:\n", eoi_fill_prompt)
        eoi = self.llm.predict(eoi_fill_prompt)
        print("LLM Prediction for EOI_FILL_TEMPLATE:\n", eoi)
        return extract_output_block(eoi)