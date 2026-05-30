"""
Progress API — Student progress & Admin dashboard
Now powered by real Supabase data
"""

from fastapi import APIRouter, HTTPException
from app.services.supabase_service import get_progress_report, get_all_students_report

router = APIRouter()

@router.get("/report/{student_id}")
async def get_student_report(student_id: str):
    try:
        report = await get_progress_report(student_id)
        return {"success": True, "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/parent-dashboard/{student_id}")
async def get_parent_dashboard(student_id: str):
    try:
        report = await get_progress_report(student_id)
        subject_names = {"physics": "পদার্থবিজ্ঞান", "chemistry": "রসায়ন", "math": "গণিত"}
        subjects = report.get("subjects", {})
        subject_summary = []
        for subject, data in subjects.items():
            score = data.get("score", 0)
            subject_summary.append({
                "subject": subject_names.get(subject, subject),
                "average_score": score,
                "total_sessions": data.get("sessions", 0),
                "status": "ভালো করছে ✅" if score >= 70
                         else "উন্নতি দরকার ⚠️" if score >= 50
                         else "বেশি মনোযোগ দরকার ❌"
            })
        return {
            "success": True,
            "dashboard": {
                "student_id": student_id,
                "total_study_sessions": report.get("total_sessions", 0),
                "average_score": report.get("average_score", 0),
                "subjects": subject_summary,
                "weak_areas": report.get("weak_areas", [])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/all-students")
async def get_admin_report():
    try:
        data = await get_all_students_report()
        return {"success": True, **data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leaderboard/{grade}/{subject}")
async def get_leaderboard(grade: str, subject: str):
    return {"success": True, "leaderboard": []}
