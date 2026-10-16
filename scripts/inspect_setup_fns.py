with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

def inspect_fn(fn_name, max_lines=60):
    print(f"\n=================== {fn_name} ===================")
    found = False
    for i, line in enumerate(lines, 1):
        if f"function {fn_name}(" in line or f"window.{fn_name} =" in line or f"const {fn_name} = " in line:
            found = True
            for j in range(i-1, min(len(lines), i + max_lines)):
                print(f"{j+1:4d}: {lines[j].rstrip()[:110]}")
            break
    if not found:
        print(f"Function {fn_name} NOT FOUND!")

inspect_fn("setupMovesSafetyFilters", 40)
inspect_fn("initMatchupAnalyzer", 50)
inspect_fn("initPunishAssistant", 40)
inspect_fn("initComboLab", 40)
inspect_fn("initPunishQuiz", 40)
inspect_fn("setupStageFilters", 40)
inspect_fn("renderFeaturedMoves", 30)
inspect_fn("populateHeroCombatTriad", 30)
