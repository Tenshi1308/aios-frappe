import json
import os
import time
import requests
import frappe

def get_llm_config():
    try:
        setting = frappe.get_single("AIOS Setting")
        base_url = setting.base_url or "https://9router.nadif.dev/v1"
        api_key = setting.get_password("api_key") or ""
        model = setting.model_name or "wdb/deepseek-ai/DeepSeek-V4-Flash-0731"
        temperature = float(setting.temperature) if setting.temperature is not None else 0.3
        return {
            "base_url": base_url.rstrip("/"),
            "api_key": api_key,
            "model": model,
            "temperature": temperature,
            "timeout": 90.0
        }
    except Exception:
        return {
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
            "model": "llama3",
            "temperature": 0.3,
            "timeout": 90.0
        }

def chat_stream(messages, max_tokens=4096, temperature=None):
    cfg = get_llm_config()
    url = f"{cfg['base_url']}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg['api_key']}"
    }
    payload = {
        "model": cfg["model"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature if temperature is not None else cfg["temperature"],
        "stream": True
    }

    max_attempts = 2
    last_err = None

    for attempt in range(1, max_attempts + 1):
        try:
            res = requests.post(url, headers=headers, json=payload, stream=True, timeout=cfg["timeout"])
            if not res.ok:
                raise Exception(f"HTTP {res.status_code}: {res.text[:200]}")

            res.encoding = "utf-8"

            for line in res.iter_lines(decode_unicode=True):
                if not line:
                    continue
                line = line.strip()
                if not line.startswith("data:"):
                    continue
                data_str = line[5:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if delta:
                        yield delta
                except Exception:
                    continue

            return

        except Exception as e:
            last_err = e
            if attempt < max_attempts:
                time.sleep(1)
                continue

    yield f"Mohon maaf, server AI memerlukan waktu lebih lama dari biasanya ({str(last_err)}). Silakan coba ajukan pertanyaan kembali."

def clean_messages_for_llm(messages):
    cleaned = []
    for m in messages:
        role = m.get("role")
        if role == "assistant":
            msg_dict = {"role": "assistant"}
            if m.get("content"):
                msg_dict["content"] = m["content"]
            if m.get("tool_calls"):
                msg_dict["tool_calls"] = []
                for tc in m["tool_calls"]:
                    clean_tc = {
                        "id": tc.get("id", f"call_{len(msg_dict['tool_calls'])+1}"),
                        "type": "function",
                        "function": {
                            "name": tc.get("function", {}).get("name"),
                            "arguments": tc.get("function", {}).get("arguments", "{}")
                        }
                    }
                    msg_dict["tool_calls"].append(clean_tc)
            if not msg_dict.get("content") and not msg_dict.get("tool_calls"):
                msg_dict["content"] = ""
            cleaned.append(msg_dict)
        elif role == "tool":
            cleaned.append({
                "role": "tool",
                "tool_call_id": m.get("tool_call_id", "call_1"),
                "content": str(m.get("content", ""))
            })
        else:
            cleaned.append({
                "role": role,
                "content": str(m.get("content", ""))
            })
    return cleaned

def chat_completion(messages, tools=None, max_tokens=4096, temperature=None):
    cfg = get_llm_config()
    url = f"{cfg['base_url']}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg['api_key']}"
    }
    payload = {
        "model": cfg["model"],
        "messages": clean_messages_for_llm(messages),
        "max_tokens": max_tokens,
        "temperature": temperature if temperature is not None else cfg["temperature"],
        "stream": False
    }
    
    if tools:
        payload["tools"] = tools

    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=cfg["timeout"])
            if not res.ok:
                raise Exception(f"HTTP {res.status_code}: {res.text[:200]}")
            
            data = res.json()
            message = data.get("choices", [{}])[0].get("message", {})
            if not message.get("content"):
                reasoning_text = message.get("reasoning_content") or message.get("reasoning")
                if reasoning_text and not message.get("tool_calls"):
                    message["content"] = reasoning_text
            return message
        except Exception as e:
            if attempt < max_attempts:
                time.sleep(1)
                continue
            raise Exception(f"LLM API Error: {str(e)}")
