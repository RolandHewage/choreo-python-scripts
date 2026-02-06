"""Tests to validate the README contains the high-level architecture diagram."""

import os
import re

README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")


def _read_readme():
    with open(README_PATH, "r") as f:
        return f.read()


def test_readme_contains_mermaid_diagram():
    content = _read_readme()
    assert "```mermaid" in content, "README should contain a Mermaid diagram"
    assert "```" in content.split("```mermaid", 1)[1], "Mermaid block should be closed"


def test_diagram_references_all_extraction_scripts():
    content = _read_readme()
    expected_scripts = [
        "extract_aws_key_vault_secret_refs.py",
        "extract_app_db_secret_refs.py",
        "extract_rudder_db_secret_refs.py",
        "extract_config_svc_db_secret_refs.py",
        "extract_cloud_manager_db_secret_refs.py",
    ]
    for script in expected_scripts:
        assert script in content, f"Diagram should reference {script}"


def test_diagram_references_analysis_scripts():
    content = _read_readme()
    expected_scripts = [
        "detect_stale_secrets.py",
        "detect_stale_secrets_detailed.py",
        "sort_stale_secrets.py",
        "filter_type1_uuids.py",
    ]
    for script in expected_scripts:
        assert script in content, f"Diagram should reference {script}"


def test_diagram_shows_three_phases():
    content = _read_readme()
    assert "Phase 1" in content or "Data Extraction" in content
    assert "Phase 2" in content or "Stale Secret Detection" in content
    assert "Phase 3" in content or "Safe Deletion" in content


def test_high_level_architecture_section_exists():
    content = _read_readme()
    assert "## High-Level Architecture" in content
