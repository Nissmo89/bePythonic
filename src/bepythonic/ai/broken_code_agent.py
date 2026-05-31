from __future__ import annotations

import json
import os
import time
from pathlib import Path
from urllib import error, parse, request

GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
GEMINI_MODEL_ENV = "GEMINI_MODEL"
GEMINI_FALLBACK_MODELS_ENV = "GEMINI_FALLBACK_MODELS"
GEMINI_API_VERSION_ENV = "GEMINI_API_VERSION"
GEMINI_DISCOVER_MODELS_ENV = "GEMINI_DISCOVER_MODELS"

DEFAULT_API_VERSION = "v1beta"
DEFAULT_MODEL = "gemini-3.5-flash"
MAX_FALLBACK_MODELS = 8
DEFAULT_FALLBACK_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]

MODELS_LIST_PAGE_SIZE = 200
MAX_MODELS_LIST_PAGES = 5
MAX_RATE_LIMIT_RETRIES = 2
DEFAULT_RETRY_SECONDS = 3.0
MIN_RETRY_SECONDS = 1.0
MAX_RETRY_SECONDS = 12.0

CODE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "language": {"type": "string"},
        "code": {"type": "string"},
    },
    "required": ["language", "code"],
}

LESSON_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "conceptId": {"type": "string"},
        "conceptTitle": {"type": "string"},
        "summary": {"type": "string"},
        "lessons": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "level": {"type": "string"},
                    "minutes": {"type": "integer"},
                    "summary": {"type": "string"},
                    "objectives": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "blocks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "heading": {"type": "string"},
                                "body": {"type": "string"}
                            },
                            "required": ["heading", "body"]
                        }
                    },
                    "starter": {"type": "string"}
                },
                "required": ["id", "title", "level", "minutes", "summary", "objectives", "blocks", "starter"]  # noqa: E501
            }
        }
    },
    "required": ["conceptId", "conceptTitle", "summary", "lessons"]
}
_ENV_LOADED = False


