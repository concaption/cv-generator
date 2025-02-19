"""
path: app/routers/main.py

This file contains the main router for the application.
"""

from fastapi import APIRouter, Request, BackgroundTasks, File, UploadFile, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from starlette.responses import Response
from app.asi import ASI_CV
from app.schema import Profile, RawProfile
from app.config import settings

import os

router = APIRouter()
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)



@router.post("/")
async def create_cv(profile: Profile, file_format: str = "pdf", output_type: str = "url"):
    asi_cv = ASI_CV()
    asi_cv._add_name_title(profile.Name, profile.Title)
    for qualification in profile.Qualifications:
        asi_cv._add_qualification(qualification.Degree, qualification.Field, qualification.Institution, str(qualification.Year))
    for skill in profile.TechnicalSkills:
        asi_cv._add_technical_skill(skill)
    for language in profile.Languages:
        asi_cv._add_language(language.Language, language.Proficiency)
    for country in profile.Countries:
        asi_cv._add_country(country)
    for summary in profile.SummaryOfExperience:
        asi_cv._add_summary_of_experience(summary)
    for experience in profile.Experiences:
        asi_cv._add_experience(str(experience.DateRange), experience.Position, experience.Organisation, experience.Location, experience.Summary, experience.IsSelected)
    try:
        output = asi_cv.generate_cv(file_format=file_format, output_type=output_type, bucket_name=settings.BUCKET_NAME, folder=settings.BUCKET_FOLDER, credentials=settings.CREDENTIALS)
        if output_type == "url":
            return {"url": output}
        if output_type == "file":
            if file_format == "docx":
                print("docx")
                return Response(content=output, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            if file_format == "pdf":
                return Response(content=output, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/" , response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@router.post("/raw_data")
async def for_raw_data(profile: RawProfile, file_format: str = "pdf", output_type: str = "url"):
    asi_cv = ASI_CV()
    asi_cv._add_name_title(profile.Name, profile.Title)
    qualifications = profile.Qualifications.replace("•", "").split("|")
    for qualification in qualifications:
        # degree, field, institution, year = qualification.split(",")
        # asi_cv._add_qualification(degree, field, institution, year)
        asi_cv._add_raw_qualification(qualification)
    for skill in profile.TechnicalSkills:
        asi_cv._add_technical_skill(skill)
    # language are in this format English (excellent), French (basic)
    # split by comma and then by space
    languages = profile.Languages.split(",")
    for language in languages:
        language, proficiency = language.split(" (")
        proficiency = proficiency.replace(")", "")
        asi_cv._add_language(language, proficiency)
    for country in profile.Countries:
        asi_cv._add_country(country)
    summary_of_experiences = profile.SummaryOfExperience.split("||")
    for summary in summary_of_experiences:
        asi_cv._add_summary_of_experience(summary)
    experiences_years = profile.ExperienceYears.split(",")
    experiences_headers = profile.ExperienceHeader.split("|")
    experiences_content = profile.ExperienceContent.split("#")
    # make length of experiences_years and experiences_headers the same
    if len(experiences_years) > len(experiences_headers):
        experiences_headers = experiences_headers + [""] * (len(experiences_years) - len(experiences_headers))
    if len(experiences_headers) > len(experiences_years):
        experiences_years = experiences_years + [""] * (len(experiences_headers) - len(experiences_years))
    for i, experience_header in enumerate(experiences_headers):
        if len(experiences_years) > i:
            date_range = experiences_years[i]
            asi_cv._add_raw_experience(date_range, experience_header, experiences_content[i])
            # asi_cv._add_experience(date_range, position, organisation, location, experiences_content[i], True)
    try:
        output = asi_cv.generate_cv(file_format=file_format, output_type=output_type, bucket_name=settings.BUCKET_NAME, folder=settings.BUCKET_FOLDER, credentials=settings.CREDENTIALS)
        if output_type == "url":
            return {"url": output}
        if output_type == "file":
            if file_format == "docx":
                print("docx")
                return Response(content=output, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            if file_format == "pdf":
                return Response(content=output, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
