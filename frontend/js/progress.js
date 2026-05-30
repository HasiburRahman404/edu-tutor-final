// ─── Progress — Supabase Direct ──────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
    const session = await checkAuth();
    if (!session) return;

    const userId = session.user.id;
    const sb     = getSupabase();

    try {
        const { data: sessions, error } = await sb
            .from('sessions')
            .select('subject, score, max_score, percentage')
            .eq('user_id', userId);

        if (error) throw error;

        const total    = sessions.length;
        const avgScore = total > 0
            ? Math.round(sessions.reduce((s, r) => s + (r.percentage || 0), 0) / total)
            : 0;

        document.getElementById('total-sessions').textContent = total || '০';
        document.getElementById('avg-score').textContent      = avgScore + '%';

        const subjectNames = {
            physics:   '⚛️ পদার্থবিজ্ঞান',
            chemistry: '🧪 রসায়ন',
            math:      '📐 গণিত'
        };

        const grouped = { physics: [], chemistry: [], math: [] };
        sessions.forEach(s => {
            if (grouped[s.subject]) grouped[s.subject].push(s.percentage || 0);
        });

        const list = document.getElementById('subject-progress');
        list.innerHTML = '';

        Object.entries(grouped).forEach(([key, scores]) => {
            const count  = scores.length;
            const score  = count > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / count) : 0;
            const status = score >= 70 ? '✅ ভালো করছ'
                         : score >= 50 ? '⚠️ উন্নতি দরকার'
                         : '❌ বেশি মনোযোগ দরকার';

            list.innerHTML += `
              <div class="subject-progress-item">
                <h4>${subjectNames[key]}</h4>
                <div class="progress-bar-bg">
                  <div class="progress-bar-fill" style="width:${score}%"></div>
                </div>
                <p style="font-size:13px;color:#888;margin-top:6px">
                  ${score}% · ${count} সেশন · ${status}
                </p>
              </div>`;
        });

        document.getElementById('loading-progress').style.display  = 'none';
        document.getElementById('progress-content').style.display  = 'block';

    } catch (err) {
        document.getElementById('loading-progress').innerHTML =
            '<p>লোড করা যায়নি: ' + err.message + '</p>';
    }
});
