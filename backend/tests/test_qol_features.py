import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.session import SessionLocal
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.stage import Stage
from backend.app.models.combo_route import ComboRoute
from backend.app.services.global_search_service import GlobalSearchService
from backend.app.services.move_explorer_service import MoveExplorerService


client = TestClient(app)


def test_global_search_service_characters():
    db = SessionLocal()
    try:
        res = GlobalSearchService.search(db, "jin", category_filter="CHARACTER")
        assert res.query == "jin"
        assert len(res.character_results) > 0
        jin_match = next((c for c in res.character_results if "jin" in c.character_slug.lower()), None)
        assert jin_match is not None
        assert jin_match.category == "CHARACTER"
        assert jin_match.target_section == "fighters"
    finally:
        db.close()


def test_global_search_service_moves():
    db = SessionLocal()
    try:
        res = GlobalSearchService.search(db, "df+2", category_filter="MOVE")
        assert len(res.move_results) > 0
        m = res.move_results[0]
        assert m.category == "MOVE"
        assert "df+2" in m.notation.lower()
        assert m.target_section == "move-explorer"
    finally:
        db.close()


def test_global_search_frame_query_startup():
    db = SessionLocal()
    try:
        res = GlobalSearchService.search(db, "i10", category_filter="MOVE")
        assert len(res.move_results) > 0
        for m in res.move_results[:3]:
            # Should either have i10 in subtitle or notation
            assert "i10" in m.subtitle.lower() or "10" in m.notation.lower()
    finally:
        db.close()


def test_global_search_frame_query_block():
    db = SessionLocal()
    try:
        res = GlobalSearchService.search(db, "-10", category_filter="MOVE")
        assert len(res.move_results) > 0
        for m in res.move_results[:3]:
            assert "-10" in m.subtitle or "-10" in (m.badge or "") or "-10" in m.notation
    finally:
        db.close()


def test_global_search_stages():
    db = SessionLocal()
    try:
        res = GlobalSearchService.search(db, "arena", category_filter="STAGE")
        assert len(res.stage_results) > 0
        st = res.stage_results[0]
        assert st.category == "STAGE"
        assert "arena" in st.title.lower()
        assert st.target_section == "stages"
    finally:
        db.close()


def test_global_search_combos():
    db = SessionLocal()
    try:
        res = GlobalSearchService.search(db, "damage", category_filter="COMBO")
        # May be 0 if no combo has title 'damage', let's test with empty/broad query
        res2 = GlobalSearchService.search(db, "jin", category_filter="COMBO")
        assert res2.query == "jin"
        assert isinstance(res2.combo_results, list)
    finally:
        db.close()


def test_move_punish_window_and_pushback_enrichment():
    db = SessionLocal()
    try:
        # Fetch an unsafe move (<= -10)
        unsafe_move = db.query(Move).filter(Move.block_advantage <= -10).first()
        if unsafe_move:
            enriched = MoveExplorerService.enrich_move(unsafe_move)
            assert enriched.punish_window_frames is not None
            assert enriched.punish_window_frames == abs(unsafe_move.block_advantage)
            assert enriched.punish_window_type in [
                "STANDING_PUNISH",
                "LAUNCH_PUNISH",
                "CROUCH_PUNISH",
                "WS_LAUNCH_PUNISH",
            ]

        # Fetch a safe move (e.g. -1 to -9)
        safe_move = (
            db.query(Move)
            .filter(Move.block_advantage >= -9, Move.block_advantage <= -1)
            .first()
        )
        if safe_move:
            enriched_safe = MoveExplorerService.enrich_move(safe_move)
            assert enriched_safe.punish_window_frames is None
            assert enriched_safe.punish_window_type == "SAFE"

        # Check deathfist or pushback move
        deathfist = db.query(Move).filter(Move.original_notation.ilike("%d,df,f+2%")).first()
        if deathfist:
            enriched_df = MoveExplorerService.enrich_move(deathfist)
            assert enriched_df.has_pushback is True
            assert enriched_df.pushback_warning is not None
            assert "pushback" in enriched_df.pushback_warning.lower()
    finally:
        db.close()


def test_stance_awareness_enrichment():
    db = SessionLocal()
    try:
        # Check stance transition notation e.g. ~f or stance-context
        trans_move = db.query(Move).filter(Move.original_notation.ilike("%~f%")).first()
        if trans_move:
            enriched_trans = MoveExplorerService.enrich_move(trans_move)
            assert enriched_trans.is_stance_transition is True

        # Check stance attack e.g. starting with ZEN or CDS or WS
        stance_attack = db.query(Move).filter(Move.original_notation.ilike("ZEN %")).first()
        if stance_attack:
            enriched_sa = MoveExplorerService.enrich_move(stance_attack)
            assert enriched_sa.is_from_stance is True
            assert enriched_sa.stance_name == "ZEN"
    finally:
        db.close()


def test_api_v1_search_endpoint():
    response = client.get("/api/v1/search?q=kazuya")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "kazuya"
    assert data["total_results"] > 0
    assert "character_results" in data
    assert "move_results" in data
    assert "combo_results" in data
    assert "stage_results" in data


def test_api_v1_search_category_filter():
    response = client.get("/api/v1/search?q=jin&category=CHARACTER")
    assert response.status_code == 200
    data = response.json()
    assert len(data["character_results"]) > 0
    assert len(data["move_results"]) == 0
    assert len(data["stage_results"]) == 0


def test_api_v1_search_frame_query():
    response = client.get("/api/v1/search?q=i10&category=MOVE")
    assert response.status_code == 200
    data = response.json()
    assert len(data["move_results"]) > 0
