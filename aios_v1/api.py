import frappe
import requests
import json
import re

def safe_parse_json(raw_text):
    """
    Parser JSON tahan-banting: membersihkan trailer SSE seperti 'data: [DONE]'
    atau teks tambahan yang ditempelkan gateway AI.
    """
    text = raw_text.strip()
    if "data: [DONE]" in text:
        text = text.split("data: [DONE]")[0].strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Cari kurung kurawal pertama dan terakhir untuk mengambil objek JSON valid
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            clean_json = text[start:end+1]
            return json.loads(clean_json)
        raise

@frappe.whitelist()
def ask_intelligence(message, context=None):
    """
    Endpoint utama Department Intelligence AIOS.
    """
    if not message:
        frappe.throw("Pesan tidak boleh kosong.")

    # 1. Ambil konfigurasi dari DocType AIOS Setting
    settings = frappe.get_single("AIOS Setting")
    
    api_key = settings.get_password("api_key")
    if not api_key:
        frappe.throw("API Key belum diatur di AIOS Setting! Silakan isi terlebih dahulu di Desk.")

    base_url = settings.base_url or "https://api.openai.com/v1"
    model_name = settings.model_name or "deepseek-chat"
    temperature = settings.temperature or 0.2
    system_ethos = settings.system_ethos or (
        "Kamu adalah Department Intelligence AI untuk sistem ERP perusahaan.\n"
        "1. Anti-halusinasi: Jangan mengarang data jika tidak tersedia.\n"
        "2. Sebutkan sumber data dengan objektif.\n"
        "3. Gunakan Bahasa Indonesia yang profesional dan jelas.\n"
        "4. Berikan rekomendasi keputusan bisnis yang konkret."
    )

    # 2. Susun Payload Chat
    endpoint = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"{system_ethos}\n\n"
        f"Konteks Tambahan Perusahaan:\n{context if context else 'Belum ada konteks data terlampir.'}"
    )

    payload = {
        "model": model_name,
        "temperature": float(temperature),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    }

    # 3. Panggil LLM API
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        # Gunakan parser tahan-banting
        data = safe_parse_json(response.text)
        
        reply = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        return {
            "success": True,
            "reply": reply,
            "usage": usage,
            "model": model_name
        }

    except Exception as e:
        frappe.log_error(title="AIOS Intelligence Call Error", message=str(e))
        return {
            "success": False,
            "error": f"Gagal menghubungi AI Engine: {str(e)}"
        }
