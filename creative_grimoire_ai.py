"""
Creative Grimoire AI

A small, self-contained generator that blends "grimoire" concepts across
languages into a structured, creative ritual text. This is a toy generator
meant for inspiration and prompt scaffolding.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Sequence


@dataclass(frozen=True)
class GrimoireSource:
    name: str
    era: str
    notes: str


@dataclass(frozen=True)
class IncantationLine:
    language: str
    text: str
    meaning: str


@dataclass
class Lexicon:
    verbs: Sequence[str] = field(default_factory=list)
    nouns: Sequence[str] = field(default_factory=list)
    adjectives: Sequence[str] = field(default_factory=list)


@dataclass
class GrimoireConfig:
    seed: int | None = None
    lines: int = 6
    include_sources: bool = True
    include_sigils: bool = True
    include_ritual_steps: bool = True


LANGUAGE_SAMPLES: Dict[str, Dict[str, str]] = {
    "Latin": {
        "invoke": "Invoco",
        "bind": "Alligo",
        "veil": "Velamen",
        "spark": "Scintilla",
    },
    "Greek": {
        "invoke": "Kaleo",
        "bind": "Desmeo",
        "veil": "Kalyptra",
        "spark": "Spatha",
    },
    "Sanskrit": {
        "invoke": "Ahvayami",
        "bind": "Bandhayami",
        "veil": "Avritam",
        "spark": "Tejas",
    },
    "Old Norse": {
        "invoke": "Kalla",
        "bind": "Binda",
        "veil": "Hjup",
        "spark": "Neisti",
    },
    "Japanese": {
        "invoke": "Yobikake",
        "bind": "Shibaru",
        "veil": "Kakusu",
        "spark": "Hibana",
    },
    "Arabic": {
        "invoke": "Ad'u",
        "bind": "Arbit",
        "veil": "Sitr",
        "spark": "Shu'la",
    },
    "Hebrew": {
        "invoke": "Kore",
        "bind": "Kashar",
        "veil": "Seter",
        "spark": "Nitzots",
    },
    "Nahuatl": {
        "invoke": "Tlahtoa",
        "bind": "Tlalil",
        "veil": "Quemitl",
        "spark": "Tletl",
    },
}

DEFAULT_LEXICON = Lexicon(
    verbs=["weave", "summon", "awaken", "seal", "ignite", "harmonize"],
    nouns=["veil", "sigil", "ember", "chorus", "threshold", "archive"],
    adjectives=["luminous", "hidden", "resonant", "ancient", "stellate"],
)

SOURCES: List[GrimoireSource] = [
    GrimoireSource("Atramenta Codex", "Late Antiquity", "Starlit ink rites"),
    GrimoireSource("Verdant Scriptorium", "Medieval", "Botanical divination"),
    GrimoireSource("Obsidian Ledger", "Renaissance", "Mirror-bound sigils"),
    GrimoireSource("Astral Companion", "Modern", "Harmonic attunements"),
]

SIGILS = ["⚚", "✶", "☾", "✺", "⌖", "⟡", "✵"]


class CreativeGrimoireAI:
    def __init__(self, config: GrimoireConfig | None = None) -> None:
        self.config = config or GrimoireConfig()
        self.random = random.Random(self.config.seed)

    def _select_languages(self) -> List[str]:
        languages = list(LANGUAGE_SAMPLES.keys())
        self.random.shuffle(languages)
        return languages[: self.config.lines]

    def _compose_line(self, language: str, concept: str) -> IncantationLine:
        sample = LANGUAGE_SAMPLES[language]
        verb = sample["invoke"]
        bind = sample["bind"]
        meaning = f"{verb} {concept}; {bind} the {concept}."
        text = f"{verb} {sample['spark']} {sample['veil']} {concept}."
        return IncantationLine(language=language, text=text, meaning=meaning)

    def _choose_concept(self, lexicon: Lexicon) -> str:
        verb = self.random.choice(lexicon.verbs)
        noun = self.random.choice(lexicon.nouns)
        adjective = self.random.choice(lexicon.adjectives)
        return f"{adjective} {noun} to {verb}"

    def _ritual_steps(self) -> List[str]:
        return [
            "Sketch a circle of intent, leaving a single gate open.",
            "Name the guiding star and breathe on the sigil three times.",
            "Place the archive at the threshold and listen for resonance.",
            "Seal the rite with a mirrored breath and a closing word.",
        ]

    def generate(self, lexicon: Lexicon | None = None) -> str:
        lexicon = lexicon or DEFAULT_LEXICON
        languages = self._select_languages()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        sections: List[str] = [
            f"Creative Grimoire AI — Invocation Draft ({timestamp})",
            "=" * 62,
        ]

        if self.config.include_sources:
            sources = self.random.sample(SOURCES, k=2)
            sections.append("Sources Consulted:")
            for source in sources:
                sections.append(f"- {source.name} ({source.era}): {source.notes}")
            sections.append("")

        sections.append("Incantation Lines:")
        for language in languages:
            concept = self._choose_concept(lexicon)
            line = self._compose_line(language, concept)
            sections.append(f"[{line.language}] {line.text}")
            sections.append(f"  → {line.meaning}")

        if self.config.include_sigils:
            sigils = " ".join(self.random.sample(SIGILS, k=3))
            sections.extend(["", f"Sigils: {sigils}"])

        if self.config.include_ritual_steps:
            sections.extend(["", "Ritual Steps:"])
            for idx, step in enumerate(self._ritual_steps(), start=1):
                sections.append(f"{idx}. {step}")

        return "\n".join(sections)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--lines", type=int, default=6, help="Number of lines")
    parser.add_argument("--no-sources", action="store_true", help="Hide sources")
    parser.add_argument("--no-sigils", action="store_true", help="Hide sigils")
    parser.add_argument("--no-ritual", action="store_true", help="Hide ritual steps")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GrimoireConfig(
        seed=args.seed,
        lines=args.lines,
        include_sources=not args.no_sources,
        include_sigils=not args.no_sigils,
        include_ritual_steps=not args.no_ritual,
    )
    ai = CreativeGrimoireAI(config)
    print(ai.generate())


if __name__ == "__main__":
    main()
