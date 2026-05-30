// ─── Tutor ───────────────────────────────────────────────────
const SUBJECTS = {
  physics:   { name: '⚛️ পদার্থবিজ্ঞান', chapters: ['অধ্যায় ১: ভৌত রাশি এবং তাদের পরিমাপ','অধ্যায় ২: গতি','অধ্যায় ৩: বল','অধ্যায় ৪: কাজ, ক্ষমতা ও শক্তি','অধ্যায় ৫: পদার্থের অবস্থা ও চাপ','অধ্যায় ৬: বস্তুর ওপর তাপের প্রভাব','অধ্যায় ৭: তরঙ্গ ও শব্দ','অধ্যায় ৮: আলোর প্রতিফলন','অধ্যায় ৯: আলোর প্রতিসরণ','অধ্যায় ১০: স্থির বিদ্যুৎ','অধ্যায় ১১: চল বিদ্যুৎ','অধ্যায় ১২: বিদ্যুতের চৌম্বক ক্রিয়া','অধ্যায় ১৩: তেজস্ক্রিয়তা ও ইলেকট্রনিকস'] },
  chemistry: { name: '🧪 রসায়ন', chapters: ['অধ্যায় ১: রসায়নের ধারণা','অধ্যায় ২: পদার্থের অবস্থা','অধ্যায় ৩: পদার্থের গঠন','অধ্যায় ৪: পর্যায় সারণি','অধ্যায় ৫: রাসায়নিক বন্ধন','অধ্যায় ৬: মোলের ধারণা ও রাসায়নিক গণনা','অধ্যায় ৭: রাসায়নিক বিক্রিয়া','অধ্যায় ৮: রসায়ন ও শক্তি','অধ্যায় ৯: এসিড-ক্ষারক সমতা','অধ্যায় ১০: খনিজ সম্পদ: ধাতু-অধাতু','অধ্যায় ১১: খনিজ সম্পদ: জীবাশ্ম','অধ্যায় ১২: আমাদের জীবনে রসায়ন'] },
  math:      { name: '📐 গণিত', chapters: ['অধ্যায় ১: বাস্তব সংখ্যা','অধ্যায় ২: সেট ও ফাংশন','অধ্যায় ৩: বীজগাণিতিক রাশি','অধ্যায় ৪: সূচক ও লগারিদম','অধ্যায় ৫: এক চলকবিশিষ্ট সমীকরণ','অধ্যায় ৬: রেখা, কোণ ও ত্রিভুজ','অধ্যায় ৭: ব্যাবহারিক জ্যামিতি','অধ্যায় ৮: বৃত্ত','অধ্যায় ৯: ত্রিকোণমিতিক অনুপাত','অধ্যায় ১০: দূরত্ব ও উচ্চতা','অধ্যায় ১১: বীজগাণিতিক অনুপাত ও সমানুপাত','অধ্যায় ১২: দুই চলকবিশিষ্ট সরল সহসমীকরণ','অধ্যায় ১৩: সসীম ধারা','অধ্যায় ১৪: অনুপাত, সদৃশতা ও প্রতিসমতা','অধ্যায় ১৫: ক্ষেত্রফল সম্পর্কিত উপপাদ্য ও সম্পাদ্য','অধ্যায় ১৬: পরিমিতি','অধ্যায় ১৭: পরিসংখ্যান'] }
};

const BLOOM_NAMES = ['মনে রাখো', 'বুঝো', 'প্রয়োগ করো', 'বিশ্লেষণ করো', 'মূল্যায়ন করো', 'সৃষ্টি করো'];

let currentSubject  = '';
let currentChapter  = '';
let currentQuestion = null;
let currentBloom    = 0;
let hintIndex       = 0;

document.addEventListener('DOMContentLoaded', () => {
  checkAuth();
  currentSubject = localStorage.getItem('selected_subject') || 'physics';
  const subj = SUBJECTS[currentSubject];
  document.getElementById('subject-title').textContent = subj.name;

  const list = document.getElementById('chapter-list');
  subj.chapters.forEach((ch) => {
    const btn = document.createElement('button');
    btn.className   = 'chapter-btn';
    btn.textContent = ch;
    btn.onclick     = () => startChapter(ch);
    list.appendChild(btn);
  });
});

function startChapter(chapter) {
  currentChapter = chapter;
  currentBloom   = 0;
  document.getElementById('chapter-section').style.display  = 'none';
  document.getElementById('question-section').style.display = 'block';
  loadQuestion();
}

