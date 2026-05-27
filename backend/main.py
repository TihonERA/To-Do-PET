from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
import os

from backend.api.v1 import auth, tasks, users

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "pages"))

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})

@app.get("/registration")
async def registration_page(request: Request):
    return templates.TemplateResponse(name="registration.html", context={"request": request})