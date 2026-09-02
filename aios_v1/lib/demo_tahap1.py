import json
import frappe
from aios_v1.lib.llm_client import chat_completion
from aios_v1.lib.tool_registry import get_all_tools_schema, execute_tool

@frappe.whitelist(allow_guest=False)
def run_demo(prompt="Jam berapa sekarang di Tokyo?"):
    """
    Script interaktif untuk mengetes Function Calling Tahap 1.
    Cara jalankan via terminal:
    bench execute aios_v1.lib.demo_tahap1.run_demo --args '{"prompt": "Jam berapa sekarang di London?"}'
    """
    print(f"\n[1] USER PROMPT: '{prompt}'")
    
    messages = [{"role": "user", "content": prompt}]
    tools = get_all_tools_schema()
    
    print(f"[2] MENGIRIM KE LLM DENGAN {len(tools)} TOOLS TERDAFTAR...")
    try:
        response = chat_completion(messages, tools=tools)
    except Exception as e:
        print(f"FULL ERROR: {str(e)}")
        return f"LLM API Error: {str(e)}"
    
    print("\n[3] BALASAN DARI LLM:")
    # Cek apakah LLM memutuskan untuk menggunakan tool
    if response.get("tool_calls"):
        tool_call = response["tool_calls"][0]
        func_name = tool_call["function"]["name"]
        func_args = tool_call["function"]["arguments"]
        
        print(f" -> 🤖 LLM memutuskan untuk memakai tool: '{func_name}'")
        print(f" -> 📦 Argumen yang diberikan LLM: {func_args}")
        
        # Eksekusi tool
        print("\n[4] MENGEKSEKUSI TOOL...")
        result = execute_tool(func_name, func_args)
        print(f" -> ✅ Hasil dari sistem kita: {result}")
        
        # Pastikan format message bersih (tanpa field reasoning/extra dari DeepSeek)
        assistant_msg = {
            "role": "assistant",
            "content": response.get("content") or "",
            "tool_calls": response.get("tool_calls")
        }
        
        messages.append(assistant_msg) # Masukkan assistant message
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "name": func_name,
            "content": result
        })
        
        print("\n[5] MENGIRIM KEMBALI HASIL TOOL KE LLM...")
        final_response = chat_completion(messages)
        print(f" -> 🤖 Kesimpulan LLM: {final_response.get('content')}")
        
        return {
            "status": "success",
            "tool_used": func_name,
            "final_answer": final_response.get("content")
        }
    else:
        print(f" -> 🤖 LLM menjawab langsung: {response.get('content')}")
        return {
            "status": "success",
            "tool_used": "none",
            "final_answer": response.get("content")
        }
