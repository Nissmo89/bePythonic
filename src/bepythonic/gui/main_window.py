from __future__ import annotations

import ast
import json
from pathlib import Path

from PyQt6.QtCore import QObject, QThread, QUrl, pyqtSignal, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWidgets import QFileDialog, QMainWindow
from qframelesswindow import FramelessMainWindow, StandardTitleBar
from qframelesswindow.webengine import FramelessWebEngineView

from bepythonic.ai.broken_code_agent import (
    ask_ai_tutor,
    generate_broken_code,
    generate_custom_lesson,
)
from bepythonic.gui.demo_html import EDITOR_HTML


def _ensure_pyqt6_frameless_binding() -> None:
    modules = {
        cls.__module__.split(".", 1)[0]
        for qt_class in (FramelessMainWindow, StandardTitleBar, FramelessWebEngineView)
        for cls in qt_class.__mro__
    }
    if "PySide6" in modules or "PyQt6" not in modules:
        raise RuntimeError(
            "qframelesswindow must come from PyQt6-Frameless-Window. "
            "Uninstall PySideSix-Frameless-Window and reinstall this project."
        )


_ensure_pyqt6_frameless_binding()


class BePythonicTitleBar(StandardTitleBar):
    """Dark title bar matching the embedded studio UI."""

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setFixedHeight(36)
        self.titleLabel.setStyleSheet(
            """
            QLabel {
                background: transparent;
                color: #edf3f8;
                font: 13px 'Geist', 'Segoe UI', sans-serif;
                padding: 0 8px;
            }
            """
        )
        self.setStyleSheet(
            """
            BePythonicTitleBar {
                background: #121214;
                border-bottom: 1px solid #303841;
            }
            """
        )

        normal = "#B0BEC5"
        hover = "#76ABAE"
        pressed = "#F5F5F5"
        transparent = "#00000000"
        hover_bg = "#1876abae"
        pressed_bg = "#2a76abae"
        close_hover_bg = "#ffff5722"
        close_pressed_bg = "#ffe64a19"

        for button in (self.minBtn, self.maxBtn, self.closeBtn):
            button.setFixedSize(44, 36)
            button.setNormalColor(normal)
            button.setHoverColor(hover)
            button.setPressedColor(pressed)
            button.setNormalBackgroundColor(transparent)
            button.setHoverBackgroundColor(hover_bg)
            button.setPressedBackgroundColor(pressed_bg)

        self.closeBtn.setHoverColor("#ffffff")
        self.closeBtn.setPressedColor("#ffffff")
        self.closeBtn.setHoverBackgroundColor(close_hover_bg)
        self.closeBtn.setPressedBackgroundColor(close_pressed_bg)


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


class CodeExecutionWorker(QObject):
    """Background worker for running Python code safely."""

    finished = pyqtSignal(bool, str, str, int)  # ok, stdout, stderr, exit_code
    done = pyqtSignal()

    def __init__(self, code: str) -> None:
        super().__init__()
        self.code = code

    def run(self) -> None:
        import os
        import subprocess
        import sys
        import tempfile

        # Save code to a temp file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as temp_file:  # noqa: E501
            temp_file.write(self.code)
            temp_file_path = temp_file.name

        try:
            # Run code inside current venv python interpreter
            result = subprocess.run(
                [sys.executable, temp_file_path],
                capture_output=True,
                text=True,
                timeout=5.0
            )
            self.finished.emit(result.returncode == 0, result.stdout, result.stderr, result.returncode)  # noqa: E501
        except subprocess.TimeoutExpired:
            self.finished.emit(False, "", "Error: Code execution timed out after 5.0 seconds.", -1)
        except Exception as e:
            self.finished.emit(False, "", f"Error running code: {e!s}", -1)
        finally:
            try:
                os.remove(temp_file_path)
            except OSError:
                pass
            self.done.emit()


class TutorChatWorker(QObject):
    """Background worker for Gemini Tutor chat conversations."""

    finished = pyqtSignal(str)
    failed = pyqtSignal(str)
    done = pyqtSignal()

    def __init__(self, messages_json: str) -> None:
        super().__init__()
        self.messages_json = messages_json

    def run(self) -> None:
        try:
            response = ask_ai_tutor(self.messages_json)
        except Exception as error:
            self.failed.emit(str(error))
        else:
            self.finished.emit(response)
        finally:
            self.done.emit()


class CustomLessonWorker(QObject):
    """Background worker for Gemini custom lesson generation."""

    finished = pyqtSignal(str)
    failed = pyqtSignal(str)
    done = pyqtSignal()

    def __init__(self, topic: str) -> None:
        super().__init__()
        self.topic = topic

    def run(self) -> None:
        try:
            lesson_json = generate_custom_lesson(self.topic)
        except Exception as error:
            self.failed.emit(str(error))
        else:
            self.finished.emit(lesson_json)
        finally:
            self.done.emit()


