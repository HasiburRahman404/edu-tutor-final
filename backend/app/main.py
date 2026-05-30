
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
"""
EduTutor BD — FastAPI Backend
Bengali AI Tutor for SSC/HSC Students
Deployed on Vercel via Mangum
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.api import tutor, progress, auth
from app.core.config import settings

app = FastAPI(
    title="EduTutor BD API",
    description="Bengali AI Tutor for SSC Students",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/auth",     tags=["Auth"])
app.include_router(tutor.router,    prefix="/api/tutor",    tags=["Tutor"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])

@app.get("/")
async def root():
    return {"message": "EduTutor BD API চলছে ✅", "version": "2.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Vercel serverless handler
handler = Mangum(app)
