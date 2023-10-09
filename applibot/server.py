from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
import argparse

from applibot.applibot import Applibot
from applibot.utils.config_loader import load_config

app = FastAPI()
bot_instance = None

def get_applibot():
    global bot_instance
    return bot_instance

@app.post("/resume/")
async def post_resume_route(resume_text: str, applibot: Applibot = Depends(get_applibot)):
    return await applibot.post_resume(resume_text)

@app.get("/resumes/")
async def get_resumes_route(limit: int = Query(10), applibot: Applibot = Depends(get_applibot)):
    return await applibot.get_resumes(limit)

@app.delete("/resume/{resume_id}/")
async def delete_resume_route(resume_id: str, applibot: Applibot = Depends(get_applibot)):
    return await applibot.delete_resume(resume_id)

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
