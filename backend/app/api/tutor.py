"""
Tutor API Endpoints
প্রশ্ন তৈরি, উত্তর মূল্যায়ন ও ফলো-আপ
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.gemini_service import (
    generate_question, evaluate_answer, generate_followup_question
)
from app.services.supabase_service import get_or_create_student, save_session
from app.core.bloom_taxonomy import BloomLevel, get_bloom_level_from_score
from typing import Optional

router = APIRouter()

class StartSessionRequest(BaseModel):
    student_id: str
    student_name: str
    grade: str
    subject: str
    chapter_id: str
    previous_score: Optional[float] = 50.0

class AnswerRequest(BaseModel):
    student_id: str
    subject: str
    chapter_id: str
    question: str
    student_answer: str
    expected_keywords: list
    bloom_level: int
    marks: int
    session_id: Optional[str] = None

class FollowupRequest(BaseModel):
    student_id: str
    subject: str
    chapter_id: str
    previous_question: str
    student_answer: str
    weak_areas: list
    bloom_level: int


@router.post("/start-session")
async def start_session(req: StartSessionRequest):
    try:
        student = await get_or_create_student(
            user_id=req.student_id,
            name=req.student_name,
            grade=req.grade
        )

        bloom_level = BloomLevel(1)

        question_data = await generate_question(
            subject=req.subject,
            level=req.grade,
            chapter_id=req.chapter_id,
            bloom_level=bloom_level,
            student_id=req.student_id,
            previous_weak_areas=[]
        )

        # ✅ Frontend এর জন্য flat response
        return {
            "success":    True,
            "question":   question_data.get("question", ""),
            "hints":      question_data.get("hints", []),
            "marks":      question_data.get("marks", 5),
            "bloom_level": bloom_level.value,
            "expected_keywords": question_data.get("expected_keywords", []),
            "chapter_reference": question_data.get("chapter_reference", ""),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"সেশন শুরু করতে সমস্যা: {str(e)}")


@router.post("/evaluate")
async def evaluate_student_answer(req: AnswerRequest):
    try:
        bloom_level = BloomLevel(req.bloom_level)

        evaluation = await evaluate_answer(
            question=req.question,
            student_answer=req.student_answer,
            expected_keywords=req.expected_keywords,
            bloom_level=bloom_level,
            marks=req.marks,
            subject=req.subject,
            chapter_id=req.chapter_id
        )

        await save_session(
            student_id=req.student_id,
            session_data={
                "subject":        req.subject,
                "chapter_id":     req.chapter_id,
                "question":       req.question,
                "student_answer": req.student_answer,
                "score":          evaluation.get("score", 0),
            }
        )

        # ✅ Frontend এর জন্য flat response
        return {
            "success":         True,
            "score":           evaluation.get("score", 0),
            "max_score":       evaluation.get("max_score", req.marks),
            "percentage":      evaluation.get("percentage", 0),
            "feedback_bengali": evaluation.get("feedback_bengali", ""),
            "correct_answer":  evaluation.get("correct_answer", ""),
            "weak_areas":      evaluation.get("weak_areas", []),
            "encouragement":   evaluation.get("encouragement", ""),
            "is_correct":      evaluation.get("is_correct", False),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"মূল্যায়নে সমস্যা: {str(e)}")


@router.post("/followup")
async def get_followup(req: FollowupRequest):
    try:
        bloom_level = BloomLevel(req.bloom_level)

        followup = await generate_followup_question(
            previous_question=req.previous_question,
            student_answer=req.student_answer,
            weak_areas=req.weak_areas,
            bloom_level=bloom_level,
            subject=req.subject,
            chapter_id=req.chapter_id
        )

        # ✅ Frontend এর জন্য flat response
        return {
            "success":          True,
            "followup_question": followup.get("followup_question", ""),
            "hints":            followup.get("hints", []),
            "easier":           followup.get("easier", True),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ফলো-আপ তৈরিতে সমস্যা: {str(e)}")


@router.get("/subjects")
async def get_subjects():
    try:
        from app.core.nctb_curriculum import NCTB_CURRICULUM
        curriculum = NCTB_CURRICULUM
    except:
        curriculum = {}

    return {
        "subjects": {
            "physics":   "পদার্থবিজ্ঞান",
            "chemistry": "রসায়ন",
            "math":      "গণিত"
        },
        "curriculum": curriculum
    }