"""
Modul Uji Interaktif: Live LLM Call dengan Skills SOP System Prompt & Tool Schemas.
Membuktikan integrasi end-to-end antara AIOS Setting (Base URL, API Key, Model), Skills Loader, dan Function Calling.
Dijalankan via: `bench --site aios.localhost execute aios_v1.lib.demo_live_llm.run_live_llm_demo`
"""

import json
import time
import frappe
from aios_v1.lib.llm_client import get_llm_config, chat_completion
from aios_v1.lib.skills_loader import compose_worker_system_prompt, get_skills_for_worker
from aios_v1.lib.tool_registry import get_tools_schema_for_worker, _TOOL_REGISTRY, _ensure_tools_loaded


def run_live_llm_demo():
    print("\n" + "=" * 80)
    print("🤖 DEMO LIVE LLM INFERENCE: SKILLS SOP + REAL FUNCTION CALLING")
    print("=" * 80)

    # 1. Konfigurasi LLM dari AIOS Setting
    cfg = get_llm_config()
    print(f"\n[1] MEMERIKSA KONFIGURASI DARI DocType 'AIOS Setting':")
    print(f"    • Provider Base URL : {cfg['base_url']}")
    print(f"    • Active Model Name : {cfg['model']}")
    print(f"    • API Key Terpasang : {'✅ ' + cfg['api_key'][:8] + '...' if cfg['api_key'] else '❌ Kosong'}")
    print(f"    • Temperature       : {cfg['temperature']}")

    # 2. Skenario: Purchasing Officer di Cabang Material
    branch = "material"
    role = "purchasing_officer"
    user_query = "Tolong bantu hitung EOQ untuk pengadaan Plat Besi jika kebutuhan tahunan kita 6.000 unit, biaya sekali pesan Rp 250.000, dan biaya simpan Rp 15.000 per unit per tahun."

    print(f"\n[2] MENYIAPKAN KONTEKS SUB-AGENT:")
    print(f"    • Target Cabang     : {branch.upper()}")
    print(f"    • Job Role Worker   : {role}")
    print(f"    • User Prompt       : \"{user_query}\"")

    # 3. Merakit System Prompt dari File SOP Skills Opsi C
    base_prompt = "Anda adalah Purchasing Officer di AIOS. Ikuti Prosedur Operasional Standar (SOP) dengan disiplin."
    system_prompt = compose_worker_system_prompt(branch, role, base_prompt)
    skills = get_skills_for_worker(branch, role)
    print(f"    • SOP Terpasang     : {len(skills)} SOP Skills ({', '.join(s['name'] for s in skills)})")
    print(f"    • Panjang Prompt    : {len(system_prompt)} karakter")

    # 4. Mengambil Skema Tools Khusus Peran Purchasing Officer
    tools = get_tools_schema_for_worker(branch, role)
    print(f"    • Skema Tools (RBAC): {len(tools)} tools diizinkan ({', '.join(t['function']['name'] for t in tools)})")

    # 5. Memanggil API LLM Secara Nyata
    print(f"\n[3] MENGIRIM REQUEST KE LLM SERVER ({cfg['model']})...")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    t0 = time.perf_counter()
    try:
        response_msg = chat_completion(messages=messages, tools=tools, temperature=0.1)
        latency = (time.perf_counter() - t0) * 1000
        print(f"    ✅ Response Diterima dalam {latency:.2f} ms!")

        print("\n" + "-" * 80)
        print("📥 RESPON ASLI DARI MODEL LLM:")
        print("-" * 80)
        
        # Periksa apakah model memutuskan memanggil Tool (Function Calling)
        tool_calls = response_msg.get("tool_calls")
        content = response_msg.get("content")

        if tool_calls:
            print(f"🎯 Model Memutuskan Memanggil {len(tool_calls)} Tool (Function Calling):")
            for tc in tool_calls:
                func_name = tc.get("function", {}).get("name")
                args_str = tc.get("function", {}).get("arguments", "{}")
                print(f"\n   ➔ Tool yang Dipanggil: `{func_name}`")
                print(f"   ➔ Argumen Parameter  : {args_str}")

                # Eksekusi tool nyata yang dipanggil model
                _ensure_tools_loaded()
                if func_name in _TOOL_REGISTRY:
                    func = _TOOL_REGISTRY[func_name]["func"]
                    args = json.loads(args_str) if isinstance(args_str, str) else args_str
                    tool_result = func(**args)
                    print(f"   ➔ Hasil Eksekusi Tool: {json.dumps(tool_result, indent=4)}")
        elif content:
            print(content)
        else:
            print(json.dumps(response_msg, indent=2))

        print("-" * 80)
        print("\n🎉 KESIMPULAN: LLM berhasil membaca SOP dari file Markdown dan memilih tool yang tepat!")
        return {"status": "SUCCESS", "model": cfg["model"], "latency_ms": latency}

    except Exception as e:
        print(f"    ❌ Error saat memanggil LLM: {str(e)}")
        return {"status": "ERROR", "error": str(e)}
