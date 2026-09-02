---
name: "Overtime and BPJS Statutory Deductions Workflow"
slug: "overtime-and-bpjs-statutory-deductions"
version: "1.0.0"
branch: "hr"
role: "payroll_officer"
tools_required:
  - "calculate_overtime_hours"
  - "calculate_bpjs_contributions"
triggers:
  - "hitung lembur karyawan"
  - "upah lembur depnaker"
  - "iuran bpjs ketenagakerjaan"
  - "potongan bpjs kesehatan"
  - "statutory payroll deductions"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Payroll Officer, skill ini mengatur penghitungan upah lembur resmi sesuai formula ketenagakerjaan (hari kerja biasa vs akhir pekan) serta penghitungan porsi iuran jaminan sosial BPJS Ketenagakerjaan dan BPJS Kesehatan baik yang ditanggung perusahaan maupun dipotong dari upah karyawan.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penghitungan Upah Lembur Karyawan (`calculate_overtime_hours`)**:
   * Panggil `calculate_overtime_hours(employee_id, hourly_rate, workday_overtime_hours, weekend_overtime_hours)`.
2. **Kalkulasi Kontribusi & Potongan BPJS (`calculate_bpjs_contributions`)**:
   * Panggil `calculate_bpjs_contributions(gross_salary)`.
   * Pisahkan porsi beban tunjangan perusahaan (*Company Contribution*) dan potongan gaji (*Employee Deduction*).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Upah per jam mengacu pada formula resmi Depnaker ($\text{Gaji Pokok} / 173$).

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Perhitungan lembur dan BPJS wajib mematuhi batas pagu regulasi ketenagakerjaan.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung upah lembur karyawan EMP-012 dengan upah Rp 50.000/jam (3 jam kerja reguler dan 4 jam libur akhir pekan)."
**Tool Call:** `calculate_overtime_hours(employee_id="EMP-012", hourly_rate=50000, workday_overtime_hours=3, weekend_overtime_hours=4)`
**Respon AI:** "Perhitungan Lembur #EMP-012: Rp 675.000 (Total 7 jam lembur terverifikasi)."
