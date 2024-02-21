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
from app.schema import Profile

import os

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/")
async def create_cv(profile: Profile, file_format: str = "pdf", output_type: str = "file"):
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
    pdf_bytes = asi_cv.generate_cv()
    output = asi_cv.generate_cv(file_format=file_format, output_type=output_type)
    if output_type == "file":
        if file_format == "docx":
            print("docx")
            return Response(content=output, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        if file_format == "pdf":
            return Response(content=output, media_type="application/pdf")

@router.get("/generate_example")
async def generate_example():
    data = { 
        "Name": "Rosaline Adey",
        "Title": "Procurement Consultant",
        "Qualifications":
        [{
        "Degree": "D.Phil.",
        "Field": "Economics",
        "Institution": "University of Oxford",
        "Year": "2000"
        },
        {
        "Degree": "M.Phil.",
        "Field": "Economics",
        "Institution": "University of Cambridge",
        "Year": "1994"
        },
        {
        "Degree": "BSC",
        "Field": "Economics/Mathematics/Statistics",
        "Institution": "Makerere University",
        "Year": "1991"
        }
    ],
    "TechnicalSkills": [
        "Computable General Equilibrium Modelling",
        "Econometric modelling",
        "Programming",
        "Fiscal Policy Analysis",
        "Macroeconomic Analysis",
        "Policy Development",
        "Public Financial Management",
        "Research and Analysis",
        "Economic Policy",
        "Data Collection",
        "Training",
        "Lecturing",
        "Consultancy"
    ],
    "Languages": [
        {
        "Language": "English",
        "Proficiency": "Fluent"
        },
        {
        "Language": "French",
        "Proficiency": "Intermediate"
        },
        {
        "Language": "Luganda",
        "Proficiency": "Native"
        }
    ],
    "Countries": [
        "Sierra Leone",
        "Cote D’Ivoire",
        "Kazakhstan",
        "Kyrgyzstan",
        "Philippines",
        "Tajikistan",
        "Togo"
    ],
    "SummaryOfExperience": [
        "Rosaline Adey is a renowned procurement consultant with over 12 years of experience working within government and NGOs on the fields of procurement, PFM, and supply chain programmes, aiming to enhance the procurement procedures of different countries, including Sierra Leone. She has worked closely with a diverse and complex range of partners and stakeholders, including governments, international donors, civil society, and the private sector. Her past experiences working with different stakeholders have honed her understanding of the intricacies associated with the procurement process and have enabled her to use her knowledge to improve efficiency and the effectiveness of the procurement systems.",
        "Rosie has worked extensively with the Government of Sierra Leone (GoSL) to develop their procurement systems. This is evidenced by her work as a Procurement Adviser on projects such as the EU-funded State Building Contract Technical Assistance and FCDO-funded Building Core Systems projects. Under these roles, Rosie worked updating the manual for public sector procurement in line with the revised Act and Regulations. She also provided procurement training for staff in the Procurement Regulatory Authority (PRA) and developed a Strategic Action Improvement Plan for all stakeholders of the public procurement system in Sierra Leone including policymakers, procurement officers, the private sector and civil society. She also carried out in-depth analytical tasks on ways to improve efficiency across the procurement system by developing a range of related documents on procurement issues and increasing long-term value for money.",
        "In addition, Rosie has experience in the analysis of PFM in developing countries, including public expenditure-related assessments such as PEFA and the OECD’s methodology for assessing public procurement systems. She has extensive knowledge of donor procurement rules, regulations, policies, procedures, institutional structures, performance measurement, and good practices of national and international public procurement systems including public-private partnerships."
    ],
    "Experiences": [
        {
            "DateRange": "2022 – present",
            "Position": "Project Management Lead",
            "Organisation": "USAID/Global Environment & Technology Foundation (GETF)",
            "Location": "Sierra Leone",
            "Summary": "Rosaline is leading the implementation, stakeholder engagement, and overall project management to ensure the scope and direction of the project is on schedule, and in line with client expectation; managing in-country stakeholder relationships-national counterparts, program implementing partners, the USAID and other donor partners- to achieve project success; coordinating inputs and alignment across national/donor health supply chain stakeholder landscape and the PLM project team; ensuring the implementation of the technical and strategic aspects of the project.",
            "IsSelected": "True"
        },
        {
            "DateRange": "2021 – 2022",
            "Position": "Project Sponsor",
            "Organisation": "African Development Bank",
            "Location": "Sierra Leone",
            "Summary": "Rosaline was responsible for the overall project management and implementation of the project, including the development of project plans, budgets, and schedules; managing the project team to ensure the project is delivered on time and within budget; ensuring the project delivers the expected outcomes and benefits; and ensuring the project is effectively resourced and managed to deliver the expected outcomes.",
            "IsSelected": "True"
        },
        {
            "DateRange": "2021",
            "Position": "Senior Public Financial Management Expert",
            "Organisation": "B&S Europe",
            "Location": "Sierra Leone",
            "Summary": "Rosaline was responsible for providing technical assistance to the Ministry of Finance in Sierra Leone to improve the public financial management system. She provided technical assistance to the Ministry of Finance to improve the public financial management system, including the development of a public financial management reform strategy, and the development of a public financial management reform action plan.",
            "IsSelected": "True"
        },
        {
            "DateRange": "2020",
            "Position": "Consultant",
            "Organisation": "Oxford Policy Management",
            "Location": "Sierra Leone",
            "Summary": "Rosaline was responsible for providing technical assistance to the Ministry of Finance in Sierra Leone to improve the public financial management system. She provided technical assistance to the Ministry of Finance to improve the public financial management system, including the development of a public financial management reform strategy, and the development of a public financial management reform action plan."

        },
        {
            "DateRange": "2018 – 2019",
            "Position": "Procurement Adviser",
            "Organisation": "State Building Contract Technical Assistance",
            "Location": "EU, Sierra Leone",
            "Summary": "Rosaline was responsible for providing technical assistance to the Ministry of Finance in Sierra Leone to improve the public financial management system. She provided technical assistance to the Ministry of Finance to improve the public financial management system, including the development of a public financial management reform strategy, and the development of a public financial management reform action plan."
        },
        {
            "DateRange": "2016 – 2017",
            "Position": "Procurement Adviser",
            "Organisation": "Building Core Systems (BCS) Project",
            "Location": "FCDO, Sierra Leone",
            "Summary": "Rosaline was responsible for providing technical assistance to the Ministry of Finance in Sierra Leone to improve the public financial management system. She provided technical assistance to the Ministry of Finance to improve the public financial management system, including the development of a public financial management reform strategy, and the development of a public financial management reform action plan."
        },
        {
            "DateRange": "2016",
            "Position": "Project Coordinator",
            "Organisation": "The Learning Foundation",
            "Location": "Sierra Leone",
            "Summary": "Rosaline was responsible for providing technical assistance to the Ministry of Finance in Sierra Leone to improve the public financial management system. She provided technical assistance to the Ministry of Finance to improve the public financial management system, including the development of a public financial management reform strategy, and the development of a public financial management reform action plan."
        },
        {
            "DateRange": "2015 – 2016",
            "Position": "Consultant",
            "Organisation": "TCC Investment Partners",
            "Location": "UK",
            "Summary": "Rosaline was responsible for providing technical assistance to the Ministry of Finance in Sierra Leone to improve the public financial management system. She provided technical assistance to the Ministry of Finance to improve the public financial management system, including the development of a public financial management reform strategy, and the development of a public financial management reform action plan."
        },
        {
            "DateRange": "2012 – 2014",
            "Position": "Consultant",
            "Organisation": "Crown Agents",
            "Location": "UK",
            "Summary": "Rosaline was responsible for providing technical assistance to the Ministry of Finance in Sierra Leone to improve the public financial management system. She provided technical assistance to the Ministry of Finance to improve the public financial management system, including the development of a public financial management reform strategy, and the development of a public financial management reform action plan."
        },
    ]
    }
    return data

    
