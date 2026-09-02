---
name: "RFQ and Vendor Quote Comparison Workflow"
slug: "rfq-and-vendor-quote-comparison"
version: "1.0.0"
branch: "material"
role: "sourcing_specialist"
tools_required:
  - "create_draft_rfq"
  - "compare_vendor_quotations"
triggers:
  - "buat rfq penawaran vendor"
  - "request for quotation"
  - "bandingkan penawaran vendor"
  - "komparasi harga supplier"
  - "evaluasi tender pengadaan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Sourcing Specialist, skill ini mengatur perancangan draf permintaan penawaran harga (*Request for Quotation / RFQ*) ke beberapa kandidat pemasok serta pembuatan matriks perbandingan harga, spesifikasi, dan *lead time* antar penawaran yang masuk.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pembuatan Draf Dokumen RFQ (`create_draft_rfq`)**:
   * Panggil `create_draft_rfq(items, candidate_vendors, submission_deadline)`.
   * Terbitkan Action Draft Card untuk disetujui manajer sourcing.
2. **Komparasi Penawaran Masuk (`compare_vendor_quotations`)**:
   * Setelah batas waktu pengumpulan penawaran selesai, panggil `compare_vendor_quotations(rfq_id, vendor_quotes)`.
   * Rekomendasikan vendor pemenang (*Best Bid Recommendation*).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Minimal melibatkan 2 kandidat vendor untuk asas persaingan sehat.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh proses perbandingan penawaran wajib transparan dan mematuhi etika pengadaan independen.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan draf RFQ untuk pengadaan 1000 unit Bearing SKF ke 3 vendor kandidat dengan batas pengumpulan 10 September 2026."
**Tool Call:** `create_draft_rfq(items=[{"item": "Bearing SKF 6204", "qty": 1000}], candidate_vendors=["PT Sumber Teknik", "CV Prima Mandiri", "PT Global Bearing"], submission_deadline="2026-09-10")`
**Respon AI:** "Draf RFQ untuk 3 vendor berhasil dibuat: [Review Draf RFQ](/draft/DRF-RFQ-001)."
