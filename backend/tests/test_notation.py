import pytest
from backend.app.services.notation import NotationEngine, DIRECTIONS


def test_all_nine_directions():
    """Validates directional arrows and English translations for all 9 states."""
    expected = {
        "u": ("↑", "Up", "8"),
        "ub": ("↖", "Up Back", "7"),
        "uf": ("↗", "Up Forward", "9"),
        "b": ("←", "Back", "4"),
        "n": ("•", "Neutral", "5"),
        "f": ("→", "Forward", "6"),
        "db": ("↙", "Down Back", "1"),
        "d": ("↓", "Down", "2"),
        "df": ("↘", "Down Forward", "3"),
    }
    for code, (arrow, english, numpad) in expected.items():
        res = NotationEngine.convert(code)
        assert res.arrow_display == arrow, f"Failed arrow for {code}"
        assert res.english_display == english, f"Failed english for {code}"
        assert res.numpad_display == numpad, f"Failed numpad for {code}"


def test_df_plus_2_test_case():
    """
    Mandatory Section 7 Test Case: df+2
    - Arrow: ↘ + 2
    - English: Down Forward + Right Punch
    - Numpad: 3 + 2 (direction and attack button identified separately)
    - Controller: ↘ + △ (PlayStation), ↘ + Y (Xbox), ↘ + 2 (Arcade)
    """
    # PlayStation layout
    res_ps = NotationEngine.convert("df+2", controller_layout="PLAYSTATION")
    assert res_ps.arrow_display == "↘ + 2"
    assert res_ps.english_display == "Down Forward + Right Punch"
    assert res_ps.numpad_display == "3 + 2"
    assert res_ps.controller_display == "↘ + △"
    assert not res_ps.has_unsupported_syntax

    # Xbox layout
    res_xbox = NotationEngine.convert("df+2", controller_layout="XBOX")
    assert res_xbox.controller_display == "↘ + Y"

    # Arcade layout
    res_arcade = NotationEngine.convert("df+2", controller_layout="ARCADE")
    assert res_arcade.controller_display == "↘ + 2"


def test_simultaneous_vs_sequential_inputs():
    """Ensures distinction between simultaneous (1+2) and sequential (1, 2)."""
    # Simultaneous: 1+2
    res_sim = NotationEngine.convert("1+2")
    assert res_sim.arrow_display == "1 + 2"
    assert res_sim.english_display == "Left Punch + Right Punch"
    assert len(res_sim.tokens) == 1
    assert res_sim.tokens[0].is_simultaneous is True

    # Sequential: 1, 2
    res_seq = NotationEngine.convert("1, 2")
    assert " , " in res_seq.arrow_display
    assert res_seq.english_display == "Left Punch , Right Punch"
    assert len(res_seq.tokens) == 2
    assert res_seq.tokens[0].is_simultaneous is False
    assert res_seq.tokens[1].is_simultaneous is False


def test_holds_and_repeated_inputs():
    """Verifies hold states (F, D) and repeated directions (f,f)."""
    res_dash = NotationEngine.convert("f, f")
    assert res_dash.arrow_display == "→ , →"
    assert len(res_dash.tokens) == 2

    # Hold detection
    tok_hold = NotationEngine.parse_token("F")
    assert tok_hold.is_hold is True


def test_unsupported_notation_preservation():
    """
    Section 7 requirement: Unsupported notation MUST be preserved
    rather than silently discarded, and reported for review.
    """
    res = NotationEngine.convert("df+2, UNKNOWN_SYNTAX_99")
    assert res.has_unsupported_syntax is True
    assert "UNKNOWN_SYNTAX_99" in res.unsupported_tokens
    # Original notation preserved in display string without data loss
    assert "UNKNOWN_SYNTAX_99" in res.arrow_display
    assert "UNKNOWN_SYNTAX_99" in res.english_display