async function loadQuestion() {
  document.getElementById('loading-question').style.display = 'block';
  document.getElementById('question-text').style.display    = 'none';
  document.getElementById('feedback-section').style.display = 'none';
  document.getElementById('hints-section').style.display    = 'none';
  document.getElementById('hint-text').style.display        = 'none';
  document.getElementById('answer-input').value             = '';
  hintIndex = 0;

  document.getElementById('bloom-badge').textContent = BLOOM_NAMES[currentBloom] || 'মনে রাখো';

  try {
    const studentId = localStorage.getItem('user_id') || 'user_1';
    // ✅ Python Backend use করো
    const data = await pyCall('/tutor/start-session', {
      student_id:     studentId,
      student_name:   localStorage.getItem('user_name') || 'Student',
      grade:          localStorage.getItem('user_grade') || 'SSC',
      subject:        currentSubject,
      chapter_id:     currentChapter,
      previous_score: 0
    });

    currentQuestion = data;
    document.getElementById('question-text').textContent = data.question;
    document.getElementById('marks-badge').textContent   = (data.marks || 5) + ' নম্বর';
    document.getElementById('loading-question').style.display = 'none';
    document.getElementById('question-text').style.display    = 'block';

    if (data.hints && data.hints.length > 0) {
      document.getElementById('hints-section').style.display = 'block';
    }
  } catch (err) {
    document.getElementById('loading-question').innerHTML = '<p>প্রশ্ন লোড করা যায়নি। Backend চালু আছে কিনা চেক করো।</p>';
  }
}

function showHint() {
  if (!currentQuestion || !currentQuestion.hints) return;
  const hints = currentQuestion.hints;
  if (hintIndex < hints.length) {
    document.getElementById('hint-text').textContent    = '💡 ' + hints[hintIndex];
    document.getElementById('hint-text').style.display = 'block';
    hintIndex++;
  }
}

async function submitAnswer() {
  const answer = document.getElementById('answer-input').value.trim();
  if (!answer) { alert('উত্তর লিখো!'); return; }

  const btn       = document.getElementById('submit-btn');
  btn.disabled    = true;
  btn.textContent = 'মূল্যায়ন হচ্ছে...';

  try {
    const studentId = localStorage.getItem('user_id') || 'user_1';
    // ✅ Python Backend use করো
    const data = await pyCall('/tutor/evaluate', {
      student_id:        studentId,
      subject:           currentSubject,
      chapter_id:        currentChapter,
      question:          currentQuestion.question,
      student_answer:    answer,
      expected_keywords: currentQuestion.expected_keywords || [],
      bloom_level:       currentBloom + 1,
      marks:             currentQuestion.marks || 5
    });

    document.getElementById('score-display').textContent         = `${data.score}/${data.max_score} নম্বর (${data.percentage}%)`;
    document.getElementById('feedback-text').textContent         = data.feedback_bengali || '';
    document.getElementById('correct-answer').textContent        = data.correct_answer ? '✅ সঠিক উত্তর: ' + data.correct_answer : '';
    document.getElementById('encouragement-text').textContent    = data.encouragement || '';
    document.getElementById('feedback-section').style.display    = 'block';

    if (data.percentage >= 70 && currentBloom < 5) currentBloom++;

    // ✅ MySQL এ session save করো (PHP API)
    await saveSession({
      subject:        currentSubject,
      chapter_id:     currentChapter,
      question:       currentQuestion.question,
      student_answer: answer,
      score:          data.score,
      max_score:      data.max_score,
      percentage:     data.percentage,
    });

  } catch (err) {
    alert('মূল্যায়ন করা যায়নি: ' + err.message);
  } finally {
    btn.disabled    = false;
    btn.textContent = 'উত্তর জমা দাও';
  }
}

function nextQuestion() {
  loadQuestion();
}

async function getFollowup() {
  const answer = document.getElementById('answer-input').value.trim();
  try {
    const studentId = localStorage.getItem('user_id') || 'user_1';
    const data = await pyCall('/tutor/followup', {
      student_id:        studentId,
      subject:           currentSubject,
      chapter_id:        currentChapter,
      previous_question: currentQuestion.question,
      student_answer:    answer,
      weak_areas:        [],
      bloom_level:       currentBloom + 1,
    });
    currentQuestion = {
      question:          data.followup_question,
      hints:             data.hints || [],
      marks:             5,
      expected_keywords: []
    };
    document.getElementById('question-text').textContent      = data.followup_question;
    document.getElementById('feedback-section').style.display = 'none';
    document.getElementById('answer-input').value             = '';
  } catch (err) {
    alert('ফলো-আপ প্রশ্ন আনা যায়নি।');
  }
}
