"""Thread-safe helper for reading and writing user preferences and stats."""
from __future__ import annotations

import json
from pathlib import Path
from threading import RLock
from typing import Any, Dict

__all__ = ["UserDataStore"]

_DEFAULT_DATA = {
    "preferences": {
        "story_type": "daily",
        "daily_words": 5,
        "user_level": "intermediate",
        "language": "en",
    },
    "stats": {
        "total_stories": 0,
        "total_words_learned": 0,
        "streak_days": 0,
        "last_activity_date": None,
    },
}


class UserDataStore:
    """Simple JSON-backed persistence layer for lightweight data."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._lock = RLock()
        self._ensure_exists()

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------
    @property
    def file_path(self) -> Path:
        return self._file_path

    def read_all(self) -> Dict[str, Any]:
        with self._lock:
            return json.loads(self._file_path.read_text(encoding="utf-8"))

    def get_preferences(self) -> Dict[str, Any]:
        return self.read_all().get("preferences", {}).copy()

    def update_preferences(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            data = self.read_all()
            data.setdefault("preferences", {}).update(updates)
            self._file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return data["preferences"].copy()

    def get_stats(self) -> Dict[str, Any]:
        return self.read_all().get("stats", {}).copy()

    def update_stats(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            data = self.read_all()
            stats = data.setdefault("stats", {})
            for key, value in updates.items():
                stats[key] = value
            self._file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return stats.copy()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _ensure_exists(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._file_path.write_text(
                json.dumps(_DEFAULT_DATA, ensure_ascii=False, indent=2), encoding="utf-8"
            )
