from typing import List
from datetime import timedelta, datetime
from typing import Optional
import argparse

from fastapi import FastAPI, Depends, HTTPException, status, Header, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from applibot.utils.postgres_store import UserInDB, Resume
from applibot.utils.config_loader import load_config

parser = argparse.ArgumentParser(description='Run the resume server.')
parser.add_argument('--config', required=True, type=str, help='Path to the configuration YAML file.')
args = parser.parse_args()
config = load_config(args.config)

# Database setup
db_store = config.objects.postgres_store

# FastAPI app
app = FastAPI()

# Dependency for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.raw.service.token_url)

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

# Security
pwd_context = CryptContext(schemes=config.raw.service.pwd_context_schemes, deprecated=config.raw.service.pwd_context_depricated)

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

# API endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_store.get_db)):
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
async def sign_up(user: User, db: Session = Depends(db_store.get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    create_user(db, user)
    return user

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

@app.get("/users/{user_id}/resumes/", response_model=List[ResumeResponse])
async def get_resumes_for_user(
    user_id: int,
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(db_store.get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view these resumes")
    db_resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
    return db_resumes

@app.delete("/resume/{resume_id}/", response_model=dict)
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


# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.raw.service.host, port=config.raw.service.port)
