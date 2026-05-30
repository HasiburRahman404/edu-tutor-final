"""
AI Tutor Service — Groq API
বাংলা ভাষায় প্রশ্ন, মূল্যায়ন ও ফিডব্যাক তৈরি করে
"""

import os
import json
import re
import time
from typing import Optional
from app.core.bloom_taxonomy import BloomLevel, BLOOM_PROMPTS, BLOOM_BENGALI_NAMES
from app.services.rag_service import retrieve_nctb_context

# ✅ Groq client
try:
    from groq import Groq
    _groq_client = None

    def get_client():
        global _groq_client
        if _groq_client is None:
            api_key = os.environ.get("GROQ_API_KEY") or ""
            from app.core.config import settings
            api_key = getattr(settings, "GROQ_API_KEY", api_key)
            _groq_client = Groq(api_key=api_key)
        return _groq_client

except ImportError:
    raise ImportError("groq package install করো: pip install groq")

GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PERSONA = """
তুমি একজন অভিজ্ঞ বাংলাদেশী শিক্ষক। তুমি SSC ও HSC শিক্ষার্থীদের পদার্থবিজ্ঞান,
রসায়ন এবং গণিত পড়াও। তোমার বৈশিষ্ট্য:
- সবসময় বাংলায় কথা বলো
- সহজ ও বন্ধুত্বপূর্ণ ভাষা ব্যবহার করো
- শিক্ষার্থীকে উৎসাহিত করো
- NCTB পাঠ্যক্রম অনুসরণ করো
- উদাহরণ দেওয়ার সময় বাংলাদেশের প্রেক্ষাপট ব্যবহার করো
- উত্তর মূল্যায়নে সর্বদা কঠোর ও সৎ থাকো
"""

