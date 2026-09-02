"""
Canonical Data Models untuk AIOS.
Mendefinisikan entitas bisnis terstandarisasi yang digunakan oleh Sub-Agent dan Tools.
Tools beroperasi di atas Canonical Data Model, TIDAK query ke skema raw database klien.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class CanonicalField:
    name: str
    data_type: str  # "string", "number", "date", "boolean", "json"
    description: str
    required: bool = False

@dataclass
class CanonicalEntity:
    name: str
    description: str
    category: str  # "Master Data", "Transaction", "Inventory", "HR", etc.
    fields: Dict[str, CanonicalField] = field(default_factory=dict)

# Kamus canonical entities yang didukung oleh AIOS
CANONICAL_SCHEMA: Dict[str, CanonicalEntity] = {
    "Product": CanonicalEntity(
        name="Product",
        description="Master data katalog barang/produk",
        category="Master Data",
        fields={
            "id": CanonicalField("id", "string", "Kode atau SKU produk", required=True),
            "name": CanonicalField("name", "string", "Nama produk", required=True),
            "category": CanonicalField("category", "string", "Kategori produk"),
            "price": CanonicalField("price", "number", "Harga satuan"),
            "stock": CanonicalField("stock", "number", "Jumlah stok tersedia"),
            "unit": CanonicalField("unit", "string", "Satuan unit barang (misal: Pcs, Kg, Box)")
        }
    ),
    "Customer": CanonicalEntity(
        name="Customer",
        description="Master data pelanggan/klien",
        category="Master Data",
        fields={
            "id": CanonicalField("id", "string", "ID / Kode pelanggan", required=True),
            "name": CanonicalField("name", "string", "Nama lengkap pelanggan", required=True),
            "phone": CanonicalField("phone", "string", "Nomor telepon / WhatsApp"),
            "email": CanonicalField("email", "string", "Alamat email"),
            "city": CanonicalField("city", "string", "Kota / Lokasi pelanggan")
        }
    ),
    "Employee": CanonicalEntity(
        name="Employee",
        description="Master data karyawan dan struktur organisasi",
        category="HR",
        fields={
            "id": CanonicalField("id", "string", "NIK / NIP karyawan", required=True),
            "name": CanonicalField("name", "string", "Nama lengkap karyawan", required=True),
            "role": CanonicalField("role", "string", "Jabatan atau posisi"),
            "department": CanonicalField("department", "string", "Divisi / Departemen"),
            "salary": CanonicalField("salary", "number", "Gaji pokok"),
            "hireDate": CanonicalField("hireDate", "date", "Tanggal mulai bekerja")
        }
    ),
    "SalesOrder": CanonicalEntity(
        name="SalesOrder",
        description="Transaksi pesanan penjualan pelanggan",
        category="Transaction",
        fields={
            "id": CanonicalField("id", "string", "Nomor nota / nomor pesanan", required=True),
            "date": CanonicalField("date", "date", "Tanggal transaksi penjualan", required=True),
            "customerId": CanonicalField("customerId", "string", "ID Pelanggan terkait"),
            "productId": CanonicalField("productId", "string", "ID Produk yang dipesan"),
            "quantity": CanonicalField("quantity", "number", "Kuantitas produk yang dipesan"),
            "amount": CanonicalField("amount", "number", "Total nilai penjualan / omzet"),
            "status": CanonicalField("status", "string", "Status order (DRAFT, CONFIRMED, COMPLETED, CANCELLED)")
        }
    ),
    "PurchaseOrder": CanonicalEntity(
        name="PurchaseOrder",
        description="Transaksi pengadaan / pesanan pembelian ke pemasok",
        category="Transaction",
        fields={
            "id": CanonicalField("id", "string", "Nomor PO pengadaan", required=True),
            "date": CanonicalField("date", "date", "Tanggal pembuatan PO", required=True),
            "supplier": CanonicalField("supplier", "string", "Nama pemasok / vendor"),
            "amount": CanonicalField("amount", "number", "Total nilai pengadaan"),
            "status": CanonicalField("status", "string", "Status PO (DRAFT, APPROVED, RECEIVED, CANCELLED)")
        }
    )
}

def get_canonical_entity(entity_name: str) -> Optional[CanonicalEntity]:
    """Mengambil definisi skema entitas canonical berdasarkan namanya (case-insensitive)."""
    for key, entity in CANONICAL_SCHEMA.items():
        if key.lower() == entity_name.lower():
            return entity
    return None
