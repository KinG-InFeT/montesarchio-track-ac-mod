#!/usr/bin/env python3
"""Cross-platform CLI build for Pista Caudina mod.

Runs the same 3-step pipeline as the Manager GUI Build tab:
  1. Export KN5 from Blender
  2. Setup mod folder structure
  3. Generate AI line from Blender

Usage:
    python build_cli.py
"""

import os
import shutil
import subprocess
import sys

# Ensure scripts/ is on the path for platform_utils
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
import platform_utils


def main():
    blend_file = os.path.join(ROOT_DIR, "pista_caudina.blend")
    if not os.path.isfile(blend_file):
        print("Error: pista_caudina.blend not found.")
        sys.exit(1)

    blender = platform_utils.find_blender()
    venv_py = platform_utils.venv_python()

    # Verify venv exists
    if not os.path.isfile(venv_py):
        print(f"Error: venv Python not found at {venv_py}")
        print("Create it first:")
        if platform_utils.IS_WINDOWS:
            print("  python -m venv .venv")
            print("  .venv\\Scripts\\pip install -r requirements.txt")
        else:
            print("  python3 -m venv .venv")
            print("  .venv/bin/pip install -r requirements.txt")
        sys.exit(1)

    steps = [
        ("1/3 - Export KN5", [
            blender, "--background", blend_file,
            "--python", os.path.join(ROOT_DIR, "scripts", "export_kn5.py"),
        ]),
        ("2/3 - Mod folder", [
            venv_py, os.path.join(ROOT_DIR, "scripts", "setup_mod_folder.py"),
        ]),
        ("3/3 - AI line", [
            blender, "--background", blend_file,
            "--python", os.path.join(ROOT_DIR, "scripts", "generate_ai_line.py"),
        ]),
    ]

    print("=== Pista Caudina - Build mod ===")
    print()

    for label, cmd in steps:
        print(f"[{label}] Running...")
        result = subprocess.run(cmd, cwd=ROOT_DIR)
        if result.returncode != 0:
            print(f"[{label}] FAILED (exit code {result.returncode})")
            sys.exit(1)
        print(f"[{label}] Done.")
        print()

    # Copy KN5 to mod folder
    src_kn5 = os.path.join(ROOT_DIR, "pista_caudina.kn5")
    dst_kn5 = os.path.join(ROOT_DIR, "mod", "pista_caudina", "pista_caudina.kn5")
    if os.path.isfile(src_kn5):
        os.makedirs(os.path.dirname(dst_kn5), exist_ok=True)
        shutil.copy2(src_kn5, dst_kn5)
        print("KN5 copied to mod/pista_caudina/")

    print()
    print("=== Build completed! ===")


if __name__ == "__main__":
    main()
