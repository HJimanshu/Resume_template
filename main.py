from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import pdfkit
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Set Jinja2 template directory
templates = Jinja2Templates(directory="templates")

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
# pdfkit.from_string(templates, output_path, configuration=config)
# @app.get("/download/simple-cv")
# def download_simple_cv():
#     file_path = os.path.join("static", "himanshu_cv.pdf")
#     print("Trying to serve file:", file_path)
#     return FileResponse(path=file_path, filename="Himanshu_Resume.pdf", media_type="application/pdf")

@app.post("/generate-cv/")
async def generate_cv(request: Request, option: str = Form(...)):
    if option == "simple":
        return FileResponse("static/himanshu_cv.pdf", filename="Simple_CV.pdf", media_type="application/pdf")
    
    elif option == "template":
        print("Rendering template...")
        # Render the resume_template.html with context data
        rendered = templates.get_template("resume_template.html").render({
            "name": "Himanshu",
            "role": "Web developer",
            "social_links": {
            "facebook": "https://facebook.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://linkedin.com/in/your-profile",
            "instagram": "https://instagram.com"
            },
            "about": "Hii, I'm Himanshu,a Python web developer with 1.2 years of experience,specializing in Python frameworks. I aim to contribute to a company’s growth while advancing my professionaldevelopment and career.",
            "work_experience": [
               {"date": "10/2024 - 02/2025", "title": "Software Engineer Associate - Blackcoffer", "desc": "Developed FastAPI-based APIs for fetching and analyzing GCP SQL and VM logs with BigQuery integration and cost insights via Google Recommendations API; contributed to a FastAPI-MySQL-Neo4j-React stack for structured data processing and visualization; and built a custom-styled, cPanel-hosted portfolio website with enhanced UI and seamless deployment."},
               {"date": "09/2023 - 12/2023", "title": "Python Web Developer - Virtuoso Netsoft", "desc": "Completed a 4-month internship on the Omni-Channel Communication Project, leading a 7-member team and developing an Email Reminder & Confirmation System using Django."},
               {"date": "04/2023 - 09/2023", "title": "Python full stack intern - Solitaire Infosys", "desc": "Completed a 6-month internship focused on full-stack CRUD applications, including a Hospital Management System built with Flask and MySQL"}
            ],
            "education": [
               {"year": "2021 - 2023", "institution": "HIET", "desc": "B.Tech CSE"},
               {"year": "2017 - 2020", "institution": "Govt Polytechnic", "desc": "Diploma in CS"},
               {"year": "2014 - 2017", "institution": "GOVT. SEN. SEC. SCHOOL,KOT", "desc": "12th class(Non-medical)"},
               {"year": "2013 - 2015", "institution": "GOVT. SEN. SEC. SCHOOL,KOT", "desc": "10th class"}
           
            ],
            "services": [
               {"icon": "bx bx-code-alt", "title": "Web development", "desc": "Building responsive and scalable websites."},
               {"icon": "bx bxs-paint", "title": "Web Design", "desc": "Crafting clean, modern, and user-friendly designs."},
               {"icon": "bx bxs-paint", "title": "DBMS", "desc": "Efficient database design, management, and optimization."},
               {"icon": "bx bxs-paint", "title": "Live project", "desc": "Real-time project development with practical solutions."}
            ],

            "skills": {
            "frontend": ["HTML", "CSS", "JS", "React"],
            "backend": ["Python", "FastAPI", "Node.js"],
            "design": ["Figma"]
            },
            "contact": {
            "email": "himanshu@example.com",
            "phone": "+91-9816884822",
            "location": "India"
            }
        })
        print("Rendered HTML.")
        # Output path for generated PDF
        pdf_path = os.path.join("static", "generated_resume.pdf")
        print("sgdjhsgkjcscsljsl",pdf_path)

        # Create PDF from rendered HTML string
        pdfkit.from_string(rendered, pdf_path, configuration=config,options={
    "enable-local-file-access": "",
    "load-error-handling": "ignore"
})
        print("PDF generated.")
        return FileResponse(pdf_path, filename="Template_CV.pdf", media_type="application/pdf")