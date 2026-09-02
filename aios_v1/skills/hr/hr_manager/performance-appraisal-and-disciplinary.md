---
name: "Performance Appraisal and Disciplinary Workflow"
slug: "performance-appraisal-and-disciplinary"
version: "1.0.0"
branch: "hr"
role: "hr_manager"
tools_required:
  - "conduct_performance_appraisal"
  - "process_personnel_action"
  - "issue_warning_letter"
triggers:
  - "penilaian kinerja tahunan"
  - "tindakan personalia promosi mutasi"
  - "surat peringatan sp karyawan"
  - "evaluasi performa kpi tahunan"
  - "tata tertib kedisiplinan pegawai"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai HR Manager, skill ini mengatur kepemimpinan tata kelola personalia korporat: pelaksanaan penilaian kinerja tahunan (*Performance Appraisal & KPI Grade*), penerbitan draf tindakan personalia (Promosi Jabatan, Mutasi, Penyesuaian Gaji), dan penegakan sanksi disipliner resmi (Surat Peringatan SP 1/SP 2/SP 3).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penilaian Kinerja Berkala (`conduct_performance_appraisal`)**:
   * Panggil `conduct_performance_appraisal(employee_id, kpi_score, core_values_score, manager_notes)`.
   * Tetapkan predikat kinerja: Grade A (Exceeds), Grade B (Meets), atau Grade C (Needs Improvement).
2. **Keputusan Tindakan Personalia Promosi/Mutasi (`process_personnel_action`)**:
   * Untuk karyawan berprestasi tinggi, panggil `process_personnel_action(...)`.
3. **Penegakan Disiplin Kerja (`issue_warning_letter`)**:
   * Untuk pelanggaran SOP, panggil `issue_warning_letter(employee_id, warning_level, violation_details)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter skor KPI dan nilai budaya kerja harus bernilai 0 - 100.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh tindakan sanksi disiplin dan promosi wajib melalui kartu otorisasi draf persetujuan.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan draf penilaian kinerja tahunan untuk karyawan EMP-005 dengan skor KPI 88, nilai budaya 90, dan catatan 'Sangat berprestasi'."
**Tool Call:** `conduct_performance_appraisal(employee_id="EMP-005", kpi_score=88.0, core_values_score=90.0, manager_notes="Sangat berprestasi dan konsisten melampaui target tim.")`
**Respon AI:** "Draf Penilaian Kinerja #EMP-005 Grade A (Exceeds Expectations) berhasil dibuat: [Review Draf](/draft/DRF-APPRAISAL-001)."
