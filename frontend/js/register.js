// ─── Register — Supabase Auth ─────────────────────────────────
let selectedRole = 'student';
const ADMIN_CODE = 'edututor2024';   // Change this secret!

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('register-btn');
    if (btn) btn.dataset.text = 'রেজিস্ট্রেশন করুন';
});

function setRole(role) {
    selectedRole = role;
    document.querySelectorAll('[id^="role-"]').forEach(b => b.classList.remove('active'));
    document.getElementById('role-' + role).classList.add('active');
    document.getElementById('grade-group').style.display      = role === 'student' ? 'block' : 'none';
    document.getElementById('admin-code-group').style.display = role === 'admin'   ? 'block' : 'none';
}

async function handleRegister() {
    hideMessages();
    const name     = document.getElementById('name').value.trim();
    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!name || !email || !password) {
        showError('সব তথ্য পূরণ করুন।');
        return;
    }
    if (password.length < 6) {
        showError('পাসওয়ার্ড কমপক্ষে ৬ অক্ষরের হতে হবে।');
        return;
    }
    if (selectedRole === 'admin') {
        const adminCode = document.getElementById('admin-code').value.trim();
        if (adminCode !== ADMIN_CODE) {
            showError('Admin code সঠিক নয়।');
            return;
        }
    }

    setLoading('register-btn', true);
    try {
        const sb  = getSupabase();
        const res = await sb.auth.signUp({
            email,
            password,
            options: {
                data: { name, grade: 'SSC', role: selectedRole }
            }
        });

        if (res.error) throw new Error(res.error.message);

        showSuccess('অ্যাকাউন্ট তৈরি হয়েছে! ইমেইল চেক করুন (confirm link আসতে পারে)।');
        setTimeout(() => window.location.href = '/index.html', 3000);
    } catch (err) {
        showError(err.message || 'রেজিস্ট্রেশন ব্যর্থ হয়েছে।');
    } finally {
        setLoading('register-btn', false, 'রেজিস্ট্রেশন করুন');
    }
}
