from __future__ import annotations

import ast
import json
from pathlib import Path

from PyQt6.QtCore import QObject, QThread, QUrl, pyqtSignal, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QFileDialog, QMainWindow

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


class WebUiBridge(QObject):
    """QWebChannel bridge used by the embedded web app."""

    bridgeEvent = pyqtSignal(str, str)

    def __init__(self, parent_window: QMainWindow) -> None:
        super().__init__(parent_window)
        self._window = parent_window
        self._worker_thread: QThread | None = None
        self._worker: CodeGenerationWorker | None = None
        self._current_file: Path | None = None

    def _emit(self, event_name: str, payload: dict[str, object] | None = None) -> None:
        body = payload if payload is not None else {}
        self.bridgeEvent.emit(event_name, json.dumps(body))

    @pyqtSlot()
    def ready(self) -> None:
        self._emit("bridge:ready", {"ok": True})

    @pyqtSlot(str)
    def generateBrokenCode(self, topic: str) -> None:  # noqa: N802
        if self._worker_thread is not None:
            self._emit(
                "ai:error",
                {"message": "Generation already in progress. Wait for current request."},
            )
            return

        trimmed_topic = topic.strip()
        if not trimmed_topic:
            self._emit("ai:error", {"message": "Enter a topic first."})
            return

        worker_thread = QThread(self)
        worker = CodeGenerationWorker(trimmed_topic)
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

        self._emit("ai:loading", {"loading": True, "topic": trimmed_topic})
        worker_thread.start()

    def _handle_code_generation_success(self, code: str) -> None:
        self._emit("editor:setCode", {"code": code})
        self._emit(
            "ai:message",
            {
                "kind": "success",
                "message": "Generated a broken Python exercise and loaded it into editor.",
            },
        )

    def _handle_code_generation_error(self, message: str) -> None:
        self._emit(
            "ai:error",
            {
                "message": message
                or "Gemini could not return usable code. Check API key/network/model settings.",
            },
        )

    def _finish_generation_job(self) -> None:
        self._worker = None
        self._worker_thread = None
        self._emit("ai:loading", {"loading": False})

    @pyqtSlot(str)
    def syntaxCheck(self, code: str) -> None:  # noqa: N802
        try:
            ast.parse(code)
        except SyntaxError as error:
            details = (
                f"{error.msg} (line {error.lineno}, column {error.offset})"
                if error.lineno is not None
                else str(error)
            )
            self._emit(
                "syntax:result",
                {
                    "ok": False,
                    "message": details,
                },
            )
            return

        self._emit(
            "syntax:result",
            {
                "ok": True,
                "message": "No Python syntax errors found.",
            },
        )

    @pyqtSlot()
    def openPythonFile(self) -> None:  # noqa: N802
        file_name, _ = QFileDialog.getOpenFileName(
            self._window,
            "Open Python File",
            str(self._current_file.parent) if self._current_file else "",
            "Python Files (*.py);;All Files (*)",
        )
        if not file_name:
            self._emit("file:canceled", {"action": "open"})
            return

        try:
            code = Path(file_name).read_text(encoding="utf-8")
        except OSError as error:
            self._emit(
                "file:error",
                {
                    "action": "open",
                    "message": str(error),
                },
            )
            return

        self._current_file = Path(file_name)
        self._emit(
            "file:opened",
            {
                "name": self._current_file.name,
                "code": code,
            },
        )

    @pyqtSlot(str)
    def savePythonFile(self, code: str) -> None:  # noqa: N802
        initial_path = str(self._current_file) if self._current_file else "exercise.py"
        file_name, _ = QFileDialog.getSaveFileName(
            self._window,
            "Save Python File",
            initial_path,
            "Python Files (*.py);;All Files (*)",
        )
        if not file_name:
            self._emit("file:canceled", {"action": "save"})
            return

        save_path = Path(file_name)
        try:
            save_path.write_text(code, encoding="utf-8")
        except OSError as error:
            self._emit(
                "file:error",
                {
                    "action": "save",
                    "message": str(error),
                },
            )
            return

        self._current_file = save_path
        self._emit("file:saved", {"name": save_path.name})

    def shutdown(self) -> None:
        if self._worker_thread is not None and self._worker_thread.isRunning():
            self._worker_thread.quit()
            self._worker_thread.wait(2000)


class BePythonicWindow(QMainWindow):
    """Main window with embedded CodeMirror editor and AI web interface."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("bePythonic - Kinetic Studio")
        self.resize(1360, 860)

        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)
        self.statusBar().hide()

        self._bridge = WebUiBridge(self)
        self._web_channel = QWebChannel(self.web_view.page())
        self._web_channel.registerObject("backend", self._bridge)
        self.web_view.page().setWebChannel(self._web_channel)

        self.web_view.loadFinished.connect(self._handle_editor_loaded)
        self.load_editor_page()

    def _handle_editor_loaded(self, success: bool) -> None:
        if not success:
            print("Failed to load studio page in QWebEngineView.")

    def load_editor_page(self) -> None:
        self.web_view.setHtml(EDITOR_HTML, QUrl("https://bepythonic.local/studio/"))

    def closeEvent(self, event) -> None:  # type: ignore[override]
        self._bridge.shutdown()
        super().closeEvent(event)
