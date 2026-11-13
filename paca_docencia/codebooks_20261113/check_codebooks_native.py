#!/usr/bin/env python3
"""PACA DOCENCIA: local-only native execution of four newly prepared codebooks.

No GitHub Actions, network, arbitrary notebook discovery or third-party execution.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOKS = (
    "01_qaoa_maxcut_baseline.ipynb",
    "02_tfim_exact_reference.ipynb",
    "03_mps_svd_compression.ipynb",
    "04_hhl_classical_control.ipynb",
)

def check():
    try:
        import numpy  # noqa: F401
    except ImportError:
        return {"status":"HOLD_NUMPY_NOT_INSTALLED","tested":[]}
    results = []
    for name in NOTEBOOKS:
        path=ROOT/"codebooks"/name
        if not path.is_file():
            return {"status":"HOLD_NOTEBOOK_MISSING","missing":name,"tested":results}
        book=json.loads(path.read_text(encoding="utf-8"))
        if book.get("nbformat")!=4:
            return {"status":"HOLD_NOTEBOOK_FORMAT","missing":name,"tested":results}
        cells=book.get("cells",[])
        if any(c.get("outputs") or c.get("execution_count") is not None
               for c in cells if c.get("cell_type")=="code"):
            return {"status":"HOLD_NOTEBOOK_STORED_OUTPUT","missing":name,"tested":results}
        snippets=["".join(c["source"]) if isinstance(c["source"],list) else c["source"]
                  for c in cells if c.get("cell_type")=="code"]
        if not snippets:
            return {"status":"HOLD_NO_EXECUTABLE_CELLS","missing":name,"tested":results}
        # Only four exact allowlisted files; no notebooks imported from external sources.
        proc=subprocess.run([sys.executable,"-I","-c","\n\n".join(snippets)],
             cwd=ROOT,text=True,capture_output=True,timeout=30,check=False)
        if proc.returncode:
            return {"status":"HOLD_NATIVE_CODEBOOK_FAILED","failed":name,
                    "exit_code":proc.returncode,"tested":results}
        results.append({"path":name,"code_cells":len(snippets),"status":"PASS"})
    return {"status":"PASS_NATIVE_CODEBOOKS","tested":results,
            "github_actions_used":False,"third_party_notebooks_executed":False}

if __name__=="__main__":
    try:
        receipt=check()
    except (OSError,ValueError,subprocess.TimeoutExpired,json.JSONDecodeError):
        receipt={"status":"HOLD_NATIVE_RUNNER_ERROR"}
    print(json.dumps(receipt,sort_keys=True,ensure_ascii=False))
    raise SystemExit(0 if receipt["status"]=="PASS_NATIVE_CODEBOOKS" else 2)
