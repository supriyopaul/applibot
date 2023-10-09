import datetime
from fastapi import Query

from applibot.utils.misc import compute_sha256
from applibot.utils.lancedb_store import ResumeSchema

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