from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("YOUR API KEY"))

# Initialize FastAPI
app = FastAPI(title="AI Resume Builder")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL when deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- MODELS ----
class ResumeRequest(BaseModel):
    name: str
    email: str
    phone: str
    skills: list[str]
    experience: str
    education: str
    projects: list[str]
    career_goal: str | None = None


class CoverLetterRequest(BaseModel):
    name: str
    position: str
    company: str
    skills: list[str]
    experience: str


class PortfolioRequest(BaseModel):
    name: str
    skills: list[str]
    projects: list[str]
    bio: str


# ---- ROUTES ----
@app.get("/")
def root():
    return {"message": "AI Resume Builder API is running. Go to /docs to test endpoints."}


@app.post("/generate-resume/")
async def generate_resume(data: ResumeRequest):
    try:
        prompt = f"""
        Write a professional resume for:
        Name: {data.name}
        Email: {data.email}
        Phone: {data.phone}
        Education: {data.education}
        Experience: {data.experience}
        Skills: {', '.join(data.skills)}
        Projects: {', '.join(data.projects)}
        Career Goal: {data.career_goal if data.career_goal else 'Not specified'}

        Format: 
        - Header (Name, Contact)
        - Career Objective
        - Education
        - Experience
        - Skills
        - Projects
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume writer."},
                {"role": "user", "content": prompt},
            ],
        )

        resume_text = response.choices[0].message.content.strip()
        return {"generated_resume": resume_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-cover-letter/")
async def generate_cover_letter(data: CoverLetterRequest):
    try:
        prompt = f"""
        Write a compelling cover letter for {data.name}, applying for the {data.position} position at {data.company}.
        Include the following:
        - Relevant experience: {data.experience}
        - Key skills: {', '.join(data.skills)}
        The tone should be professional and enthusiastic.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional career consultant."},
                {"role": "user", "content": prompt},
            ],
        )

        letter = response.choices[0].message.content.strip()
        return {"generated_cover_letter": letter}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-portfolio/")
async def generate_portfolio(data: PortfolioRequest):
    try:
        prompt = f"""
        Create a professional portfolio profile for:
        Name: {data.name}
        Bio: {data.bio}
        Skills: {', '.join(data.skills)}
        Projects: {', '.join(data.projects)}

        Format sections as:
        - About Me
        - Skills
        - Projects
        - Contact Information
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a portfolio design assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        portfolio_text = response.choices[0].message.content.strip()
        return {"generated_portfolio": portfolio_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
