---
name: "Pareto VIP and Churn Risk Analysis Workflow"
slug: "pareto-vip-and-churn-analysis"
version: "1.0.0"
branch: "sales"
role: "sales_data_analyst"
tools_required:
  - "get_top_pareto_customers"
  - "predict_customer_churn_risk"
triggers:
  - "pelanggan pareto 80 20"
  - "vip customer analysis"
  - "prediksi risiko churn"
  - "retensi akun kunci"
  - "analisis pelanggan strategis"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Sales Data Analyst, skill ini mengatur identifikasi 20% pelanggan VIP yang menyumbang 80% omzet (*Pareto Analysis*) serta mendeteksi dini indikasi penurunan aktivitas (*Churn Risk*) pada pelanggan strategis.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Identifikasi Pelanggan Pareto Kunci (`get_top_pareto_customers`)**:
   * Panggil `get_top_pareto_customers(top_percent)`.
2. **Evaluasi Risiko Kehilangan Pelanggan (`predict_customer_churn_risk`)**:
   * Panggil `predict_customer_churn_risk(customer_id, days_since_last_order)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter cut-off persentase pareto antara 10% s/d 30%.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Pelanggan VIP yang terdeteksi berisiko churn tinggi wajib segera dilaporkan ke Sales Manager.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Analisis pelanggan Pareto 20% teratas dan periksa risiko churn pelanggan #CUST-089."
**Tool Call:** `get_top_pareto_customers(top_percent=20.0)`
**Tool Call:** `predict_customer_churn_risk(customer_id="CUST-089", days_since_last_order=64)`
**Respon AI:** "2 Pelanggan teratas menyumbang 64.1% omzet. Pelanggan CUST-089 terdeteksi risiko Churn MEDIUM (inaktif 64 hari)."
