from datetime import timedelta, datetime
from typing import List, Optional
import argparse
import functools

import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status, Header, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from applibot.utils.misc import (compute_sha256, extract_output_block,
                                 print_green, print_orange, print_purple,
                                 print_red, print_yellow)
from applibot.templates import (QUESTION_EXTRACTION_TEMPLATE, QUESTION_RESPONSE_TEMPLATE,
                                COVER_LETTER_TEMPLATE, COVER_LETTER_FILL_TEMPLATE,
                                DM_REPLY_TEMPLATE, DM_REPLY_FILL_TEMPLATE,
                                EXPRESSION_OF_INTEREST_TEMPLATE, EOI_FILL_TEMPLATE,
                                INFO_FORMATTING_TEMPLATE, DM_REPLY_FILL_TEMPLATE,
                                ANALYSIS_TEMPLATE)
from applibot.utils.postgres_store import UserInDB, Resume
from applibot.utils.config_loader import load_config
from applibot.fill_appllication_form import answer_form as fill_form


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
parser = argparse.ArgumentParser(description='Run the Applibot server.')
parser.add_argument('--config', required=True, type=str, help='Path to the configuration YAML file.')
args = parser.parse_args()
config = load_config(args.config)
db_store = config.objects.postgres_store
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.raw.service.token_url)
pwd_context = CryptContext(schemes=config.raw.service.pwd_context_schemes, deprecated=config.raw.service.pwd_context_depricated)
embedding = config.objects.embedding
llm = config.objects.llm
info_store = config.objects.info_store

INFO_RETRIEVAL_LIMIT = 5
ALL_INFO_LIMIT = 1000

