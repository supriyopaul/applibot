from fastapi import FastAPI, Depends, Query, Form
import argparse

from applibot.applibot import Applibot
from applibot.utils.config_loader import load_config

app = FastAPI()
bot_instance = None

def get_applibot():
    global bot_instance
    return bot_instance

@app.post("/resume/")
async def post_resume_route(resume_text: str = Form(...), applibot: Applibot = Depends(get_applibot)):
    return await applibot.post_resume(resume_text)

@app.get("/resumes/")
async def get_resumes_route(limit: int = Query(10), applibot: Applibot = Depends(get_applibot)):
    return await applibot.get_resumes(limit)

@app.delete("/resume/{resume_id}/")
async def delete_resume_route(resume_id: str, applibot: Applibot = Depends(get_applibot)):
    return await applibot.delete_resume(resume_id)

@app.post("/info/")
async def post_info_route(info_text: str = Form(...), applibot: Applibot = Depends(get_applibot)):
    return await applibot.post_info(info_text)

@app.post("/format-info/")
async def format_info_route(info_text: str = Form(...), applibot: Applibot = Depends(get_applibot)):
    return {"formatted_text": await applibot.format_info(info_text)}

@app.post("/questions/")
async def post_questions_route(question: str = Form(...), applibot: Applibot = Depends(get_applibot)):
    return await applibot.post_questions(question)

@app.delete("/info/{info_id}/")
async def delete_info_route(info_id: str, applibot: Applibot = Depends(get_applibot)):
    return await applibot.delete_info(info_id)

@app.post("/cover-letter/")
async def generate_cover_letter_route(job_description: str = Form(...), applibot: Applibot = Depends(get_applibot)):
    return await applibot.generate_cover_letter(job_description)

@app.post("/dm-reply/")
async def dm_reply_route(dm: str = Form(...), job_description: str = Form(...), applibot: Applibot = Depends(get_applibot)):
    return await applibot.reply_to_dm(dm, job_description)

@app.post("/eoi/")
async def generate_eoi_route(job_description: str = Form(...), applibot: Applibot = Depends(get_applibot)):
    """Route to generate an Expression of Interest letter based on company/field details."""
    return await applibot.generate_eoi(job_description)

async def export_info(self):
    """API to export all the info from the info store."""
    return await self.get_all_info()

async def import_info(self, info_list: list):
    """API to import a list of info to the info store."""
    for info in info_list:
        await self.post_info(info_text=info['text'])
    return {"status": "Info imported successfully"}

def main():
    parser = argparse.ArgumentParser(description='Run the resume server.')
    parser.add_argument('--config', required=True, type=str, help='Path to the configuration YAML file.')
    args = parser.parse_args()
    global bot_instance
    config = load_config(args.config)
    bot_instance = Applibot(config)

    import uvicorn
    uvicorn.run(app, host=config.objects.service.host, port=config.objects.service.port)  # Adjust this based on your needs or load it from your config.

if __name__ == "__main__":
    main()