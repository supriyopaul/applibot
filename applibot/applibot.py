import datetime
import asyncio
from fastapi import Query
from langchain.prompts import PromptTemplate
from applibot.utils.misc import compute_sha256, extract_output_block
from applibot.templates import (QUESTION_EXTRACTION_TEMPLATE, QUESTION_RESPONSE_TEMPLATE,
                                COVER_LETTER_TEMPLATE, COVER_LETTER_FILL_TEMPLATE,
                                DM_REPLY_TEMPLATE, EXPRESSION_OF_INTEREST_TEMPLATE,
                                EOI_FILL_TEMPLATE, INFO_FORMATTING_TEMPLATE, DM_REPLY_FILL_TEMPLATE,
                                ANALYSIS_TEMPLATE)

def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

class Applibot:
    INFO_LIMIT = 5

    def __init__(self, config):
        self.embedding = config.objects.embedding
        self.llm = config.objects.llm
        self.resume_store = config.objects.resume_store
        self.info_store = config.objects.info_store

        self.templates = {
            "question_extraction": PromptTemplate(input_variables=["unformatted_info"], template=QUESTION_EXTRACTION_TEMPLATE),
            "question_response": PromptTemplate(input_variables=["questions", "resume", "info_text"], template=QUESTION_RESPONSE_TEMPLATE),
            "cover_letter": PromptTemplate(input_variables=["job_description"], template=COVER_LETTER_TEMPLATE),
            "cover_letter_fill": PromptTemplate(input_variables=["cover_template", "resume", "info_text"], template=COVER_LETTER_FILL_TEMPLATE),
            "dm_reply": PromptTemplate(input_variables=["dm"], template=DM_REPLY_TEMPLATE),
            "dm_reply_fill": PromptTemplate(input_variables=["dm_reply_template", "resume", "info_text"], template=DM_REPLY_FILL_TEMPLATE),
            "expression_of_interest": PromptTemplate(input_variables=["job_description"], template=EXPRESSION_OF_INTEREST_TEMPLATE),
            "eoi_fill": PromptTemplate(input_variables=["eoi_template", "resume", "info_text"], template=EOI_FILL_TEMPLATE),
            "info_formatting": PromptTemplate(input_variables=["unformatted_info"], template=INFO_FORMATTING_TEMPLATE),
            "analysis": PromptTemplate(input_variables=["job_description", "resume", "info_text"], template=ANALYSIS_TEMPLATE)
        }

    async def get_latest_resume(self):
        resumes_df = self.resume_store.table.to_pandas()
        return resumes_df.sort_values(by='timestamp', ascending=False).iloc[0]['text']

    async def get_relevant_info_texts(self, text):
        query_vector = self.embedding.embed_query(text)
        relevant_info_df = self.info_store.table.search(query_vector).limit(self.INFO_LIMIT).to_df()
        return '\n'.join(relevant_info_df['text'].tolist())

    async def format_and_predict(self, template_name, **kwargs):
        prompt = self.templates[template_name].format(**kwargs)
        print(f"Formatted Prompt for {template_name.upper()}:\n", prompt)
        prediction = self.llm.predict(prompt)
        print(f"LLM Prediction for {template_name.upper()}:\n", prediction)
        return extract_output_block(prediction)

    async def post_resume(self, resume_text: str):
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

    async def get_resumes(self, limit: int = Query(10)):
        resumes_df = self.resume_store.table.to_pandas()
        latest_resumes = resumes_df.sort_values(by='timestamp', ascending=False).head(limit)
        return latest_resumes.drop(columns=['vector']).to_dict(orient='records')
    
    async def delete_resume(self, resume_id: str):
        self.resume_store.table.delete(f'id = "{resume_id}"')
        return {"status": "Resume deleted successfully"}

    async def format_info(self, info_text: str):
        return await self.format_and_predict("info_formatting", unformatted_info=info_text)

    async def post_info(self, info_text: str):
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
        latest_resume = await self.get_latest_resume()
        extracted_questions = await self.format_and_predict("question_extraction", unformatted_info=question_text)
        relevant_info_texts = await self.get_relevant_info_texts(extracted_questions)
        answers = await self.format_and_predict("question_response", questions=extracted_questions, resume=latest_resume, info_text=relevant_info_texts)
        return answers

    async def skill_match(self, job_description: str):
        latest_resume = await self.get_latest_resume()
        relevant_info_texts = await self.get_relevant_info_texts(job_description)
        analysis = await self.format_and_predict("analysis", job_description=job_description, resume=latest_resume, info_text=relevant_info_texts)
        return analysis

    async def delete_info(self, info_id: str):
        self.info_store.table.delete(f'id = "{info_id}"')
        return {"status": "Info deleted successfully"}

    async def get_all_info(self):
        infos_df = self.info_store.table.to_pandas()
        return infos_df.drop(columns=['vector']).to_dict(orient='records')

    async def generate_cover_letter(self, job_description: str):
        latest_resume = await self.get_latest_resume()
        cover_letter_template = await self.format_and_predict("cover_letter", job_description=job_description)
        relevant_info_texts = await self.get_relevant_info_texts(cover_letter_template)
        cover_letter = await self.format_and_predict("cover_letter_fill", cover_template=cover_letter_template, resume=latest_resume, info_text=relevant_info_texts)
        return cover_letter
    
    async def reply_to_dm(self, dm: str, job_description: str):
        latest_resume = await self.get_latest_resume()
        dm_response_template = await self.format_and_predict("dm_reply", dm=dm)
        relevant_info_texts = await self.get_relevant_info_texts(dm_response_template)
        dm_response = await self.format_and_predict("dm_reply_fill", dm_reply_template=dm_response_template, resume=latest_resume, info_text=relevant_info_texts)
        return dm_response

    async def generate_eoi(self, job_description: str):
        latest_resume = await self.get_latest_resume()
        eoi_template = await self.format_and_predict("expression_of_interest", job_description=job_description)
        relevant_info_texts = await self.get_relevant_info_texts(eoi_template)
        eoi = await self.format_and_predict("eoi_fill", eoi_template=eoi_template, resume=latest_resume, info_text=relevant_info_texts)
        return eoi