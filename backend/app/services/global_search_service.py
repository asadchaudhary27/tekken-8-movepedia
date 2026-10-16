import re
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.combo_route import ComboRoute
from backend.app.models.stage import Stage
from backend.app.schemas.search import SearchResultItem, GlobalSearchResponse


class GlobalSearchService:
    """
    High-performance global search engine across characters, moves, combos, stages,
    and frame-data queries.
    """

    @classmethod
    def search(
        cls,
        db: Session,
        query_str: str,
        category_filter: Optional[str] = "ALL",
        limit_per_category: int = 10,
    ) -> GlobalSearchResponse:
        q = (query_str or "").strip().lower()
        if not q:
            return GlobalSearchResponse(query="", total_results=0)

        cat_filter = (category_filter or "ALL").upper()

        char_items: List[SearchResultItem] = []
        move_items: List[SearchResultItem] = []
        combo_items: List[SearchResultItem] = []
        stage_items: List[SearchResultItem] = []

        # 1. Search Characters
        if cat_filter in ["ALL", "CHARACTER", "CHARACTERS", "FIGHTERS"]:
            chars = (
                db.query(Character)
                .filter(
                    or_(
                        Character.name.ilike(f"%{q}%"),
                        Character.slug.ilike(f"%{q}%"),
                        Character.archetype.ilike(f"%{q}%"),
                        Character.hurtbox_class.ilike(f"%{q}%"),
                    )
                )
                .limit(limit_per_category)
                .all()
            )
            for c in chars:
                char_items.append(
                    SearchResultItem(
                        id=c.id,
                        category="CHARACTER",
                        title=c.name,
                        subtitle=f"{c.archetype or 'Tekken Fighter'} • {c.hurtbox_class or 'MALE_STANDARD'}",
                        character_name=c.name,
                        character_slug=c.slug,
                        badge=c.archetype or "Fighter",
                        target_section="fighters",
                        deep_link_params={"character_slug": c.slug, "character_id": c.id},
                    )
                )


        # 2. Search Stages
        if cat_filter in ["ALL", "STAGE", "STAGES", "ARENAS"]:
            stages = (
                db.query(Stage)
                .filter(
                    or_(
                        Stage.name.ilike(f"%{q}%"),
                        Stage.slug.ilike(f"%{q}%"),
                        Stage.location.ilike(f"%{q}%"),
                        Stage.boundary_shape.ilike(f"%{q}%"),
                    )
                )
                .limit(limit_per_category)
                .all()
            )
            for s in stages:
                shape = s.boundary_shape or ("Walled" if s.has_walls else "Infinite")
                hazards = []
                if s.wall_break: hazards.append("Wall Break")
                if s.floor_break: hazards.append("Floor Break")
                if s.balcony_break: hazards.append("Balcony Break")
                if not s.has_walls: hazards.append("Infinite")
                hazards_str = " • ".join(hazards) if hazards else "Standard Enclosed"

                stage_items.append(
                    SearchResultItem(
                        id=s.id,
                        category="STAGE",
                        title=s.name,
                        subtitle=f"{s.location or 'Official Battleground'} — {hazards_str}",
                        badge=shape,
                        target_section="stages",
                        deep_link_params={"stage_id": s.id, "stage_slug": s.slug},
                    )
                )

        # 3. Search Combos
        if cat_filter in ["ALL", "COMBO", "COMBOS"]:
            combos = (
                db.query(ComboRoute)
                .join(Character)
                .filter(
                    or_(
                        ComboRoute.title.ilike(f"%{q}%"),
                        ComboRoute.notation_sequence.ilike(f"%{q}%"),
                        ComboRoute.starter_move_name.ilike(f"%{q}%"),
                        ComboRoute.starter_move_input.ilike(f"%{q}%"),
                        ComboRoute.combo_type.ilike(f"%{q}%"),
                        Character.name.ilike(f"%{q}%"),
                    )
                )
                .limit(limit_per_category)
                .all()
            )
            for cb in combos:
                char_name = cb.character.name if cb.character else "Fighter"
                char_slug = cb.character.slug if cb.character else "jin"
                combo_items.append(
                    SearchResultItem(
                        id=cb.id,
                        category="COMBO",
                        title=f"{char_name}: {cb.title}",
                        subtitle=f"Starter: {cb.starter_move_input or 'df+2'} • {cb.total_damage} DMG ({cb.hit_count} Hits)",
                        character_name=char_name,
                        character_slug=char_slug,
                        notation=cb.notation_sequence,
                        badge=f"{cb.total_damage} DMG",
                        target_section="combo-lab",
                        deep_link_params={
                            "character_slug": char_slug,
                            "combo_id": cb.id,
                        },
                    )
                )

        # 4. Search Moves
        if cat_filter in ["ALL", "MOVE", "MOVES"]:
            # Check frame-specific startup pattern: e.g. "i10", "i15", "10f", "15f"
            startup_match = re.match(r"^i?(\d{1,2})f?$", q)
            # Check block advantage query: e.g. "-10", "-15", "+4"
            block_match = re.match(r"^([+-]?\d{1,2})$", q)

            move_query = db.query(Move).join(Character)

            if startup_match and len(q) <= 4:
                val = int(startup_match.group(1))
                move_query = move_query.filter(
                    or_(
                        Move.startup_frames == val,
                        Move.original_notation.ilike(f"%{q}%"),
                        Move.name.ilike(f"%{q}%"),
                    )
                )
            elif block_match and len(q) <= 3:
                val = int(block_match.group(1))
                move_query = move_query.filter(
                    or_(
                        Move.block_advantage == val,
                        Move.original_notation.ilike(f"%{q}%"),
                    )
                )
            else:
                move_query = move_query.filter(
                    or_(
                        Move.original_notation.ilike(f"%{q}%"),
                        Move.normalized_notation.ilike(f"%{q}%"),
                        Move.name.ilike(f"%{q}%"),
                        Move.hit_level.ilike(f"%{q}%"),
                        Character.name.ilike(f"%{q}%"),
                    )
                )

            moves = move_query.limit(limit_per_category).all()
            for m in moves:
                c_name = m.character.name if m.character else "Fighter"
                c_slug = m.character.slug if m.character else "jin"

                # Construct clean frame overview
                su_str = f"i{m.startup_frames}" if m.startup_frames else (m.startup_raw or "i--")
                ba = m.block_advantage
                if ba is not None:
                    ba_str = f"+{ba}" if ba > 0 else (f"{ba}" if ba < 0 else "±0")
                else:
                    ba_str = m.block_advantage_raw or "--"

                hl_str = (m.hit_level or "").upper()
                name_str = f" ({m.name})" if m.name else ""

                move_items.append(
                    SearchResultItem(
                        id=m.id,
                        category="MOVE",
                        title=f"{c_name}: {m.original_notation}{name_str}",
                        subtitle=f"{su_str} • Block: {ba_str} • {hl_str} • {m.damage or 0} DMG",
                        character_name=c_name,
                        character_slug=c_slug,
                        notation=m.original_notation,
                        badge=ba_str,
                        target_section="move-explorer",
                        deep_link_params={
                            "character_slug": c_slug,
                            "move_id": m.id,
                            "notation": m.original_notation,
                        },
                    )
                )

        all_results = char_items + move_items + combo_items + stage_items
        total = len(all_results)

        return GlobalSearchResponse(
            query=query_str,
            total_results=total,
            results=all_results,
            character_results=char_items,
            move_results=move_items,
            combo_results=combo_items,
            stage_results=stage_items,
        )
