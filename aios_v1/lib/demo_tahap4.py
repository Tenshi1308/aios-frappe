"""
Demo CLI untuk Tahap 4: Canonical Data Model & Semantic Mapping.
Memperagakan bagaimana Sub-Agent mengakses data via Data Access Agent dan bagaimana
Graceful Degradation bekerja ketika konsep/field tidak ada di DB klien.
"""

import json
import frappe
from aios_v1.lib.data_access_agent import get_data_access_agent

def run_demo(tenant_id: int = 1):
    agent = get_data_access_agent(tenant_id)
    
    print("\n" + "="*65)
    print("🚀 DEMO TAHAP 4: CANONICAL DATA MODEL & GRACEFUL DEGRADATION")
    print("="*65)
    
    # 1. Tampilkan Kamus Canonical Schema Terdaftar
    print("\n[1] CANONICAL SCHEMA TERDAFTAR DI AIOS:")
    from aios_v1.lib.canonical_models import CANONICAL_SCHEMA
    for ent_name, ent_def in CANONICAL_SCHEMA.items():
        field_names = list(ent_def.fields.keys())
        print(f" • {ent_name:14} [{ent_def.category:12}] : {', '.join(field_names)}")
    
    # 2. Simulasi query ke Data Access Agent
    print("\n[2] PENGUJIAN QUERY ENTITAS VALID (Product) KE DATA ACCESS AGENT:")
    res_product = agent.query("Product", fields=["id", "name", "price", "stock"])
    print(f" -> Status: {res_product.get('status')}")
    print(f" -> Penjelasan Sistem: {res_product.get('message')}")
    
    # 3. Pengujian Graceful Degradation (Field Tidak Tersedia)
    print("\n[3] PENGUJIAN GRACEFUL DEGRADATION (Field Tidak Tersedia di Skema Klien):")
    res_missing_field = agent.query("Product", fields=["name", "warranty_code_custom", "depreciation_rate"])
    print(f" -> Status: {res_missing_field.get('status')}")
    print(f" -> Penjelasan Sistem: {res_missing_field.get('message')}")
    
    # 4. Pengujian Entitas yang Belum Dipetakan Sama Sekali
    print("\n[4] PENGUJIAN ENTITAS YANG BELUM DIPETAKAN (WarrantyClaim):")
    res_unmapped = agent.query("WarrantyClaim")
    print(f" -> Status: {res_unmapped.get('status')}")
    print(f" -> Missing Concept: {res_unmapped.get('missing_concept')}")
    print(f" -> Penjelasan Sistem: {res_unmapped.get('message')}")
    
    print("\n" + "="*65)
    print("✅ HASIL: Sistem beroperasi murni via Canonical Data Model.")
    print("   Jika data tidak lengkap, sistem TIDAK berhalusinasi, melainkan")
    print("   mengembalikan status 'concept_not_available' secara anggun.")
    print("="*65 + "\n")
    
    return {
        "status": "success",
        "demo_results": {
            "product_query": res_product.get("status"),
            "graceful_field_degradation": res_missing_field.get("status"),
            "unmapped_concept_degradation": res_unmapped.get("status")
        }
    }

if __name__ == "__main__":
    run_demo()
