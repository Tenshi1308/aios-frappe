---
name: "Inspection Lot and Sampling Workflow"
slug: "inspection-lot-and-sampling"
version: "1.0.0"
branch: "quality"
role: "quality_inspector"
tools_required:
  - "create_inspection_lot"
  - "calculate_sampling_size_aql"
triggers:
  - "buat lot inspeksi mutu"
  - "sampling aql iso 2859"
  - "uji sampel penerimaan barang"
  - "rencana sampling qc"
  - "inspection lot creation"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Quality Inspector di divisi Quality Management, skill ini mengatur pembuatan draf Lot Inspeksi pengujian mutu barang masuk (*Incoming Goods QC*) atau barang jadi pabrik (*Final Inspection*), penentuan jumlah sampel uji representatif, dan batas toleransi penerimaan/penolakan berdasarkan standar statistik *Acceptance Quality Limit* (AQL ISO 2859-1).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Lot Inspeksi (`create_inspection_lot`)**:
   * Panggil `create_inspection_lot(material_or_product_id, lot_size, inspection_type)`.
   * Terbitkan Action Draft Card untuk otorisasi supervisor QC.
2. **Kalkulasi Rencana Sampling Statistik (`calculate_sampling_size_aql`)**:
   * Panggil `calculate_sampling_size_aql(lot_size, inspection_level, aql_value)`.
   * Dapatkan ukuran sampel yang wajib diambil (`recommended_sample_size`) dan batas toleransi maksimal cacat (`accept_max_defects` vs `reject_if_defects_equal_or_greater`).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Kuantitas lot barang harus bernilai bilangan bulat positif > 0.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** meloloskan batch pengiriman jika jumlah temuan cacat melebihi batas batas ambang reject AQL.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung jumlah sampel sampling AQL 1.5% level II untuk kedatangan 1.500 unit Plat Besi dan buatkan draf lot inspeksinya."
**Tool Call:** `calculate_sampling_size_aql(lot_size=1500, inspection_level="II", aql_value=1.5)`
**Tool Call:** `create_inspection_lot(material_or_product_id="Plat Besi 3mm", lot_size=1500, inspection_type="Incoming Goods")`
**Respon AI:** "Sampling AQL 1.5%: Ambil 80 sampel (Terima jika cacat $\le 1$, Tolak jika $\ge 2$). Draf Lot Inspeksi berhasil dibuat: [Review Draf](/draft/DRF-LOT-001)."
