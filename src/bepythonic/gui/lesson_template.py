from __future__ import annotations

from bepythonic.gui.course_data import CourseLesson, LessonPage
from bepythonic.gui.qt_compat import (
    QFont,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

try:
    from qfluentwidgets import BodyLabel, CardWidget, SubtitleLabel
except ImportError as error:
    raise RuntimeError(
        "Fluent UI dependencies are missing. Install them with "
        '`pip install "PyQt6-Fluent-Widgets[full]" -i https://pypi.org/simple/`.'
    ) from error


def _build_mono_font() -> QFont:
    font = QFont("JetBrains Mono", 11)
    font.setStyleHint(QFont.StyleHint.Monospace)
    font.setFixedPitch(True)
    return font


def _page_type_label(page_type: str) -> str:
    return page_type.replace("_", " ").strip().title()


def _body_label(text: str, parent: QWidget | None = None) -> BodyLabel:
    label = BodyLabel(text, parent)
    label.setWordWrap(True)
    return label


def _clear_layout(layout: QVBoxLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        child_layout = item.layout()
        if widget is not None:
            widget.deleteLater()
        elif child_layout is not None:
            _clear_layout(child_layout)  # type: ignore[arg-type]


class LessonTemplateView(QWidget):
    """Reusable JSON-fed lesson template renderer."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(14)

    def set_lesson(self, lesson: CourseLesson) -> None:
        _clear_layout(self._layout)
        for index, page in enumerate(lesson.pages, start=1):
            self._layout.addWidget(self._build_page_card(index, page))
        self._layout.addStretch(1)

    def _build_page_card(self, index: int, page: LessonPage) -> CardWidget:
        card = CardWidget(self)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = SubtitleLabel(f"{index}. {page.title}", card)
        title.setWordWrap(True)
        layout.addWidget(title)

        layout.addWidget(_body_label(f"Type: {_page_type_label(page.page_type)}", card))

        if page.content:
            layout.addWidget(_body_label(page.content, card))

        if page.prompt_text:
            layout.addWidget(_body_label(page.prompt_text, card))

        if page.question:
            layout.addWidget(QLabel("Question", card))
            layout.addWidget(_body_label(page.question, card))

        if page.options:
            layout.addWidget(QLabel("Options", card))
            for option_index, option in enumerate(page.options, start=1):
                layout.addWidget(_body_label(f"{option_index}. {option}", card))

        if page.code.strip():
            layout.addWidget(QLabel("Code", card))
            code_view = QPlainTextEdit(card)
            code_view.setReadOnly(True)
            code_view.setFont(_build_mono_font())
            code_view.setPlainText(page.code)
            code_view.setMinimumHeight(max(140, 28 * (page.code.count("\n") + 2)))
            layout.addWidget(code_view)

        if page.answer:
            layout.addWidget(QLabel("Answer", card))
            layout.addWidget(_body_label(page.answer, card))

        if page.answers:
            layout.addWidget(QLabel("Accepted Answers", card))
            layout.addWidget(_body_label(", ".join(page.answers), card))

        if page.explanation:
            layout.addWidget(QLabel("Explanation", card))
            layout.addWidget(_body_label(page.explanation, card))

        return card
