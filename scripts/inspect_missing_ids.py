import re

with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

missing_ids = [
    'comboCHToggle',
    'comboDifficultyFilter',
    'comboHeatToggle',
    'covOverallPct',
    'covRosterCount',
    'covRosterPct',
    'covTotalMoves',
    'featuredMovesList',
    'heroOpponentAvatar',
    'heroOpponentSelect',
    'heroPlayerAvatar',
    'heroPlayerSelect',
    'heroStageSelect',
    'heroStageThumb',
    'navFavBadge',
    'searchQuickInput',
    'sidebarQuickFighters',
    'sourcesGrid',
    'tacticsHubModal',
    'usefulMovesCountPill'
]

for mid in missing_ids:
    print(f"\n=== ID: {mid} ===")
    for idx, line in enumerate(lines, 1):
        if mid in line:
            print(f"  Line {idx}: {line.strip()[:100]}")
