import re

def verify():
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    with open('frontend/assets/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    with open('frontend/assets/js/app.js', 'r', encoding='utf-8') as f:
        js = f.read()

    ids = [
        'rosterGrid', 'rosterGridContainer', 'carouselTrack', 'carouselPrevBtn', 'carouselNextBtn',
        'btnNavSearch', 'btnNavNotation', 'btnNavTactics', 'btnNavNotes', 'btnNavShare', 'btnNavFav', 'btnNavGear',
        'userModeSwitcher', 'navControllerToggle', 'topNavbar', 'heroBannerSection', 'viewModeGridBtn', 'viewModeRibbonBtn',
        'rosterSearchInput', 'rosterSortSelect', 'movesTableBody', 'movesPaginationBar'
    ]

    missing = [i for i in ids if f'id="{i}"' not in html]
    print(f"Missing IDs: {missing if missing else 'None! All IDs present.'}")

    # Check button classes in CSS
    required_classes = [
        '.btn', '.btn-primary', '.btn-secondary', '.btn-accent', '.btn-cyan', '.btn-danger', '.btn-destructive',
        '.btn-sm', '.btn-xs', '.btn-lg', '.btn-icon',
        '.btn-nav-search', '.btn-nav-notation', '.btn-nav-tactics', '.btn-nav-notes', '.btn-nav-share',
        '.btn-nav-fav', '.btn-nav-gear', '.btn-swagger',
        '.btn-hero-primary', '.btn-hero-secondary',
        '.roster-grid', '.roster-fighter-card', '.roster-avatar-wrap', '.roster-avatar',
        '.roster-dlc-tag', '.btn-roster-fav', '.roster-card-name', '.roster-card-style',
        '.roster-card-meta', '.roster-card-actions', '.btn-roster-action',
        '.moves-table', '.moves-table-container', '.analyzer-table', '.combo-card'
    ]

    missing_classes = [c for c in required_classes if c not in css]
    print(f"Missing CSS classes: {missing_classes if missing_classes else 'None! All required classes present.'}")

    # Check that roster card template in app.js has proper markup
    assert 'roster-card-meta' in js, "roster-card-meta missing in app.js"
    assert 'roster-card-actions' in js, "roster-card-actions missing in app.js"
    assert 'btn-roster-dossier' in js, "btn-roster-dossier missing in app.js"
    assert 'btn-roster-matchup' in js, "btn-roster-matchup missing in app.js"
    assert 'btn-roster-combos' in js, "btn-roster-combos missing in app.js"
    print("app.js roster card template structure: VERIFIED!")

if __name__ == '__main__':
    verify()
