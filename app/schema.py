from typing import List, Optional
from pydantic import BaseModel, Field

class Qualification(BaseModel):
    Degree: str
    Field: str
    Institution: str
    Year: str

class Language(BaseModel):
    Language: str
    Proficiency: str

class Experience(BaseModel):
    DateRange: str
    Position: str
    Organisation: str
    Location: str
    Summary: str
    IsSelected: Optional[bool] = None

class Profile(BaseModel):
    Name: str
    Title: str
    Qualifications: List[Qualification]
    TechnicalSkills: List[str] = Field(..., example=["Skill1", "Skill2"])
    Languages: List[Language]
    Countries: List[str]
    SummaryOfExperience: List[str]
    Experiences: List[Experience]

class RawProfile(BaseModel):
    Name: str
    Title: str
    Qualifications: str
    TechnicalSkills: List[str] = Field(..., example=["Skill1", "Skill2"])
    Languages: str
    Countries: List[str]
    SummaryOfExperience: str
    ExperienceHeader: str
    ExperienceContent: str