class WebUiBridge(QObject):
    """QWebChannel bridge used by the embedded web app."""

    bridgeEvent = pyqtSignal(str, str)  # noqa: N815

    def __init__(self, parent_window: QMainWindow) -> None:
        super().__init__()
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
    def generateCustomLesson(self, topic: str) -> None:  # noqa: N802
        if self._worker_thread is not None:
            self._emit(
                "lesson:error",
                {"message": "Generation already in progress. Wait for current request."},
            )
            return

        trimmed_topic = topic.strip()
        if not trimmed_topic:
            self._emit("lesson:error", {"message": "Enter a topic first."})
            return

        worker_thread = QThread(self)
        worker = CustomLessonWorker(trimmed_topic)
        worker.moveToThread(worker_thread)

        worker_thread.started.connect(worker.run)
        worker.finished.connect(self._handle_lesson_success)
        worker.failed.connect(self._handle_lesson_error)
        worker.done.connect(worker.deleteLater)
        worker.done.connect(worker_thread.quit)
        worker.done.connect(self._finish_lesson_job)
        worker_thread.finished.connect(worker_thread.deleteLater)

        self._worker_thread = worker_thread
        self._worker = worker

        self._emit("lesson:loading", {"loading": True, "topic": trimmed_topic})
        worker_thread.start()

    def _handle_lesson_success(self, lesson_json: str) -> None:
        self._emit("lesson:success", {"lesson": lesson_json})

    def _handle_lesson_error(self, message: str) -> None:
        self._emit("lesson:error", {"message": message or "Could not generate lesson."})

    def _finish_lesson_job(self) -> None:
        self._worker = None
        self._worker_thread = None
        self._emit("lesson:loading", {"loading": False})

    @pyqtSlot(str)
    def runCode(self, code: str) -> None:  # noqa: N802
        if self._worker_thread is not None:
            self._emit("run:error", {"message": "A background task is already running."})
            return

        worker_thread = QThread(self)
        worker = CodeExecutionWorker(code)
        worker.moveToThread(worker_thread)

        worker_thread.started.connect(worker.run)
        worker.finished.connect(self._handle_run_success)
        worker.done.connect(worker.deleteLater)
        worker.done.connect(worker_thread.quit)
        worker.done.connect(self._finish_run_job)
        worker_thread.finished.connect(worker_thread.deleteLater)

        self._worker_thread = worker_thread
        self._worker = worker

        self._emit("run:loading", {"loading": True})
        worker_thread.start()

    def _handle_run_success(self, ok: bool, stdout: str, stderr: str, exit_code: int) -> None:
        self._emit("run:result", {
            "ok": ok,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code
        })

    def _finish_run_job(self) -> None:
        self._worker = None
        self._worker_thread = None
        self._emit("run:loading", {"loading": False})

    @pyqtSlot(str)
    def askAiTutor(self, messages_json: str) -> None:  # noqa: N802
        if self._worker_thread is not None:
            self._emit("tutor:error", {"message": "A background task is already running."})
            return

        worker_thread = QThread(self)
        worker = TutorChatWorker(messages_json)
        worker.moveToThread(worker_thread)

        worker_thread.started.connect(worker.run)
        worker.finished.connect(self._handle_tutor_success)
        worker.failed.connect(self._handle_tutor_error)
        worker.done.connect(worker.deleteLater)
        worker.done.connect(worker_thread.quit)
        worker.done.connect(self._finish_tutor_job)
        worker_thread.finished.connect(worker_thread.deleteLater)

        self._worker_thread = worker_thread
        self._worker = worker

        self._emit("tutor:loading", {"loading": True})
        worker_thread.start()

    def _handle_tutor_success(self, response: str) -> None:
        self._emit("tutor:response", {"text": response})

    def _handle_tutor_error(self, message: str) -> None:
        self._emit("tutor:error", {"message": message})

    def _finish_tutor_job(self) -> None:
        self._worker = None
        self._worker_thread = None
        self._emit("tutor:loading", {"loading": False})

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


class BePythonicWindow(FramelessMainWindow):
    """Main window with embedded CodeMirror editor and AI web interface."""

    def __init__(self) -> None:
        super().__init__()
        self.setTitleBar(BePythonicTitleBar(self))
        self.setMenuWidget(self.titleBar)
        self.setWindowTitle("bePythonic - Python Practice Studio")
        self.resize(1360, 860)

        self.web_view = FramelessWebEngineView(self)
        self.setCentralWidget(self.web_view)
        self.titleBar.raise_()

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

    def closeEvent(self, event) -> None:  # noqa: N802  # type: ignore[override]
        self._bridge.shutdown()
        super().closeEvent(event)
