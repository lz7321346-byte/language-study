"""Utilities for working with the vocabulary dataset used by the API."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from threading import RLock
from typing import Any, Dict, Iterable, List, Sequence

__all__ = [
    "VocabularyEntry",
    "VocabularyManager",
]


@dataclass(frozen=True)
class VocabularyEntry:
    """A single vocabulary item with metadata used by the application."""

    word: str
    meaning: str
    language: str = "en"
    part_of_speech: str | None = None
    example: str | None = None
    level: str | None = None
    tags: Sequence[str] = ()

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "VocabularyEntry":
        """Create an entry from a dictionary, filling sensible defaults."""

        return cls(
            word=payload["word"],
            meaning=payload.get("meaning", ""),
            language=payload.get("language", "en").lower(),
            part_of_speech=payload.get("part_of_speech"),
            example=payload.get("example"),
            level=(payload.get("level") or "intermediate").lower(),
            tags=tuple(payload.get("tags", [])),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable representation of the entry."""

        return {
            "word": self.word,
            "meaning": self.meaning,
            "language": self.language,
            "part_of_speech": self.part_of_speech,
            "example": self.example,
            "level": self.level,
            "tags": list(self.tags),
        }


class VocabularyManager:
    """Load vocabulary information and provide helper query methods."""

    def __init__(self, dataset_path: Path) -> None:
        self._path = dataset_path
        self._lock = RLock()
        self._entries: List[VocabularyEntry] = []
        self._load_dataset()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def dataset_path(self) -> Path:
        return self._path

    @property
    def entries(self) -> Sequence[VocabularyEntry]:
        return tuple(self._entries)

    @property
    def languages(self) -> Sequence[str]:
        return sorted({entry.language for entry in self._entries})

    def refresh(self) -> None:
        """Reload the dataset from disk."""

        self._load_dataset()

    def get_daily_words(
        self,
        count: int,
        *,
        language: str | None = None,
        level: str | None = None,
        reference_date: date | None = None,
    ) -> List[Dict[str, Any]]:
        """Return a deterministic selection of entries for the given day."""

        if count <= 0:
            return []

        language = language.lower() if language else None
        level = level.lower() if level else None

        filtered = [
            entry
            for entry in self._entries
            if (language is None or entry.language == language)
            and (level is None or entry.level == level)
        ]

        if not filtered:
            filtered = list(self._entries)

        if not filtered:
            return []

        reference_date = reference_date or date.today()
        start_index = reference_date.toordinal() % len(filtered)

        result: List[VocabularyEntry] = []
        for offset in range(count):
            idx = (start_index + offset) % len(filtered)
            result.append(filtered[idx])

        return [entry.to_dict() for entry in result]

    def search(self, keyword: str, *, language: str | None = None) -> List[Dict[str, Any]]:
        """Perform a case-insensitive keyword search."""

        keyword = keyword.strip().lower()
        if not keyword:
            return []

        language = language.lower() if language else None

        results: List[VocabularyEntry] = []
        for entry in self._entries:
            if language and entry.language != language:
                continue
            if keyword in entry.word.lower() or keyword in entry.meaning.lower():
                results.append(entry)

        return [entry.to_dict() for entry in results]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_dataset(self) -> None:
        with self._lock:
            if not self._path.exists():
                raise FileNotFoundError(f"Vocabulary dataset not found: {self._path}")

            payload = json.loads(self._path.read_text(encoding="utf-8"))
            entries_raw: Iterable[Dict[str, Any]] = payload if isinstance(payload, list) else payload.get("items", [])

            self._entries = [VocabularyEntry.from_dict(item) for item in entries_raw]

            if not self._entries:
                raise ValueError("The vocabulary dataset is empty; please provide at least one entry.")
