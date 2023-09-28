from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl
from enum import Enum

class Gender(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    NON_BINARY = 'Non-Binary'
    OTHER = 'Other'
    PREFER_NOT_TO_SAY = 'Prefer not to say'

class SkillLevel(str, Enum):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

class Education(BaseModel):
    institution: str
    degree: str
    major: Optional[str] = None  # Making major optional
    start_date: datetime
    end_date: Optional[datetime]
    gpa: Optional[float]

class WorkExperience(BaseModel):
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime]
    responsibilities: List[str]

class Skill(BaseModel):
    name: str
    level: SkillLevel
    experience_years: float

class Resume(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    address: str
    gender: Gender
    total_experience: float
    linkedin: HttpUrl
    github: HttpUrl
    website: Optional[HttpUrl] = None
    summary: str
    education: List[Education]
    work_experience: List[WorkExperience]
    skills: List[Skill]
    languages: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    hobbies: Optional[List[str]] = None
    references: Optional[List[str]] = None

if __name__ == "__main__":
    resume = Resume(
        full_name='John Doe',
        email='john.doe@example.com',
        phone_number='123-456-7890',
        address='123 Street, City, State, ZIP',
        gender=Gender.MALE,
        total_experience=5.0,
        linkedin='https://www.linkedin.com/in/johndoe/',
        github='https://github.com/johndoe',
        summary='Experienced software engineer...',
        education=[
            Education(
                institution='University XYZ',
                degree='Bachelor of Science in Computer Science',
                start_date=datetime(2015, 8, 1),
                end_date=datetime(2019, 5, 31),
                gpa=3.5
            )
        ],
        work_experience=[
            WorkExperience(
                company='ABC Corp',
                position='Software Engineer',
                start_date=datetime(2019, 6, 1),
                end_date=datetime(2022, 9, 24),
                responsibilities=['Develop software', 'Write tests']
            )
        ],
        skills=[
            Skill(name='Python', level=SkillLevel.ADVANCED, experience_years=5.0)
        ]
    )

    print(resume.model_dump_json(indent=4))
