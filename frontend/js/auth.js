// ─── Login — Supabase Auth ────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
    const sb      = getSupabase();
    const session = await sb.auth.getSession();
    if (session?.data?.session) {
        const role = localStorage.getItem('user_role');
        window.location.href = role === 'admin' ? '/admin.html' : '/home.html';
    }
    const btn = document.getElementById('login-btn');
    if (btn) btn.dataset.text = 'লগইন করুন';
});

async function handleLogin() {
    hideMessages();
    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
        showError('ইমেইল ও পাসওয়ার্ড দিন।');
        return;
    }

    setLoading('login-btn', true);
    try {
        const sb  = getSupabase();
        const res = await sb.auth.signInWithPassword({ email, password });

        if (res.error) throw new Error(res.error.message);

        const userId = res.data.user.id;

        // Fetch profile for name/role/grade
        const { data: profile } = await sb
            .from('profiles')
            .select('name, role, grade')
            .eq('id', userId)
            .single();

        localStorage.setItem('user_id',    userId);
        localStorage.setItem('user_name',  profile?.name  || email);
        localStorage.setItem('user_role',  profile?.role  || 'student');
        localStorage.setItem('user_grade', profile?.grade || 'SSC');

        if (profile?.role === 'admin') {
            window.location.href = '/admin.html';
        } else {
            window.location.href = '/home.html';
        }
    } catch (err) {
        showError(err.message || 'লগইন ব্যর্থ হয়েছে।');
    } finally {
        setLoading('login-btn', false, 'লগইন করুন');
    }
}
