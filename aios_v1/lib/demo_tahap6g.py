"""
Demo CLI untuk Sub-tahap 6G: Katalog Tools Cabang Quality Management (17 Tools) & Role-Scoping.
Memperagakan isolasi Inspector vs Control Officer vs Engineer, kalkulasi SPC Cpk, AQL Sampling, dan Draf Lot Inspeksi.
"""

import json
from aios_v1.lib.tool_registry import execute_tool, get_tools_schema_for_worker
import aios_v1.lib.tools.quality_tools

def run_demo():
    print("\n" + "="*72)
    print("🚀 DEMO SUB-TAHAP 6G: TOOLS QUALITY MANAGEMENT (17 TOOLS)")
    print("="*72)

    # 1. Peragaan Role-Scoping
    print("\n[1] PERAGAAN ROLE-SCOPING (ISOLASI HAK AKSES TOOLS):")
    inspector_tools = get_tools_schema_for_worker(branch="quality", worker_key="quality_inspector")
    officer_tools = get_tools_schema_for_worker(branch="quality", worker_key="quality_control_officer")
    engineer_tools = get_tools_schema_for_worker(branch="quality", worker_key="quality_engineer")
    
    print(f" • Quality Inspector       : Memiliki {len(inspector_tools)} tools (Hanya Sampling AQL/Uji Lab/Kalibrasi)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in inspector_tools[:2]]}")
    print(f" • Quality Control Officer : Memiliki {len(officer_tools)} tools (Hanya Otorisasi Lot/CoA/NCR/Quality Alert)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in officer_tools[:2]]}")
    print(f" • Quality Engineer        : Memiliki {len(engineer_tools)} tools (Hanya SPC/FPY/CAPA/Inspection Plan)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in engineer_tools[:2]]}")

    # 2. Peragaan Tool Inspector: calculate_sampling_size_aql
    print("\n[2] EKSEKUSI TOOL INSPECTOR: calculate_sampling_size_aql")
    args_aql = {"lot_size": 2500, "inspection_level": "II", "aql_value": 1.5}
    res_aql = json.loads(execute_tool("calculate_sampling_size_aql", json.dumps(args_aql)))
    print(f" -> Ukuran Lot    : {res_aql['lot_size']} unit")
    print(f" -> Target AQL    : {res_aql['aql_target']}%")
    print(f" -> Sampel Wajib  : {res_aql['recommended_sample_size']} unit sampel")
    print(f" -> Kriteria      : Terima jika cacat <= {res_aql['acceptance_criteria']['accept_max_defects']}, Tolak jika >= {res_aql['acceptance_criteria']['reject_if_defects_equal_or_greater']}")
    print(f" -> Pesan         : {res_aql['message']}")

    # 3. Peragaan Tool Engineer: run_spc_analysis
    print("\n[3] EKSEKUSI TOOL ENGINEER: run_spc_analysis")
    args_spc = {
        "sample_measurements": [10.02, 10.01, 10.04, 9.99, 10.00, 10.03, 10.01, 9.98],
        "upper_spec_limit": 10.15,
        "lower_spec_limit": 9.85
    }
    res_spc = json.loads(execute_tool("run_spc_analysis", json.dumps(args_spc)))
    print(f" -> Rata-rata (X) : {res_spc['mean']}")
    print(f" -> Std Dev (s)   : {res_spc['stdev']}")
    print(f" -> Indeks Cp     : {res_spc['cp']}")
    print(f" -> Indeks Cpk    : {res_spc['cpk']} (Status: {res_spc['process_capability']})")

    # 4. Peragaan Tool Action: create_inspection_lot
    print("\n[4] EKSEKUSI TOOL ACTION: create_inspection_lot")
    args_lot = {
        "material_or_product_id": "Pipa Stainless Steel SUS304",
        "lot_size": 1200,
        "inspection_type": "Incoming Goods Inspection",
        "tenant_id": 1
    }
    res_lot = json.loads(execute_tool("create_inspection_lot", json.dumps(args_lot)))
    print(f" -> Draft Lot ID  : {res_lot['draft_id']}")
    print(f" -> Kartu UI Link : {res_lot['card_markdown']}")
    print(f" -> Status        : {res_lot['status']}")

    print("\n" + "="*72)
    print("✅ HASIL: 17 Tools Cabang Quality Management siap dipanggil dengan isolasi role.")
    print("="*72 + "\n")

    return {
        "status": "success",
        "inspector_tools_count": len(inspector_tools),
        "officer_tools_count": len(officer_tools),
        "engineer_tools_count": len(engineer_tools),
        "draft_lot": res_lot["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
