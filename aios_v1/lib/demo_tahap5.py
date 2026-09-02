"""
Demo CLI untuk Tahap 5: Central Swarm Router, Task Ledger, dan Safety Limits.
Memperagakan kolaborasi multi-cabang (Sales -> Inventory -> Purchasing) dan pencegahan infinite loop.
"""

import json
from aios_v1.lib.swarm_router import get_swarm_router, register_branch_handler
from aios_v1.lib.task_ledger import get_task_ledger

def run_demo(tenant_id: int = 1):
    import time
    router = get_swarm_router(tenant_id)
    ledger = get_task_ledger(tenant_id)
    suffix = int(time.time())
    
    print("\n" + "="*68)
    print("🚀 DEMO TAHAP 5: CENTRAL SWARM ROUTER & SAFETY LIMITS")
    print("="*68)
    
    # -------------------------------------------------------------
    # Skenario 1: Happy Path Orkestrasi Multi-Agent (3-Hop Chain)
    # -------------------------------------------------------------
    task_1 = f"TSK-SWARM-DEMO-{suffix}"
    print("\n[SKENARIO 1] KOLABORASI MULTI-CABANG (Sales -> Inventory -> Purchasing):")
    
    # Hop 1: Sales konsultasi ke Inventory
    print(" -> [Hop 1] Sales AI meminta data stok ke Inventory AI...")
    r1 = router.route_message(
        task_id=task_1,
        from_branch="Sales",
        to_branch="Inventory",
        message_type="consultation",
        payload={"query": "Cek ketersediaan 100 unit Baut M8"}
    )
    print(f"    Status: {r1['status']} | Depth: {r1['chain_depth']} | Pesan: {r1['message']}")
    
    # Hop 2: Inventory meminta Purchasing membuat draf PO
    print(" -> [Hop 2] Stok kurang! Inventory AI meminta Purchasing AI buat PO...")
    r2 = router.route_message(
        task_id=task_1,
        from_branch="Inventory",
        to_branch="Purchasing",
        message_type="action_request",
        payload={"item": "Baut M8", "qty": 50, "vendor": "PT Sumber Makmur"}
    )
    print(f"    Status: {r2['status']} | Depth: {r2['chain_depth']} | Pesan: {r2['message']}")
    
    # Hop 3: Purchasing meminta CFO konfirmasi anggaran
    print(" -> [Hop 3] Purchasing AI meneruskan ke CFO (Finance) untuk approval...")
    r3 = router.route_message(
        task_id=task_1,
        from_branch="Purchasing",
        to_branch="Finance",
        message_type="consultation",
        payload={"budget_check_amount": 75000}
    )
    print(f"    Status: {r3['status']} | Depth: {r3['chain_depth']} | Pesan: {r3['message']}")
    
    # Periksa ringkasan di Task Ledger
    chain_summary = ledger.get_task_chain(task_1)
    print(f"\n 📊 Ringkasan Global Task Ledger untuk {task_1}:")
    print(f"    Total Hops: {len(chain_summary['hops'])}")
    print(f"    Status Chain: {chain_summary['status']}")
    print(f"    Cabang Terakhir: {chain_summary['current_branch']}")

    # -------------------------------------------------------------
    # Skenario 2: Pencegahan Infinite Loop (Max Chain Depth = 5)
    # -------------------------------------------------------------
    task_loop = f"TSK-SWARM-LOOP-{suffix}"
    print("\n" + "-"*68)
    print("[SKENARIO 2] PENCEGAHAN INFINITE LOOP (Max Chain Depth Guard):")
    print(" -> Mensimulasikan agen yang salah logika dan saling ping-pong...")
    
    branches = ["Sales", "Inventory", "Purchasing", "Finance", "Logistics", "Sales", "Inventory"]
    for i in range(len(branches) - 1):
        from_b = branches[i]
        to_b = branches[i+1]
        res_loop = router.route_message(
            task_id=task_loop,
            from_branch=from_b,
            to_branch=to_b,
            message_type="consultation",
            payload={"ping": i+1}
        )
        if res_loop["ok"]:
            print(f"    Hop {res_loop['chain_depth']}: {from_b} ➔ {to_b} [OK]")
        else:
            print(f"    Hop {i+1}: {from_b} ➔ {to_b} [DITOLAK - {res_loop['status']}]")
            print(f"    🛡️ Safety Guard Triggered: {res_loop['message']}")

    print("\n" + "="*68)
    print("✅ HASIL: Swarm Router berhasil mengoordinasikan pesan antar cabang")
    print("   dan Safety Limits secara otomatis menghentikan loop liar.")
    print("="*68 + "\n")

    return {
        "status": "success",
        "demo_results": {
            "chain_status": chain_summary["status"],
            "loop_guard_status": res_loop["status"]
        }
    }

if __name__ == "__main__":
    run_demo()
