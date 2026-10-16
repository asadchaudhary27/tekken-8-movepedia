"""
Gameplay Guides & Pro Competitive Intelligence Endpoints.
Serves full compendium data: Sidesteps, Throw Breaks, Anti-Cheese, Installs,
10-Hit Counters, Movement Bible, Hardware Settings, and Consolidated Character Tactics.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, HTTPException, status
from backend.app.services.gameplay_knowledge import GameplayKnowledgeService

router = APIRouter()


@router.get("/index", summary="Get guides compendium summary")
def get_guides_index():
    return GameplayKnowledgeService.get_all_guides_index()


@router.get("/sidesteps", summary="Get universal sidestep & weak side chart")
def get_sidesteps(q: Optional[str] = Query(None, description="Filter by character or side (e.g. Jin, SSL)")):
    return GameplayKnowledgeService.get_sidesteps(q)


@router.get("/throw-breaks", summary="Get complete throw break & grapple encyclopedia")
def get_throw_breaks(
    q: Optional[str] = Query(None, description="Filter by character or throw name"),
    category: Optional[str] = Query(None, description="Filter by category (Command Throw, Generic Throw, Side Throw, Back Throw)"),
    break_input: Optional[str] = Query(None, description="Filter by break input (1, 2, 1+2, Unbreakable)")
):
    return GameplayKnowledgeService.get_throw_breaks(q, category, break_input)


@router.get("/anti-cheese", summary="Get anti-cheese & knowledge check destroyer guide")
def get_anti_cheese(q: Optional[str] = Query(None, description="Filter by character or string")):
    return GameplayKnowledgeService.get_anti_cheese(q)


@router.get("/installs", summary="Get unique character installs & buff meters")
def get_installs(q: Optional[str] = Query(None, description="Filter by character or install name")):
    return GameplayKnowledgeService.get_installs(q)


@router.get("/wall-combos", summary="Get roster wall combo enders & tornado tools")
def get_wall_combos(
    q: Optional[str] = Query(None, description="Filter by character name"),
    route_type: Optional[str] = Query(None, description="Filter by route type (Max Damage, Post-Tornado, Oki)")
):
    return GameplayKnowledgeService.get_wall_combos(q, route_type)


@router.get("/ten-hit-combos", summary="Get 10-hit combo destroyer counter table")
def get_ten_hit_combos(q: Optional[str] = Query(None, description="Filter by character name")):
    return GameplayKnowledgeService.get_ten_hit_counters(q)


@router.get("/heat-smashes", summary="Get Heat System & Heat Smash danger matrix")
def get_heat_smashes(
    q: Optional[str] = Query(None, description="Filter by character, move, or strategy"),
    category: Optional[str] = Query(None, description="Filter by category"),
    view: Optional[str] = Query("matrix", description="View mode: 'matrix' for danger categories, 'characters' for all 43 fighters")
):
    return GameplayKnowledgeService.get_heat_smashes(query=q, category=category, view=view)


@router.get("/character-heat-smashes", summary="Get complete Heat Smash table for all 43 fighters")
def get_character_heat_smashes(
    q: Optional[str] = Query(None, description="Filter by character, input, stance, or notes"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    return GameplayKnowledgeService.get_character_heat_smashes(query=q, category=category)


@router.get("/movement-bible", summary="Get advanced movement & execution bible")
def get_movement_bible(q: Optional[str] = Query(None, description="Filter by technique name or input")):
    return GameplayKnowledgeService.get_movement_bible(query=q)


@router.get("/hardware-settings", summary="Get controller comparison & zero-lag settings")
def get_hardware_settings():
    return GameplayKnowledgeService.get_hardware_settings()


@router.get("/emergency-protocol", summary="Get brain freeze emergency blender protocol")
def get_emergency_protocol(
    q: Optional[str] = Query(None, description="Filter by scenario, situation, or panic trigger"),
    character: Optional[str] = Query(None, description="Filter by character name or slug")
):
    return GameplayKnowledgeService.get_emergency_protocol(query=q, character=character)


@router.get("/character/{slug}", summary="Get consolidated pro tactical intelligence for a character")
def get_character_tactics(slug: str):
    sidestep = GameplayKnowledgeService.get_sidestep_for_character(slug)
    throw_break = GameplayKnowledgeService.get_throw_break_for_character(slug)
    all_throws = GameplayKnowledgeService.get_all_throws_for_character(slug)
    anti_cheese = GameplayKnowledgeService.get_anti_cheese_for_character(slug)
    install = GameplayKnowledgeService.get_install_for_character(slug)
    wall_combo = GameplayKnowledgeService.get_wall_combo_for_character(slug)
    all_wall_combos = GameplayKnowledgeService.get_all_wall_combos_for_character(slug)
    ten_hit = GameplayKnowledgeService.get_ten_hit_for_character(slug)
    heat_smash = GameplayKnowledgeService.get_heat_smash_for_character(slug)
    blender = GameplayKnowledgeService.get_emergency_protocol(character=slug)

    return {
        "character_slug": slug,
        "sidestep": sidestep,
        "throw_break": throw_break,
        "all_throws": all_throws,
        "anti_cheese": anti_cheese,
        "install": install,
        "wall_combo": wall_combo,
        "all_wall_combos": all_wall_combos,
        "ten_hit_counter": ten_hit,
        "heat_smash": heat_smash,
        "blender_scenarios": blender
    }