class GeminiStatusError(RuntimeError):
    def __init__(
        self,
        status_code: int,
        message: str,
        retry_after_seconds: float | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.retry_after_seconds = retry_after_seconds


def _strip_env_value(raw_value: str) -> str:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _load_env_file(env_path: Path) -> None:
    try:
        contents = env_path.read_text(encoding="utf-8")
    except OSError:
        return

    for line in contents.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("export "):
            stripped = stripped[7:].strip()

        if "=" not in stripped:
            continue

        key, raw_value = stripped.split("=", 1)
        env_key = key.strip()
        if not env_key or env_key in os.environ:
            continue

        os.environ[env_key] = _strip_env_value(raw_value)


def ensure_env_loaded() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    candidates: list[Path] = []
    explicit_path = os.getenv("BEPYTHONIC_DOTENV_PATH")
    if explicit_path:
        candidates.append(Path(explicit_path).expanduser())

    cwd_env = Path.cwd() / ".env"
    project_env = Path(__file__).resolve().parents[3] / ".env"
    candidates.append(cwd_env)
    if project_env != cwd_env:
        candidates.append(project_env)

    for env_path in candidates:
        if env_path.is_file():
            _load_env_file(env_path)

    _ENV_LOADED = True


def get_api_key() -> str:
    ensure_env_loaded()
    api_key = os.getenv(GEMINI_API_KEY_ENV)

    if not api_key:
        raise RuntimeError(
            f"Missing API key. Set {GEMINI_API_KEY_ENV} before running this script."
        )

    return api_key


def get_api_version() -> str:
    ensure_env_loaded()
    raw_value = os.getenv(GEMINI_API_VERSION_ENV, DEFAULT_API_VERSION).strip().lower()
    return raw_value if raw_value in {"v1", "v1beta"} else DEFAULT_API_VERSION


def should_discover_models() -> bool:
    ensure_env_loaded()
    raw_value = os.getenv(GEMINI_DISCOVER_MODELS_ENV, "1").strip().lower()
    return raw_value not in {"0", "false", "no", "off"}


def get_api_error_message(body_text: str) -> str:
    try:
        data = json.loads(body_text)
    except json.JSONDecodeError:
        return body_text.strip() or "Unknown Gemini API error"

    if not isinstance(data, dict):
        return body_text.strip() or "Unknown Gemini API error"

    error_data = data.get("error")
    if isinstance(error_data, dict):
        message = error_data.get("message")
        if isinstance(message, str) and message.strip():
            return message

    return body_text.strip() or "Unknown Gemini API error"


def parse_retry_after_seconds(retry_after_header: str | None) -> float | None:
    if not retry_after_header:
        return None

    try:
        seconds = float(retry_after_header.strip())
    except ValueError:
        return None

    if seconds < 0:
        return None

    return seconds


def split_model_list(raw_models: str | None) -> list[str]:
    if not raw_models:
        return []

    return [model.strip() for model in raw_models.split(",") if model.strip()]


def unique_models(models: list[str]) -> list[str]:
    unique: list[str] = []

    for model in models:
        if model not in unique:
            unique.append(model)

    return unique


def get_configured_model_settings() -> tuple[str, list[str]]:
    ensure_env_loaded()
    model = os.getenv(GEMINI_MODEL_ENV, DEFAULT_MODEL).strip() or DEFAULT_MODEL
    configured_fallbacks = split_model_list(os.getenv(GEMINI_FALLBACK_MODELS_ENV))
    fallback_models = configured_fallbacks or DEFAULT_FALLBACK_MODELS
    fallback_models = unique_models(fallback_models)
    fallback_models = [fallback for fallback in fallback_models if fallback != model]
    fallback_models = fallback_models[:MAX_FALLBACK_MODELS]

    return model, fallback_models


def build_generate_endpoint(model: str, api_version: str) -> str:
    encoded_model = parse.quote(model, safe="")
    return (
        f"https://generativelanguage.googleapis.com/{api_version}/models/"
        f"{encoded_model}:generateContent"
    )


def build_models_list_endpoint(api_version: str, page_token: str | None = None) -> str:
    query = {"pageSize": str(MODELS_LIST_PAGE_SIZE)}

    if page_token:
        query["pageToken"] = page_token

    return (
        f"https://generativelanguage.googleapis.com/{api_version}/models?"
        f"{parse.urlencode(query)}"
    )


def send_json_request(
    *,
    url: str,
    api_key: str,
    method: str = "GET",
    payload: dict | None = None,
    timeout_seconds: int = 60,
) -> dict:
    data = None
    headers = {"x-goog-api-key": api_key}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    http_request = request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with request.urlopen(http_request, timeout=timeout_seconds) as response:
            raw_response = response.read().decode("utf-8")
    except error.HTTPError as http_error:
        body_text = http_error.read().decode("utf-8", errors="replace")
        retry_after = parse_retry_after_seconds(http_error.headers.get("Retry-After"))
        raise GeminiStatusError(
            status_code=http_error.code,
            message=get_api_error_message(body_text),
            retry_after_seconds=retry_after,
        ) from http_error
    except error.URLError as url_error:
        raise RuntimeError(
            "Could not reach Gemini API. Check your internet connection and try again."
        ) from url_error

    try:
        parsed_response = json.loads(raw_response)
    except json.JSONDecodeError as json_error:
        raise RuntimeError("Gemini API returned invalid JSON.") from json_error

    if not isinstance(parsed_response, dict):
        raise RuntimeError("Gemini API returned an unexpected response shape.")

    return parsed_response


def list_generate_content_models(api_key: str, api_version: str) -> list[str]:
    available_models: list[str] = []
    page_token: str | None = None

    for _ in range(MAX_MODELS_LIST_PAGES):
        response_data = send_json_request(
            url=build_models_list_endpoint(api_version=api_version, page_token=page_token),
            api_key=api_key,
            method="GET",
            timeout_seconds=30,
        )

        models = response_data.get("models")
        if not isinstance(models, list):
            break

        for model_data in models:
            if not isinstance(model_data, dict):
                continue

            methods = model_data.get("supportedGenerationMethods")
            if not isinstance(methods, list) or "generateContent" not in methods:
                continue

            base_model = model_data.get("baseModelId")
            if isinstance(base_model, str) and base_model.strip():
                available_models.append(base_model.strip())

            model_name = model_data.get("name")
            if isinstance(model_name, str) and model_name.startswith("models/"):
                available_models.append(model_name.split("/", 1)[1].strip())

        next_page_token = response_data.get("nextPageToken")
        if not isinstance(next_page_token, str) or not next_page_token.strip():
            break

        page_token = next_page_token

    return unique_models([model for model in available_models if model])


def pick_auto_models(available_models: list[str]) -> list[str]:
    preferred_prefixes = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
    ]

    selected: list[str] = []

    for prefix in preferred_prefixes:
        for model in available_models:
            if model == prefix or model.startswith(prefix + "-"):
                selected.append(model)

    if not selected:
        selected = [model for model in available_models if model.startswith("gemini-")]

    return unique_models(selected)[: MAX_FALLBACK_MODELS + 1]


