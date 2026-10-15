"""
Tekken 8 Notation Normalization and Multi-Projection Visualization Engine.

Translates Tekken move notation into 4 standardized projections:
1. Directional Arrows (↑, ↖, ↗, ←, •, →, ↙, ↓, ↘)
2. English Directional & Button Names
3. Numpad Notation (Direction [1-9] + Buttons)
4. Physical Controller Layouts (PlayStation, Xbox, Arcade)
"""

import re
from typing import List, Dict, Tuple, Optional
from backend.app.schemas.notation import (
    NotationToken,
    NotationConversionResponse
)

# 9 Canonical Direction Mappings
DIRECTIONS = {
    "u":  {"arrow": "↑", "english": "Up",           "numpad": "8"},
    "ub": {"arrow": "↖", "english": "Up Back",      "numpad": "7"},
    "u/b": {"arrow": "↖", "english": "Up Back",     "numpad": "7"},
    "uf": {"arrow": "↗", "english": "Up Forward",   "numpad": "9"},
    "u/f": {"arrow": "↗", "english": "Up Forward",  "numpad": "9"},
    "b":  {"arrow": "←", "english": "Back",         "numpad": "4"},
    "n":  {"arrow": "•", "english": "Neutral",      "numpad": "5"},
    "•":  {"arrow": "•", "english": "Neutral",      "numpad": "5"},
    "f":  {"arrow": "→", "english": "Forward",      "numpad": "6"},
    "db": {"arrow": "↙", "english": "Down Back",    "numpad": "1"},
    "d/b": {"arrow": "↙", "english": "Down Back",   "numpad": "1"},
    "d":  {"arrow": "↓", "english": "Down",         "numpad": "2"},
    "df": {"arrow": "↘", "english": "Down Forward", "numpad": "3"},
    "d/f": {"arrow": "↘", "english": "Down Forward", "numpad": "3"},
}

# Attack Button Meanings
BUTTON_ENGLISH = {
    "1": "Left Punch",
    "2": "Right Punch",
    "3": "Left Kick",
    "4": "Right Kick"
}

# Controller Physical Mappings
CONTROLLER_BUTTONS = {
    "PLAYSTATION": {
        "1": "□",  # Square
        "2": "△",  # Triangle
        "3": "✕",  # Cross
        "4": "○"   # Circle
    },
    "XBOX": {
        "1": "X",
        "2": "Y",
        "3": "A",
        "4": "B"
    },
    "ARCADE": {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4"
    }
}

# Known Stances & Special Contexts
KNOWN_STANCES = {
    "ZEN", "HRA", "LFS", "RFS", "SAV", "RLX", "AOP", "RDS", "CRA",
    "CD", "WR", "WS", "FC", "SS", "SSL", "SSR", "BT", "H.", "R.", "HEAT", "RAGE"
}


