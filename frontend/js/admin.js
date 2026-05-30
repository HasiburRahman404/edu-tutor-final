// ─── Admin Dashboard — Supabase Direct ───────────────────────
document.addEventListener('DOMContentLoaded', async () => {
    const session = await checkAuth();
    if (!session) return;

    const role = localStorage.getItem('user_role');
    if (role !== 'admin') {
        window.location.href = '/index.html';
        return;
    }

    document.getElementById('admin-name').textContent =
        localStorage.getItem('user_name') || 'Admin';

    const sb = getSupabase();

    try {
        // Fetch all student profiles
        const { data: profiles } = await sb
            .from('profiles')
            .select('*')
            .eq('role', 'student');

        // Fetch all sessions
        const { data: allSessions } = await sb
            .from('sessions')
            .select('user_id, subject, percentage');

        const totalStudents = profiles?.length || 0;
        const totalSessions = allSessions?.length || 0;
        const overallAvg    = totalSessions > 0
            ? Math.round(allSessions.reduce((s, r) => s + (r.percentage || 0), 0) / totalSessions)
            : 0;

        document.getElementById('total-students').textContent = totalStudents || '০';
        document.getElementById('total-sessions').textContent = totalSessions || '০';
        document.getElementById('overall-avg').textContent    = overallAvg + '%';

        const list = document.getElementById('student-list');
        list.innerHTML = '';

        if (profiles && profiles.length > 0) {
            profiles.forEach(student => {
                const userSessions = allSessions.filter(s => s.user_id === student.id);
                const count        = userSessions.length;
                const avgScore     = count > 0
                    ? Math.round(userSessions.reduce((s, r) => s + (r.percentage || 0), 0) / count)
                    : 0;

                const subjAvg = (subj) => {
                    const ss = userSessions.filter(s => s.subject === subj);
                    return ss.length > 0
                        ? Math.round(ss.reduce((s, r) => s + (r.percentage || 0), 0) / ss.length)
                        : 0;
                };

                const status = avgScore >= 70 ? '✅ ভালো'
                             : avgScore >= 50 ? '⚠️ মাঝারি'
                             : '❌ দুর্বল';

                list.innerHTML += `
                  <div class="subject-progress-item" style="margin-bottom:12px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                      <h4 style="margin:0">${student.name}</h4>
                      <span style="font-size:13px;color:#888">${student.email}</span>
                    </div>
                    <div style="display:flex;gap:16px;font-size:13px;color:#888;margin-bottom:8px">
                      <span>📚 ${count} সেশন</span>
                      <span>📊 গড়: ${avgScore}%</span>
                      <span>${status}</span>
                      <span>🎓 ${student.grade || 'SSC'}</span>
                    </div>
                    <div class="progress-bar-bg">
                      <div class="progress-bar-fill" style="width:${avgScore}%"></div>
                    </div>
                    <div style="display:flex;gap:8px;margin-top:8px;font-size:12px;color:#888">
                      <span>⚛️ পদার্থ: ${subjAvg('physics')}%</span>
                      <span>🧪 রসায়ন: ${subjAvg('chemistry')}%</span>
                      <span>📐 গণিত: ${subjAvg('math')}%</span>
                    </div>
                  </div>`;
            });
        } else {
            list.innerHTML = '<p style="color:#888;text-align:center">এখনো কোনো শিক্ষার্থী নেই।</p>';
        }

        document.getElementById('loading-admin').style.display = 'none';
        document.getElementById('admin-content').style.display = 'block';

    } catch (err) {
        document.getElementById('loading-admin').innerHTML =
            '<p>লোড করা যায়নি: ' + err.message + '</p>';
    }
});
