from __future__ import annotations

APP_STYLESHEET = """
QMainWindow, QWidget#appRoot {
    background: #f3ede2;
}

QWidget {
    color: #201a15;
    font-family: "Trebuchet MS", "Aptos", "Segoe UI", sans-serif;
    font-size: 13px;
}

QFrame#titleBar {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #3b2716,
        stop: 1 #6d4a2c
    );
    border: 1px solid #8f6946;
    border-radius: 0px;
}

QLabel#windowTitle {
    color: #fff8ee;
    font-size: 15px;
    font-weight: 700;
}

QLabel#windowCaption {
    color: #ead8c1;
    font-size: 11px;
}

QLabel#windowBadge {
    background: rgba(255, 248, 238, 0.15);
    border: 1px solid rgba(255, 248, 238, 0.18);
    border-radius: 999px;
    color: #fff6ea;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
}

QFrame#panel {
    background: #fffaf1;
    border: 1px solid #dccab0;
    border-radius: 18px;
}

QLabel[role="eyebrow"] {
    color: #8d6232;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
}

QLabel[role="headline"] {
    color: #1d1b19;
    font-size: 22px;
    font-weight: 700;
}

QLabel[role="subtle"] {
    color: #6d6255;
}

QLabel[role="pill"] {
    background: #efe2cb;
    border: 1px solid #dcc29c;
    border-radius: 999px;
    color: #6c4c21;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
}

QTabWidget::pane {
    border: 1px solid #dccab0;
    border-radius: 16px;
    background: #fffaf1;
    top: -1px;
}

QTabBar::tab {
    background: #ecdfcb;
    border: 1px solid #dccab0;
    border-bottom: none;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    color: #6e5e4d;
    min-width: 100px;
    padding: 9px 16px;
    margin-right: 6px;
    font-weight: 600;
}

QTabBar::tab:selected {
    background: #fffaf1;
    color: #1d1b19;
}

QTreeWidget,
QListWidget,
QPlainTextEdit,
QTextBrowser,
QLineEdit,
QComboBox {
    background: #fffdf8;
    border: 1px solid #d9ccb9;
    border-radius: 14px;
    padding: 8px 10px;
    selection-background-color: #dcebe7;
    selection-color: #173a39;
}

QTreeWidget::item,
QListWidget::item {
    padding: 6px 4px;
    border-radius: 10px;
}

QTreeWidget::item:selected,
QListWidget::item:selected {
    background: #dcebe7;
    color: #173a39;
}

QPlainTextEdit,
QTextBrowser {
    padding: 12px;
}

QPushButton {
    border-radius: 12px;
    padding: 9px 14px;
    border: 1px solid #d7c7b1;
    background: #f5ebdb;
    color: #2d2620;
    font-weight: 600;
}

QPushButton:hover {
    background: #efdfc8;
}

QPushButton:pressed {
    background: #e7d4bb;
}

QPushButton[variant="accent"] {
    background: #1d716d;
    border: 1px solid #14524f;
    color: #f8fffd;
}

QPushButton[variant="accent"]:hover {
    background: #165e5b;
}

QPushButton[variant="accent"]:pressed {
    background: #124c49;
}

QPushButton[variant="ghost"] {
    background: #fffaf1;
}

QPushButton[variant="windowControl"] {
    background: rgba(255, 248, 238, 0.12);
    border: 1px solid rgba(255, 248, 238, 0.18);
    border-radius: 10px;
    color: #fff8ee;
    font-size: 16px;
    font-weight: 700;
    padding: 0px;
}

QPushButton[variant="windowControl"]:hover {
    background: rgba(255, 248, 238, 0.22);
}

QPushButton[variant="windowControl"]:pressed {
    background: rgba(255, 248, 238, 0.28);
}

QPushButton[variant="windowClose"] {
    background: #8f3b2f;
    border: 1px solid #a34c40;
    border-radius: 10px;
    color: #fff8ee;
    font-size: 18px;
    font-weight: 700;
    padding: 0px;
}

QPushButton[variant="windowClose"]:hover {
    background: #a04336;
}

QPushButton[variant="windowClose"]:pressed {
    background: #7f3329;
}

QStatusBar {
    background: #ede1cf;
    color: #5f5448;
}
"""
