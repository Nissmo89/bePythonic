from __future__ import annotations

import json
import os

OPENROUTER_API_KEY_ENV = "OPENROUTER_API_KEY"
OPENROUTER_MODEL_ENV = "OPENROUTER_MODEL"
OPENROUTER_FALLBACK_MODELS_ENV = "OPENROUTER_FALLBACK_MODELS"

DEFAULT_MODEL = "qwen/qwen3-next-80b-a3b-instruct:free"
MAX_FALLBACK_MODELS = 6
DEFAULT_FALLBACK_MODELS = [
    "deepseek/deepseek-v4-flash:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "openrouter/free",
]


def get_client():
    api_key = os.getenv(OPENROUTER_API_KEY_ENV)

    if not api_key:
        raise RuntimeError(
            f"Missing API key. Set {OPENROUTER_API_KEY_ENV} before running this script."
        )

    try:
        from openai import OpenAI
    except ImportError as error:
        raise RuntimeError(
            "Missing dependency. Install it with: python3 -m pip install openai"
        ) from error

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "My Local App",
        },
    )


def get_api_error_message(error):
    try:
        body = error.response.json()
        return body.get("error", {}).get("message") or str(body)
    except Exception:
        return str(error)


def split_model_list(raw_models):
    if not raw_models:
        return []

    return [model.strip() for model in raw_models.split(",") if model.strip()]


def unique_models(models):
    unique = []

    for model in models:
        if model not in unique:
            unique.append(model)

    return unique


def get_model_settings():
    model = os.getenv(OPENROUTER_MODEL_ENV, DEFAULT_MODEL).strip() or DEFAULT_MODEL
    configured_fallbacks = split_model_list(
        os.getenv(OPENROUTER_FALLBACK_MODELS_ENV)
    )
    fallback_models = configured_fallbacks or DEFAULT_FALLBACK_MODELS
    fallback_models = unique_models(fallback_models)
    fallback_models = [fallback for fallback in fallback_models if fallback != model]
    fallback_models = fallback_models[:MAX_FALLBACK_MODELS]

    return model, fallback_models


def get_model_candidates():
    model, fallback_models = get_model_settings()
    return unique_models([model] + fallback_models)


def get_response_text(response):
    choices = getattr(response, "choices", None)

    if not choices:
        return ""

    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", None)

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
            else:
                text = getattr(item, "text", None)

            if text:
                parts.append(text)

        return "\n".join(parts).strip()

    return ""


def extract_json_text(text):
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


def parse_code_response(ai_reply):
    try:
        data = json.loads(extract_json_text(ai_reply))
    except json.JSONDecodeError as error:
        raise ValueError("invalid JSON") from error

    if not isinstance(data, dict):
        raise ValueError("JSON must be an object")

    code = data.get("code")

    if not isinstance(code, str) or not code.strip():
        raise ValueError("missing code field")

    return code


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


def generate_broken_code(topic):
    user_prompt = f"""
Generate one broken Python exercise.

Topic: {topic}
Difficulty: beginner
"""

    try:
        from openai import APIConnectionError, APIStatusError, APITimeoutError
    except ImportError as error:
        raise RuntimeError(
            "Missing dependency. Install it with: python3 -m pip install openai"
        ) from error

    client = get_client()
    last_error = None

    for model in get_model_candidates():
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=1200,
                temperature=0.7,
            )
        except APIStatusError as error:
            message = get_api_error_message(error)

            if error.status_code == 401:
                raise RuntimeError(
                    "OpenRouter rejected the API key. Check that OPENROUTER_API_KEY "
                    "is set to your newest key in this terminal."
                ) from error

            last_error = f"{model}: OpenRouter API error {error.status_code}: {message}"
            print(f"Skipping {model}: OpenRouter API error {error.status_code}.")
            continue
        except (APIConnectionError, APITimeoutError) as error:
            raise RuntimeError(
                "Could not reach OpenRouter. Check your internet connection and try again."
            ) from error

        used_model = getattr(response, "model", model)
        ai_reply = get_response_text(response)

        if not ai_reply:
            last_error = f"{used_model}: empty response content"
            print(f"Skipping {used_model}: empty response content.")
            continue

        try:
            code = parse_code_response(ai_reply)
        except ValueError as error:
            last_error = f"{used_model}: {error}"
            print(f"Skipping {used_model}: {error}.")
            continue

        print(f"\nUsed model: {used_model}")
        return code

    raise RuntimeError(
        f"No fallback model returned usable code. Last issue: {last_error}"
    )


def main():
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

