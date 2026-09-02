---
name: "Batch Payroll Processing Workflow"
slug: "batch-payroll-processing"
version: "1.0.0"
branch: "hr"
role: "payroll_officer"
tools_required:
  - "calculate_payroll_batch"
  - "generate_payslip"
triggers:
  - "proses payroll bulanan"
  - "hitung gaji karyawan massal"
  - "cetak slip gaji"
  - "rekap gaji bulanan"
  - "payroll batch processing"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Payroll Officer, skill ini mengatur kalkulasi gaji massal bulanan seluruh karyawan perusahaan (*Batch Payroll*), pemotongan pajak PPh 21 dan iuran BPJS, penerbitan draf pencairan gaji untuk otorisasi pimpinan, serta pembuatan rincian slip gaji personal karyawan.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Kalkulasi Batch Penggajian Massal (`calculate_payroll_batch`)**:
   * Panggil `calculate_payroll_batch(payroll_month, total_employees)`.
   * Terbitkan Action Draft Card untuk otorisasi Finance & HR Manager.
2. **Penerbitan Rincian Slip Gaji Personal (`generate_payslip`)**:
   * Panggil `generate_payslip(employee_id, base_salary, allowances, overtime_pay)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Data kehadiran bulanan harus sudah dikunci (*Attendance Finalized*).

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** mencairkan dana gaji tanpa kartu otorisasi persetujuan draf (*Draft Card mandatory*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Jalankan kalkulasi payroll bulan September 2026 untuk 45 karyawan aktif."
**Tool Call:** `calculate_payroll_batch(payroll_month="September 2026", total_employees=45)`
**Respon AI:** "Draf Penggajian September 2026 senilai Rp 351.900.000 (Take Home Pay) siap diotorisasi: [Review Draf](/draft/DRF-PAYROLL-001)."
