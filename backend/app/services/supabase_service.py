"""
Supabase Service — Real Implementation
Handles auth, sessions, and progress using Supabase
"""

from supabase import create_client, Client
from app.core.config import settings
from typing import Optional

_client: Optional[Client] = None

def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _client


# ─── Auth ────────────────────────────────────────────────────

async def supabase_signup(email: str, password: str, name: str, grade: str = "SSC", role: str = "student") -> dict:
    sb = get_client()
    # Use anon client for signup
    anon_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    res = anon_client.auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {"name": name, "grade": grade, "role": role}
        }
    })
    if res.user:
        return {
            "success": True,
            "user_id": str(res.user.id),
            "message": f"স্বাগতম {name}! অ্যাকাউন্ট তৈরি হয়েছে।"
        }
    raise Exception("অ্যাকাউন্ট তৈরি করা যায়নি।")


async def supabase_signin(email: str, password: str) -> dict:
    anon_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    res = anon_client.auth.sign_in_with_password({"email": email, "password": password})
    if res.user and res.session:
        # Fetch profile for role/name/grade
        sb = get_client()
        profile = sb.table("profiles").select("*").eq("id", str(res.user.id)).single().execute()
        data = profile.data or {}
        return {
            "success":      True,
            "access_token": res.session.access_token,
            "user_id":      str(res.user.id),
            "user_name":    data.get("name", email),
            "role":         data.get("role", "student"),
            "grade":        data.get("grade", "SSC"),
        }
    raise Exception("লগইন ব্যর্থ।")


# ─── Student ─────────────────────────────────────────────────

async def get_or_create_student(user_id: str, name: str = "", email: str = "", grade: str = "SSC") -> dict:
    sb = get_client()
    res = sb.table("profiles").select("*").eq("id", user_id).single().execute()
    if res.data:
        return res.data
    # Create if not exists
    sb.table("profiles").insert({
        "id": user_id, "name": name, "email": email, "grade": grade, "role": "student"
    }).execute()
    return {"id": user_id, "name": name, "email": email, "grade": grade}


# ─── Sessions ────────────────────────────────────────────────

async def save_session(student_id: str, session_data: dict) -> dict:
    sb = get_client()
    sb.table("sessions").insert({
        "user_id":        student_id,
        "subject":        session_data.get("subject", ""),
        "chapter_id":     session_data.get("chapter_id", ""),
        "question":       session_data.get("question", ""),
        "student_answer": session_data.get("student_answer", ""),
        "score":          session_data.get("score", 0),
        "max_score":      session_data.get("max_score", 5),
        "percentage":     session_data.get("percentage", 0),
    }).execute()
    return {"status": "ok"}


# ─── Progress ────────────────────────────────────────────────

async def get_progress_report(student_id: str) -> dict:
    sb = get_client()
    res = sb.table("sessions").select("*").eq("user_id", student_id).execute()
    sessions = res.data or []

    total = len(sessions)
    avg   = round(sum(s.get("percentage", 0) for s in sessions) / total) if total else 0

    subjects = {"physics": [], "chemistry": [], "math": []}
    for s in sessions:
        subj = s.get("subject", "")
        if subj in subjects:
            subjects[subj].append(s.get("percentage", 0))

    subject_data = {}
    for key, scores in subjects.items():
        count = len(scores)
        subject_data[key] = {
            "score":    round(sum(scores) / count) if count else 0,
            "sessions": count
        }

    return {
        "student_id":      student_id,
        "total_sessions":  total,
        "average_score":   avg,
        "weak_areas":      [],
        "subjects":        subject_data,
    }


async def get_all_students_report() -> dict:
    """Admin: all students with their progress"""
    sb = get_client()
    profiles = sb.table("profiles").select("*").eq("role", "student").execute().data or []
    sessions_all = sb.table("sessions").select("*").execute().data or []

    total_sessions = len(sessions_all)
    overall_avg = round(sum(s.get("percentage", 0) for s in sessions_all) / total_sessions) if total_sessions else 0

    students = []
    for p in profiles:
        uid = p["id"]
        user_sessions = [s for s in sessions_all if s["user_id"] == uid]
        count = len(user_sessions)
        avg = round(sum(s.get("percentage", 0) for s in user_sessions) / count) if count else 0

        def subj_avg(subj):
            ss = [s.get("percentage", 0) for s in user_sessions if s.get("subject") == subj]
            return round(sum(ss) / len(ss)) if ss else 0

        students.append({
            "id":             uid,
            "name":           p.get("name", ""),
            "email":          p.get("email", ""),
            "grade":          p.get("grade", "SSC"),
            "total_sessions": count,
            "avg_score":      avg,
            "physics_avg":    subj_avg("physics"),
            "chemistry_avg":  subj_avg("chemistry"),
            "math_avg":       subj_avg("math"),
        })

    students.sort(key=lambda x: x["avg_score"], reverse=True)
    return {
        "total_students": len(profiles),
        "total_sessions": total_sessions,
        "overall_avg":    overall_avg,
        "students":       students,
    }
