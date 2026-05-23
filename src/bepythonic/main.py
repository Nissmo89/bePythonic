from __future__ import annotations

import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from bepythonic.gui.main_window import BePythonicWindow


def _merged_chromium_flags(existing: str) -> str:
    required_flags = [
        "--disable-gpu",
        "--disable-gpu-compositing",
        "--use-angle=swiftshader",
    ]
    merged = existing.strip().split()
    for flag in required_flags:
        if flag not in merged:
            merged.append(flag)
    return " ".join(merged).strip()


def _configure_windows_rendering() -> None:
    # Some Windows setups (especially packaged apps) show a black QWebEngine surface
    # when GPU acceleration/drivers are incompatible with Qt WebEngine.
    if not sys.platform.startswith("win"):
        return

    if os.getenv("BEPYTHONIC_WINDOWS_SAFE_RENDER", "1").strip().lower() in {
        "0",
        "false",
        "no",
        "off",
    }:
        return

    os.environ.setdefault("QT_OPENGL", "software")
    os.environ.setdefault("QSG_RHI_BACKEND", "software")
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = _merged_chromium_flags(
        os.getenv("QTWEBENGINE_CHROMIUM_FLAGS", "")
    )

    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, True)


def main() -> None:
    """GUI entrypoint."""
    _configure_windows_rendering()
    app = QApplication(sys.argv)
    app.setApplicationName("bePythonic")

    window = BePythonicWindow()
    window.show()

    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