def get_model_candidates(api_key: str, api_version: str) -> list[str]:
    primary_model, fallback_models = get_configured_model_settings()
    configured_candidates = unique_models([primary_model, *fallback_models])

    if not should_discover_models():
        return configured_candidates

    try:
        available_models = list_generate_content_models(
            api_key=api_key,
            api_version=api_version,
        )
    except GeminiStatusError as error:
        if error.status_code in (401, 403):
            raise RuntimeError(
                "Gemini rejected the API key. Check that GEMINI_API_KEY is set to "
                "a valid Google AI Studio key in this terminal."
            ) from error

        print("Skipping model discovery due to Gemini API error.")
        return configured_candidates
    except RuntimeError:
        print("Skipping model discovery because Gemini API could not be reached.")
        return configured_candidates

    if not available_models:
        return configured_candidates

    available_set = set(available_models)
    filtered_candidates = [
        model for model in configured_candidates if model in available_set
    ]

    if filtered_candidates:
        return filtered_candidates

    discovered_fallbacks = pick_auto_models(available_models)
    return discovered_fallbacks or configured_candidates


def get_generate_payload(user_prompt: str, use_structured_output: bool, response_schema: dict | None = None) -> dict:  # noqa: E501
    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT.strip()}],
        },
        "contents": [{"role": "user", "parts": [{"text": user_prompt.strip()}]}],
        "generationConfig": {
            "maxOutputTokens": 1200,
            "temperature": 0.7,
        },
    }

    if use_structured_output:
        payload["generationConfig"]["responseMimeType"] = "application/json"
        payload["generationConfig"]["responseSchema"] = response_schema or CODE_RESPONSE_SCHEMA

    return payload


def should_retry_without_schema(error_message: str) -> bool:
    normalized = error_message.lower()
    schema_markers = [
        "response schema",
        "responseschema",
        "response_schema",
        "responsejsonschema",
        "response mime",
        "responsemimetype",
        "response_mime_type",
    ]
    return any(marker in normalized for marker in schema_markers)


def sleep_for_rate_limit(retry_after_seconds: float | None) -> None:
    delay_seconds = retry_after_seconds or DEFAULT_RETRY_SECONDS
    delay_seconds = max(MIN_RETRY_SECONDS, min(MAX_RETRY_SECONDS, delay_seconds))
    time.sleep(delay_seconds)


def generate_content(model: str, user_prompt: str, api_key: str, api_version: str, response_schema: dict | None = None) -> dict:  # noqa: E501
    use_structured_output = True
    rate_limit_retries = 0

    while True:
        payload = get_generate_payload(
            user_prompt=user_prompt,
            use_structured_output=use_structured_output,
            response_schema=response_schema
        )

        try:
            return send_json_request(
                url=build_generate_endpoint(model=model, api_version=api_version),
                api_key=api_key,
                method="POST",
                payload=payload,
                timeout_seconds=60,
            )
        except GeminiStatusError as error:
            if error.status_code == 429 and rate_limit_retries < MAX_RATE_LIMIT_RETRIES:
                rate_limit_retries += 1
                sleep_for_rate_limit(error.retry_after_seconds)
                continue

            if (
                use_structured_output
                and error.status_code == 400
                and should_retry_without_schema(str(error))
            ):
                use_structured_output = False
                continue

            raise


def get_response_text(response_data: dict) -> str:
    candidates = response_data.get("candidates")

    if not isinstance(candidates, list) or not candidates:
        return ""

    first_candidate = candidates[0]
    if not isinstance(first_candidate, dict):
        return ""

    content = first_candidate.get("content")
    if not isinstance(content, dict):
        return ""

    parts = content.get("parts")
    if not isinstance(parts, list):
        return ""

    text_parts: list[str] = []

    for part in parts:
        if not isinstance(part, dict):
            continue

        text = part.get("text")
        if isinstance(text, str) and text.strip():
            text_parts.append(text)

    return "\n".join(text_parts).strip()


def get_prompt_block_reason(response_data: dict) -> str | None:
    prompt_feedback = response_data.get("promptFeedback")
    if not isinstance(prompt_feedback, dict):
        return None

    block_reason = prompt_feedback.get("blockReason")
    if isinstance(block_reason, str) and block_reason.strip():
        return block_reason.strip()

    return None


