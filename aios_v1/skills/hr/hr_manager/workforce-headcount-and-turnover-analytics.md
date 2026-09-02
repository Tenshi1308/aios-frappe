---
name: "Workforce Headcount and Turnover Analytics Workflow"
slug: "workforce-headcount-and-turnover-analytics"
version: "1.0.0"
branch: "hr"
role: "hr_manager"
tools_required:
  - "track_employee_turnover_rate"
  - "run_headcount_report"
triggers:
  - "laporan headcount karyawan"
  - "turnover rate pegawai"
  - "analisis retensi sdm"
  - "demografi tenaga kerja"
  - "rekap jumlah karyawan divisi"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai HR Manager, skill ini mengatur analisis strategis jumlah tenaga kerja (*Headcount Analytics*) lintas seluruh departemen perusahaan, evaluasi rasio perputaran karyawan (*Employee Turnover Rate*), serta pemantauan kesehatan retensi talenta korporat.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Laporan Demografi Tenaga Kerja (`run_headcount_report`)**:
   * Panggil `run_headcount_report()` untuk memetakan jumlah karyawan aktif per divisi, gender, dan jenis kontrak.
2. **Evaluasi Rasio Turnover Karyawan (`track_employee_turnover_rate`)**:
   * Panggil `track_employee_turnover_rate(period_year=2026)`.
   * Bandingkan dengan rata-rata patokan industri (*Industry Benchmark*).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Data kepegawaian harus terhubung dengan database master karyawan aktif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika turnover rate melebihi ambang batas risiko (> 12%), segera susun rencana aksi retensi.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tampilkan laporan komposisi headcount karyawan dan analisis turnover tahun 2026."
**Tool Call:** `run_headcount_report()`
**Tool Call:** `track_employee_turnover_rate(period_year=2026)`
**Respon AI:** "Total 84 karyawan aktif di 5 departemen. Turnover rate tahun 2026 terpantau sangat sehat di angka 6.8% (Benchmark: 10.5%)."
