"""
Tekken 8 Master Gameplay Knowledge & Strategy Service.
Loads and serves authoritative data from the master compendium covering:
- Universal Sidestep & Weak Side Matrix (Part 5)
- Throw Break & Grapple Encyclopedia (Part 8)
- Anti-Cheese & Knowledge Check Destroyer Guide (Part 14)
- 10-Hit Combo Destroyer Bible (Part 19)
- Character Installs, Buff Meters & Stocks (Part 23)
- Wall Combo Enders & Tornado Matrix (Part 22)
- Heat System Masterclass & Heat Smash Danger Matrix (Part 12)
- Advanced Movement Execution Bible (Part 16)
- Zero-Lag Hardware & Leverless SOCD Settings (Part 26)
- Emergency Blender Protocol (Part 21)
"""

import os
import json
from typing import Dict, List, Any, Optional

COMPENDIUM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "knowledge", "master_compendium.json"))


class GameplayKnowledgeService:
    _data: Optional[Dict[str, Any]] = None

    @classmethod
    def _load_data(cls) -> Dict[str, Any]:
        if cls._data is None:
            if os.path.exists(COMPENDIUM_PATH):
                with open(COMPENDIUM_PATH, "r", encoding="utf-8") as f:
                    cls._data = json.load(f)
            else:
                cls._data = {}
        return cls._data

    @classmethod
    def get_sidesteps(cls, query: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("sidesteps", [])
        if not query:
            return data
        q = query.lower().strip()
        return [item for item in data if q in item["character"].lower() or q in item["weak_side"].lower()]

    @classmethod
    def get_sidestep_for_character(cls, char_name_or_slug: str) -> Optional[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        for item in cls._load_data().get("sidesteps", []):
            c_name = item["character"].lower()
            if clean in c_name or c_name in clean:
                return item
        return None

    @classmethod
    def get_throw_breaks(cls, query: Optional[str] = None, category: Optional[str] = None, break_input: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("throw_breaks", [])
        res = data
        if query:
            q = query.lower().strip()
            res = [item for item in res if q in item["character"].lower() or q in item["throw_name"].lower() or q in item.get("input_notation", "").lower()]
        if category:
            cat = category.lower().strip()
            res = [item for item in res if cat in item.get("category", "").lower()]
        if break_input:
            bi = break_input.lower().strip()
            res = [item for item in res if bi in item.get("break_input", "").lower()]
        return res

    @classmethod
    def get_throw_break_for_character(cls, char_name_or_slug: str) -> Optional[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        for item in cls._load_data().get("throw_breaks", []):
            c_name = item["character"].lower()
            c_slug = item.get("character_slug", "").lower()
            if clean in c_name or c_name in clean or clean == c_slug:
                return item
        return None

    @classmethod
    def get_all_throws_for_character(cls, char_name_or_slug: str) -> List[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        return [
            item for item in cls._load_data().get("throw_breaks", [])
            if clean in item["character"].lower() or item["character"].lower() in clean or clean == item.get("character_slug", "").lower()
        ]

    @classmethod
    def get_anti_cheese(cls, query: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("anti_cheese", [])
        if not query:
            return data
        q = query.lower().strip()
        return [item for item in data if q in item["character"].lower() or q in item["cheese_move"].lower()]

    @classmethod
    def get_anti_cheese_for_character(cls, char_name_or_slug: str) -> Optional[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        for item in cls._load_data().get("anti_cheese", []):
            c_name = item["character"].lower()
            if clean in c_name or c_name in clean:
                return item
        return None

    @classmethod
    def get_installs(cls, query: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("installs", [])
        if not query:
            return data
        q = query.lower().strip()
        return [item for item in data if q in item["character"].lower() or q in item["install_name"].lower()]

    @classmethod
    def get_install_for_character(cls, char_name_or_slug: str) -> Optional[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        for item in cls._load_data().get("installs", []):
            c_name = item["character"].lower()
            if clean in c_name or c_name in clean:
                return item
        return None

    @classmethod
    def get_wall_combos(cls, query: Optional[str] = None, route_type: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("wall_combos", [])
        res = data
        if query:
            q = query.lower().strip()
            res = [item for item in res if q in item["character"].lower() or q in item.get("wall_ender", "").lower()]
        if route_type:
            rt = route_type.lower().strip()
            res = [item for item in res if rt in item.get("route_type", "").lower()]
        return res

    @classmethod
    def get_wall_combo_for_character(cls, char_name_or_slug: str) -> Optional[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        for item in cls._load_data().get("wall_combos", []):
            c_name = item["character"].lower()
            c_slug = item.get("character_slug", "").lower()
            if clean in c_name or c_name in clean or clean == c_slug:
                return item
        return None

    @classmethod
    def get_all_wall_combos_for_character(cls, char_name_or_slug: str) -> List[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        return [
            item for item in cls._load_data().get("wall_combos", [])
            if clean in item["character"].lower() or item["character"].lower() in clean or clean == item.get("character_slug", "").lower()
        ]

    @classmethod
    def get_ten_hit_counters(cls, query: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("ten_hit_counters", [])
        if not query:
            return data
        q = query.lower().strip()
        return [item for item in data if q in item["character"].lower() or q in item.get("combo_input", "").lower()]

    @classmethod
    def get_ten_hit_for_character(cls, char_name_or_slug: str) -> Optional[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        for item in cls._load_data().get("ten_hit_counters", []):
            c_name = item["character"].lower()
            c_slug = item.get("character_slug", "").lower()
            if clean in c_name or c_name in clean or clean == c_slug:
                return item
        return None

    @classmethod
    def get_heat_smashes(cls, query: Optional[str] = None, category: Optional[str] = None, view: Optional[str] = None) -> List[Dict[str, Any]]:
        if view == "characters":
            return cls.get_character_heat_smashes(query=query, category=category)

        data = cls._load_data().get("heat_smashes", [])
        res = data
        if query:
            q = query.lower().strip()
            res = [
                item for item in res
                if q in item.get("category", "").lower()
                or q in item.get("characters", "").lower()
                or q in item.get("properties", "").lower()
                or q in item.get("counter_strategy", "").lower()
            ]
        if category:
            cat = category.lower().strip()
            res = [item for item in res if cat in item.get("category", "").lower()]
        return res

    @classmethod
    def get_character_heat_smashes(cls, query: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("character_heat_smashes", [])
        res = data
        if query:
            q = query.lower().strip()
            res = [
                item for item in res
                if q in item.get("character", "").lower()
                or q in item.get("command_input", "").lower()
                or q in item.get("stance_transition", "").lower()
                or q in item.get("hazard_property", "").lower()
                or q in item.get("properties", "").lower()
                or q in item.get("tactical_counter", "").lower()
            ]
        if category:
            cat = category.lower().strip()
            res = [item for item in res if cat in item.get("category", "").lower()]
        return res

    @classmethod
    def get_heat_smash_for_character(cls, char_name_or_slug: str) -> Optional[Dict[str, Any]]:
        clean = char_name_or_slug.lower().strip()
        for item in cls._load_data().get("character_heat_smashes", []):
            c_name = item.get("character", "").lower()
            c_slug = item.get("character_slug", "").lower()
            if clean in c_name or c_name in clean or clean == c_slug:
                return item
        return None

    @classmethod
    def get_movement_bible(cls, query: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("movement_bible", [])
        if not query:
            return data
        q = query.lower().strip()
        return [
            item for item in data
            if q in item.get("technique", "").lower()
            or q in item.get("input", "").lower()
            or q in item.get("socd_shortcut", "").lower()
            or q in item.get("why", "").lower()
            or q in item.get("tactical_use", "").lower()
            or q in item.get("warning", "").lower()
        ]

    @classmethod
    def get_hardware_settings(cls) -> Dict[str, Any]:
        return cls._load_data().get("hardware_settings", {})

    @classmethod
    def get_emergency_protocol(cls, query: Optional[str] = None, character: Optional[str] = None) -> List[Dict[str, Any]]:
        data = cls._load_data().get("blender_emergency_protocol", [])
        res = data
        if query:
            q = query.lower().strip()
            res = [
                item for item in res
                if q in item.get("character", "").lower()
                or q in item.get("scenario", "").lower()
                or q in item.get("situation", "").lower()
                or q in item.get("panic_trigger", "").lower()
                or q in item.get("verified_safe_response", "").lower()
                or q in item.get("action", "").lower()
            ]
        if character:
            c = character.lower().strip()
            res = [
                item for item in res
                if c in item.get("character", "").lower()
                or c in item.get("character_slug", "").lower()
            ]
        return res

    @classmethod
    def get_all_guides_index(cls) -> Dict[str, Any]:
        d = cls._load_data()
        return {
            "title": "Tekken 8 Master Competitive Compendium",
            "version": "3.00.02 (Season 2 Standard)",
            "total_sidesteps": len(d.get("sidesteps", [])),
            "total_throw_breaks": len(d.get("throw_breaks", [])),
            "total_anti_cheese_guides": len(d.get("anti_cheese", [])),
            "total_character_installs": len(d.get("installs", [])),
            "total_wall_combo_guides": len(d.get("wall_combos", [])),
            "total_10_hit_counters": len(d.get("ten_hit_counters", [])),
            "total_heat_smash_categories": len(d.get("heat_smashes", [])),
            "total_character_heat_smashes": len(d.get("character_heat_smashes", [])),
            "total_movement_techniques": len(d.get("movement_bible", [])),
            "total_blender_scenarios": len(d.get("blender_emergency_protocol", [])),
            "hardware_and_zero_lag": True
        }