def extract_json_text(text: str) -> str:
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or start > end:
        return text

    return text[start : end + 1]


def strip_markdown_code_fence(text: str) -> str:
    stripped = text.strip()

    if not stripped.startswith("```"):
        return text

    lines = stripped.splitlines()
    if len(lines) < 3 or lines[-1].strip() != "```":
        return text

    return "\n".join(lines[1:-1]).strip()


def looks_like_python_code(text: str) -> bool:
    line_count = len([line for line in text.splitlines() if line.strip()])
    if line_count < 8:
        return False

    hints = [
        "def ",
        "class ",
        "import ",
        "from ",
        "for ",
        "while ",
        "if ",
        "print(",
        "return ",
    ]
    return any(hint in text for hint in hints)


def parse_code_response(ai_reply: str) -> str:
    candidates = [ai_reply, strip_markdown_code_fence(ai_reply)]

    for candidate in candidates:
        try:
            data = json.loads(extract_json_text(candidate))
        except json.JSONDecodeError:
            continue

        if not isinstance(data, dict):
            continue

        code = data.get("code")
        if isinstance(code, str) and code.strip():
            return code

    cleaned_reply = strip_markdown_code_fence(ai_reply)

    if looks_like_python_code(cleaned_reply):
        return cleaned_reply

    raise ValueError("invalid JSON")


SYSTEM_PROMPT = """
You are a backend code generator for a Python coding practice app.

Return ONLY valid JSON.
No markdown.
No explanation.
No text before or after JSON.

JSON schema:
{
  "language": "python",
  "code": "string"
}

Rules for "code":
- It must contain exactly ONE broken Python program.
- Do not include multiple snippets.
- Do not include markdown fences.
- Do not include explanations or hints.
- Program length: 20 to 80 lines.
- Bugs: 3 to 7 intentional beginner-level bugs.
- The code should be suitable to paste directly into a code editor.
- Do not include the solution.

Return only JSON.
"""


def generate_broken_code(topic: str) -> str:
    user_prompt = f"""
Generate one broken Python exercise.

Topic: {topic}
Difficulty: beginner
"""

    api_key = get_api_key()
    api_version = get_api_version()
    last_error = None

    for model in get_model_candidates(api_key=api_key, api_version=api_version):
        try:
            response = generate_content(
                model=model,
                user_prompt=user_prompt,
                api_key=api_key,
                api_version=api_version,
            )
        except GeminiStatusError as error:
            if error.status_code in (401, 403):
                raise RuntimeError(
                    "Gemini rejected the API key. Check that GEMINI_API_KEY is set to "
                    "a valid Google AI Studio key in this terminal."
                ) from error

            if error.status_code == 429:
                last_error = f"{model}: Gemini API rate limit exceeded (429)."
                print(f"Skipping {model}: Gemini API rate limit exceeded (429).")
                continue

            last_error = f"{model}: Gemini API error {error.status_code}: {error}"
            print(f"Skipping {model}: Gemini API error {error.status_code}.")
            continue

        used_model = model
        ai_reply = get_response_text(response)

        if not ai_reply:
            block_reason = get_prompt_block_reason(response)
            if block_reason:
                last_error = f"{used_model}: prompt blocked ({block_reason})"
                print(f"Skipping {used_model}: prompt blocked ({block_reason}).")
            else:
                last_error = f"{used_model}: empty response content"
                print(f"Skipping {used_model}: empty response content.")
            continue

        try:
            code = parse_code_response(ai_reply)
        except ValueError as parse_error:
            last_error = f"{used_model}: {parse_error}"
            print(f"Skipping {used_model}: {parse_error}.")
            continue

        print(f"\nUsed model: {used_model}")
        return code

    raise RuntimeError(
        "No fallback model returned usable code. "
        f"Last issue: {last_error}"
    )


LESSON_SYSTEM_PROMPT = """
You are a curriculum designer for a Python coding practice app.
Return ONLY valid JSON matching the provided schema.
No markdown. No explanation. No text before or after JSON.
Generate an engaging, practical lesson for the given topic.
"""