class NotationEngine:
    """Modular notation conversion and normalization engine."""

    @classmethod
    def normalize_string(cls, raw: str) -> str:
        """Standardizes delimiters, slashes and whitespace."""
        s = raw.strip()
        # Standardize arrow/separator symbols
        s = s.replace("►", ",").replace("->", ",").replace(">", ",")
        # Standardize directional slashes: d/f -> df, d/b -> db, u/f -> uf, u/b -> ub
        s = re.sub(r'\bd/f\b', 'df', s, flags=re.IGNORECASE)
        s = re.sub(r'\bd/b\b', 'db', s, flags=re.IGNORECASE)
        s = re.sub(r'\bu/f\b', 'uf', s, flags=re.IGNORECASE)
        s = re.sub(r'\bu/b\b', 'ub', s, flags=re.IGNORECASE)
        # Normalize multiple spaces
        s = re.sub(r'\s*,\s*', ', ', s)
        return s

    @classmethod
    def parse_token(cls, raw_token: str) -> NotationToken:
        """Parses a single sequential input token (e.g. 'df+2', '1+2', 'F', 'qcf+1')."""
        token = raw_token.strip()
        if not token:
            return NotationToken(raw_token="", is_unsupported=True, unsupported_reason="Empty token")

        # Check for hold modifier (uppercase direction like F, D, B, U)
        is_hold = False
        if token in ["F", "D", "B", "U"] or "*(max)" in token or "[hold]" in token.lower():
            is_hold = True

        # Check for just-frame (timing marker ':')
        is_just_frame = ":" in token

        # Clean token for parsing
        clean_token = token.replace("*(max)", "").replace(":", "")

        # Split simultaneous components (connected with '+')
        if "+" in clean_token:
            parts = clean_token.split("+")
            is_simultaneous = True
        else:
            parts = [clean_token]
            is_simultaneous = False

        dir_part: Optional[str] = None
        buttons: List[str] = []
        unsupported: List[str] = []

        for p in parts:
            p_lower = p.lower()
            if p_lower in DIRECTIONS:
                dir_part = p_lower
            elif p in ["1", "2", "3", "4"]:
                buttons.append(p)
            elif len(p) > 1 and all(ch in ["1", "2", "3", "4"] for ch in p):
                # E.g. '12' -> ['1', '2']
                buttons.extend(list(p))
            elif p.upper() in KNOWN_STANCES or p.endswith("."):
                # Stance or special state prefix
                pass
            else:
                unsupported.append(p)

        direction_code = dir_part
        direction_arrow = DIRECTIONS[dir_part]["arrow"] if dir_part else None
        direction_english = DIRECTIONS[dir_part]["english"] if dir_part else None
        direction_numpad = DIRECTIONS[dir_part]["numpad"] if dir_part else None

        buttons_english = [BUTTON_ENGLISH[b] for b in buttons if b in BUTTON_ENGLISH]
        buttons_ps = [CONTROLLER_BUTTONS["PLAYSTATION"].get(b, b) for b in buttons]
        buttons_xbox = [CONTROLLER_BUTTONS["XBOX"].get(b, b) for b in buttons]
        buttons_arcade = [CONTROLLER_BUTTONS["ARCADE"].get(b, b) for b in buttons]

        is_unsupported = len(unsupported) > 0
        unsupported_reason = f"Unrecognized components: {', '.join(unsupported)}" if is_unsupported else None

        return NotationToken(
            raw_token=token,
            direction_code=direction_code,
            direction_arrow=direction_arrow,
            direction_english=direction_english,
            direction_numpad=direction_numpad,
            buttons=buttons,
            buttons_english=buttons_english,
            buttons_playstation=buttons_ps,
            buttons_xbox=buttons_xbox,
            buttons_arcade=buttons_arcade,
            is_simultaneous=is_simultaneous,
            is_hold=is_hold,
            is_just_frame=is_just_frame,
            is_unsupported=is_unsupported,
            unsupported_reason=unsupported_reason
        )

    @classmethod
    def convert(cls, raw_notation: str, controller_layout: str = "PLAYSTATION") -> NotationConversionResponse:
        """Translates a full notation sequence into 4 projection modes."""
        normalized = cls.normalize_string(raw_notation)
        tokens_raw = [t.strip() for t in normalized.split(",") if t.strip()]

        parsed_tokens: List[NotationToken] = []
        unsupported_list: List[str] = []

        arrow_chunks = []
        english_chunks = []
        numpad_chunks = []
        controller_chunks = []

        layout_key = controller_layout.upper()
        if layout_key not in CONTROLLER_BUTTONS:
            layout_key = "PLAYSTATION"

        for raw_t in tokens_raw:
            tok = cls.parse_token(raw_t)
            parsed_tokens.append(tok)

            if tok.is_unsupported:
                unsupported_list.append(tok.raw_token)
                arrow_chunks.append(tok.raw_token)
                english_chunks.append(tok.raw_token)
                numpad_chunks.append(tok.raw_token)
                controller_chunks.append(tok.raw_token)
                continue

            # 1. Arrow Display
            arrow_parts = []
            if tok.direction_arrow:
                arrow_parts.append(tok.direction_arrow)
            if tok.buttons:
                arrow_parts.extend(tok.buttons)
            arrow_str = " + ".join(arrow_parts) if tok.is_simultaneous else "".join(arrow_parts)
            arrow_chunks.append(arrow_str or tok.raw_token)

            # 2. English Display
            eng_parts = []
            if tok.direction_english:
                eng_parts.append(tok.direction_english)
            eng_parts.extend(tok.buttons_english)
            eng_str = " + ".join(eng_parts)
            english_chunks.append(eng_str or tok.raw_token)

            # 3. Numpad Display (Direction and Attack button identified separately)
            num_parts = []
            if tok.direction_numpad:
                num_parts.append(tok.direction_numpad)
            num_parts.extend(tok.buttons)
            num_str = " + ".join(num_parts) if tok.is_simultaneous else "".join(num_parts)
            numpad_chunks.append(num_str or tok.raw_token)

            # 4. Controller Display
            ctl_parts = []
            if tok.direction_arrow:
                ctl_parts.append(tok.direction_arrow)
            if layout_key == "PLAYSTATION":
                ctl_parts.extend(tok.buttons_playstation)
            elif layout_key == "XBOX":
                ctl_parts.extend(tok.buttons_xbox)
            else:
                ctl_parts.extend(tok.buttons_arcade)
            ctl_str = " + ".join(ctl_parts) if tok.is_simultaneous else "".join(ctl_parts)
            controller_chunks.append(ctl_str or tok.raw_token)

        arrow_display = " , ".join(arrow_chunks)
        english_display = " , ".join(english_chunks)
        numpad_display = " , ".join(numpad_chunks)
        controller_display = " , ".join(controller_chunks)

        return NotationConversionResponse(
            original_notation=raw_notation,
            normalized_notation=normalized,
            arrow_display=arrow_display,
            english_display=english_display,
            numpad_display=numpad_display,
            controller_display=controller_display,
            controller_layout=layout_key,
            tokens=parsed_tokens,
            unsupported_tokens=unsupported_list,
            has_unsupported_syntax=len(unsupported_list) > 0
        )
