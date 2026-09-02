"""
Data Access Agent untuk AIOS.
Menyediakan antarmuka tunggal bagi semua Sub-Agent dan Tools untuk mengakses data bisnis klien.
Mengimplementasikan Semantic Mapping dan Graceful Degradation (Anti-Halusinasi).
"""

import frappe
from typing import Dict, Any, List, Optional
from aios_v1.lib.canonical_models import get_canonical_entity, CANONICAL_SCHEMA
from aios_v1.data_access.query_engine import get_mapping_lookup, execute_canonical_query

class DataAccessAgent:
    def __init__(self, tenant_id: int):
        self.tenant_id = tenant_id

    def is_concept_available(self, entity_name: str, field_name: Optional[str] = None) -> bool:
        """Memeriksa apakah entitas (dan field tertentu) sudah dipetakan di database klien."""
        _, lookup = get_mapping_lookup(self.tenant_id)
        if not lookup:
            return False

        entity_lower = entity_name.lower()
        if field_name:
            return (entity_lower, field_name.lower()) in lookup
        
        # Cek apakah ada minimal 1 field terpetakan untuk entitas ini
        return any(ent == entity_lower for (ent, _) in lookup.keys())

    def query(
        self,
        entity: str,
        fields: Optional[List[str]] = None,
        filters: Optional[List[Dict[str, Any]]] = None,
        order_by: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        aggregate: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Mengeksekusi query data bisnis via Canonical Data Model dengan Graceful Degradation.
        
        Return Structure:
        - status: "success" | "partial" | "concept_not_available"
        - rows: list data hasil query (jika ada)
        - missing_concept: nama konsep yang tidak tersedia (jika ada)
        - message: pesan status / catatan degradasi
        """
        conn_name, lookup = get_mapping_lookup(self.tenant_id)
        if not conn_name or not lookup:
            return {
                "status": "concept_not_available",
                "missing_concept": entity,
                "message": f"Belum ada koneksi database atau mapping aktif untuk tenant {self.tenant_id}.",
                "rows": [],
                "rowCount": 0
            }

        entity_lower = entity.lower()
        
        # 1. Cek apakah entitas ada dalam Canonical Schema
        canonical_def = get_canonical_entity(entity)
        if not canonical_def:
            return {
                "status": "concept_not_available",
                "missing_concept": entity,
                "message": f"Entitas '{entity}' bukan merupakan Canonical Model yang valid di AIOS.",
                "rows": [],
                "rowCount": 0
            }

        # 2. Cek apakah entitas terpetakan pada DB klien
        mapped_fields = [fld for (ent, fld) in lookup.keys() if ent == entity_lower]
        if not mapped_fields:
            return {
                "status": "concept_not_available",
                "missing_concept": entity,
                "message": f"Konsep '{entity}' belum tersedia atau dipetakan di sistem database Anda.",
                "rows": [],
                "rowCount": 0
            }

        # 3. Cek ketersediaan field yang diminta (Graceful Degradation)
        target_fields = fields or list(canonical_def.fields.keys())
        available_fields = [f for f in target_fields if f.lower() in mapped_fields]
        missing_fields = [f for f in target_fields if f.lower() not in mapped_fields]

        if not available_fields:
            return {
                "status": "concept_not_available",
                "missing_concept": f"{entity}.{','.join(missing_fields)}",
                "message": f"Fitur ini membutuhkan data {entity} ({', '.join(missing_fields)}) yang belum tersedia di sistem Anda.",
                "rows": [],
                "rowCount": 0
            }

        # 4. Bangun query dan eksekusi via query_engine
        query_payload = {
            "entity": entity,
            "fields": available_fields,
            "filters": filters or [],
            "orderBy": order_by,
            "limit": limit,
            "aggregate": aggregate
        }

        exec_res = execute_canonical_query(self.tenant_id, query_payload)
        if not exec_res.get("ok"):
            return {
                "status": "concept_not_available",
                "missing_concept": entity,
                "message": exec_res.get("error", "Gagal mengeksekusi query canonical."),
                "rows": [],
                "rowCount": 0
            }

        # 5. Format hasil (apakah full success atau partial degradation)
        if missing_fields:
            return {
                "status": "partial",
                "missing_fields": missing_fields,
                "message": f"Data '{entity}' berhasil diambil secara parsial. Kolom yang belum tersedia: {', '.join(missing_fields)}.",
                "columns": exec_res.get("columns", []),
                "rows": exec_res.get("rows", []),
                "rowCount": exec_res.get("rowCount", 0)
            }

        return {
            "status": "success",
            "columns": exec_res.get("columns", []),
            "rows": exec_res.get("rows", []),
            "rowCount": exec_res.get("rowCount", 0),
            "message": f"Data '{entity}' berhasil diambil lengkap."
        }

def get_data_access_agent(tenant_id: int) -> DataAccessAgent:
    """Helper factory untuk inisialisasi DataAccessAgent."""
    return DataAccessAgent(tenant_id=tenant_id)
