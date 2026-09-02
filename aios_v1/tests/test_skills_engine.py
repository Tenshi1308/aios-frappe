"""
Unit Test Suite untuk AIOS Skills Engine & Loader (Role-Centric Architecture Opsi C - Tahap 6M.1 s/d 6M.8).
Menguji parser YAML frontmatter, path discovery hierarki <branch>/<role>/, smart caching, resolusi RBAC per role,
serta integritas 61 skills aktif di Orchestrator, Finance, Sales, Material, HR, Manufacturing, dan Quality.
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
name: "Inspection Lot and Sampling"
slug: "inspection-lot-and-sampling"
version: "1.0.0"
branch: "quality"
role: "quality_inspector"
tools_required:
  - "create_inspection_lot"
triggers:
  - "sampling aql"
priority: "high"
---

# 1. Peran & Tujuan Bisnis
Mengatur rencana sampling pengujian mutu.
"""
        metadata, body = parse_frontmatter(raw_md)
        self.assertEqual(metadata.get("name"), "Inspection Lot and Sampling")
        self.assertEqual(metadata.get("slug"), "inspection-lot-and-sampling")
        self.assertEqual(metadata.get("role"), "quality_inspector")
        self.assertEqual(len(metadata.get("tools_required", [])), 1)
        self.assertIn("# 1. Peran & Tujuan Bisnis", body)

    # =========================================================================
    # 2. TEST LOAD SINGLE SKILL FROM FILE DENGAN PATH DISCOVERY
    # =========================================================================
    def test_02_load_skill_from_file_hierarchy(self):
        """Memastikan load_skill_from_file mengekstrak branch dan role dari hierarki direktori."""
        content = """---
name: "SPC Analysis"
slug: "spc-analysis"
version: "1.0.0"
tools_required:
  - "run_spc_analysis"
priority: "high"
---
# Content SOP
Analisis kapabilitas Cpk.
"""
        file_path = self._create_sample_skill_file("quality", "quality_engineer", "spc.md", content)
        skill = load_skill_from_file(file_path)

        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "SPC Analysis")
        self.assertEqual(skill["branch"], "quality")
        self.assertEqual(skill["role"], "quality_engineer")
        self.assertIn("quality_engineer", skill["roles"])
        self.assertEqual(skill["priority"], "high")
        self.assertIn("run_spc_analysis", skill["tools_required"])

    # =========================================================================
    # 3. TEST ROLE VARIANT NORMALIZATION
    # =========================================================================
    def test_03_normalize_role_variants(self):
        """Memastikan variasi nama peran (kebab-case, snake_case, space-case) dikenali setara."""
        variants_kebab = _normalize_role_variants("quality-control-officer")
        self.assertIn("quality-control-officer", variants_kebab)
        self.assertIn("quality_control_officer", variants_kebab)
        self.assertIn("quality control officer", variants_kebab)

    # =========================================================================
    # 4. TEST ROLE-CENTRIC RBAC DISCOVERY (QUALITY & CROSS-BRANCH)
    # =========================================================================
    def test_04_get_skills_for_worker_rbac_option_c(self):
        """Menguji pemisahan hak akses peran mandiri (Role-Centric Quality)."""
        # 1. Quality Inspector (2 skills di quality/quality_inspector/)
        ins_skills = get_skills_for_worker(branch="quality", worker_key="quality_inspector")
        ins_slugs = [s["slug"] for s in ins_skills]
        self.assertEqual(len(ins_slugs), 2)
        self.assertIn("inspection-lot-and-sampling", ins_slugs)
        self.assertIn("measurement-recording-and-calibration", ins_slugs)
        self.assertNotIn("usage-decision-and-coa-issuance", ins_slugs)

        # 2. Quality Control Officer (2 skills di quality/quality_control_officer/)
        qco_skills = get_skills_for_worker(branch="quality", worker_key="quality_control_officer")
        qco_slugs = [s["slug"] for s in qco_skills]
        self.assertEqual(len(qco_slugs), 2)
        self.assertIn("usage-decision-and-coa-issuance", qco_slugs)
        self.assertIn("quality-notification-and-ncr", qco_slugs)

        # 3. Quality Engineer (2 skills di quality/quality_engineer/)
        qen_skills = get_skills_for_worker(branch="quality", worker_key="quality_engineer")
        qen_slugs = [s["slug"] for s in qen_skills]
        self.assertEqual(len(qen_slugs), 2)
        self.assertIn("spc-and-process-capability-analysis", qen_slugs)
        self.assertIn("first-pass-yield-and-capa-tracking", qen_slugs)

        # 4. Quality Auditor (1 skill di quality/quality_auditor/)
        aud_skills = get_skills_for_worker(branch="quality", worker_key="quality_auditor")
        aud_slugs = [s["slug"] for s in aud_skills]
        self.assertEqual(len(aud_slugs), 1)
        self.assertIn("internal-audit-and-findings-reporting", aud_slugs)

        # 5. Quality Manager (9 skills Quality + 3 skills Orchestrator = 12 skills)
        mgr_skills = get_skills_for_worker(branch="quality", worker_key="manager")
        self.assertEqual(len(mgr_skills), 12)

    # =========================================================================
    # 5. TEST VALIDATE SKILL DEPENDENCIES
    # =========================================================================
    def test_05_validate_skill_dependencies(self):
        """Memastikan validasi dependensi tools_required mencocokkan ke _TOOL_REGISTRY."""
        valid_skill = {
            "name": "Quality Test",
            "slug": "test-valid-qa",
            "tools_required": ["run_spc_analysis", "make_usage_decision"]
        }
        res_valid = validate_skill_dependencies(valid_skill)
        self.assertTrue(res_valid["valid"])
        self.assertEqual(len(res_valid["missing_tools"]), 0)

    # =========================================================================
    # 6. TEST COMPOSE WORKER SYSTEM PROMPT
    # =========================================================================
    def test_06_compose_worker_system_prompt(self):
        """Memastikan perakitan SOP ke dalam prompt berjalan rapi."""
        base_prompt = "Anda adalah Quality Engineer profesional."
        composed = compose_worker_system_prompt(branch="quality", worker_key="quality_engineer", base_prompt=base_prompt)

        self.assertIn("Anda adalah Quality Engineer profesional.", composed)
        self.assertIn("[STANDARD OPERATING PROCEDURES & WORKFLOW SKILLS]", composed)
        self.assertIn("SPC and Process Capability Analysis", composed)
        self.assertIn("First Pass Yield and CAPA Tracking", composed)

    # =========================================================================
    # 7. TEST REAL SKILLS INTEGRITY (61 SKILLS AKTIF)
    # =========================================================================
    def test_07_real_skills_integrity(self):
        """Menguji integritas seluruh 61 file skill nyata di direktori skills/ (Opsi C)."""
        all_skills = load_all_skills(force_reload=True)
        
        # Total harus 61 skills (3 Orch + 11 Fin + 10 Sales + 10 Mat + 11 HR + 7 Mfg + 9 QA)
        self.assertEqual(len(all_skills), 61, f"Ekspektasi 61 skills, ditemukan {len(all_skills)}: {list(all_skills.keys())}")

        # Pastikan validasi seluruh tools_required (100% dari 61 skills) valid di _TOOL_REGISTRY
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
