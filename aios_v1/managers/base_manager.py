import json
import frappe
from aios_v1.shared.aios_ethos import AIOS_ETHOS
from aios_v1.shared.base_persona import BASE_PERSONA
from aios_v1.lib.llm_client import chat_stream
from aios_v1.plugin_manager.registry import get_branches, get_worker

class BaseManager:
    def __init__(self, branch_def):
        self.branch = branch_def

    def manager_persona(self) -> str:
        return self.branch.get("manager_persona") or f"Anda adalah AI Manager bidang {self.branch['name']} di AIOS — manajer yang mengoordinasikan seluruh spesialis/worker di bidang ini."

    def ensure_conversation(self, company_id: int) -> int:
        tenant_name = str(company_id)
        existing = frappe.get_all(
            "AIOS Conversation",
            filters={"tenant": tenant_name, "branch": self.branch["key"]},
            order_by="modified desc",
            limit=1
        )
        if existing:
            return int(existing[0].name)

        doc = frappe.new_doc("AIOS Conversation")
        doc.tenant = tenant_name
        doc.branch = self.branch["key"]
        doc.title = f"Sesi {self.branch['name']}"
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return int(doc.name)

    def get_worker_def(self, worker_key: str):
        if not worker_key or worker_key == "manager":
            return None
        return get_worker(self.branch["key"], worker_key)

    def build_system_prompt(self, worker_def) -> str:
        parts = [AIOS_ETHOS, self.manager_persona()]

        if worker_def:
            has_skill_depth = (
                worker_def.get("personality") or
                worker_def.get("priorities") or
                worker_def.get("answerStructure") or
                worker_def.get("antiPatterns")
            )
            if has_skill_depth:
                skill_lines = ["[SKILL DEPTH & GAYA ANALISIS]"]
                if worker_def.get("personality"):
                    skill_lines.append(f"- Kepribadian: {worker_def['personality']}")
                if worker_def.get("priorities"):
                    skill_lines.append("- Prioritas utama saat menganalisis:")
                    for i, p in enumerate(worker_def["priorities"], 1):
                        skill_lines.append(f"  {i}. {p}")
                if worker_def.get("answerStructure"):
                    skill_lines.append(f"- Struktur jawaban: {' -> '.join(worker_def['answerStructure'])}.")
                if worker_def.get("antiPatterns"):
                    skill_lines.append("- JANGAN (Batasan Tegas):")
                    for ap in worker_def["antiPatterns"]:
                        skill_lines.append(f"  - {ap}")
                parts.append("\n".join(skill_lines))
            else:
                parts.append(BASE_PERSONA)

            parts.append(
                f"Saat ini Anda SEDANG BERPERAN SEBAGAI SUB-AGENT SPESIALIS: {worker_def['jobRole']}.\n"
                f"Fokus tugas: {worker_def['description']}\n"
                f"Batas data yang relevan dengan peran Anda: {', '.join(worker_def.get('relevantEntities', []))}."
            )
        else:
            parts.append(BASE_PERSONA)
            parts.append(f"""Saat ini Anda SEDANG BERPERAN SEBAGAI: AI MANAGER (UMUM) bidang {self.branch['name']}.
Fokus tugas: Mengoordinasikan seluruh operasional dan spesialis/worker di bidang {self.branch['name']}.
PENTING: Jangan meniru atau melanjutkan peran sub-agent spesialis tertentu dari percakapan sebelumnya. Jawablah murni dari perspektif AI Manager umum yang bertugas memimpin cabang ini.""")

        parts.append("""
ATURAN JAWABAN (WAJIB):
1. Jawab dalam bahasa Indonesia, ramah, ringkas, terstruktur dan profesional.
2. Anda adalah bagian dari AIOS (platform AI enterprise), bukan asisten publik umum.
3. Bantu pengguna menganalisis data, memberikan rekomendasi operasional, dan menjawab pertanyaan terkait bidang Anda.""")

        base_prompt = "\n\n".join(parts)

        # Integrasi Fase 6M.13: Perkayaan Dinamis Prompt dengan SOP Skills Terdaftar
        try:
            from aios_v1.lib.skills_loader import compose_worker_system_prompt
            branch_key = self.branch.get("key", "").lower()
            worker_key = worker_def.get("key", "manager") if worker_def else "manager"
            enriched_prompt = compose_worker_system_prompt(
                branch=branch_key,
                worker_key=worker_key,
                base_prompt=base_prompt
            )
            return enriched_prompt
        except Exception as e:
            frappe.log_error(f"Error injecting skills SOP in BaseManager: {e}", "AIOS Skills Loader")
            return base_prompt

    def handle_stream(self, company_id: int, user_message: str, worker_key: str = None, conversation_id: int = None):
        if not conversation_id:
            conversation_id = self.ensure_conversation(company_id)

        # 1. Kirim Meta Event
        yield f"data: {json.dumps({'type': 'meta', 'conversationId': conversation_id})}\n\n"

        # 2. Simpan Pesan User ke DocType AIOS Message
        user_msg_doc = frappe.new_doc("AIOS Message")
        user_msg_doc.conversation = str(conversation_id)
        user_msg_doc.role = "user"
        user_msg_doc.worker_key = worker_key or "manager"
        user_msg_doc.content = user_message
        user_msg_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        # 3. Ambil Riwayat Percakapan
        recent_messages = frappe.get_all(
            "AIOS Message",
            filters={"conversation": str(conversation_id)},
            fields=["role", "worker_key", "content"],
            order_by="creation desc",
            limit=6
        )
        recent_messages.reverse()

        worker_def = self.get_worker_def(worker_key)
        system_prompt = self.build_system_prompt(worker_def)

        llm_messages = [{"role": "system", "content": system_prompt}]
        for m in recent_messages[:-1]:
            content = m.content
            # Jika sedang di mode Manager, tandai riwayat sub-agent lama agar model tidak terdistraksi
            if worker_def is None and m.worker_key and m.worker_key != "manager":
                content = f"[{m.worker_key}]: {m.content}"
            llm_messages.append({"role": "user" if m.role == "user" else "assistant", "content": content})

        # Suntikkan direktif peran aktif dan data aktual database client
        if worker_def is None:
            llm_messages.append({
                "role": "system",
                "content": f"[DIREKTIF PERAN AKTIF]: Anda adalah AI MANAGER {self.branch['name'].upper()} (UMUM). Anda BUKAN Budgeting Staff atau sub-agent lainnya. Jawablah tegas sebagai AI Manager umum yang mengoordinasikan seluruh sub-agent."
            })
        else:
            llm_messages.append({
                "role": "system",
                "content": f"[DIREKTIF PERAN AKTIF]: Anda saat ini sedang berbicara sebagai Sub-Agent Spesialis: {worker_def['jobRole']}. Terapkan keahlian mendalam peran {worker_def['jobRole']}."
            })

        # Ambil data faktual dari database client via Safe Query Engine
        data_used = []
        try:
            from aios_v1.data_access.query_engine import get_relevant_business_data
            data_context, data_used = get_relevant_business_data(company_id, user_message, self.branch["key"], worker_def)
            if data_context:
                llm_messages.append({"role": "system", "content": data_context})
        except Exception as e:
            frappe.log_error(f"Error fetching business data in manager: {e}", "AIOS Data Query")

        llm_messages.append({"role": "user", "content": user_message})

        # 4. Stream Jawaban dari LLM
        full_reply = ""
        delegated_to = worker_def["jobRole"] if worker_def else "Manager"

        for delta in chat_stream(llm_messages):
            full_reply += delta
            yield f"data: {json.dumps({'type': 'delta', 'text': delta})}\n\n"

        # 5. Simpan Pesan Assistant ke DocType AIOS Message
        asst_msg_doc = frappe.new_doc("AIOS Message")
        asst_msg_doc.conversation = str(conversation_id)
        asst_msg_doc.role = "manager" if not worker_def else "worker"
        asst_msg_doc.worker_key = worker_key or "manager"
        asst_msg_doc.content = full_reply
        asst_msg_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        # 6. Kirim Done Event
        yield f"data: {json.dumps({'type': 'done', 'conversationId': conversation_id, 'delegatedTo': delegated_to, 'dataUsed': data_used, 'limitation': '', 'tokens': len(full_reply.split())})}\n\n"
