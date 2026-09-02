---
name: "Employee Master Onboarding Workflow"
slug: "employee-master-onboarding"
version: "1.0.0"
branch: "hr"
role: "hr_staff"
tools_required:
  - "create_employee_record"
  - "check_probation_status"
triggers:
  - "input karyawan baru"
  - "onboarding pegawai"
  - "master data karyawan"
  - "cek status probation"
  - "evaluasi masa percobaan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai HR Staff, skill ini mengatur pencatatan master data pegawai baru (*Employee Master Record*), penerbitan draf onboarding karyawan baru untuk diotorisasi manajer, serta pemantauan berkala masa probation karyawan yang akan segera berakhir.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Data Karyawan Baru (`create_employee_record`)**:
   * Panggil `create_employee_record(full_name, nik_ktp, position, department, join_date, base_salary)`.
   * Terbitkan Action Draft Card untuk otorisasi HR Manager.
2. **Pemantauan Masa Evaluasi Probation (`check_probation_status`)**:
   * Panggil `check_probation_status(days_window=30)` untuk menyaring karyawan yang mendekati batas 3 bulan masa percobaan.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* NIK KTP dan tanggal mulai kerja harus valid.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh data pribadi karyawan (*PII*) wajib dilindungi sesuai regulasi privasi data.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan draf master data karyawan baru atas nama Ahmad Fauzi, posisi Junior Frontend Dev di Divisi IT mulai 1 Oktober 2026 gaji Rp 7.500.000."
**Tool Call:** `create_employee_record(full_name="Ahmad Fauzi", nik_ktp="3171029988770001", position="Junior Frontend Dev", department="Engineering & IT", join_date="2026-10-01", base_salary=7500000)`
**Respon AI:** "Draf Master Karyawan 'Ahmad Fauzi' berhasil dibuat: [Review Draf](/draft/DRF-EMP-001)."
