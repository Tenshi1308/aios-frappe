---
name: "Task Orchestration and Delegation Workflow"
slug: "task-orchestration-and-delegation"
version: "1.0.0"
branch: "orchestrator"
role: "ai_manager"
tools_required:
  - "orchestrator_delegate_to_subagent"
  - "broadcast_policy_update"
  - "summarize_branch_status"
triggers:
  - "delegasikan tugas"
  - "bagi tugas subagent"
  - "broadcast kebijakan"
  - "ringkasan status cabang"
  - "status operasional divisi"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai AI Manager (Pimpinan Orkestrasi Divisi), skill ini mengatur alur dekomposisi tugas hierarkis, pendelegasian instruksi ke sub-agent spesialis yang tepat, pemantauan kesehatan operasional cabang, dan penyebaran kebijakan baru (*Policy Broadcast*) ke seluruh sub-agent di bawah koordinasinya.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Permintaan Pengguna & Dekomposisi Tugas**:
   * Evaluasi maksud pengguna dan tentukan apakah tugas membutuhkan peran spesialis.
2. **Pendelegasian Tugas ke Sub-Agent (`orchestrator_delegate_to_subagent`)**:
   * Pilih `worker_key` yang memiliki domain keahlian yang sesuai.
   * Susun parameter `task_instruction` dan sertakan payload data konteks.
   * Panggil tool `orchestrator_delegate_to_subagent(branch, worker_key, task_instruction, context_data)`.
3. **Penyebaran Kebijakan Operasional (`broadcast_policy_update`)**:
   * Jika ada perubahan aturan bisnis mendesak, panggil `broadcast_policy_update(branch, policy_topic, policy_payload)`.
4. **Ringkasan Status Operasional Cabang (`summarize_branch_status`)**:
   * Jika user meminta laporan divisi, panggil `summarize_branch_status(branch, period)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter `branch` dan `worker_key` harus terdaftar di sistem.
* Instruksi pendelegasian harus spesifik, jelas, dan memuat tujuan hasil akhir.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** mendelegasikan tugas di luar wewenang fungsional sub-agent.
* Jika sub-agent gagal menyelesaikan tugas, Manajer wajib melakukan investigasi dan eskalasi.

# 5. Contoh Interaksi (Few-Shot Examples)

### Contoh: Pendelegasian Analisis Rasio ke Financial Analyst
**User:** "Tolong hitung rasio likuiditas dan solvabilitas kuartal ini."
**Tool Call:** `orchestrator_delegate_to_subagent(branch="finance", worker_key="financial_analyst", task_instruction="Hitung Current Ratio dan Quick Ratio Q2 2026", context_data={"period": "2026-Q2"})`
**Respon AI:** "Tugas telah didelegasikan ke Financial Analyst. Hasil analisis akan segera dirangkum."
