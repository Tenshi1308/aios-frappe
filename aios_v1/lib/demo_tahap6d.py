"""
Demo CLI untuk Sub-tahap 6D: Katalog Tools Cabang Material, Inventory & Purchasing (15 Tools).
Memperagakan pengecekan ketersediaan stok, kalkulasi ROP/EOQ, dan pembuatan Draf Purchase Order.
"""

import json
from aios_v1.lib.tool_registry import execute_tool
import aios_v1.lib.tools.material_tools

def run_demo():
    print("\n" + "="*70)
    print("🚀 DEMO SUB-TAHAP 6D: TOOLS MATERIAL, INVENTORY & PURCHASING (15 TOOLS)")
    print("="*70)

    # 1. Peragaan Tool Ketersediaan Stok
    print("\n[1] EKSEKUSI TOOL: check_stock_availability")
    args_stock = {"product_id": "Baut M8x20 Baja", "warehouse": "Gudang Utama", "tenant_id": 1}
    res_stock = json.loads(execute_tool("check_stock_availability", json.dumps(args_stock)))
    print(f" -> Stok Fisik   : {res_stock['physical_stock']} {res_stock['unit']}")
    print(f" -> Reserved     : {res_stock['reserved_stock']} {res_stock['unit']}")
    print(f" -> Siap Pakai   : {res_stock['available_stock']} {res_stock['unit']} (Status: {res_stock['stock_status']})")
    print(f" -> Pesan        : {res_stock['message']}")

    # 2. Peragaan Tool Reorder Point & EOQ
    print("\n[2] EKSEKUSI TOOL: calculate_reorder_point & calculate_economic_order_qty")
    args_rop = {"daily_demand": 25, "lead_time_days": 7, "safety_stock": 75}
    res_rop = json.loads(execute_tool("calculate_reorder_point", json.dumps(args_rop)))
    print(f" -> Reorder Point : {res_rop['reorder_point']} unit")
    
    args_eoq = {"annual_demand": 9000, "order_cost": 150000, "annual_holding_cost_per_unit": 300}
    res_eoq = json.loads(execute_tool("calculate_economic_order_qty", json.dumps(args_eoq)))
    print(f" -> EOQ Optimal   : {res_eoq['eoq_units']} unit/order ({res_eoq['orders_per_year']}x pemesanan/tahun)")
    print(f" -> Pesan         : {res_eoq['message']}")

    # 3. Peragaan Tool Action: create_draft_purchase_order
    print("\n[3] EKSEKUSI TOOL ACTION: create_draft_purchase_order")
    args_po = {
        "vendor_name": "PT Sumber Makmur Baja Perkasa",
        "items": [
            {"product": "Baut M8x20 Baja Grade 8.8", "qty": 3000, "unit_price": 1200},
            {"product": "Mur M8 Baja Hexagonal", "qty": 3000, "unit_price": 600}
        ],
        "delivery_date": "2026-09-15",
        "tenant_id": 1
    }
    res_po = json.loads(execute_tool("create_draft_purchase_order", json.dumps(args_po)))
    print(f" -> Draft PO ID   : {res_po['draft_id']}")
    print(f" -> Total PO Nilai: Rp {res_po['total_amount']:,.0f} (termasuk PPN 11%)")
    print(f" -> Kartu UI Link : {res_po['card_markdown']}")
    print(f" -> Status        : {res_po['status']}")

    print("\n" + "="*70)
    print("✅ HASIL: 15 Tools Cabang Material & Purchasing siap dipanggil AI Manager.")
    print("="*70 + "\n")

    return {
        "status": "success",
        "rop_sample": res_rop["reorder_point"],
        "draft_po": res_po["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
