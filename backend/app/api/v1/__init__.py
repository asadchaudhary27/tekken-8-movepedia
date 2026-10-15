from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health,
    characters,
    moves,
    notation,
    coverage,
    sources,
    stages,
    matchup,
    punishment,
    combos
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(characters.router, prefix="/characters", tags=["Characters"])
api_router.include_router(moves.router, prefix="/moves", tags=["Moves"])
api_router.include_router(notation.router, prefix="/notation", tags=["Notation"])
api_router.include_router(coverage.router, prefix="/coverage", tags=["Coverage & QA"])
api_router.include_router(sources.router, prefix="/sources", tags=["Data Sources"])
api_router.include_router(stages.router, prefix="/stages", tags=["Stages"])
api_router.include_router(matchup.router, prefix="/matchup", tags=["Matchup Analyzer"])
api_router.include_router(punishment.router, prefix="/punishment", tags=["Smart Punishment"])
api_router.include_router(combos.router, prefix="/combos", tags=["Combos & Stage Routes"])
