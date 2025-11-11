"""Rule-based story generator used as a drop-in replacement for MetaGPT."""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from pydantic import BaseModel, Field, validator

__all__ = [
    "StoryGenerator",
    "StoryRequest",
    "StoryResult",
]

_DEFAULT_TEMPLATES = {
    "en": {
        "intros": [
            "On a {setting} afternoon, {protagonist} decided it was time for something different.",
            "Every adventure begins with a spark, and today {protagonist} felt brave.",
        ],
        "outros": [
            "And with that gentle reminder, the day faded into a warm memory.",
            "The lesson lingered as {protagonist} smiled at how much could change in a single day.",
        ],
    },
    "zh": {
        "intros": [
            "在{setting}的下午，{protagonist}决定尝试一些新的事情。",
            "每次冒险都由一丝火花开始，今天{protagonist}特别勇敢。",
        ],
        "outros": [
            "故事到这里暂告一段落，但新的灵感正在悄悄萌芽。",
            "{protagonist}轻轻点头，发现只要迈出一步，世界就会变得不同。",
        ],
    },
}

_LEVEL_TONES = {
    "beginner": "a gentle and encouraging",
    "intermediate": "an inspiring yet clear",
    "advanced": "a vivid and thought-provoking",
}

_STORY_SETTINGS = {
    "daily": "bright city",
    "travel": "busy train station",
    "fantasy": "mystical forest",
    "business": "modern startup hub",
}

_PARAGRAPH_COUNT = {
    "short": 2,
    "medium": 3,
    "long": 5,
}


class StoryRequest(BaseModel):
    """Validation model for incoming story requests."""

    words: List[str] = Field(..., min_items=1)
    user_level: str = Field(default="intermediate")
    story_type: str = Field(default="daily")
    story_length: str = Field(default="medium")
    custom_requirements: Optional[str] = None
    language: str = Field(default="en")

    @validator("words")
    def _strip_words(cls, value: Iterable[str]) -> List[str]:
        cleaned = [word.strip() for word in value if word.strip()]
        if not cleaned:
            raise ValueError("At least one non-empty word is required.")
        return cleaned

    @validator("user_level", "story_type", "story_length", "language", pre=True)
    def _normalize(cls, value: str) -> str:
        return (value or "").strip().lower() or "unknown"


@dataclass
class StoryResult:
    """Structured response returned by :class:`StoryGenerator`."""

    title: str
    body: str
    difficulty_level: str
    words_used: List[Dict[str, object]]
    estimated_reading_time: int
    language: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "title": self.title,
            "body": self.body,
            "difficulty_level": self.difficulty_level,
            "words_used": self.words_used,
            "estimated_reading_time": self.estimated_reading_time,
            "language": self.language,
        }


class StoryGenerator:
    """Generate contextual stories without relying on external LLM services."""

    def __init__(self, template_path: Path | None = None) -> None:
        self._templates = self._load_templates(template_path)

    def generate(self, request: StoryRequest) -> StoryResult:
        language = request.language if request.language in self._templates else "en"
        templates = self._templates[language]

        intro = self._cycle_pick(templates.get("intros", []), request.words)
        outro = self._cycle_pick(templates.get("outros", []), reversed(request.words))

        protagonist = self._pick_protagonist(request.user_level)
        setting = _STORY_SETTINGS.get(request.story_type, "cosy study room")
        tone = _LEVEL_TONES.get(request.user_level, "an engaging")
        paragraphs = _PARAGRAPH_COUNT.get(request.story_length, 3)

        intro_text = intro.format(setting=setting, protagonist=protagonist)
        outro_text = outro.format(protagonist=protagonist)

        body_sections = [intro_text]
        body_sections.extend(
            self._build_word_paragraphs(request.words, tone, protagonist, setting, paragraphs)
        )
        if request.custom_requirements:
            body_sections.append(self._render_custom_request(request.custom_requirements, language))
        body_sections.append(outro_text)

        body = "\n\n".join(body_sections)

        words_used = self._build_word_usage_summary(body, request.words)
        title = self._build_title(request.story_type, request.words, language)
        estimated_minutes = max(1, ceil(len(body.split()) / 140))

        return StoryResult(
            title=title,
            body=body,
            difficulty_level=request.user_level,
            words_used=words_used,
            estimated_reading_time=estimated_minutes,
            language=language,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _load_templates(self, template_path: Path | None) -> Dict[str, Dict[str, List[str]]]:
        if template_path and template_path.exists():
            import json

            data = json.loads(template_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                merged = {**_DEFAULT_TEMPLATES}
                for lang, sections in data.items():
                    if not isinstance(sections, dict):
                        continue
                    merged.setdefault(lang, {})
                    merged[lang].update({k: list(v) for k, v in sections.items() if isinstance(v, list)})
                return merged
        return {lang: {key: list(values) for key, values in sections.items()} for lang, sections in _DEFAULT_TEMPLATES.items()}

    @staticmethod
    def _cycle_pick(options: List[str], source: Iterable[str]) -> str:
        options = options or _DEFAULT_TEMPLATES["en"]["intros"]
        material = tuple(source)
        if not options:
            return ""
        index = abs(hash(material)) % len(options) if material else 0
        return options[index]

    @staticmethod
    def _pick_protagonist(level: str) -> str:
        if level == "beginner":
            return "a curious learner"
        if level == "advanced":
            return "a seasoned explorer"
        return "an eager student"

    @staticmethod
    def _build_word_paragraphs(
        words: List[str],
        tone: str,
        protagonist: str,
        setting: str,
        max_sections: int,
    ) -> List[str]:
        if max_sections <= 0:
            max_sections = len(words)

        chunk_size = max(1, ceil(len(words) / max_sections))
        paragraphs: List[str] = []
        for idx in range(0, len(words), chunk_size):
            chunk = words[idx : idx + chunk_size]
            sentences = []
            for word in chunk:
                sentences.append(
                    (
                        f"With {tone} voice, {protagonist} used the word '{word}' while navigating the {setting}, "
                        "discovering how it illuminates real-life conversations."
                    )
                )
            paragraphs.append(" ".join(sentences))
        return paragraphs

    @staticmethod
    def _render_custom_request(requirements: str, language: str) -> str:
        if language == "zh":
            return f"额外要求：{requirements.strip()}"
        return f"Special request noted: {requirements.strip()}"

    @staticmethod
    def _build_word_usage_summary(body: str, words: List[str]) -> List[Dict[str, object]]:
        lower_body = body.lower()
        summary: List[Dict[str, object]] = []
        for word in words:
            found = word.lower() in lower_body
            summary.append({"word": word, "found": found})
        return summary

    @staticmethod
    def _build_title(story_type: str, words: List[str], language: str) -> str:
        keyword = ", ".join(words[:3])
        if language == "zh":
            return f"{story_type.title()} 故事：{keyword}"
        return f"{story_type.title()} Story featuring {keyword}"
