import json
import frappe
from datetime import datetime
from typing import Optional, List, Dict, Any

_TOOL_REGISTRY: Dict[str, Any] = {}

def ai_tool(name: str, description: str, parameters: Optional[Dict[str, Any]] = None, branch: Optional[str] = None, roles: Optional[List[str]] = None):
    """
    Decorator to register a python function as an AI Tool.
    `branch`: Nama divisi ERP (misal: 'hr', 'finance', 'sales')
    `roles`: List job role yang diizinkan mengakses tool ini (misal: ['recruiter', 'hr_manager'])
    """
    def decorator(func):
        _TOOL_REGISTRY[name] = {
            "name": name,
            "description": description,
            "parameters": parameters or {},
            "branch": branch.lower() if branch else None,
            "roles": [r.lower() for r in roles] if roles else [],
            "func": func
        }
        return func
    return decorator

def _ensure_tools_loaded():
    """Memastikan seluruh tool modules (AI Manager + 9 cabang ERP) telah di-import & terdaftar."""
    import aios_v1.lib.ai_manager_tools
    import aios_v1.lib.tools

def get_all_tools_schema():
    """Returns list of all tools formatted for LLM API (OpenAI spec)."""
    _ensure_tools_loaded()
    schemas = []
    for t_name, t_data in _TOOL_REGISTRY.items():
        schemas.append({
            "type": "function",
            "function": {
                "name": t_data["name"],
                "description": t_data["description"],
                "parameters": {
                    "type": "object",
                    "properties": t_data["parameters"],
                    "required": list(t_data["parameters"].keys())
                }
            }
        })
    return schemas

def get_tools_schema_for_worker(branch: str, worker_key: str = "manager"):
    """
    Mengembalikan skema tools khusus yang diizinkan untuk worker/role tertentu (Prinsip Least Privilege).
    """
    _ensure_tools_loaded()
    schemas = []
    branch_lower = branch.lower() if branch else ""
    worker_lower = worker_key.lower() if worker_key else "manager"
    
    for t_name, t_data in _TOOL_REGISTRY.items():
        t_branch = t_data.get("branch")
        t_roles = t_data.get("roles", [])
        
        # 1. Global tools (tanpa branch spesifik) selalu diizinkan
        if not t_branch:
            is_allowed = True
        # 2. AI Manager Orchestrator tools diizinkan untuk semua AI Manager cabang
        elif t_branch in ["ai_manager", "orchestrator"] and (worker_lower in ["manager", "ai_manager", f"{branch_lower}_manager"] or branch_lower in ["orchestrator", "ai_manager"]):
            is_allowed = True
        # 3. Jika worker adalah AI Manager cabang -> dapat akses seluruh tools cabang tsb
        elif worker_lower in ["manager", "ai_manager", f"{branch_lower}_manager"] and t_branch == branch_lower:
            is_allowed = True
        # 4. Jika sub-agent spesifik -> cek apakah worker_key ada di t_roles
        elif t_branch == branch_lower and (not t_roles or worker_lower in t_roles or any(r in t_roles for r in [worker_lower, worker_lower.replace('_', '-'), worker_lower.replace('-', '_')])):
            is_allowed = True
        else:
            is_allowed = False
            
        if is_allowed:
            schemas.append({
                "type": "function",
                "function": {
                    "name": t_data["name"],
                    "description": t_data["description"],
                    "parameters": {
                        "type": "object",
                        "properties": t_data["parameters"],
                        "required": list(t_data["parameters"].keys())
                    }
                }
            })
    return schemas

def execute_tool(name: str, arguments_json: str):
    """Executes a registered tool."""
    _ensure_tools_loaded()
    if name not in _TOOL_REGISTRY:
        return json.dumps({"error": f"Tool {name} not found"})
    
    try:
        kwargs = json.loads(arguments_json)
        func = _TOOL_REGISTRY[name]["func"]
        result = func(**kwargs)
        return json.dumps(result)
    except Exception as e:
        frappe.log_error(message=str(e), title=f"AIOS Tool Error: {name}")
        return json.dumps({"error": str(e)})

# ==========================================
# 1. DUMMY TOOL (For Testing - Tahap 1)
# ==========================================

@ai_tool(
    name="get_current_time",
    description="Mendapatkan tanggal dan waktu saat ini di zona waktu tertentu.",
    parameters={
        "timezone": {
            "type": "string",
            "description": "Timezone string, contoh: 'Asia/Jakarta' atau 'UTC'"
        }
    }
)
def get_current_time(timezone="Asia/Jakarta"):
    import pytz
    try:
        tz = pytz.timezone(timezone)
        return {"current_time": datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"), "timezone": timezone}
    except Exception as e:
        return {"error": f"Invalid timezone: {timezone}"}
