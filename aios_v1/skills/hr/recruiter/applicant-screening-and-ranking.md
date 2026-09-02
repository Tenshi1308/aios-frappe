---
name: "Applicant Screening and Ranking Workflow"
slug: "applicant-screening-and-ranking"
version: "1.0.0"
branch: "hr"
role: "recruiter"
tools_required:
  - "screen_applicant_profile"
triggers:
  - "screening pelamar kerja"
  - "skoring resume cv"
  - "seleksi berkas kandidat"
  - "peringkat pelamar kerja"
  - "evaluasi kecocokan pelamar"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Recruiter, skill ini mengatur alur penyaringan dan pencocokan resume kandidat (*CV Screening*) terhadap kualifikasi posisi yang dilamar, perhitungan skor kesesuaian (*Match Score*), dan penyusunan rekomendasi kelolosan ke tahap wawancara.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Profil & Portofolio Kandidat**:
   * Kumpulkan data `skills`, `years_of_experience`, dan `applied_position`.
2. **Kalkulasi Skor Kesesuaian (`screen_applicant_profile`)**:
   * Panggil `screen_applicant_profile(candidate_name, skills, years_of_experience, applied_position)`.
   * Evaluasi rekomendasi kelolosan: Lolos Interview ($\ge 75\%$) atau Talent Pool ($< 75\%$).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Pengalaman kerja harus bernilai angka non-negatif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Proses penyaringan wajib adil, bebas bias gender, suku, atau agama (*Equal Employment Opportunity*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Screening CV kandidat Dian Pratama yang melamar Senior Backend Dev dengan pengalaman 5 tahun dan skill Python, PostgreSQL, Docker, Redis."
**Tool Call:** `screen_applicant_profile(candidate_name="Dian Pratama", skills=["Python", "PostgreSQL", "Docker", "Redis"], years_of_experience=5, applied_position="Senior Backend Dev")`
**Respon AI:** "Screening CV Dian Pratama: Skor kecocokan 82.0% (Rekomendasi: Lolos ke Tahap Interview User)."
