"""Flask API powering the language study application."""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError

try:  # pragma: no cover - runtime import guard
    from .story_generator import StoryGenerator, StoryRequest
    from .user_data import UserDataStore
    from .vocabulary_manager import VocabularyManager
except ImportError:  # Support running the module as a script
    import sys

    BACKEND_DIR = Path(__file__).resolve().parent
    if str(BACKEND_DIR) not in sys.path:
        sys.path.insert(0, str(BACKEND_DIR))
    from story_generator import StoryGenerator, StoryRequest  # type: ignore
    from user_data import UserDataStore  # type: ignore
    from vocabulary_manager import VocabularyManager  # type: ignore

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
CONFIG_DIR = ROOT_DIR / "config"

VOCAB_FILE = DATA_DIR / "vocabulary.json"
USER_DATA_FILE = DATA_DIR / "user_data.json"
TEMPLATE_FILE = CONFIG_DIR / "story_templates.json"

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.INFO)

vocabulary_manager = VocabularyManager(VOCAB_FILE)
user_store = UserDataStore(USER_DATA_FILE)
story_generator = StoryGenerator(TEMPLATE_FILE)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def success(payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return {"success": True, "data": payload or {}}


def failure(message: str, *, status_code: int = 400) -> Any:
    response = jsonify({"success": False, "error": message})
    response.status_code = status_code
    return response


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/api/health", methods=["GET"])
def health_check():
    data = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "available_languages": vocabulary_manager.languages,
    }
    return jsonify(success(data))


@app.route("/api/vocabulary/daily", methods=["GET"])
def vocabulary_daily():
    try:
        count = int(request.args.get("count", 5))
    except ValueError:
        return failure("count must be an integer", status_code=400)

    language = request.args.get("language")
    level = request.args.get("level")

    words = vocabulary_manager.get_daily_words(count, language=language, level=level)
    return jsonify(success({"items": words, "count": len(words)}))


@app.route("/api/vocabulary/search", methods=["GET"])
def vocabulary_search():
    keyword = request.args.get("q", "")
    language = request.args.get("language")
    results = vocabulary_manager.search(keyword, language=language)
    return jsonify(success({"items": results, "count": len(results)}))


@app.route("/api/user/preferences", methods=["GET", "PUT"])
def user_preferences():
    if request.method == "GET":
        return jsonify(success(user_store.get_preferences()))

    updates = request.get_json(silent=True) or {}
    if not isinstance(updates, dict):
        return failure("Invalid payload. Expected JSON object.")
    updated = user_store.update_preferences(updates)
    return jsonify(success(updated))


@app.route("/api/learning/stats", methods=["GET"])
def learning_stats():
    return jsonify(success(user_store.get_stats()))


@app.route("/api/learning/progress", methods=["POST"])
def update_learning_progress():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return failure("Invalid payload. Expected JSON object.")

    stats = user_store.get_stats()
    for key in ("total_stories", "total_words_learned"):
        if key in payload:
            try:
                stats[key] = max(0, int(payload[key]))
            except (ValueError, TypeError):
                return failure(f"{key} must be an integer")

    if "streak_days" in payload:
        try:
            stats["streak_days"] = max(0, int(payload["streak_days"]))
        except (ValueError, TypeError):
            return failure("streak_days must be an integer")

    stats["last_activity_date"] = datetime.utcnow().date().isoformat()
    updated = user_store.update_stats(stats)
    return jsonify(success(updated))


@app.route("/api/story/generate", methods=["POST"])
def story_generate():
    payload = request.get_json(silent=True) or {}
    try:
        request_model = StoryRequest(**payload)
    except ValidationError as exc:
        return failure(exc.errors()[0]["msg"] if exc.errors() else "Invalid request payload")

    story = story_generator.generate(request_model)
    data = story.to_dict()
    user_store.update_stats(
        {
            "total_stories": user_store.get_stats().get("total_stories", 0) + 1,
            "last_activity_date": datetime.utcnow().date().isoformat(),
        }
    )
    return jsonify(success(data))


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------


@app.errorhandler(404)
def not_found(_: Exception):
    return failure("Endpoint not found", status_code=404)


@app.errorhandler(500)
def server_error(error: Exception):
    app.logger.exception("Unhandled error: %s", error)
    return failure("Internal server error", status_code=500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
