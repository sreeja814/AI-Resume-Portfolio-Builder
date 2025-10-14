import openai
from jinja2 import Template
import pdfkit

openai.api_key = " "

def generate_resume_text(student_data: dict) -> str:
    """
    Generate resume content using OpenAI GPT.
    """
    prompt = f"""
    Generate a professional resume for the following student:

    Name: {student_data['name']}
    Email: {student_data['email']}
    Phone: {student_data.get('phone', '')}
    LinkedIn: {student_data.get('linkedin', '')}
    GitHub: {student_data.get('github', '')}
    Skills: {', '.join(student_data['skills'])}
    Education: {', '.join(student_data['education'])}
    Experience: {', '.join(student_data.get('experience', []))}
    Projects: {', '.join([p['title'] + ': ' + p['description'] for p in student_data['projects']])}
    Career Objective: {student_data.get('career_objective', '')}

    Provide the resume in a clean text format.
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=800
    )
    return response.choices[0].text.strip()

def generate_cover_letter(student_data: dict, job_role: str) -> str:
    """
    Generate a tailored cover letter for a specific role.
    """
    prompt = f"""
    Write a professional cover letter for {student_data['name']} applying for {job_role}. 
    Include skills, projects, and experiences from the following data:

    Skills: {', '.join(student_data['skills'])}
    Projects: {', '.join([p['title'] + ': ' + p['description'] for p in student_data['projects']])}
    Experience: {', '.join(student_data.get('experience', []))}
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=600
    )
    return response.choices[0].text.strip()

def generate_pdf(content: str, filename: str):
    """
    Convert text content to PDF using HTML template.
    """
    html_template = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; }}
                ul {{ margin: 0; padding-left: 20px; }}
            </style>
        </head>
        <body>
            <pre>{content}</pre>
        </body>
    </html>
    """
    pdfkit.from_string(html_template, filename)
