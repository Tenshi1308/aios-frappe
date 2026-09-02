import os
import sqlite3
import hashlib
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseDatabaseAdapter(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.engine = (config.get("engine") or "sqlite").lower()

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """Test connection and return dict(ok=True/False, message=str)."""
        pass

    @abstractmethod
    def extract_schema(self) -> Dict[str, Any]:
        """Extract raw tables, columns, data types, primary keys, foreign keys."""
        pass

    @abstractmethod
    def execute_read_query(self, sql: str, params: Optional[List[Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Execute a strictly read-only query and return row dicts."""
        pass

    @abstractmethod
    def quote_identifier(self, ident: str) -> str:
        """Quote a table or column name safely."""
        pass

def compute_schema_hash(schema: Dict[str, Any]) -> str:
    """Generate SHA256 deterministic hash of schema tables and columns."""
    normalized = []
    for t in sorted(schema.get("tables", []), key=lambda x: x["name"]):
        cols = [f"{c['name']}:{c['type']}" for c in sorted(t.get("columns", []), key=lambda c: c["name"])]
        normalized.append(f"{t['name']}({','.join(cols)})")
    raw = "|".join(normalized)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