templates = {
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

# Pydantic models for requests & responses
class User(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ResumeResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, email: str):
    return db.query(UserInDB).filter(UserInDB.email == email).first()

def create_user(db, user: User):
    fake_hashed_password = get_password_hash(user.password)
    db_user = UserInDB(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.raw.service.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.raw.service.secret_key, algorithm=config.raw.service.hash_algorithm)
    return encoded_jwt

async def format_and_predict(template_name, llm_instance=None, **kwargs):
    if llm_instance is None:
        llm_instance = llm
    prompt = templates[template_name].format(**kwargs)
    print_orange(f"Formatted Prompt for {template_name.upper()}:\n")
    print_purple(prompt)
    prediction = llm_instance.predict(prompt)
    print_orange(f"LLM Prediction for {template_name.upper()}:\n")
    print_green(prediction)
    return extract_output_block(prediction)

def compute_distance(query_vector, v):
    return np.linalg.norm(np.array(v) - query_vector)

async def get_relevant_info_texts(text, user_id):
    query_vector = embedding.embed_query(text)
    user_info = info_store.table.to_pandas()[info_store.table.to_pandas()['user_id'] == f'{user_id}']
    distance_func = functools.partial(compute_distance, query_vector)
    user_info['distance'] = user_info['vector'].apply(distance_func)
    relevant_info_df = user_info.sort_values('distance').head(INFO_RETRIEVAL_LIMIT)
    return '\n'.join(relevant_info_df['text'].tolist())

async def fetch_latest_resume(db: Session, user_id: int):
    latest_resume = db.query(Resume) \
                      .filter(Resume.user_id == user_id) \
                      .order_by(Resume.created_at.desc()) \
                      .first()
    return latest_resume.content

# Dependency
def get_current_user(db: Session = Depends(db_store.get_db), token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.raw.service.secret_key, algorithms=[config.raw.service.hash_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def format_info_helper(unformatted_info_text: str, user_llm):
    return await format_and_predict("info_formatting", llm_instance=user_llm, unformatted_info=unformatted_info_text)

# API endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_store.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.raw.service.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/signup", response_model=User)
async def sign_up(
    user: User,
    db: Session = Depends(db_store.get_db)
):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    create_user(db, user)
    return user

@app.post("/update_openai_key/")
async def update_openai_key(new_openai_key: str = Form(...), current_user: UserInDB = Depends(get_current_user), db: Session = Depends(db_store.get_db)):
    if not new_openai_key.strip():
        raise HTTPException(status_code=400, detail="API key cannot be empty")
    current_user.openai_api_key = new_openai_key.strip()
    db.add(current_user)
    db.commit()
    return {"message": "OpenAI API key updated successfully"}

@app.get("/get_openai_key/")
async def get_openai_key(current_user: UserInDB = Depends(get_current_user)):
    return {"openai_api_key": current_user.openai_api_key}

@app.delete("/delete_openai_key/")
async def delete_openai_key(current_user: UserInDB = Depends(get_current_user), db: Session = Depends(db_store.get_db)):
    current_user.openai_api_key = None
    db.add(current_user)
    db.commit()
    return {"message": "OpenAI API key deleted successfully"}

@app.post("/resume/", response_model=ResumeResponse)
async def upload_resume(
    resume_content: str = Form(...),
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    db_resume = Resume(user_id=current_user.id, content=resume_content)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return {"id": db_resume.id, "content": db_resume.content, "created_at": db_resume.created_at}

@app.get("/resumes/latest", response_model=ResumeResponse)
async def get_latest_resume(
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    latest_resume = db.query(Resume)\
                      .filter(Resume.user_id == current_user.id)\
                      .order_by(Resume.created_at.desc())\
                      .first()
    if not latest_resume:
        raise HTTPException(status_code=404, detail="No resume found")
    return latest_resume

@app.get("/resumes/", response_model=List[ResumeResponse])
async def get_resumes_for_user(
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    user_resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return user_resumes

@app.delete("/resume/", response_model=dict)
async def delete_resume(
    resume_id: int,
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    db_resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    if db_resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this resume")
    db.delete(db_resume)
    db.commit()
    return {"message": f"Resume with id {resume_id} deleted successfully."}

@app.post("/info/")
async def post_info(
    info_text: str = Form(...),
    current_user: UserInDB = Depends(get_current_user)
):
    info_id = compute_sha256(info_text)
    if not info_store.table.search().where(f'user_id="{current_user.id}" AND id="{info_id}"').to_df().empty:
        raise HTTPException(
            status_code=400,
            detail=f"Record with id {info_id} and user_id {current_user.id} already exists in the table."
        )
    formatted_info_text = await format_and_predict("info_formatting", unformatted_info=info_text)
    data = {
        "text": formatted_info_text,
        "id": info_id,
        "vector": embedding.embed_query(formatted_info_text),
        "user_id": current_user.id,
    }
    
    info_store.table.add([data])
    del data['vector']
    return data

@app.post("/format-info/")
async def format_info_endpoint(unformatted_info_text: str = Form(...), current_user: UserInDB = Depends(get_current_user)):
    if not current_user.openai_api_key:
         raise HTTPException(status_code=400, detail="Please update your OpenAI API key before generating responses.")
    user_llm = ChatOpenAI(model=config.raw.chat_model.model_name, temperature=config.raw.chat_model.temperature, openai_api_key=current_user.openai_api_key)
    return await format_info_helper(unformatted_info_text, user_llm)

@app.post("/questions/")
async def post_questions_route(
    question: str = Form(...),
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    if not current_user.openai_api_key:
         raise HTTPException(status_code=400, detail="Please update your OpenAI API key before generating responses.")
    user_llm = ChatOpenAI(model=config.raw.chat_model.model_name, temperature=config.raw.chat_model.temperature, openai_api_key=current_user.openai_api_key)
    latest_resume = await fetch_latest_resume(db, current_user.id)
    extracted_questions = await format_info_helper(question, user_llm)
    # Check if questions were successfully extracted
    if not extracted_questions.strip() or "no questions provided" in extracted_questions.lower():
         raise HTTPException(status_code=400, detail="No questions found in the provided input. Please include questions between '=====Questions start=====' and '=====Questions end====='.")
    relevant_info_texts = await get_relevant_info_texts(extracted_questions, user_id=current_user.id)
    answers = await format_and_predict("question_response", llm_instance=user_llm, questions=extracted_questions, resume=latest_resume, info_text=relevant_info_texts)
    return {"filled_form": answers}

@app.get("/users/infos/")
async def get_user_infos(
    current_user: UserInDB = Depends(get_current_user)
):
    user_infos_df = info_store.table.search().where(f'user_id="{current_user.id}"').limit(ALL_INFO_LIMIT).to_df()
    user_infos_df = user_infos_df.drop(columns=['vector'])
    return user_infos_df.to_dict('records')

@app.delete("/info/")
async def delete_info_route(
    info_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    info_store.table.delete(f'id = "{info_id}" AND user_id="{current_user.id}"')
    return {"status": "Info deleted successfully"}

@app.post("/cover-letter/")
async def generate_cover_letter_route(
    job_description: str = Form(...),
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    if not current_user.openai_api_key:
         raise HTTPException(status_code=400, detail="Please update your OpenAI API key before generating responses.")
    user_llm = ChatOpenAI(model=config.raw.chat_model.model_name, temperature=config.raw.chat_model.temperature, openai_api_key=current_user.openai_api_key)
    latest_resume = await fetch_latest_resume(db, current_user.id)
    cover_letter_template = await format_and_predict("cover_letter", llm_instance=user_llm, job_description=job_description)
    relevant_info_texts = await get_relevant_info_texts(cover_letter_template, user_id=current_user.id)
    cover_letter = await format_and_predict("cover_letter_fill", llm_instance=user_llm,
                                            cover_template=cover_letter_template,
                                            resume=latest_resume,
                                            info_text=relevant_info_texts)
    return cover_letter

@app.post("/dm-reply/")
async def dm_reply_route(
    dm: str = Form(...),
    job_description: str = Form(...),
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    if not current_user.openai_api_key:
         raise HTTPException(status_code=400, detail="Please update your OpenAI API key before generating responses.")
    user_llm = ChatOpenAI(model=config.raw.chat_model.model_name, temperature=config.raw.chat_model.temperature, openai_api_key=current_user.openai_api_key)
    latest_resume = await fetch_latest_resume(db, current_user.id)
    dm_response_template = await format_and_predict("dm_reply", llm_instance=user_llm, dm=dm)
    relevant_info_texts = await get_relevant_info_texts(dm_response_template, user_id=current_user.id)
    dm_response = await format_and_predict("dm_reply_fill", llm_instance=user_llm,
                                           dm_reply_template=dm_response_template,
                                           resume=latest_resume,
                                           info_text=relevant_info_texts)
    return dm_response

@app.post("/eoi/")
async def generate_eoi_route(
    job_description: str = Form(...),
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    if not current_user.openai_api_key:
         raise HTTPException(status_code=400, detail="Please update your OpenAI API key before generating responses.")
    user_llm = ChatOpenAI(model=config.raw.chat_model.model_name, temperature=config.raw.chat_model.temperature, openai_api_key=current_user.openai_api_key)
    latest_resume = await fetch_latest_resume(db, current_user.id)
    eoi_template = await format_and_predict("expression_of_interest", llm_instance=user_llm, job_description=job_description)
    relevant_info_texts = await get_relevant_info_texts(eoi_template, user_id=current_user.id)
    eoi = await format_and_predict("eoi_fill", llm_instance=user_llm,
                                   eoi_template=eoi_template,
                                   resume=latest_resume,
                                   info_text=relevant_info_texts)
    return eoi

@app.post("/skill-match/")
async def skill_match(
    job_description: str = Form(...),
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    if not current_user.openai_api_key:
         raise HTTPException(status_code=400, detail="Please update your OpenAI API key before generating responses.")
    user_llm = ChatOpenAI(model=config.raw.chat_model.model_name, temperature=config.raw.chat_model.temperature, openai_api_key=current_user.openai_api_key)
    latest_resume = await fetch_latest_resume(db, current_user.id)
    relevant_info_texts = await get_relevant_info_texts(job_description, user_id=current_user.id)
    analysis = await format_and_predict("analysis", llm_instance=user_llm,
                                        job_description=job_description,
                                        resume=latest_resume,
                                        info_text=relevant_info_texts)
    return analysis

@app.post("/update_credentials")
async def update_credentials(
    current_password: str = Form(...),
    new_password: str = Form(...),
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.hashed_password = get_password_hash(new_password)
    db.add(current_user)
    db.commit()
    return {"message": "Password updated successfully"}


def main():
    import uvicorn
    uvicorn.run(app,
                host=config.objects.service.host,
                port=config.objects.service.port,
                workers=config.objects.service.workers,
                )

if __name__ == "__main__":
    main()
