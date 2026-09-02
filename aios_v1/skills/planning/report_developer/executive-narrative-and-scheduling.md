---
name: "Executive Narrative and Scheduling Workflow"
slug: "executive-narrative-and-scheduling"
version: "1.0.0"
branch: "planning"
role: "report_developer"
tools_required:
  - "generate_executive_summary"
  - "schedule_automated_report"
triggers:
  - "rangkuman narasi eksekutif direksi"
  - "jadwalkan pengiriman laporan otomatis"
  - "executive summary report"
  - "otomasi jadwal laporan bulanan"
  - "report broadcast schedule"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Report Developer, skill ini mengatur pembuatan rangkuman narasi ringkas tingkat eksekutif (*Executive Summary & Narrative Insights*) untuk pimpinan C-Level / Dewan Direksi, serta penyusunan draf jadwal otomatisasi pengiriman laporan berkala (*Automated Report Scheduling*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penyusunan Rangkuman Narasi Eksekutif (`generate_executive_summary`)**:
   * Panggil `generate_executive_summary(period_title)`.
   * Hasilkan poin-poin capaian strategis dan proyeksi bisnis ke depan.
2. **Penerbitan Draf Jadwal Otomasi Laporan (`schedule_automated_report`)**:
   * Panggil `schedule_automated_report(report_title, frequency, recipient_emails)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Daftar email penerima harus merupakan alamat email yang valid.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Laporan dengan data sensitif direksi dilarang dijadwalkan ke milis publik umum.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan narasi eksekutif untuk Q3-2026 dan jadwalkan pengiriman laporan mingguan ke direksi@ekasa.co.id setiap Senin pagi."
**Tool Call:** `generate_executive_summary(period_title="Q3-2026 Performance Review")`
**Tool Call:** `schedule_automated_report(report_title="Weekly Executive Brief", frequency="Weekly (Monday 08:00 WIB)", recipient_emails=["direksi@ekasa.co.id"])`
**Respon AI:** "Executive Summary Q3-2026 berhasil dibuat. Draf Jadwal Otomasi Laporan siap di-approve: [Review Draf](/draft/DRF-SCH-001)."
