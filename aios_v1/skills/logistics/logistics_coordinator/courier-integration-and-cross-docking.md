---
name: "Courier Integration and Cross-Docking Workflow"
slug: "courier-integration-and-cross-docking"
version: "1.0.0"
branch: "logistics"
role: "logistics_coordinator"
tools_required:
  - "manage_courier_integrations"
  - "create_draft_cross_docking"
triggers:
  - "integrasi kurir pihak ketiga 3pl"
  - "rekomendasi tarif kurir kargo ekspedisi"
  - "operasi cross docking transit cepat"
  - "pindah muat langsung dermaga staging"
  - "3pl freight selection"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Logistics Coordinator, skill ini mengatur perbandingan tarif serta pemilihan kurir ekspedisi pihak ketiga (*3PL Courier Integration*), serta penyusunan draf instruksi kerja *Cross-Docking* (pemindahan langsung barang dari truk masuk ke truk keluar di dermaga staging tanpa penyimpanan rak gudang) untuk mempercepat perputaran barang.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemeriksaan Tarif Opsi 3PL (`manage_courier_integrations`)**:
   * Panggil `manage_courier_integrations(origin_postal, dest_postal, weight_kg)`.
   * Pilih kurir dengan biaya dan estimasi waktu terbaik (`recommended_courier`).
2. **Penerbitan Draf Operasi Cross-Docking (`create_draft_cross_docking`)**:
   * Panggil `create_draft_cross_docking(inbound_delivery_id, outbound_delivery_id, transfer_items, staging_bay)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Kode pos asal dan tujuan harus valid.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Operasi Cross-Docking wajib diselesaikan dalam waktu maksimal $1 \times 4$ jam di area staging.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Cari opsi kurir kargo terbaik dari kode pos 17530 ke 40115 untuk muatan 150 kg dan siapkan draf cross docking di Bay-02."
**Tool Call:** `manage_courier_integrations(origin_postal="17530", dest_postal="40115", weight_kg=150)`
**Tool Call:** `create_draft_cross_docking(inbound_delivery_id="INB-100", outbound_delivery_id="OUT-200", transfer_items=[{"item": "Sparepart", "qty": 150}], staging_bay="Bay-02")`
**Respon AI:** "Rekomendasi 3PL: J&T Cargo (Rp 6.000.000). Draf Operasi Cross-Docking di Bay-02 siap di-approve: [Review Draf](/draft/DRF-XDOCK-001)."
