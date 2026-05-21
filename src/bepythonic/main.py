from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from bepythonic.gui.main_window import BePythonicWindow


def main() -> None:
    """GUI entrypoint."""
    app = QApplication(sys.argv)
    app.setApplicationName("bePythonic")

    window = BePythonicWindow()
    window.show()

    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
