"""
Bloom's Taxonomy Engine — প্রশ্নের কঠিনতা স্তর নির্ধারণ
6 স্তর: Remember → Understand → Apply → Analyze → Evaluate → Create
"""

from enum import Enum
from typing import Dict, List

class BloomLevel(Enum):
    REMEMBER = 1       # মনে রাখা (MCQ, সংজ্ঞা)
    UNDERSTAND = 2     # বোঝা (ব্যাখ্যা করো)
    APPLY = 3          # প্রয়োগ (সমস্যা সমাধান)
    ANALYZE = 4        # বিশ্লেষণ (কারণ খোঁজা)
    EVALUATE = 5       # মূল্যায়ন (তুলনা করো)
    CREATE = 6         # সৃষ্টি (নকশা তৈরি করো)

BLOOM_PROMPTS: Dict[BloomLevel, str] = {
    BloomLevel.REMEMBER: """
        মনে রাখার স্তরের প্রশ্ন তৈরি করো। 
        প্রশ্ন হবে সংজ্ঞা, সূত্র, বা তথ্য মনে করার জন্য।
        উদাহরণ: "নিউটনের প্রথম সূত্রটি কী?"
    """,
    BloomLevel.UNDERSTAND: """
        বোঝার স্তরের প্রশ্ন তৈরি করো।
        প্রশ্ন হবে ধারণা ব্যাখ্যা করার জন্য।
        উদাহরণ: "জড়তার সূত্র দিয়ে কী বোঝায় তা ব্যাখ্যা করো।"
    """,
    BloomLevel.APPLY: """
        প্রয়োগের স্তরের প্রশ্ন তৈরি করো।
        প্রশ্ন হবে সূত্র বা ধারণা ব্যবহার করে সমস্যা সমাধানের জন্য।
        উদাহরণ: "একটি বস্তুর ভর ৫ কেজি, বল ১০ N হলে ত্বরণ কত?"
    """,
    BloomLevel.ANALYZE: """
        বিশ্লেষণের স্তরের প্রশ্ন তৈরি করো।
        প্রশ্ন হবে কারণ-প্রভাব বিশ্লেষণের জন্য।
        উদাহরণ: "ঘর্ষণ বল না থাকলে আমাদের দৈনন্দিন জীবনে কী পরিবর্তন আসত?"
    """,
    BloomLevel.EVALUATE: """
        মূল্যায়নের স্তরের প্রশ্ন তৈরি করো।
        প্রশ্ন হবে তুলনা বা মতামত দেওয়ার জন্য।
        উদাহরণ: "নবায়নযোগ্য ও অ-নবায়নযোগ্য শক্তির মধ্যে কোনটি ভবিষ্যতের জন্য ভালো এবং কেন?"
    """,
    BloomLevel.CREATE: """
        সৃষ্টির স্তরের প্রশ্ন তৈরি করো।
        প্রশ্ন হবে নতুন কিছু তৈরি বা ডিজাইন করার জন্য।
        উদাহরণ: "তুমি যদি একটি সোলার গাড়ি তৈরি করতে চাও, তাহলে কোন কোন পদার্থবিজ্ঞানের নীতি ব্যবহার করবে?"
    """,
}

BLOOM_BENGALI_NAMES = {
    BloomLevel.REMEMBER: "মনে রাখা (Remember)",
    BloomLevel.UNDERSTAND: "বোঝা (Understand)",
    BloomLevel.APPLY: "প্রয়োগ (Apply)",
    BloomLevel.ANALYZE: "বিশ্লেষণ (Analyze)",
    BloomLevel.EVALUATE: "মূল্যায়ন (Evaluate)",
    BloomLevel.CREATE: "সৃষ্টি (Create)",
}

def get_next_bloom_level(current_score: float, current_level: BloomLevel) -> BloomLevel:
    """
    স্কোরের উপর ভিত্তি করে পরবর্তী Bloom স্তর নির্ধারণ।
    ৭০%+ স্কোর = পরবর্তী স্তরে যাও
    ৫০% এর নিচে = আগের স্তরে ফিরে যাও
    """
    if current_score >= 70 and current_level.value < 6:
        return BloomLevel(current_level.value + 1)
    elif current_score < 50 and current_level.value > 1:
        return BloomLevel(current_level.value - 1)
    return current_level

def get_bloom_level_from_score(total_score: float) -> BloomLevel:
    """মোট স্কোর থেকে শুরুর Bloom স্তর নির্ধারণ।"""
    if total_score < 30:
        return BloomLevel.REMEMBER
    elif total_score < 50:
        return BloomLevel.UNDERSTAND
    elif total_score < 65:
        return BloomLevel.APPLY
    elif total_score < 80:
        return BloomLevel.ANALYZE
    elif total_score < 90:
        return BloomLevel.EVALUATE
    else:
        return BloomLevel.CREATE