def _generate(prompt: str) -> str:
    client = get_client()
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PERSONA},
                    {"role": "user",   "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if '429' in str(e) and attempt < 2:
                print(f"Rate limit — {30}s অপেক্ষা করছি...")
                time.sleep(30)
            else:
                raise e

def _parse_json(text: str) -> Optional[dict]:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return None


async def generate_question(
    subject: str,
    level: str,
    chapter_id: str,
    bloom_level: BloomLevel,
    student_id: str,
    previous_weak_areas: list = []
) -> dict:
    rag_context = await retrieve_nctb_context(
        subject=subject,
        chapter_id=chapter_id,
        query=f"{subject} {chapter_id} question"
    )

    bloom_prompt    = BLOOM_PROMPTS.get(bloom_level, "একটি প্রশ্ন তৈরি করো।")
    weak_areas_text = ""
    if previous_weak_areas:
        weak_areas_text = f"\nশিক্ষার্থীর দুর্বল দিক: {', '.join(previous_weak_areas)}"

    prompt = f"""
বিষয়: {subject}
শ্রেণি: {level}
অধ্যায়: {chapter_id}
Bloom's Taxonomy স্তর: {BLOOM_BENGALI_NAMES.get(bloom_level, 'মনে রাখো')}
{weak_areas_text}

NCTB পাঠ্যপুস্তক থেকে প্রাসঙ্গিক তথ্য:
{rag_context}

নির্দেশনা: {bloom_prompt}

একটি প্রশ্ন তৈরি করো এবং নিচের JSON ফরম্যাটে উত্তর দাও:
{{
  "question": "প্রশ্নটি বাংলায়",
  "question_type": "short_answer",
  "hints": ["হিন্ট ১", "হিন্ট ২"],
  "expected_keywords": ["কীওয়ার্ড ১", "কীওয়ার্ড ২"],
  "marks": 5,
  "bloom_level": "{bloom_level.name}",
  "chapter_reference": "অধ্যায় রেফারেন্স"
}}

শুধু JSON আউটপুট দাও।
"""

    text   = _generate(prompt)
    result = _parse_json(text)
    if result:
        return result

    return {
        "question":          text,
        "question_type":     "short_answer",
        "hints":             [],
        "expected_keywords": [],
        "marks":             5,
        "bloom_level":       bloom_level.name,
        "chapter_reference": chapter_id
    }


async def evaluate_answer(
    question: str,
    student_answer: str,
    expected_keywords: list,
    bloom_level: BloomLevel,
    marks: int,
    subject: str,
    chapter_id: str
) -> dict:

    # ✅ খালি উত্তর হলে সরাসরি 0 দাও
    if not student_answer or student_answer.strip() == "":
        return {
            "score":            0,
            "max_score":        marks,
            "percentage":       0,
            "feedback_bengali": "তুমি কোনো উত্তর দাওনি। উত্তর লিখে জমা দাও।",
            "correct_answer":   "",
            "weak_areas":       ["উত্তর দেওয়া হয়নি"],
            "encouragement":    "চেষ্টা করো! তুমি পারবে।",
            "is_correct":       False
        }

    rag_context = await retrieve_nctb_context(
        subject=subject,
        chapter_id=chapter_id,
        query=question
    )

    prompt = f"""
তুমি একজন কঠোর পরীক্ষক। নিচের উত্তরটি মূল্যায়ন করো।

প্রশ্ন: {question}
শিক্ষার্থীর উত্তর: {student_answer}
সর্বোচ্চ নম্বর: {marks}
প্রত্যাশিত কীওয়ার্ড: {', '.join(expected_keywords)}

NCTB পাঠ্যপুস্তক থেকে সঠিক তথ্য:
{rag_context}

মূল্যায়নের নিয়ম:
1. শিক্ষার্থীর উত্তর কতটুকু সঠিক তা যাচাই করো
2. উত্তরে প্রত্যাশিত কীওয়ার্ড আছে কিনা দেখো
3. সম্পূর্ণ ভুল উত্তরে score 0 দাও
4. আংশিক সঠিক উত্তরে সেই অনুযায়ী নম্বর দাও
5. সম্পূর্ণ সঠিক উত্তরেই শুধু পূর্ণ নম্বর দাও
6. percentage = (score / {marks}) * 100

নিচের JSON ফরম্যাটে উত্তর দাও:
{{
  "score": 0,
  "max_score": {marks},
  "percentage": 0,
  "feedback_bengali": "কেন এই নম্বর দেওয়া হলো তার বিস্তারিত ব্যাখ্যা",
  "correct_answer": "সঠিক উত্তর বাংলায়",
  "weak_areas": ["কোথায় ভুল হয়েছে"],
  "encouragement": "উৎসাহমূলক বার্তা",
  "is_correct": false
}}

শুধু JSON আউটপুট দাও।
"""

    text   = _generate(prompt)
    result = _parse_json(text)
    if result:
        result["max_score"] = marks
        # percentage সঠিক করো
        if result.get("score") is not None:
            result["percentage"] = round((result["score"] / marks) * 100)
        return result

    return {
        "score":            0,
        "max_score":        marks,
        "percentage":       0,
        "feedback_bengali": "উত্তর মূল্যায়ন করতে সমস্যা হয়েছে। আবার চেষ্টা করো।",
        "correct_answer":   "",
        "weak_areas":       [],
        "encouragement":    "হাল ছেড়ো না! আবার চেষ্টা করো।",
        "is_correct":       False
    }


async def generate_followup_question(
    previous_question: str,
    student_answer: str,
    weak_areas: list,
    bloom_level: BloomLevel,
    subject: str,
    chapter_id: str
) -> dict:
    prompt = f"""
আগের প্রশ্ন: {previous_question}
শিক্ষার্থীর উত্তর: {student_answer}
দুর্বল দিক: {', '.join(weak_areas)}
বর্তমান Bloom's স্তর: {BLOOM_BENGALI_NAMES.get(bloom_level, 'মনে রাখো')}

শিক্ষার্থীর দুর্বলতার উপর ভিত্তি করে একটি সহজ ফলো-আপ প্রশ্ন তৈরি করো।

JSON ফরম্যাটে:
{{
  "followup_question": "ফলো-আপ প্রশ্ন বাংলায়",
  "why_this_question": "এই প্রশ্নটি কেন গুরুত্বপূর্ণ",
  "hints": ["হিন্ট ১"],
  "easier": true
}}

শুধু JSON আউটপুট দাও।
"""

    text   = _generate(prompt)
    result = _parse_json(text)
    if result:
        return result

    return {
        "followup_question": text,
        "why_this_question": "আরও ভালোভাবে বোঝার জন্য",
        "hints":             [],
        "easier":            True
    }
