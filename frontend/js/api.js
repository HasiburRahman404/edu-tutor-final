// ─── EduTutor BD — API Helper (Supabase + Vercel) ────────────
// No PHP needed — auth/progress go through Supabase JS directly

// ⚠️  REPLACE THESE with your actual Supabase project values
const SUPABASE_URL      = 'https://jdyyyefybicrqxdagvwf.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpkeXl5ZWZ5YmljcnF4ZGFndndmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAxMzE4NTIsImV4cCI6MjA5NTcwNzg1Mn0.aAe6aeSr5LRTtxqCQZ6fRGt08G52lFMTwD2ZZQ6kIa0';

// Python AI backend on Vercel (same domain)
const PY_API = '/api';

// ─── Supabase client (loaded from CDN in each HTML) ──────────
function getSupabase() {
    return window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
}

// ─── Python AI API ────────────────────────────────────────────
async function pyCall(endpoint, body = null) {
    const sb      = getSupabase();
    const session = await sb.auth.getSession();
    const token   = session?.data?.session?.access_token || '';

    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const options = { method: body ? 'POST' : 'GET', headers };
    if (body) options.body = JSON.stringify(body);

    const res  = await fetch(PY_API + endpoint, options);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'সার্ভার error');
    return data;
}

// ─── Auth helpers ─────────────────────────────────────────────
async function checkAuth() {
    const sb      = getSupabase();
    const session = await sb.auth.getSession();
    if (!session?.data?.session) {
        window.location.href = '/index.html';
        return null;
    }
    return session.data.session;
}

async function logout() {
    const sb = getSupabase();
    await sb.auth.signOut();
    localStorage.clear();
    window.location.href = '/index.html';
}

// ─── UI helpers ───────────────────────────────────────────────
function showError(msg) {
    const el = document.getElementById('error-msg');
    if (el) { el.textContent = '❌ ' + msg; el.style.display = 'block'; }
}

function showSuccess(msg) {
    const el = document.getElementById('success-msg');
    if (el) { el.textContent = '✅ ' + msg; el.style.display = 'block'; }
}

function hideMessages() {
    const e = document.getElementById('error-msg');
    const s = document.getElementById('success-msg');
    if (e) e.style.display = 'none';
    if (s) s.style.display = 'none';
}

function setLoading(btnId, loading, text = '') {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.disabled    = loading;
    btn.textContent = loading ? 'অপেক্ষা করুন...' : (text || btn.dataset.text);
}

// ─── Save session to Supabase directly ───────────────────────
async function saveSession(sessionData) {
    const sb      = getSupabase();
    const session = await sb.auth.getSession();
    const userId  = session?.data?.session?.user?.id;
    if (!userId) return;

    try {
        await sb.from('sessions').insert({
            user_id:        userId,
            subject:        sessionData.subject,
            chapter_id:     sessionData.chapter_id,
            question:       sessionData.question,
            student_answer: sessionData.student_answer,
            score:          sessionData.score,
            max_score:      sessionData.max_score,
            percentage:     sessionData.percentage,
        });
    } catch (e) {
        console.log('Session save error:', e);
    }
}
