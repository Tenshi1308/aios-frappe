---
name: "Internal Audit and Findings Reporting Workflow"
slug: "internal-audit-and-findings-reporting"
version: "1.0.0"
branch: "quality"
role: "quality_auditor"
tools_required:
  - "schedule_quality_audit"
  - "generate_audit_report"
triggers:
  - "jadwal audit mutu internal"
  - "audit iso 9001"
  - "laporan temuan audit nc"
  - "audit klausul sistem manajemen mutu"
  - "internal quality audit reporting"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Quality Auditor, skill ini mengatur penjadwalan audit mutu internal korporat (*Quality Audit Scheduling*), pelaksanaan tinjauan kepatuhan terhadap klausul ISO 9001:2015, pencatatan temuan ketidaksesuaian (*Non-Conformance Findings*), dan penerbitan laporan rekomendasi audit.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Jadwal Audit Mutu (`schedule_quality_audit`)**:
   * Panggil `schedule_quality_audit(audit_scope, lead_auditor, planned_date)`.
   * Terbitkan Action Draft Card untuk persetujuan Manajemen Representatif.
2. **Kompilasi Laporan Hasil Temuan Audit (`generate_audit_report`)**:
   * Panggil `generate_audit_report(audit_id, standard)`.
   * Rangkum temuan Minor NC / Major NC beserta rekomendasi perbaikan.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Auditor internal harus memiliki sertifikasi pemahaman audit ISO 9001 yang valid.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh temuan Major NC wajib ditindaklanjuti sebelum penutupan siklus audit (*Audit Closeout*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Jadwalkan audit mutu internal untuk Divisi Gudang & Pengadaan pada 28 September 2026 oleh Lead Auditor Hendra Gunawan."
**Tool Call:** `schedule_quality_audit(audit_scope="Gudang & Pengadaan Bahan Baku", lead_auditor="Hendra Gunawan", planned_date="2026-09-28")`
**Respon AI:** "Draf Jadwal Audit Mutu ISO 9001 (Gudang & Pengadaan) berhasil dibuat: [Review Draf](/draft/DRF-AUDIT-001)."
