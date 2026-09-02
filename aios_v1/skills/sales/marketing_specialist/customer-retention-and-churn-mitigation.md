---
name: "Customer Retention and Churn Mitigation Workflow"
slug: "customer-retention-and-churn-mitigation"
version: "1.0.0"
branch: "sales"
role: "marketing_specialist"
tools_required:
  - "predict_customer_churn_risk"
triggers:
  - "retensi pelanggan"
  - "mitigasi churn"
  - "program loyalitas pelanggan"
  - "pencegahan kehilangan klien"
  - "promosi reaktivasi akun"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Marketing Specialist, skill ini mengatur perancangan kampanye retensi pelanggan, reaktivasi akun yang mulai pasif, dan pencegahan beralihnya pelanggan ke kompetitor berbasis data jeda transaksi (*Recency Analysis*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Tingkat Risiko Churn (`predict_customer_churn_risk`)**:
   * Panggil `predict_customer_churn_risk(customer_id, days_since_last_order)`.
2. **Penerapan Rekomendasi Kampanye Pemasaran**:
   * Terapkan voucher diskon reaktivasi atau penjadwalan promo khusus sesuai tingkat risiko.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter `days_since_last_order` harus berupa integer non-negatif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Promo retensi harus tetap mempertahankan margin keuntungan minimum.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Periksa pelanggan CUST-012 yang sudah 95 hari belum beli lagi."
**Tool Call:** `predict_customer_churn_risk(customer_id="CUST-012", days_since_last_order=95)`
**Respon AI:** "Pelanggan CUST-012 terdeteksi HIGH CHURN RISK. Rekomendasi: Segera kirimkan voucher promo retensi khusus."
