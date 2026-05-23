#!/usr/bin/env python3
"""Build and run bePythonic with one cross-platform command.

Examples:
  python3 build.py                # build executable bundle then run it
  python3 build.py --run-source   # run directly from source (no PyInstaller)
  python3 build.py --build-only   # build executable only
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_NAME = "bepythonic"
ENTRY_MODULE = "bepythonic.main"
BOOTSTRAP_ENV_FLAG = "BEPYTHONIC_BUILD_BOOTSTRAPPED"


def run_cmd(cmd: list[str], *, cwd: Path = ROOT) -> None:
    print(f"[build.py] $ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd), check=True)


def project_python() -> Path:
    if os.name == "nt":
        return ROOT / ".venv" / "Scripts" / "python.exe"
    return ROOT / ".venv" / "bin" / "python"


def ensure_project_interpreter() -> None:
    target_python = project_python()
    current_python = Path(sys.executable).absolute()

    if target_python.exists():
        if current_python == target_python.absolute():
            return
    else:
        print("[build.py] Creating project virtual environment at .venv ...")
        run_cmd([sys.executable, "-m", "venv", str(ROOT / ".venv")])

    if os.getenv(BOOTSTRAP_ENV_FLAG) == "1":
        return

    if not target_python.exists():
        raise FileNotFoundError(f"Expected project interpreter at: {target_python}")

    print(f"[build.py] Re-launching with project interpreter: {target_python}")
    env = os.environ.copy()
    env[BOOTSTRAP_ENV_FLAG] = "1"
    os.execve(
        str(target_python),
        [str(target_python), str(ROOT / "build.py"), *sys.argv[1:]],
        env,
    )


def ensure_editable_install() -> None:
    run_cmd([sys.executable, "-m", "pip", "install", "-e", "."])


def ensure_pyinstaller() -> None:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("[build.py] PyInstaller not found; installing it now...")
        run_cmd(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "pyinstaller>=6.0",
                "pyinstaller-hooks-contrib",
            ]
        )


def make_launcher_file() -> Path:
    launcher_dir = ROOT / "build"
    launcher_dir.mkdir(parents=True, exist_ok=True)
    launcher = launcher_dir / "_bepythonic_launcher.py"
    launcher.write_text(
        "from bepythonic.main import main\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n",
        encoding="utf-8",
    )
    return launcher


def clean_build_artifacts() -> None:
    for path in (ROOT / "dist", ROOT / "build" / "pyinstaller", ROOT / "build" / "spec"):
        if path.exists():
            shutil.rmtree(path)


def build_executable(*, onefile: bool) -> Path:
    ensure_editable_install()
    ensure_pyinstaller()

    launcher = make_launcher_file()
    dist_dir = ROOT / "dist"
    work_path = ROOT / "build" / "pyinstaller"
    spec_path = ROOT / "build" / "spec"

    pyinstaller_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(work_path),
        "--specpath",
        str(spec_path),
        "--collect-all",
        "PyQt6",
        "--collect-submodules",
        "PyQt6.QtWebEngineWidgets",
        "--collect-submodules",
        "PyQt6.QtWebChannel",
        "--exclude-module",
        "PySide6",
        "--exclude-module",
        "PyQt5",
        "--exclude-module",
        "PySide2",
    ]

    if onefile:
        pyinstaller_cmd.append("--onefile")
    else:
        pyinstaller_cmd.append("--onedir")

    pyinstaller_cmd.append(str(launcher))
    run_cmd(pyinstaller_cmd)

    executable_name = f"{APP_NAME}.exe" if os.name == "nt" else APP_NAME
    if onefile:
        executable_path = dist_dir / executable_name
    else:
        executable_path = dist_dir / APP_NAME / executable_name

    if not executable_path.exists():
        raise FileNotFoundError(
            f"Build finished but executable was not found at: {executable_path}"
        )

    return executable_path


def run_source() -> None:
    ensure_editable_install()
    run_cmd([sys.executable, "-m", ENTRY_MODULE])


def run_executable(executable_path: Path) -> None:
    run_cmd([str(executable_path)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and run bePythonic on Linux/Windows with one command."
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Build executable and exit.",
    )
    parser.add_argument(
        "--run-source",
        action="store_true",
        help="Run from source instead of running packaged executable.",
    )
    parser.add_argument(
        "--onefile",
        action="store_true",
        help="Build a one-file executable (default is one-dir for better QtWebEngine stability).",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove previous dist/build artifacts before build.",
    )
    return parser.parse_args()


def main() -> None:
    ensure_project_interpreter()
    args = parse_args()

    if args.run_source:
        run_source()
        return

    if not args.no_clean:
        clean_build_artifacts()

    executable_path = build_executable(onefile=args.onefile)
    print(f"[build.py] Built executable: {executable_path}")

    if not args.build_only:
        run_executable(executable_path)


if __name__ == "__main__":
    main()
