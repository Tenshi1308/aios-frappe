---
name: "OKR Alignment and Variance Governance Workflow"
slug: "okr-alignment-and-variance-governance"
version: "1.0.0"
branch: "planning"
role: "planning_manager"
tools_required:
  - "track_strategic_initiatives"
  - "calculate_enterprise_scorecard"
  - "publish_corporate_bulletin"
triggers:
  - "penyelarasan inisiatif strategis okr"
  - "evaluasi balanced scorecard perusahaan"
  - "tata kelola rencana strategis korporat"
  - "rilis buletin pengumuman kebijakan direksi"
  - "strategic okr governance"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Planning Manager di divisi Strategic & Operational Planning, skill ini mengatur kepemimpinan penyelarasan sasaran strategis (*OKR & Strategic Initiatives Tracking*), evaluasi performa korporat menyeluruh menggunakan pendekatan 4 Perspektif *Balanced Scorecard*, serta penerbitan buletin pengumuman kebijakan strategis (*Corporate Bulletin Announcement*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Pelacakan Inisiatif Strategis OKR (`track_strategic_initiatives`)**:
   * Panggil `track_strategic_initiatives(initiative_title, target_completion_date, milestone_objectives, sponsor_lead)`.
   * Terbitkan Action Draft Card untuk komitmen pimpinan proyek.
2. **Evaluasi Skor Komposit Balanced Scorecard (`calculate_enterprise_scorecard`)**:
   * Panggil `calculate_enterprise_scorecard(financial_score, customer_score, internal_process_score, learning_growth_score)`.
3. **Penerbitan Draf Pengumuman Buletin Korporat (`publish_corporate_bulletin`)**:
   * Panggil `publish_corporate_bulletin(bulletin_title, target_audience, announcement_body)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Seluruh skor perspektif harus bernilai antara skala 0 hingga 100.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Target inisiatif strategis wajib selaras dengan Rencana Kerja dan Anggaran Perusahaan (RKAP).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung Balanced Scorecard korporat jika skor Finansial 88, Pelanggan 82, Proses Internal 80, dan SDM 85."
**Tool Call:** `calculate_enterprise_scorecard(financial_score=88, customer_score=82, internal_process_score=80, learning_growth_score=85)`
**Respon AI:** "Balanced Scorecard Rating: 84.1/100 (Grade: B - Solid Execution)."
