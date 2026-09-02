---
name: "Data Quality Audit and Anomaly Detection Workflow"
slug: "data-quality-audit-and-anomaly-detection"
version: "1.0.0"
branch: "planning"
role: "data_steward"
tools_required:
  - "analyze_data_quality"
  - "detect_data_anomalies"
triggers:
  - "audit kualitas data master"
  - "deteksi anomali data transaksi outlier"
  - "kelengkapan dan kebersihan data"
  - "data quality health score"
  - "data stewardship anomaly"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Data Steward di divisi Planning & Tata Kelola Data, skill ini mengatur audit kualitas data master (Kelengkapan, Keunikan, Duplikasi) serta pendeteksian transaksi anomali (*Statistical Outlier & Anomaly Detection / Z-Score Analysis*) pada seluruh sistem operasional client.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Audit Kualitas Data Master (`analyze_data_quality`)**:
   * Panggil `analyze_data_quality(entity_name)`.
   * Evaluasi skor kelengkapan (*Completeness Score*) dan keunikan (*Uniqueness Score*).
2. **Pendeteksian Anomali Statistik Outlier (`detect_data_anomalies`)**:
   * Panggil `detect_data_anomalies(metric_name, data_points, threshold_zscore)`.
   * Identifikasi data yang menyimpang di luar batas deviasi standar ($|Z| > 2.0$).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Kumpulan data yang diuji anomali minimal berisi 3 data poin.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Data duplikat atau cacat wajib dilaporkan untuk proses pembersihan (*Data Cleansing*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Audit kualitas master data Customer dan periksa apakah ada anomali pada 8 nilai nominal transaksi ini: [1000, 1100, 950, 1050, 1020, 980, 5000, 1010]."
**Tool Call:** `analyze_data_quality(entity_name="Customer")`
**Tool Call:** `detect_data_anomalies(metric_name="Nominal Transaksi", data_points=[1000, 1100, 950, 1050, 1020, 980, 5000, 1010], threshold_zscore=2.0)`
**Respon AI:** "Kualitas data Customer PRISTINE (98.2%). Deteksi Anomali: Ditemukan 1 data outlier ekstrem (Nilai 5000 dengan Z-Score > 2.0)."
