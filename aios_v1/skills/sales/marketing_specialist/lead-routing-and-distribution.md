---
name: "Lead Routing and Distribution Workflow"
slug: "lead-routing-and-distribution"
version: "1.0.0"
branch: "sales"
role: "marketing_specialist"
tools_required:
  - "match_lead_to_sales_rep"
triggers:
  - "distribusi lead baru"
  - "alokasi prospek sales"
  - "lead routing"
  - "penugasan prospek masuk"
  - "pembagian lead penjualan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Marketing Specialist, skill ini mengatur alur penyaluran dan pencocokan otomatis prospek masuk (*Inbound Leads*) kepada staf sales representative yang paling tepat berdasarkan portofolio industri dan skala nilai peluang transaksi.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Kualifikasi Awal Prospek Masuk**:
   * Kumpulkan data nama perusahaan, sektor industri, dan estimasi nilai transaksi.
2. **Pencocokan & Alokasi Tenaga Sales (`match_lead_to_sales_rep`)**:
   * Panggil `match_lead_to_sales_rep(lead_name, lead_industry, estimated_value)`.
   * Teruskan kontak prospek ke perwakilan penjualan terpilih.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter `lead_name` dan `estimated_value` harus terisi valid.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Pembagian lead harus memperhatikan kapasitas beban kerja tenaga sales secara adil.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Ada prospek baru PT Multi Mineral sektor tambang dengan estimasi deal Rp 250.000.000."
**Tool Call:** `match_lead_to_sales_rep(lead_name="PT Multi Mineral", lead_industry="Mining", estimated_value=250000000)`
**Respon AI:** "Prospek PT Multi Mineral dialokasikan ke Budi Santoso (Senior Enterprise Rep)."
