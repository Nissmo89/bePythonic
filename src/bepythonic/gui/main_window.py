from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Callable

from PyQt6.QtCore import QObject, QThread, QUrl, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QToolBar,
)

from bepythonic.ai.broken_code_agent import generate_broken_code
from bepythonic.gui.demo_html import EDITOR_HTML


class CodeGenerationWorker(QObject):
    """Background worker for Gemini code generation."""

    finished = pyqtSignal(str)
    failed = pyqtSignal(str)
    done = pyqtSignal()

    def __init__(self, topic: str) -> None:
        super().__init__()
        self.topic = topic

    def run(self) -> None:
        try:
            code = generate_broken_code(self.topic)
        except Exception as error:
            self.failed.emit(str(error))
        else:
            self.finished.emit(code)
        finally:
            self.done.emit()


class BePythonicWindow(QMainWindow):
    """Main window with embedded Ace editor and AI code generation."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("bePythonic - AI Code Editor")
        self.resize(1280, 820)

        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)
        self._worker_thread: QThread | None = None
        self._worker: CodeGenerationWorker | None = None
        self._current_file: Path | None = None

        self._build_toolbar()
        self.web_view.loadFinished.connect(self._handle_editor_loaded)
        self.statusBar().showMessage("Loading editor...")
        self.load_editor_page()

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Editor Actions", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        reset_action = QAction("Editor Home", self)
        reset_action.triggered.connect(self.load_editor_page)
        toolbar.addAction(reset_action)

        self.generate_action = QAction("Generate Broken Code", self)
        self.generate_action.triggered.connect(self.generate_broken_code_for_topic)
        toolbar.addAction(self.generate_action)

        syntax_action = QAction("Syntax Check", self)
        syntax_action.triggered.connect(self.syntax_check_editor_code)
        toolbar.addAction(syntax_action)

        open_action = QAction("Open .py", self)
        open_action.triggered.connect(self.open_python_file)
        toolbar.addAction(open_action)

        save_action = QAction("Save .py", self)
        save_action.triggered.connect(self.save_python_file)
        toolbar.addAction(save_action)

        clear_action = QAction("Clear", self)
        clear_action.triggered.connect(self.clear_editor)
        toolbar.addAction(clear_action)

    def _handle_editor_loaded(self, success: bool) -> None:
        if not success:
            self.statusBar().showMessage("Failed to load editor page.", 5000)
            return

        self.statusBar().showMessage("Editor ready.")

    def load_editor_page(self) -> None:
        self.web_view.setHtml(EDITOR_HTML, QUrl("https://bepythonic.local/editor/"))

    def _run_javascript(
        self, script: str, callback: Callable[[object], None] | None = None
    ) -> None:
        page = self.web_view.page()
        if callback is None:
            page.runJavaScript(script)
            return
        page.runJavaScript(script, callback)

    def set_editor_code(self, code: str) -> None:
        script = f"window.setEditorCode({json.dumps(code)});"
        self._run_javascript(script)

    def get_editor_code(self, callback: Callable[[str], None]) -> None:
        script = "window.getEditorCode ? window.getEditorCode() : '';"

        def receive(value: object) -> None:
            callback(value if isinstance(value, str) else "")

        self._run_javascript(script, receive)

    def clear_editor(self) -> None:
        self._run_javascript("window.clearEditor && window.clearEditor();")
        self.statusBar().showMessage("Editor cleared.", 2000)

    def generate_broken_code_for_topic(self) -> None:
        if self._worker_thread is not None:
            self.statusBar().showMessage("Generation already in progress.", 2000)
            return

        topic, ok = QInputDialog.getText(
            self,
            "Generate Broken Python Code",
            "Topic (for example: loops, lists, functions):",
        )
        if not ok:
            return

        topic = topic.strip()
        if not topic:
            QMessageBox.warning(self, "Missing Topic", "Please enter a topic first.")
            return

        self.generate_action.setEnabled(False)
        self.statusBar().showMessage(
            f"Generating broken code for topic: {topic}...", 0
        )

        worker_thread = QThread(self)
        worker = CodeGenerationWorker(topic)
        worker.moveToThread(worker_thread)

        worker_thread.started.connect(worker.run)
        worker.finished.connect(self._handle_code_generation_success)
        worker.failed.connect(self._handle_code_generation_error)
        worker.done.connect(worker.deleteLater)
        worker.done.connect(worker_thread.quit)
        worker.done.connect(self._finish_generation_job)
        worker_thread.finished.connect(worker_thread.deleteLater)

        self._worker_thread = worker_thread
        self._worker = worker
        worker_thread.start()

    def _handle_code_generation_success(self, code: str) -> None:
        self.set_editor_code(code)
        self.statusBar().showMessage(
            "Generated broken code and loaded into editor.",
            4000,
        )

    def _handle_code_generation_error(self, message: str) -> None:
        QMessageBox.critical(
            self,
            "Generation Failed",
            message
            or "Gemini could not return usable code. Check API key/network/model settings.",
        )
        self.statusBar().showMessage("Code generation failed.", 4000)

    def _finish_generation_job(self) -> None:
        self.generate_action.setEnabled(True)
        self._worker = None
        self._worker_thread = None

    def syntax_check_editor_code(self) -> None:
        def check(code: str) -> None:
            try:
                ast.parse(code)
            except SyntaxError as error:
                details = (
                    f"{error.msg}\nLine {error.lineno}, Column {error.offset}"
                    if error.lineno is not None
                    else str(error)
                )
                QMessageBox.warning(self, "Syntax Error", details)
                self.statusBar().showMessage("Syntax error found.", 3500)
                return

            QMessageBox.information(
                self,
                "Syntax Check",
                "No Python syntax errors found.",
            )
            self.statusBar().showMessage("Syntax check passed.", 2500)

        self.get_editor_code(check)

    def open_python_file(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Python File",
            str(self._current_file.parent) if self._current_file else "",
            "Python Files (*.py);;All Files (*)",
        )
        if not file_name:
            return

        try:
            code = Path(file_name).read_text(encoding="utf-8")
        except OSError as error:
            QMessageBox.critical(self, "Open Failed", str(error))
            return

        self._current_file = Path(file_name)
        self.set_editor_code(code)
        self.statusBar().showMessage(f"Loaded: {self._current_file.name}", 3000)

    def save_python_file(self) -> None:
        def save(code: str) -> None:
            initial_path = str(self._current_file) if self._current_file else "exercise.py"
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save Python File",
                initial_path,
                "Python Files (*.py);;All Files (*)",
            )
            if not file_name:
                return

            save_path = Path(file_name)
            try:
                save_path.write_text(code, encoding="utf-8")
            except OSError as error:
                QMessageBox.critical(self, "Save Failed", str(error))
                return

            self._current_file = save_path
            self.statusBar().showMessage(f"Saved: {save_path.name}", 3000)

        self.get_editor_code(save)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        if self._worker_thread is not None and self._worker_thread.isRunning():
            self._worker_thread.quit()
            self._worker_thread.wait(2000)
        super().closeEvent(event)
