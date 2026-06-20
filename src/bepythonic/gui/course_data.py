from __future__ import annotations

import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path


def _bundle_root() -> Path | None:
    bundle_path = getattr(sys, "_MEIPASS", None)
    if not bundle_path:
        return None
    return Path(bundle_path)


def project_root() -> Path:
    bundle_root = _bundle_root()
    if bundle_root is not None:
        return bundle_root
    return Path(__file__).resolve().parents[3]


def user_data_root() -> Path:
    if os.name == "nt":
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    data_root = base / "bepythonic"
    data_root.mkdir(parents=True, exist_ok=True)
    return data_root


def progress_file_path() -> Path:
    return user_data_root() / "progress.json"


def _seed_progress_file(target_path: Path) -> None:
    source_path = project_root() / "user_data" / "progress.json"
    if not source_path.is_file():
        return
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, target_path)


@dataclass(slots=True)
class LessonPage:
    page_id: str
    title: str
    page_type: str
    content: str = ""
    prompt_text: str = ""
    code: str = ""
    question: str = ""
    options: list[str] = field(default_factory=list)
    answer: str = ""
    answers: list[str] = field(default_factory=list)
    explanation: str = ""


@dataclass(slots=True)
class LessonSummary:
    lesson_id: str
    title: str
    module_id: str
    module_title: str
    file_path: Path


@dataclass(slots=True)
class CourseLesson:
    lesson_id: str
    title: str
    module_title: str
    estimated_minutes: int
    topics: list[str]
    pages: list[LessonPage]
    file_path: Path


@dataclass(slots=True)
class CourseModule:
    module_id: str
    title: str
    lessons: list[LessonSummary]


@dataclass(slots=True)
class CourseCatalog:
    course_id: str
    title: str
    description: str
    modules: list[CourseModule]
    lessons_by_id: dict[str, LessonSummary]

    @property
    def lesson_count(self) -> int:
        return len(self.lessons_by_id)


@dataclass(slots=True)
class CourseProgress:
    current_lesson: str | None = None
    current_page: int = 0
    completed_lessons: set[str] = field(default_factory=set)


def load_course_catalog(course_id: str = "python_beginner") -> CourseCatalog:
    course_dir = project_root() / "courses" / course_id
    course_path = course_dir / "course.json"
    payload = json.loads(course_path.read_text(encoding="utf-8"))

    modules: list[CourseModule] = []
    lessons_by_id: dict[str, LessonSummary] = {}

    for module_payload in payload.get("root", []):
        if module_payload.get("type") != "module":
            continue

        lessons: list[LessonSummary] = []
        for lesson_payload in module_payload.get("children", []):
            if lesson_payload.get("type") != "lesson":
                continue

            lesson_summary = LessonSummary(
                lesson_id=str(lesson_payload["id"]),
                title=str(lesson_payload["title"]),
                module_id=str(module_payload["id"]),
                module_title=str(module_payload["title"]),
                file_path=course_dir / str(lesson_payload["file"]),
            )
            lessons.append(lesson_summary)
            lessons_by_id[lesson_summary.lesson_id] = lesson_summary

        modules.append(
            CourseModule(
                module_id=str(module_payload["id"]),
                title=str(module_payload["title"]),
                lessons=lessons,
            )
        )

    return CourseCatalog(
        course_id=str(payload["id"]),
        title=str(payload["title"]),
        description=str(payload.get("description", "")),
        modules=modules,
        lessons_by_id=lessons_by_id,
    )


def load_lesson(catalog: CourseCatalog, lesson_id: str) -> CourseLesson:
    summary = catalog.lessons_by_id[lesson_id]
    payload = json.loads(summary.file_path.read_text(encoding="utf-8"))

    pages: list[LessonPage] = []
    for page_payload in payload.get("pages", []):
        pages.append(
            LessonPage(
                page_id=str(page_payload.get("id", "")),
                title=str(page_payload.get("title", "Untitled Page")),
                page_type=str(page_payload.get("type", "theory")),
                content=str(page_payload.get("content", "")),
                prompt_text=str(page_payload.get("text", "")),
                code=str(page_payload.get("code", "")),
                question=str(page_payload.get("question", "")),
                options=[str(option) for option in page_payload.get("options", [])],
                answer=str(page_payload.get("answer", "")),
                answers=[str(answer) for answer in page_payload.get("answers", [])],
                explanation=str(page_payload.get("explanation", "")),
            )
        )

    return CourseLesson(
        lesson_id=str(payload["id"]),
        title=str(payload["title"]),
        module_title=summary.module_title,
        estimated_minutes=int(payload.get("estimated_minutes", 0)),
        topics=[str(topic) for topic in payload.get("topics", [])],
        pages=pages,
        file_path=summary.file_path,
    )


def load_progress(course_id: str) -> CourseProgress:
    path = progress_file_path()
    if not path.exists():
        _seed_progress_file(path)

    if not path.exists():
        return CourseProgress()

    payload = json.loads(path.read_text(encoding="utf-8"))
    course_payload = payload.get(course_id, {})
    completed_lessons = course_payload.get("completed_lessons", [])

    return CourseProgress(
        current_lesson=course_payload.get("current_lesson"),
        current_page=int(course_payload.get("current_page", 0)),
        completed_lessons={str(lesson_id) for lesson_id in completed_lessons},
    )


def save_progress(course_id: str, progress: CourseProgress) -> None:
    path = progress_file_path()
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
    else:
        payload = {}

    payload[course_id] = {
        "current_lesson": progress.current_lesson,
        "current_page": progress.current_page,
        "completed_lessons": sorted(progress.completed_lessons),
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
