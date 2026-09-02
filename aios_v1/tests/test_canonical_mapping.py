"""
Automated Test untuk Tahap 4: Canonical Data Model & Semantic Mapping.
Menguji:
1. Validasi Canonical Schema (dataclass).
2. Graceful Degradation saat konsep atau field tidak tersedia di mapping.
3. Respons anti-halusinasi (concept_not_available).
"""

import unittest
from unittest.mock import patch, MagicMock
from aios_v1.lib.canonical_models import get_canonical_entity, CANONICAL_SCHEMA
from aios_v1.lib.data_access_agent import DataAccessAgent, get_data_access_agent

class TestCanonicalMapping(unittest.TestCase):

    def setUp(self):
        self.tenant_id = 999
        self.agent = get_data_access_agent(self.tenant_id)

    def test_canonical_schema_definitions(self):
        """Memastikan semua canonical entity terdaftar dan memiliki required fields."""
        self.assertIn("Product", CANONICAL_SCHEMA)
        self.assertIn("Customer", CANONICAL_SCHEMA)
        self.assertIn("Employee", CANONICAL_SCHEMA)
        self.assertIn("SalesOrder", CANONICAL_SCHEMA)
        self.assertIn("PurchaseOrder", CANONICAL_SCHEMA)

        product = get_canonical_entity("product")
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Product")
        self.assertIn("name", product.fields)
        self.assertTrue(product.fields["name"].required)

    @patch("aios_v1.lib.data_access_agent.get_mapping_lookup")
    def test_unmapped_entity_graceful_degradation(self, mock_lookup):
        """Uji saat entitas diminta tapi belum ada mapping-nya di DB klien."""
        # Simulasi tenant punya mapping hanya untuk Product, tapi tidak untuk Warranty
        mock_lookup.return_value = ("CONN-1", {
            ("product", "id"): {"table": "items", "column": "item_code"},
            ("product", "name"): {"table": "items", "column": "item_name"},
        })

        # Query entitas yang tidak ada di mapping
        res = self.agent.query(entity="Customer")
        self.assertEqual(res["status"], "concept_not_available")
        self.assertEqual(res["missing_concept"], "Customer")
        self.assertIn("belum tersedia", res["message"])
        self.assertEqual(res["rowCount"], 0)

    @patch("aios_v1.lib.data_access_agent.get_mapping_lookup")
    def test_unknown_entity_rejection(self, mock_lookup):
        """Uji saat entitas asing yang bukan standar canonical diminta."""
        mock_lookup.return_value = ("CONN-1", {("product", "name"): {"table": "t", "column": "c"}})
        
        res = self.agent.query(entity="NonExistentAlienEntity")
        self.assertEqual(res["status"], "concept_not_available")
        self.assertIn("bukan merupakan Canonical Model yang valid", res["message"])

    @patch("aios_v1.lib.data_access_agent.get_mapping_lookup")
    @patch("aios_v1.lib.data_access_agent.execute_canonical_query")
    def test_partial_field_degradation(self, mock_exec, mock_lookup):
        """Uji saat hanya sebagian field yang terpetakan (Graceful Degradation)."""
        # Mapping hanya ada name dan price, tapi stock TIDAK ADA
        mock_lookup.return_value = ("CONN-1", {
            ("product", "id"): {"table": "items", "column": "id"},
            ("product", "name"): {"table": "items", "column": "name"},
            ("product", "price"): {"table": "items", "column": "price"},
        })

        # Mock eksekusi query untuk field yang tersedia
        mock_exec.return_value = {
            "ok": True,
            "columns": ["id", "name", "price"],
            "rows": [{"id": "P01", "name": "Baut M8", "price": 1500}],
            "rowCount": 1
        }

        # Sub-agent meminta field name, price, dan stock
        res = self.agent.query(entity="Product", fields=["name", "price", "stock"])
        
        # Harus mengembalikan status 'partial', bukan crash/error
        self.assertEqual(res["status"], "partial")
        self.assertIn("stock", res["missing_fields"])
        self.assertEqual(len(res["rows"]), 1)
        self.assertEqual(res["rows"][0]["name"], "Baut M8")
        self.assertIn("parsial", res["message"].lower())

    @patch("aios_v1.lib.data_access_agent.get_mapping_lookup")
    def test_all_requested_fields_missing(self, mock_lookup):
        """Uji saat field spesifik yang diminta sama sekali tidak ada di mapping."""
        mock_lookup.return_value = ("CONN-1", {
            ("product", "id"): {"table": "items", "column": "id"},
            ("product", "name"): {"table": "items", "column": "name"},
        })

        # Minta field 'stock' dan 'unit' yang keduanya tidak terpetakan
        res = self.agent.query(entity="Product", fields=["stock", "unit"])
        self.assertEqual(res["status"], "concept_not_available")
        self.assertIn("stock,unit", res["missing_concept"])

    @patch("aios_v1.lib.data_access_agent.get_mapping_lookup")
    def test_concept_availability_checker(self, mock_lookup):
        """Uji helper is_concept_available."""
        mock_lookup.return_value = ("CONN-1", {
            ("product", "name"): {"table": "items", "column": "name"},
            ("product", "price"): {"table": "items", "column": "price"},
        })

        self.assertTrue(self.agent.is_concept_available("Product"))
        self.assertTrue(self.agent.is_concept_available("Product", "name"))
        self.assertFalse(self.agent.is_concept_available("Product", "stock"))
        self.assertFalse(self.agent.is_concept_available("SalesOrder"))

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCanonicalMapping)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return {
        "success": result.wasSuccessful(),
        "total_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors)
    }

if __name__ == "__main__":
    run_tests()
