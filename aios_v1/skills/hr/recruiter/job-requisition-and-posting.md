---
name: "Job Requisition and Posting Workflow"
slug: "job-requisition-and-posting"
version: "1.0.0"
branch: "hr"
role: "recruiter"
tools_required:
  - "post_job_vacancy"
triggers:
  - "buka lowongan kerja"
  - "job posting baru"
  - "permintaan rekrutmen pegawai"
  - "job vacancy requisition"
  - "lowongan posisi baru"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Recruiter di divisi Human Resource Management, skill ini mengatur alur penyusunan draf pembukaan lowongan pekerjaan baru (*Job Requisition*), penetapan kualifikasi kompetensi jabatan, dan penerbitan draf lowongan untuk mendapatkan persetujuan pimpinan.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penyusunan Rincian Formasi & Kualifikasi Lowongan**:
   * Tentukan `position_title`, `department`, `employment_type`, dan daftar `requirements`.
2. **Penerbitan Draf Lowongan Kerja (`post_job_vacancy`)**:
   * Panggil `post_job_vacancy(position_title, department, requirements, employment_type)`.
   * Terbitkan Action Draft Card untuk otorisasi HR Manager.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Departemen dan formasi jabatan harus terdaftar di bagan organisasi.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** mempublikasikan lowongan ke publik tanpa persetujuan draf dari HR Manager (*Draft Card mandatory*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan draf lowongan kerja untuk posisi Senior Backend Engineer di Divisi IT."
**Tool Call:** `post_job_vacancy(position_title="Senior Backend Engineer", department="Engineering & IT", requirements=["Minimal 4 tahun pengalaman Python/Node.js", "Paham Microservices & SQL", "Terbiasa CI/CD"], employment_type="Full-time")`
**Respon AI:** "Draf Lowongan Kerja 'Senior Backend Engineer' berhasil dibuat: [Review Draf](/draft/DRF-JOB-001)."
