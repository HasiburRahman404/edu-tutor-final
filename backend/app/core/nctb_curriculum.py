"""
NCTB সিলেবাস চ্যাপ্টার ম্যাপিং
SSC ও HSC পদার্থবিজ্ঞান, রসায়ন, গণিত
"""

NCTB_CURRICULUM = {
    "physics": {
        "SSC": {
            "chapters": [
                {"id": "phy_ssc_1",  "name": "ভৌত রাশি ও পরিমাপ",         "keywords": ["রাশি", "একক", "পরিমাপ", "SI"]},
                {"id": "phy_ssc_2",  "name": "গতি",                        "keywords": ["বেগ", "ত্বরণ", "দূরত্ব", "গতি"]},
                {"id": "phy_ssc_3",  "name": "বল",                         "keywords": ["নিউটন", "জড়তা", "বল", "ঘর্ষণ"]},
                {"id": "phy_ssc_4",  "name": "কাজ, ক্ষমতা ও শক্তি",       "keywords": ["কাজ", "ক্ষমতা", "শক্তি", "ওয়াট"]},
                {"id": "phy_ssc_5",  "name": "পদার্থের অবস্থা ও চাপ",     "keywords": ["কঠিন", "তরল", "গ্যাস", "চাপ"]},
                {"id": "phy_ssc_6",  "name": "বস্তুর উপর তাপের প্রভাব",   "keywords": ["তাপ", "তাপমাত্রা", "প্রসারণ"]},
                {"id": "phy_ssc_7",  "name": "তরঙ্গ ও শব্দ",              "keywords": ["তরঙ্গ", "শব্দ", "কম্পাঙ্ক", "বিস্তার"]},
                {"id": "phy_ssc_8",  "name": "আলোর প্রতিফলন",             "keywords": ["আলো", "প্রতিফলন", "দর্পণ"]},
                {"id": "phy_ssc_9",  "name": "আলোর প্রতিসরণ",             "keywords": ["প্রতিসরণ", "লেন্স", "স্নেলের সূত্র"]},
                {"id": "phy_ssc_10", "name": "স্থির তড়িৎ",               "keywords": ["তড়িৎ", "চার্জ", "কুলম্ব"]},
                {"id": "phy_ssc_11", "name": "চল তড়িৎ",                  "keywords": ["কারেন্ট", "ভোল্টেজ", "রোধ", "ওহমের সূত্র"]},
                {"id": "phy_ssc_12", "name": "তড়িতের চৌম্বক প্রভাব",    "keywords": ["চুম্বক", "তড়িৎচৌম্বক", "মোটর"]},
                {"id": "phy_ssc_13", "name": "আধুনিক পদার্থবিজ্ঞান",     "keywords": ["পরমাণু", "নিউক্লিয়াস", "তেজস্ক্রিয়তা"]},
            ]
        },
        "HSC": {
            "chapters": [
                {"id": "phy_hsc_1",  "name": "ভৌত জগৎ ও পরিমাপ",         "keywords": ["ভেক্টর", "স্কেলার", "মাত্রা"]},
                {"id": "phy_hsc_2",  "name": "ভেক্টর",                    "keywords": ["ভেক্টর", "অভিক্ষেপ", "যোগ"]},
                {"id": "phy_hsc_3",  "name": "গতিবিদ্যা",                 "keywords": ["সরলরৈখিক গতি", "প্রজেক্টাইল"]},
                {"id": "phy_hsc_4",  "name": "নিউটনীয় বলবিদ্যা",        "keywords": ["নিউটন", "ভরবেগ", "সংঘর্ষ"]},
                {"id": "phy_hsc_5",  "name": "কাজ, শক্তি ও ক্ষমতা",     "keywords": ["কাজ-শক্তি উপপাদ্য", "সংরক্ষণ"]},
                {"id": "phy_hsc_6",  "name": "মহাকর্ষ ও অভিকর্ষ",       "keywords": ["মহাকর্ষ", "কেপলার", "উপগ্রহ"]},
                {"id": "phy_hsc_7",  "name": "পদার্থের গাঠনিক ধর্ম",     "keywords": ["স্থিতিস্থাপকতা", "পৃষ্ঠটান"]},
                {"id": "phy_hsc_8",  "name": "পর্যাবৃত্ত গতি",           "keywords": ["SHM", "পর্যায়", "স্প্রিং"]},
                {"id": "phy_hsc_9",  "name": "তরঙ্গ",                     "keywords": ["তরঙ্গ", "তরঙ্গদৈর্ঘ্য", "ব্যতিচার"]},
                {"id": "phy_hsc_10", "name": "আদর্শ গ্যাস ও গ্যাসের গতিতত্ত্ব", "keywords": ["গ্যাস সূত্র", "গতিতত্ত্ব"]},
                {"id": "phy_hsc_11", "name": "তাপগতিবিদ্যা",             "keywords": ["তাপগতিসূত্র", "এনট্রপি"]},
                {"id": "phy_hsc_12", "name": "স্থির তড়িৎবিজ্ঞান",       "keywords": ["গাউস", "বৈদ্যুতিক বিভব"]},
                {"id": "phy_hsc_13", "name": "চল তড়িৎ",                  "keywords": ["কির্শহফ", "হুইটস্টোন"]},
                {"id": "phy_hsc_14", "name": "তড়িৎচুম্বকত্ব",           "keywords": ["ফ্যারাডে", "ইন্ডাকশন"]},
                {"id": "phy_hsc_15", "name": "আধুনিক পদার্থবিজ্ঞান",     "keywords": ["ফটোইলেকট্রিক", "কোয়ান্টাম"]},
            ]
        }
    },
    "chemistry": {
        "SSC": {
            "chapters": [
                {"id": "chem_ssc_1", "name": "রসায়নের ধারণা",            "keywords": ["রসায়ন", "পদার্থ", "মিশ্রণ"]},
                {"id": "chem_ssc_2", "name": "পদার্থের অবস্থা",          "keywords": ["কঠিন", "তরল", "বায়বীয়"]},
                {"id": "chem_ssc_3", "name": "পদার্থের গঠন",             "keywords": ["পরমাণু", "ইলেকট্রন", "প্রোটন"]},
                {"id": "chem_ssc_4", "name": "পর্যায় সারণি",            "keywords": ["পর্যায় সারণি", "মেন্ডেলিভ", "শ্রেণি"]},
                {"id": "chem_ssc_5", "name": "রাসায়নিক বন্ধন",          "keywords": ["আয়নিক", "সমযোজী", "বন্ধন"]},
                {"id": "chem_ssc_6", "name": "মোলের ধারণা",              "keywords": ["মোল", "অ্যাভোগাড্রো"]},
                {"id": "chem_ssc_7", "name": "রাসায়নিক বিক্রিয়া",      "keywords": ["বিক্রিয়া", "সমীকরণ", "বিক্রিয়ক"]},
                {"id": "chem_ssc_8", "name": "রসায়ন ও শক্তি",           "keywords": ["তাপ", "দহন", "শক্তি"]},
                {"id": "chem_ssc_9", "name": "এসিড-ক্ষারক সমতা",        "keywords": ["এসিড", "ক্ষারক", "pH", "নিরপেক্ষীকরণ"]},
                {"id": "chem_ssc_10","name": "খনিজ সম্পদ: ধাতু-অধাতু",  "keywords": ["ধাতু", "অধাতু", "আকরিক"]},
                {"id": "chem_ssc_11","name": "জীবাশ্ম জ্বালানি",        "keywords": ["কয়লা", "পেট্রোলিয়াম", "গ্যাস"]},
                {"id": "chem_ssc_12","name": "আমাদের জীবনে রসায়ন",     "keywords": ["পলিমার", "সার", "ঔষধ"]},
            ]
        }
    },
    "math": {
        "SSC": {
            "chapters": [
                {"id": "math_ssc_1", "name": "বাস্তব সংখ্যা",            "keywords": ["সংখ্যা", "মূলদ", "অমূলদ"]},
                {"id": "math_ssc_2", "name": "সেট ও ফাংশন",             "keywords": ["সেট", "ফাংশন", "ডোমেইন"]},
                {"id": "math_ssc_3", "name": "বীজগাণিতিক রাশি",         "keywords": ["বীজগাণিত", "সূত্র", "উৎপাদক"]},
                {"id": "math_ssc_4", "name": "সরল সমীকরণ",              "keywords": ["সমীকরণ", "চল", "সমাধান"]},
                {"id": "math_ssc_5", "name": "দ্বিঘাত সমীকরণ",          "keywords": ["দ্বিঘাত", "মূল", "বিভেদক"]},
                {"id": "math_ssc_6", "name": "জ্যামিতি",                 "keywords": ["ত্রিভুজ", "চতুর্ভুজ", "কোণ"]},
                {"id": "math_ssc_7", "name": "ত্রিকোণমিতি",             "keywords": ["সাইন", "কোসাইন", "ট্যানজেন্ট"]},
                {"id": "math_ssc_8", "name": "পরিমিতি",                  "keywords": ["ক্ষেত্রফল", "পরিসীমা", "আয়তন"]},
                {"id": "math_ssc_9", "name": "পরিসংখ্যান",              "keywords": ["গড়", "মধ্যক", "প্রচুরক"]},
            ]
        }
    }
}

def get_chapter_by_keywords(subject: str, level: str, text: str) -> dict | None:
    """প্রশ্নের keyword থেকে NCTB অধ্যায় খুঁজে বের করো।"""
    subject_data = NCTB_CURRICULUM.get(subject, {}).get(level, {})
    chapters = subject_data.get("chapters", [])
    text_lower = text.lower()
    
    best_match = None
    best_count = 0
    
    for chapter in chapters:
        count = sum(1 for kw in chapter["keywords"] if kw in text_lower)
        if count > best_count:
            best_count = count
            best_match = chapter
    
    return best_match

def get_all_chapters(subject: str, level: str) -> list:
    """একটি বিষয়ের সব অধ্যায়ের তালিকা।"""
    return NCTB_CURRICULUM.get(subject, {}).get(level, {}).get("chapters", [])
