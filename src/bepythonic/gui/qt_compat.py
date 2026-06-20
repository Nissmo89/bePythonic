from __future__ import annotations

try:
    from PyQt6.QtCore import (
        QEvent,
        QObject,
        QPoint,
        Qt,
        QThread,
    )
    from PyQt6.QtCore import (
        pyqtSignal as Signal,
    )
    from PyQt6.QtCore import (
        pyqtSlot as Slot,
    )
    from PyQt6.QtGui import QAction, QCloseEvent, QFont, QTextCursor
    from PyQt6.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QComboBox,
        QFileDialog,
        QFrame,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QListWidget,
        QListWidgetItem,
        QMainWindow,
        QMessageBox,
        QPlainTextEdit,
        QPushButton,
        QScrollArea,
        QSplitter,
        QStackedWidget,
        QStatusBar,
        QTabWidget,
        QTextBrowser,
        QTreeWidget,
        QTreeWidgetItem,
        QVBoxLayout,
        QWidget,
    )

    QT_API = "PyQt6"
except ImportError:
    try:
        from PySide6.QtCore import QEvent, QObject, QPoint, Qt, QThread, Signal, Slot
        from PySide6.QtGui import QAction, QCloseEvent, QFont, QTextCursor
        from PySide6.QtWidgets import (
            QAbstractItemView,
            QApplication,
            QComboBox,
            QFileDialog,
            QFrame,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QListWidget,
            QListWidgetItem,
            QMainWindow,
            QMessageBox,
            QPlainTextEdit,
            QPushButton,
            QScrollArea,
            QSplitter,
            QStackedWidget,
            QStatusBar,
            QTabWidget,
            QTextBrowser,
            QTreeWidget,
            QTreeWidgetItem,
            QVBoxLayout,
            QWidget,
        )

        QT_API = "PySide6"
    except ImportError as error:
        raise RuntimeError(
            "No Qt binding found. Install either `pip install -e .[desktop-pyqt6]` "
            "or `pip install -e .[desktop-pyside6]`."
        ) from error


__all__ = [
    "QT_API",
    "QAbstractItemView",
    "QAction",
    "QApplication",
    "QCloseEvent",
    "QComboBox",
    "QEvent",
    "QFileDialog",
    "QFont",
    "QFrame",
    "QHBoxLayout",
    "QLabel",
    "QLineEdit",
    "QListWidget",
    "QListWidgetItem",
    "QMainWindow",
    "QMessageBox",
    "QObject",
    "QPlainTextEdit",
    "QPoint",
    "QPushButton",
    "QScrollArea",
    "QSplitter",
    "QStackedWidget",
    "QStatusBar",
    "QTabWidget",
    "QTextBrowser",
    "QTextCursor",
    "QThread",
    "QTreeWidget",
    "QTreeWidgetItem",
    "QVBoxLayout",
    "QWidget",
    "Qt",
    "Signal",
    "Slot",
]
