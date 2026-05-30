async def retrieve_nctb_context(
    subject: str,
    chapter_id: str,
    query: str,
    k: int = 3
) -> str:
    try:
        return f"বিষয়: {subject}, অধ্যায়: {chapter_id} সম্পর্কিত NCTB পাঠ্যক্রম।"
    except Exception as e:
        return "পাঠ্যপুস্তক থেকে তথ্য লোড করা যাচ্ছে না।"