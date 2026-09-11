#!/usr/bin/env python3
"""Forward workspace commands to the single shared framework checkout."""
import os
from pathlib import Path
import runpy
import sys


workspace = Path(__file__).resolve().parents[2]
core = workspace / "framework/core"
script = core / "scripts" / Path(__file__).name
if not script.is_file():
    raise SystemExit(
        f"Framework compartilhado ausente: {core}. "
        "Confira o checkout alanstudio-framework e o link framework/core."
    )
os.environ["GAMES_WORKSPACE_ROOT"] = str(workspace)
sys.path.insert(0, str(core / "scripts"))
sys.argv[0] = str(script)
runpy.run_path(str(script), run_name="__main__")