def generate_custom_lesson(topic: str) -> str:
    user_prompt = f"Generate a comprehensive python learning concept and lesson JSON for the topic: {topic}"  # noqa: E501

    api_key = get_api_key()
    api_version = get_api_version()
    last_error = None

    # Temporarily override SYSTEM_PROMPT
    global SYSTEM_PROMPT
    old_system_prompt = SYSTEM_PROMPT
    SYSTEM_PROMPT = LESSON_SYSTEM_PROMPT

    try:
        for model in get_model_candidates(api_key=api_key, api_version=api_version):
            try:
                response = generate_content(
                    model=model,
                    user_prompt=user_prompt,
                    api_key=api_key,
                    api_version=api_version,
                    response_schema=LESSON_RESPONSE_SCHEMA
                )
            except GeminiStatusError as error:
                if error.status_code in (401, 403):
                    raise RuntimeError("Gemini rejected the API key.") from error
                if error.status_code == 429:
                    last_error = f"{model}: Rate limit exceeded (429)."
                    continue
                last_error = f"{model}: API error {error.status_code}."
                continue

            used_model = model
            ai_reply = get_response_text(response)

            if not ai_reply:
                continue

            try:
                # Validate JSON format
                parsed = json.loads(extract_json_text(ai_reply))
                return json.dumps(parsed)
            except json.JSONDecodeError as parse_error:
                last_error = f"{used_model}: {parse_error}"
                continue

        raise RuntimeError(f"No fallback model returned a usable lesson. Last issue: {last_error}")
    finally:
        SYSTEM_PROMPT = old_system_prompt


TUTOR_SYSTEM_PROMPT = """
You are a senior-level Python tutor and reviewer in the 'bePythonic' learning app.
Your goals:
- Explain Python concepts, syntax errors, and logic bugs in simple, clear, friendly language.
- Guide the user step-by-step. If they ask for a hint, provide a subtle clue that
  triggers critical thinking rather than giving the solution.
- Keep explanations elegant and concise.
- Format your response in clean markdown with Python code blocks where appropriate.
"""


def ask_ai_tutor(messages_json: str) -> str:
    """Send a multi-turn chat log to Gemini and return the tutor's response in markdown."""
    try:
        messages = json.loads(messages_json)
    except Exception as err:
        raise ValueError(f"Invalid messages JSON format: {err}") from err

    # Build Gemini-compliant content list
    gemini_contents = []
    for msg in messages:
        role = "user" if msg.get("role") == "user" else "model"
        text = msg.get("text", "")
        gemini_contents.append({
            "role": role,
            "parts": [{"text": text}]
        })

    payload = {
        "systemInstruction": {
            "parts": [{"text": TUTOR_SYSTEM_PROMPT.strip()}],
        },
        "contents": gemini_contents,
        "generationConfig": {
            "maxOutputTokens": 1200,
            "temperature": 0.7,
        },
    }

    api_key = get_api_key()
    api_version = get_api_version()
    last_error = None

    for model in get_model_candidates(api_key=api_key, api_version=api_version):
        try:
            response = send_json_request(
                url=build_generate_endpoint(model=model, api_version=api_version),
                api_key=api_key,
                method="POST",
                payload=payload,
                timeout_seconds=60,
            )
        except GeminiStatusError as error:
            if error.status_code in (401, 403):
                raise RuntimeError(
                    "Gemini rejected the API key. Check that GEMINI_API_KEY is set to "
                    "a valid Google AI Studio key in this terminal."
                ) from error

            if error.status_code == 429:
                last_error = f"{model}: Gemini API rate limit exceeded (429)."
                print(f"Skipping {model}: Gemini API rate limit exceeded (429).")
                continue

            last_error = f"{model}: Gemini API error {error.status_code}: {error}"
            print(f"Skipping {model}: Gemini API error {error.status_code}.")
            continue

        ai_reply = get_response_text(response)
        if ai_reply:
            print(f"\nAI Tutor used model: {model}")
            return ai_reply

        block_reason = get_prompt_block_reason(response)
        if block_reason:
            last_error = f"{model}: prompt blocked ({block_reason})"
            print(f"Skipping {model}: prompt blocked ({block_reason}).")
        else:
            last_error = f"{model}: empty response content"
            print(f"Skipping {model}: empty response content.")
        continue

    raise RuntimeError(
        "No fallback model returned usable code. "
        f"Last issue: {last_error}"
    )


def main() -> None:
    while True:
        topic = input("\nEnter topic, or 'exit': ").strip()

        if topic.lower() in ["exit", "quit"]:
            break

        try:
            code = generate_broken_code(topic)
        except RuntimeError as error:
            print(error)
            break

        if code:
            print("\n--- CODE FOR EDITOR ---\n")
            print(code)


if __name__ == "__main__":
    main()
