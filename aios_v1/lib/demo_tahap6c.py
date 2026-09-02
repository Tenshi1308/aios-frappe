"""
Demo CLI untuk Sub-tahap 6C: Katalog Tools Cabang Sales & Distribution (15 Tools).
Memperagakan pengecekan credit limit, kalkulasi diskon kuantitas, dan pembuatan Draf Sales Order.
"""

import json
from aios_v1.lib.tool_registry import execute_tool
import aios_v1.lib.tools.sales_tools

def run_demo():
    print("\n" + "="*70)
    print("🚀 DEMO SUB-TAHAP 6C: TOOLS SALES & DISTRIBUTION (15 TOOLS)")
    print("="*70)

    # 1. Peragaan Tool Credit Limit Check
    print("\n[1] EKSEKUSI TOOL: check_customer_credit_limit")
    args_cred = {"customer_id": "CUST-007", "requested_order_amount": 35000000, "tenant_id": 1}
    res_cred = json.loads(execute_tool("check_customer_credit_limit", json.dumps(args_cred)))
    print(f" -> Status Plafon : {res_cred['status']}")
    print(f" -> Sisa Plafon   : Rp {res_cred['available_credit']:,.0f}")
    print(f" -> Pesanan Baru  : Rp {res_cred['requested_amount']:,.0f}")
    print(f" -> Pesan         : {res_cred['message']}")

    # 2. Peragaan Tool Volume Discount Calculation
    print("\n[2] EKSEKUSI TOOL: calculate_volume_discount")
    args_disc = {"quantity": 750, "unit_price": 50000}
    res_disc = json.loads(execute_tool("calculate_volume_discount", json.dumps(args_disc)))
    print(f" -> Qty Beli      : {res_disc['quantity']} unit")
    print(f" -> Diskon Tier   : {res_disc['discount_percent']}%")
    print(f" -> Hemat Diskon  : Rp {res_disc['discount_amount']:,.0f}")
    print(f" -> Total Bayar   : Rp {res_disc['net_total']:,.0f}")
    print(f" -> Pesan         : {res_disc['message']}")

    # 3. Peragaan Tool Action: create_draft_sales_order
    print("\n[3] EKSEKUSI TOOL ACTION: create_draft_sales_order")
    args_so = {
        "customer_id": "PT Sumber Rejeki Abadi",
        "items": [
            {"product": "Baut M8x20 Baja", "qty": 500, "unit_price": 1500},
            {"product": "Mur M8 Galvanis", "qty": 500, "unit_price": 800}
        ],
        "payment_terms": "Net 30",
        "tenant_id": 1
    }
    res_so = json.loads(execute_tool("create_draft_sales_order", json.dumps(args_so)))
    print(f" -> Draft SO ID   : {res_so['draft_id']}")
    print(f" -> Total Nilai   : Rp {res_so['total_amount']:,.0f} (termasuk PPN 11%)")
    print(f" -> Kartu UI Link : {res_so['card_markdown']}")
    print(f" -> Status        : {res_so['status']}")

    print("\n" + "="*70)
    print("✅ HASIL: 15 Tools Cabang Sales & Distribution siap dipanggil AI Manager.")
    print("="*70 + "\n")

    return {
        "status": "success",
        "credit_status": res_cred["status"],
        "draft_so": res_so["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
