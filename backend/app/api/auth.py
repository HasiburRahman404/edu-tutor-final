"""
Auth API — Supabase Authentication
Real signup/signin using Supabase Auth
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.supabase_service import supabase_signup, supabase_signin

router = APIRouter()

class SignUpRequest(BaseModel):
    email: str
    password: str
    name: str
    grade: str = "SSC"
    role: str = "student"

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def sign_up(req: SignUpRequest):
    try:
        result = await supabase_signup(
            email=req.email,
            password=req.password,
            name=req.name,
            grade=req.grade,
            role=req.role
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin")
async def sign_in(req: SignInRequest):
    try:
        result = await supabase_signin(
            email=req.email,
            password=req.password
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail="ইমেইল বা পাসওয়ার্ড সঠিক নয়।")
