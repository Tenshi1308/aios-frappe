"""
Unit Test Suite untuk AIOS Skills Engine & Loader (Role-Centric Architecture Opsi C - Tahap 6M.1 s/d 6M.11).
Menguji parser YAML frontmatter, path discovery hierarki <branch>/<role>/, smart caching, resolusi RBAC per role,
serta integritas seluruh 86 file skills aktif (85 domain ERP + Orchestrator) di 10 cabang direktori.
"""

import os
import json
import unittest
import tempfile
import shutil
from pathlib import Path

import frappe
from aios_v1.lib.skills_loader import (
    parse_frontmatter,
    load_skill_from_file,
    load_all_skills,
    get_skill_by_slug,
    get_skills_for_worker,
    validate_skill_dependencies,
    compose_worker_system_prompt,
    clear_skills_cache,
    _normalize_role_variants,
    _SKILLS_CACHE
)


class TestSkillsEngine(unittest.TestCase):
    def setUp(self):
        clear_skills_cache()
        self.test_dir = tempfile.mkdtemp(prefix="aios_test_skills_")

    def tearDown(self):
        clear_skills_cache()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def _create_sample_skill_file(self, branch: str, role: str, filename: str, content: str) -> str:
        role_dir = os.path.join(self.test_dir, branch, role)
        os.makedirs(role_dir, exist_ok=True)
        file_path = os.path.join(role_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    # =========================================================================
    # 1. TEST PARSE FRONTMATTER
    # =========================================================================
    def test_01_parse_frontmatter_valid_and_edge_cases(self):
        """Memastikan parser YAML frontmatter memisahkan header dan body secara presisi."""
        raw_md = """---
name: "Corporate Scenario Simulation"
slug: "corporate-scenario-simulation"
version: "1.0.0"
branch: "planning"
role: "planning_manager"
tools_required:
  - "run_what_if_scenario"
triggers:
  - "simulasi what if"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis
Menjalankan simulasi skenario bisnis.
"""
        metadata, body = parse_frontmatter(raw_md)
        self.assertEqual(metadata.get("name"), "Corporate Scenario Simulation")
        self.assertEqual(metadata.get("slug"), "corporate-scenario-simulation")
        self.assertEqual(metadata.get("role"), "planning_manager")
        self.assertEqual(len(metadata.get("tools_required", [])), 1)
        self.assertIn("# 1. Peran & Tujuan Bisnis", body)

    # =========================================================================
    # 2. TEST LOAD SINGLE SKILL FROM FILE DENGAN PATH DISCOVERY
    # =========================================================================
    def test_02_load_skill_from_file_hierarchy(self):
        """Memastikan load_skill_from_file mengekstrak branch dan role dari hierarki direktori."""
        content = """---
name: "Time Series Trends"
slug: "time-series-trends"
version: "1.0.0"
tools_required:
  - "run_trend_analysis"
priority: "high"
---
# Content SOP
Analisis deret waktu.
"""
        file_path = self._create_sample_skill_file("planning", "bi_analyst", "trends.md", content)
        skill = load_skill_from_file(file_path)

        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "Time Series Trends")
        self.assertEqual(skill["branch"], "planning")
        self.assertEqual(skill["role"], "bi_analyst")
        self.assertIn("bi_analyst", skill["roles"])
        self.assertEqual(skill["priority"], "high")
        self.assertIn("run_trend_analysis", skill["tools_required"])

    # =========================================================================
    # 3. TEST ROLE VARIANT NORMALIZATION
    # =========================================================================
    def test_03_normalize_role_variants(self):
        """Memastikan variasi nama peran (kebab-case, snake_case, space-case) dikenali setara."""
        variants_kebab = _normalize_role_variants("planning-manager")
        self.assertIn("planning-manager", variants_kebab)
        self.assertIn("planning_manager", variants_kebab)
        self.assertIn("planning manager", variants_kebab)

    # =========================================================================
    # 4. TEST ROLE-CENTRIC RBAC DISCOVERY (PLANNING & CROSS-BRANCH)
    # =========================================================================
    def test_04_get_skills_for_worker_rbac_option_c(self):
        """Menguji pemisahan hak akses peran mandiri (Role-Centric Strategic Planning)."""
        # 1. BI Analyst (2 skills di planning/bi_analyst/)
        bia_skills = get_skills_for_worker(branch="planning", worker_key="bi_analyst")
        bia_slugs = [s["slug"] for s in bia_skills]
        self.assertEqual(len(bia_slugs), 2)
        self.assertIn("executive-kpi-dashboard-assembly", bia_slugs)
        self.assertIn("time-series-trends-and-forecasting", bia_slugs)
        self.assertNotIn("corporate-scenario-simulation", bia_slugs)

        # 2. Report Developer (2 skills di planning/report_developer/)
        rpt_skills = get_skills_for_worker(branch="planning", worker_key="report_developer")
        rpt_slugs = [s["slug"] for s in rpt_skills]
        self.assertEqual(len(rpt_slugs), 2)
        self.assertIn("custom-report-template-design", rpt_slugs)
        self.assertIn("executive-narrative-and-scheduling", rpt_slugs)

        # 3. Data Steward (2 skills di planning/data_steward/)
        dst_skills = get_skills_for_worker(branch="planning", worker_key="data_steward")
        dst_slugs = [s["slug"] for s in dst_skills]
        self.assertEqual(len(dst_slugs), 2)
        self.assertIn("data-quality-audit-and-anomaly-detection", dst_slugs)
        self.assertIn("data-dictionary-and-market-benchmarks", dst_slugs)

        # 4. Planning Manager (8 skills Planning + 3 skills Orchestrator = 11 skills)
        mgr_skills = get_skills_for_worker(branch="planning", worker_key="manager")
        self.assertEqual(len(mgr_skills), 11)

    # =========================================================================
    # 5. TEST VALIDATE SKILL DEPENDENCIES
    # =========================================================================
    def test_05_validate_skill_dependencies(self):
        """Memastikan validasi dependensi tools_required mencocokkan ke _TOOL_REGISTRY."""
        valid_skill = {
            "name": "Planning Test",
            "slug": "test-valid-pln",
            "tools_required": ["run_what_if_scenario", "generate_kpi_dashboard"]
        }
        res_valid = validate_skill_dependencies(valid_skill)
        self.assertTrue(res_valid["valid"])
        self.assertEqual(len(res_valid["missing_tools"]), 0)

    # =========================================================================
    # 6. TEST COMPOSE WORKER SYSTEM PROMPT
    # =========================================================================
    def test_06_compose_worker_system_prompt(self):
        """Memastikan perakitan SOP ke dalam prompt berjalan rapi."""
        base_prompt = "Anda adalah Planning Manager berpengalaman."
        composed = compose_worker_system_prompt(branch="planning", worker_key="planning_manager", base_prompt=base_prompt)

        self.assertIn("Anda adalah Planning Manager berpengalaman.", composed)
        self.assertIn("[STANDARD OPERATING PROCEDURES & WORKFLOW SKILLS]", composed)
        self.assertIn("Corporate Scenario Simulation", composed)
        self.assertIn("OKR Alignment and Variance Governance", composed)

    # =========================================================================
    # 7. TEST REAL SKILLS INTEGRITY (86 SKILLS AKTIF / 100% CANONICAL)
    # =========================================================================
    def test_07_real_skills_integrity(self):
        """Menguji integritas seluruh 86 file skill nyata di direktori skills/ (Opsi C)."""
        all_skills = load_all_skills(force_reload=True)
        
        # Total harus 86 skills (3 Orch + 11 Fin + 10 Sales + 10 Mat + 11 HR + 7 Mfg + 9 QA + 9 Log + 8 Mnt + 8 Pln)
        self.assertEqual(len(all_skills), 86, f"Ekspektasi 86 skills, ditemukan {len(all_skills)}: {list(all_skills.keys())}")

        # Pastikan validasi seluruh tools_required (100% dari 86 skills) valid di _TOOL_REGISTRY
        validation = validate_skill_dependencies()
        self.assertTrue(validation["valid"], f"Ada missing tools pada skills: {validation.get('missing_tools')}")
        self.assertEqual(len(validation["missing_tools"]), 0)


def run_tests():
    """Fungsi runner untuk dieksekusi via `bench execute`."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkillsEngine)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    summary = {
        "success": result.wasSuccessful(),
        "total_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors)
    }
    print(json.dumps(summary, indent=2))
    return summary
