from fastapi import FastAPI, Depends, Query
import argparse

from applibot.applibot import Applibot
from applibot.applibot import Resume, Info, Question
from applibot.utils.config_loader import load_config

app = FastAPI()
bot_instance = None

def get_applibot():
    global bot_instance
    return bot_instance

@app.post("/resume/")
async def post_resume_route(resume: Resume, applibot: Applibot = Depends(get_applibot)):
    return await applibot.post_resume(resume.text)

@app.get("/resumes/")
async def get_resumes_route(limit: int = Query(10), applibot: Applibot = Depends(get_applibot)):
    return await applibot.get_resumes(limit)

@app.delete("/resume/{resume_id}/")
async def delete_resume_route(resume_id: str, applibot: Applibot = Depends(get_applibot)):
    return await applibot.delete_resume(resume_id)

@app.post("/info/")
async def post_info_route(info: Info, applibot: Applibot = Depends(get_applibot)):
    return await applibot.post_info(info.text)

@app.post("/format-info/")
async def format_info_route(info: Info, applibot: Applibot = Depends(get_applibot)):
    return {"formatted_text": await applibot.format_info(info.text)}

@app.get("/info/")
async def get_info_route(question: Question, limit: int = Query(5), applibot: Applibot = Depends(get_applibot)):
    return await applibot.get_info(question.text, limit)

@app.delete("/info/{info_id}/")
async def delete_info_route(info_id: str, applibot: Applibot = Depends(get_applibot)):
    return await applibot.delete_info(info_id)

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
