"""UIMP student landing regression: the course body must not disappear."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

def test_course_landing_has_actual_content():
    text = README.read_text(encoding="utf-8")
    assert text.startswith("# Introduction to Quantum Artificial Intelligence")
    assert len(text) > 20000
    for section in ("#  2 About", "# 3 Preliminaries:", "#  5 Try the tutorials", "# EXERCISE", "# MATERIALS"):
        assert section in text
    assert "quantum linear solvers" in text.lower()
    assert "Jupyter" in text

def test_pacadoc_links_resolve_and_landing_is_student_first():
    text = README.read_text(encoding="utf-8")
    assert text.index("## Start here") < text.index("# 1 Table of Contents")
    for relative in ("PACADOC.md", "docs/sigil/SIGIL_STACK_NORMALIZATION.md"):
        assert (ROOT / relative).is_file()
        assert f"]({relative})" in text
    assert "one error · one change · one rerun · one note" in text
    assert "Do not uninstall an existing environment" in text

def test_no_duplicate_top_level_course_sections():
    text = README.read_text(encoding="utf-8")
    for marker in ("# 1 Table of Contents", "#  2 About", "# 3 Preliminaries:", "#  5 Try the tutorials"):
        assert text.count(marker) == 1
    assert re.search(r"(?m)^# 6 Python for Scientific computing", text)
