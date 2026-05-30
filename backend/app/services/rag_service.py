"""
NCTB RAG Service — ChromaDB ছাড়া (Vercel compatible)
Keyword-based context retrieval
"""

from typing import Optional

# NCTB বিষয়ভিত্তিক সাধারণ context
NCTB_CONTEXT = {
    "physics": "পদার্থবিজ্ঞান: গতি, বল, শক্তি, তরঙ্গ, আলো, তড়িৎ, চুম্বকত্ব বিষয়ক NCTB পাঠ্যক্রম।",
    "chemistry": "রসায়ন: পরমাণু, অণু, রাসায়নিক বিক্রিয়া, অ্যাসিড-ক্ষার, জৈব রসায়ন বিষয়ক NCTB পাঠ্যক্রম।",
    "biology": "জীববিজ্ঞান: কোষ, টিস্যু, অঙ্গতন্ত্র, বংশগতি, বিবর্তন বিষয়ক NCTB পাঠ্যক্রম।",
    "math": "গণিত: বীজগণিত, জ্যামিতি, ত্রিকোণমিতি, পরিসংখ্যান বিষয়ক NCTB পাঠ্যক্রম।",
    "english": "ইংরেজি: গ্রামার, রিডিং, রাইটিং, ভোকাবুলারি বিষয়ক NCTB পাঠ্যক্রম।",
    "bangla": "বাংলা: গদ্য, পদ্য, ব্যাকরণ, রচনা বিষয়ক NCTB পাঠ্যক্রম।",
}


async def retrieve_nctb_context(
    subject: str,
    chapter_id: str,
    query: str,
    k: int = 3
) -> str:
    try:
        subject_lower = subject.lower() if subject else ""
        context = NCTB_CONTEXT.get(subject_lower, "")

        if context:
            return f"বিষয়: {subject}\nঅধ্যায়: {chapter_id}\n{context}"
        else:
            return f"বিষয়: {subject}, অধ্যায়: {chapter_id} সম্পর্কিত NCTB পাঠ্যক্রম।"

    except Exception as e:
        print(f"RAG retrieval error: {e}")
        return "পাঠ্যপুস্তক থেকে তথ্য লোড করা যাচ্ছে না।"