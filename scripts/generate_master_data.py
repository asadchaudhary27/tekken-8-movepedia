"""
Authoritative generator for frontend/assets/js/tekken8MasterData.js
Produces English as the default primary language for all 44 characters
and universal combat mechanics, with full bilingual Roman Urdu preservation.
"""

import os
import re
import json

def generate_file():
    with open('master_guide_extracted.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()

    p3_start = raw_text.find('Part 3: All Characters Profile Cards')
    p4_start = raw_text.find('Part 4: Defence')
    p3_text = raw_text[p3_start:p4_start]

    char_headers = list(re.finditer(r'(?:^|\n)(\d+)\.\s+([A-Za-z0-9\s\(\)&\'\-\.]+)\n(?=Profile Card:)', p3_text))

    raw_blocks = {}
    for i, m in enumerate(char_headers):
        start = m.start()
        end = char_headers[i+1].start() if i+1 < len(char_headers) else len(p3_text)
        block = p3_text[start:end].strip()
        num = int(m.group(1))
        name = m.group(2).strip()
        raw_blocks[num] = (name, block)

    def parse_sections(block_text):
        lines = [l.strip() for l in block_text.split('\n') if l.strip()]
        sec = {}
        curr = None
        for l in lines:
            if l.startswith('Profile Card:'):
                curr = 'profile'
                sec['profile'] = l.replace('Profile Card:', '').strip()
            elif any(l.startswith(k) for k in ['Poking Buttons:', 'Poking & Pressure:', 'Poking:']):
                curr = 'poking'
                sec['poking'] = l
            elif any(l.startswith(k) for k in ['Pressure Moves:', 'Pressure:']):
                curr = 'pressure'
                sec['pressure'] = l
            elif any(l.startswith(k) for k in ['Upper/Mid/Low Mix-up:', 'Upper/Mid/Low Mix-up', 'Mix-up (', 'Mix-up:']):
                curr = 'mixup'
                sec['mixup'] = l
            elif any(l.startswith(k) for k in ['Jaal (Trap Setup):', 'Jaal:', 'Trap Setup:']):
                curr = 'jaal'
                sec['jaal'] = l
            else:
                if curr in sec:
                    sec[curr] += '\n' + l
        return sec

    # Meta definitions for all 44 characters
    meta_list = [
        # Base Roster (32)
        (1, 1, "jin", "Jin Kazama", "The Lightning of Fate", "Japan", "🇯🇵", "Yggdrasil & Jin's Allies", "Yggdrasil Alliance", "Base", "Traditional Karate • Kazama Self-Defense", "SSL", "/assets/avatars/jin.jpg"),
        (2, 2, "kazuya", "Kazuya Mishima", "Cold-Blooded Overlord", "Japan", "🇯🇵", "G-Corporation & Kazuya's Allies", "G-Corp", "Base", "Mishima Style Fighting Karate", "SSL", "/assets/avatars/kazuya.jpg"),
        (3, 3, "reina", "Reina", "The Purple Spark", "Japan", "🇯🇵", "Mishima Bloodline & Enforcers", "Mishima Bloodline", "Base", "Mishima Style Karate • Taido", "SSL", "/assets/avatars/reina.jpg"),
        (4, 5, "jun", "Jun Kazama", "Light of Sanctuary", "Japan", "🇯🇵", "Yggdrasil & Jin's Allies", "Kazama Clan", "Base", "Kazama Style Traditional Martial Arts", "SSL", "/assets/avatars/jun.jpg"),
        (5, 6, "devil-jin", "Devil Jin", "Black Wings of Ruin", "Japan", "🇯🇵", "Mishima Bloodline & Enforcers", "Devil Entity", "Base", "Advanced Mishima Style • Devil Arts", "SSL", "/assets/avatars/devil-jin.jpg"),
        (6, 7, "lars", "Lars Alexandersson", "Lion of the Rebellion", "Sweden", "🇸🇪", "Yggdrasil & Jin's Allies", "Yggdrasil Leader", "Base", "Tekken Forces Martial Arts", "SSR", "/assets/avatars/lars.jpg"),
        (7, 8, "lee", "Lee Chaolan", "Silver-Haired Demon", "Japan", "🇯🇵", "Yggdrasil & Jin's Allies", "Violet Systems", "Base", "Mishima Style Karate • Martial Arts", "SSL", "/assets/avatars/lee.jpg"),
        (8, 9, "xiaoyu", "Ling Xiaoyu", "Dancing Phoenix", "China", "🇨🇳", "Yggdrasil & Jin's Allies", "Jin's Protector", "Base", "Baguazhang • Piguazhang", "SSL", "/assets/avatars/xiaoyu.jpg"),
        (9, 10, "hwoarang", "Hwoarang", "Blood Talon", "South Korea", "🇰🇷", "Tournament Veterans & Wildcards", "Rival Wildcard", "Base", "Taekwondo", "SSL", "/assets/avatars/hwoarang.jpg"),
        (10, 11, "claudio", "Claudio Serafino", "Sirius Marksman", "Italy", "🇮🇹", "Yggdrasil & Jin's Allies", "Archers of Sirius", "Base", "Sirius Exorcism Sorcery", "SSL", "/assets/avatars/claudio.jpg"),
        (11, 12, "zafina", "Zafina", "Mystic Astrologer", "Egypt", "🇪🇬", "Yggdrasil & Jin's Allies", "Azazel Sealer", "Base", "Ancient Assassination Arts", "SSL", "/assets/avatars/zafina.jpg"),
        (12, 13, "victor", "Victor Chevalier", "Refined Striker", "France", "🇫🇷", "Yggdrasil & Jin's Allies", "UN Independent Forces", "Base", "Super Spy CQB • French Swordsmanship", "SSR", "/assets/avatars/victor.jpg"),
        (13, 14, "raven", "Raven", "Shadow Agent", "Unknown", "🌐", "Yggdrasil & Jin's Allies", "UN Intelligence", "Base", "Ninjutsu", "SSL", "/assets/avatars/raven.jpg"),
        (14, 15, "alisa", "Alisa Bosconovitch", "Destroying Angel", "Russia", "🇷🇺", "Yggdrasil & Jin's Allies", "Violet Systems", "Base", "High-Mobility Thruster Combat", "SSL", "/assets/avatars/alisa.jpg"),
        (15, 16, "nina", "Nina Williams", "Silent Assassin", "Ireland", "🇮🇪", "G-Corporation & Kazuya's Allies", "G-Corp Commander", "Base", "Assassination Martial Arts", "SSR", "/assets/avatars/nina.jpg"),
        (16, 17, "jack-8", "Jack-8", "Heavy Combat Automaton", "G-Corp", "🤖", "G-Corporation & Kazuya's Allies", "G-Corp Weapon", "Base", "Brute Force Power Combat", "SSL", "/assets/avatars/jack-8.jpg"),
        (17, 18, "feng", "Feng Wei", "God Fist", "China", "🇨🇳", "Tekken Monks & Traditional Purifiers", "Dragon Fist", "Base", "Chinese Kempo • God Fist Style", "SSL", "/assets/avatars/feng.jpg"),
        (18, 19, "dragunov", "Sergei Dragunov", "White Angel of Death", "Russia", "🇷🇺", "Tournament Veterans & Wildcards", "Red Army Spetsnaz", "Base", "Combat Sambo", "SSR", "/assets/avatars/dragunov.jpg"),
        (19, 20, "bryan", "Bryan Fury", "Harbinger of Chaos", "USA", "🇺🇸", "Tournament Veterans & Wildcards", "Cybernetic Anarchist", "Base", "Kickboxing", "SSL", "/assets/avatars/bryan.jpg"),
        (20, 21, "azucena", "Azucena Ortiz", "Coffee Queen", "Peru", "🇵🇪", "Tournament Veterans & Wildcards", "Ortiz Farm", "Base", "Rumi Maki • Mixed Martial Arts", "SSR", "/assets/avatars/azucena.jpg"),
        (21, 22, "king", "King II", "Anger of the Beast", "Mexico", "🇲🇽", "Tournament Veterans & Wildcards", "Lucha Libre", "Base", "Pro-Wrestling • Lucha Libre", "SSR", "/assets/avatars/king.jpg"),
        (22, 23, "paul", "Paul Phoenix", "Hot-Blooded Destroyer", "USA", "🇺🇸", "Tournament Veterans & Wildcards", "Indomitable Brawler", "Base", "Judobased Mixed Martial Arts", "SSR", "/assets/avatars/paul.jpg"),
        (23, 24, "law", "Marshall Law", "The Dragon", "USA", "🇺🇸", "Tournament Veterans & Wildcards", "Martial Arts Chef", "Base", "Martial Arts (Jeet Kune Do)", "SSR", "/assets/avatars/law.jpg"),
        (24, 25, "steve", "Steve Fox", "Counter-Punching Ace", "United Kingdom", "🇬🇧", "Tournament Veterans & Wildcards", "World Middleweight Champion", "Base", "Boxing", "SSL", "/assets/avatars/steve.jpg"),
        (25, 26, "asuka", "Asuka Kazama", "Spirited Peacemaker", "Japan", "🇯🇵", "Tournament Veterans & Wildcards", "Kazama Dojo", "Base", "Kazama Style Traditional Martial Arts", "SSR", "/assets/avatars/asuka.jpg"),
        (26, 27, "lili", "Lili Rochefort", "Fighting Heiress", "Monaco", "🇲🇨", "Tournament Veterans & Wildcards", "Rochefort Enterprises", "Base", "Self-Taught Gymnastic Street Fighting", "SSL", "/assets/avatars/lili.jpg"),
        (27, 28, "leo", "Leo Kliesen", "Spelunker of Truth", "Germany", "🇩🇪", "Tournament Veterans & Wildcards", "Baji Explorer", "Base", "Bajiquan", "SSL", "/assets/avatars/leo.jpg"),
        (28, 29, "shaheen", "Shaheen", "Desert Falcon", "Saudi Arabia", "🇸🇦", "Tournament Veterans & Wildcards", "G-Corp Resistance", "Base", "Military Self-Defense (CQC)", "SSL", "/assets/avatars/shaheen.jpg"),
        (29, 30, "leroy", "Leroy Smith", "Grandmaster of Drip", "USA", "🇺🇸", "Tekken Monks & Traditional Purifiers", "Wing Chun Master", "Base", "Wing Chun", "SSL", "/assets/avatars/leroy.jpg"),
        (30, 31, "yoshimitsu", "Yoshimitsu", "Mechanized Space Ninja", "Japan", "🇯🇵", "Tournament Veterans & Wildcards", "Manji Clan Leader", "Base", "Advanced Manji Ninjutsu", "SSL", "/assets/avatars/yoshimitsu.jpg"),
        (31, 32, "kuma", "Kuma II", "Master of Salmon", "Japan", "🇯🇵", "Mishima Bloodline & Enforcers", "Heihachi's Guard", "Base", "Heihachi-Style Advanced Kuma Shin Ken", "SSL", "/assets/avatars/kuma.jpg"),
        (32, 32, "panda", "Panda", "Pretty in Pink", "China", "🇨🇳", "Yggdrasil & Jin's Allies", "Xiaoyu's Bodyguard", "Base", "Heihachi-Style Advanced Kuma Shin Ken", "SSL", "/assets/avatars/panda.jpg"),

        # DLC Season 1 (4)
        (33, 4, "heihachi", "Heihachi Mishima", "The King of Iron Fist", "Japan", "🇯🇵", "Mishima Bloodline & Enforcers", "Mishima Patriarch", "Season 1", "Mishima Style Fighting Karate", "SSL", "/assets/avatars/heihachi.jpg"),
        (34, 33, "eddy", "Eddy Gordo", "Capoeira Prodigy", "Brazil", "🇧🇷", "Tekken Monks & Traditional Purifiers", "Reformed Fighter", "Season 1", "Capoeira", "SSL", "/assets/avatars/eddy.jpg"),
        (35, 34, "lidia", "Lidia Sobieska", "Prime Minister of Poland", "Poland", "🇵🇱", "Tekken Monks & Traditional Purifiers", "Polish Government", "Season 1", "Traditional Karate", "SSL", "/assets/avatars/lidia.jpg"),
        (36, 35, "clive", "Clive Rosfield", "First Shield of Rosaria", "Valisthea", "⚔️", "Guest Legends", "Dominant of Ifrit", "Season 1", "Rosarian Royal Swordsmanship • Eikonic Combat", "SSR", "/assets/avatars/clive.jpg"),

        # DLC Season 2 (4)
        (37, 36, "anna", "Anna Williams", "Scarlet Lightning", "Ireland", "🇮🇪", "G-Corporation & Kazuya's Allies", "G-Corp Commander", "Season 2", "Assassination Martial Arts", "SSR", "/assets/avatars/anna.jpg"),
        (38, 37, "fahkumram", "Fahkumram", "Thunder Striker", "Thailand", "🇹🇭", "Tournament Veterans & Wildcards", "Muay Thai Legend", "Season 2", "Muay Thai", "SSL", "/assets/avatars/fahkumram.jpg"),
        (39, 38, "armor-king", "Armor King II", "Dark Jaguar", "Mexico", "🇲🇽", "Tournament Veterans & Wildcards", "Black Jaguar Circuit", "Season 2", "Lucha Libre • Street Brawling", "SSL", "/assets/avatars/armor-king.jpg"),
        (40, 39, "miary-zo", "Miary Zo", "Primal Fighting Spirit", "Madagascar", "🇲🇬", "Tournament Veterans & Wildcards", "Spiritual Guardian", "Season 2", "Morengy • Ancient Primal Arts", "SSL", "/assets/avatars/miary-zo.jpg"),

        # DLC Season 3 (4)
        (41, 40, "kunimitsu", "Kunimitsu II", "Fox-Masked Kunoichi", "Japan", "🇯🇵", "Tournament Veterans & Wildcards", "Manji Renegade", "Season 3", "Manji Ninjutsu • Dagger Arts", "SSL", "/assets/avatars/kunimitsu.jpg"),
        (42, 41, "bob", "Bob Richards", "Speed & Weight", "USA", "🇺🇸", "Tournament Veterans & Wildcards", "Freestyle Bounty Hunter", "Season 3", "Freestyle Karate", "SSR", "/assets/avatars/bob.jpg"),
        (43, 42, "roger-jr", "Roger Jr.", "Marsupial Boxing Champ", "Australia", "🇦🇺", "G-Corporation & Kazuya's Allies", "G-Corp Bio-Lab", "Season 3", "Commando Animal Boxing", "SSL", "/assets/avatars/roger-jr.jpg"),
        (44, 43, "yujiro", "Yujiro Hanma", "The Strongest Creature on Earth", "Japan", "👹", "Guest Legends", "The Ogre", "Season 3", "Total Primal Combat • Demon Back", "SSL", "/assets/avatars/yujiro.jpg")
    ]

    # Full English Dossiers
    english_dossiers = {
        "jin": {
            "lore": "Former Head of the Mishima Zaibatsu; fights alongside Lars and Lee to stop Kazuya and rid the world of the cursed Devil Gene once and for all.",
            "poking": "Poking Buttons: 1, 2 (i10 high jabs), df+1 (Mid check poke), f+4 (Premier Range 2 keepout mid kick, CH launcher), d+4 (Fast evasive low poke), db+4 (Plus-on-hit stature low).",
            "pressure": "Pressure Moves: 2,1,4 (Safe block string with wall-splat confirm), wr+3 (While Running mid kick: +6 on block!), Electric Wind Hook Fist (f,n,d,df:2: +5 on block launcher!).",
            "mixup": "Upper/Mid/Low Mix-up (Zenshin Stance ZEN - b+3+4 or f+4~f): Low: ZEN 4 (Diving low sweep) or Hellsweep (f,n,d,df+4). Mid: ZEN 1+2 or ZEN 3 (Homing mid check). High/Throw: ZEN 1+3 (Command grab) or ZEN u+1 (Evasive launcher).",
            "trap": "The Trap Setup: Approach with d+2 (high-crushing low with +4 on hit) and f+4. When the opponent turtles, input 2,1 then hesitate into uf+2 (evasive punch) or command grab uf+1+2.",
            "step": "Sidestep Left (SSL) to evade Jin's 2,1 strings, EWHF, and f+4 keepout kicks. Beware of his df+1 mid check, which tracks to his right; step and immediately neutral block.",
            "minus": "-10 to -14 Punishable: 2,1,4 (safe on block, but 3rd hit is high duckable), df+1,4 (-13 on block), d+2 (-14 on block). -15+ Launch Punishable: Can-Can kicks d+3+4 (-15 Launch), db+4 (-15 Launch), ZEN 4 diving sweep (-26 Launch).",
            "duck": "Duck under the 3rd hit of 2,1,4 and launch with While Standing ws+2! Duck and block d+2 on reaction to launch. Low parry d+4 pokes with df.",
            "parry": "Jin's b+1+3 parry deflects virtually everything (weapons, elbows, and knees). Bait out his parry with hesitation or strike with low attacks that bypass his b+1+3 guard."
        },
        "kazuya": {
            "lore": "Leader of G Corporation; seeks absolute global domination through demonic power after slaying his father Heihachi.",
            "poking": "Poking Buttons: 1, 1 (i10 hit-confirmable 1,1,2 knockdown), df+4 (Safe mid check), db+4 (Stature low kick: +4 on hit!), df+1,2 (Fast mid check string).",
            "pressure": "Pressure Moves: EWGF (f,n,d,df:2: +5 on block high launcher!), f+4 (Crouch-forcing mid: +4 on block!), cd+1+2 (Overhead punch: +5 on block).",
            "mixup": "The 50/50 Mishima Vortex: Wave-dash into opponent's face: Low: Hellsweep (cd+4,1 - unseeable knockdown sweep) vs Mid: ff+3 (Safe mid launcher) or EWGF (High launcher).",
            "trap": "The Trap Setup: Push opponent to the wall, land f+4 (+4 crouch-forcing mid), then immediately input df+2 (Counter-Hit launcher) or cd+4,1 Hellsweep to loop them back onto the ground.",
            "step": "Sidestep Left (SSL) is Kazuya's ultimate weakness! EWGF, df+1, ff+3, and cd+1+2 all whiff cleanly against SSL. NEVER sidestep right or Hellsweep will clip you.",
            "minus": "-10 to -14 Punishable: 1,1,2 (-17 on block if unfinished/blocked), df+1,2 (-12 punish), f+1+2 (-12). -15+ Launch Punishable: Hellsweep (cd+4,1: -23 Stagger Low Launch!), df+2 (-15 Launch), Twin Pistons ws+1,2 (-15 Launch).",
            "duck": "Do not panic against wave-dash. Block LOW with db to stagger-block Hellsweep and launch with ws+2 for 85+ damage! Duck under the 2nd hit of df+1,2 if delayed.",
            "parry": "Kazuya has no reversal. Low parry db+4 with df. Kazuya's EWGF and f,f+3 can be deflected with high/mid punch and kick parries."
        },
        "reina": {
            "lore": "Student at Mishima Polytechnical School and secret daughter of Heihachi Mishima, fighting to awaken her dormant Devil Gene.",
            "poking": "Poking Buttons: 1, 1 (Hit-confirmable 1,1,2), df+1,1 (Mid-mid check), f+4 (Crouching mid pressure), db+4 (Fast low poke), ss+4 (Sidestep low sweep).",
            "pressure": "Pressure Moves: ff+2 (Demon breath into Sentai SEN: premier gap-closer), wr+3 (While running kick: +6 on block into Heaven's Wrath HW).",
            "mixup": "Upper/Mid/Low Mix-up (Sentai Stance ff+2~f): Low: SEN 3 (Low sweep into full combo). Mid: SEN 1+2 (Armor power crush) or SEN 4 (Safe mid). High: SEN 1 (Plus on block launcher).",
            "trap": "The Trap Setup: After ff+2 SEN 1 (+ on block), if opponent hesitates, hit them with cd+4 (Hellsweep) or HW 3+4 launcher.",
            "step": "Sidestep Left (SSL) evades ff+2, EWGF, and Sentai stance entries. Step-block to avoid her homing 3+4.",
            "minus": "-10 to -14 Punishable: df+1,1 (-12 on block), f+4 (-13). -15+ Launch Punishable: cd+4 Hellsweep (-23 Stagger Low Launch!), SEN 3 sweep (-20 Launch), HW 3+4 (-15 Launch).",
            "duck": "Immediately input a DICKJAB (db+1) upon blocking ff+2! This interrupts her Sentai transition and denies her entire 50/50 mix-up flow.",
            "parry": "In Heat, Reina auto-parries attacks while in Heaven's Wrath (HW d+1+2). Do NOT throw high/mid strikes; use Knees, Elbows, or Lows to break HW stance."
        },
        "jun": {
            "lore": "Wildlife Surveillance Officer and mother of Jin Kazama; returns from the sacred forests of Yakushima to purify the Devil Gene.",
            "poking": "Poking Buttons: 1, 2 (Punches into Izumo IZU stance), df+1 (Safe mid check), b+4,2 (Mid-high string), db+3 (Plus on hit low), f+4 (Plus on block high kick).",
            "pressure": "Pressure Moves: f+2,1+2 (Long range strike), Genjitsu Stance (GEN - b+3+4), Izumo Stance (IZU - u+1+2: safe mid and low options).",
            "mixup": "Upper/Mid/Low Mix-up (GEN & IZU): Low: GEN 4 (Low sweep with knockdown) or db+3. Mid: GEN 2 (Safe mid launcher) or IZU 1+2 (Guard crush).",
            "trap": "The Trap Setup: Harass with db+3 and 1,2 into IZU. When opponent freezes, use IZU 1+2 or command throw to break guard.",
            "step": "Sidestep Left (SSL) to evade Genjitsu stance pokes and f+2 lunges.",
            "minus": "-10 to -14 Punishable: f+2,1 (-13 punish), df+1,2 (-12). -15+ Launch Punishable: db+4 (-17 Stagger Low Launch!), Can-Can kicks d+3+4 (-15 Launch), IZU 4 (-16 Launch).",
            "duck": "1,2,2 and b+4,2 have high extensions: duck under them and launch with ws+2! Low parry db+3 with df.",
            "parry": "Jun can hold b+1+3 to extend her active reversal window. Crush her parry using Elbows (Paul df+1, Bryan b+1), Knees, or Weapon strikes."
        },
        "devil-jin": {
            "lore": "The demonic manifestation of Jin's cursed Mishima bloodline, consumed by destructive instincts.",
            "poking": "Poking Buttons: 1, 1 (1,1,2 knockdown string), df+1,2 (Mid check), db+2 (Ground hitting low), b+4 (Long range mid kick).",
            "pressure": "Pressure Moves: EWGF (f,n,d,df:2: +5 on block launcher!), f,f+4 (Safe mid poke), cd+3 (Long range tracking homing launcher).",
            "mixup": "Upper/Mid/Low Mix-up (Mishima Vortex): Low: Hellsweep (cd+4,4 - full knockdown sweep into combo). Mid: cd+1 (Mid launcher) or b+4.",
            "trap": "The Trap Setup: After knocking opponent down with Hellsweep, wave-dash in and mix cd+4 with fly stance mix-ups.",
            "step": "Sidestep Left (SSL) evades EWGF, b+4, and laser scrapers. Beware of cd+3 which tracks homing.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12 punish), b+1,2 (-13). -15+ Launch Punishable: Hellsweep cd+4,4 (-26 Stagger Low Launch!), cd+1 (-15 Launch), d+3+4 (-15 Launch).",
            "duck": "Laser attacks (1+2 or fly 1+2) are high: duck or sidestep! Block Hellsweep with db and launch for 85+ damage.",
            "parry": "Devil Jin's eye lasers and flying dives cannot be parried. Use standard parries against his standing punches and kicks."
        },
        "lars": {
            "lore": "Leader of the rebel army Yggdrasil; illegitimate son of Heihachi fighting alongside Jin to defeat Kazuya.",
            "poking": "Poking Buttons: 1, 2, df+1 (Standard mid check), db+1,3 (Low-high string), f+1,2,3 (Rush string into Silent Entry).",
            "pressure": "Pressure Moves: Dynamic Entry (DEN - f+3), Silent Entry (SEN - df+3), b+1 (Homing mid), fb+2,1 (Long range knockdown).",
            "mixup": "Upper/Mid/Low Mix-up: Low: DEN 2 (Low sweep) or SEN 2. Mid: DEN 3 (Safe mid) or SEN 1 (Mid launcher).",
            "trap": "The Trap Setup: Pressure with 1,2 into SEN, conditioning with SEN 1 mid, then sweep with SEN 2 low.",
            "step": "Sidestep Right (SSR) is extremely effective against Lars. Both Dynamic Entry and Silent Entry attacks whiff against SSR.",
            "minus": "-10 to -14 Punishable: fb+2,1 (-12 punish), f+1+2 (-12), df+2,1 (-13). -15+ Launch Punishable: db+4 (-15 Stagger Launch), DEN 2 sweep (-18 Launch), orbital uf+3 (-16 on block).",
            "duck": "When Lars enters DEN or SEN stance, immediately input a DICKJAB (db+1) to snuff out his flashy acrobatic mix-ups.",
            "parry": "Lars has no reversal. His kick strings from DEN and SEN are easily parried with standard punch/kick parries."
        },
        "lee": {
            "lore": "CEO of Violet Systems and adoptive son of Heihachi; tech genius aiding Jin with combat exosuits and robotics.",
            "poking": "Poking Buttons: 1, 2, df+1 (Fast mid check), b+4 (Keepout mid kick), d+3 (High-crushing low), f,f+3 (Long range mid).",
            "pressure": "Pressure Moves: Hitman Stance (HMS - 3+4), Acid Rain (1:3:3:3 just-frame), wr+3,4 (While running pressure).",
            "mixup": "Upper/Mid/Low Mix-up: Low: Slide (fc df,d,df+3) or HMS 3 (Low sweep). Mid: HMS 2 or ws+2,3 (Mid launcher).",
            "trap": "The Trap Setup: Keep out with b+4 into HMS cancel. When opponent rushes forward, launch with HMS 2 or Counter-Hit 4.",
            "step": "Sidestep Left (SSL) evades Lee's b+4 keepout, f,f+3, and Hitman stance entries.",
            "minus": "-10 to -14 Punishable: 1,2,4 (-13), df+1,2 (-12), b+1:1,2 (-14). -15+ Launch Punishable: Slide fc df,d,df+3 (-23 Stagger Low Launch!), d+4,4 (-16 Launch), HMS 3 sweep (-18 Launch).",
            "duck": "1,2,4 and Acid Rain have high extensions: duck under them and launch with ws+2! Block Slide with db and hopkick.",
            "parry": "Lee has a b+1+2 punch parry. Crush his parry with Knees (Bryan f+3, Lars b+4) or Elbows."
        },
        "xiaoyu": {
            "lore": "Chinese martial artist dedicated to saving Jin from his self-destructive path of vengeance.",
            "poking": "Poking Buttons: 1, d+2 (Fast low), df+1, b+1 (Fast 8-frame elbow check), f+1+2.",
            "pressure": "Pressure Moves: Art of Phoenix (AOP - d+1+2: ducks under mids), Rain Dance Stance (RDS - b+3+4), f,f+3 into RDS.",
            "mixup": "Upper/Mid/Low Mix-up: Low: AOP 4 (Low sweep) or RDS d+3. Mid: AOP 1+2 (Mid launcher) or RDS 4 (Tornado launcher).",
            "trap": "The Trap Setup: Enter AOP under opponent's mid checks. When their move whiffs overhead, launch with AOP uf+3 or AOP 1+2.",
            "step": "Sidestep Left (SSL) tracks Xiaoyu's evasive lateral shifts. Maintain Range 2 spacing.",
            "minus": "-10 to -14 Punishable: df+1 (-12 on poor spacing), 3,4 (-13). -15+ Launch Punishable: AOP 4 sweep (-17 Launch), RDS 4 (-16 Launch), Cali Roll ws+2 (-15 Launch).",
            "duck": "AOP ducks under standard mids! Beat AOP by using GROUND-HITTING MIDS (e.g. d+2, db+2, or stomps).",
            "parry": "Xiaoyu has evasive b+1 parries. Do not throw high punches; use Knees and heavy mids."
        },
        "hwoarang": {
            "lore": "Korean Taekwondo master and eternal rival to Jin Kazama, searching for him amidst the global conflict.",
            "poking": "Poking Buttons: 1, 2, df+1 (Mid check), d+3,4 (Low-high into Flamingo), b+3 (Safe keepout launcher on whiff).",
            "pressure": "Pressure Moves: Left Flamingo (LFS) and Right Flamingo (RFS), Peacekeeper (f,f+4: + on block), Backlash (3~4: armored high launcher).",
            "mixup": "Upper/Mid/Low Mix-up: Low: RFS d+4,3 (Sweeping low kick) or d+3,4. Mid: RFS 2 or LFS 3+4 (Power mid launcher).",
            "trap": "The Trap Setup: Land d+3,4 into Right Flamingo, then mix up RFS 2 (Mid safe) with RFS d+4,3 (Low).",
            "step": "Sidestep Left (SSL) evades Right Flamingo mix-ups and Peacekeeper f,f+4. Duck Left Flamingo moves.",
            "minus": "-10 to -14 Punishable: b+3 (-12 on block, -19 on whiff), f+1+2 (-13). -15+ Launch Punishable: d+4,4 (-15 Launch), RFS d+4,3 (-16 Launch), Backlash 3~4 (-10 duckable high).",
            "duck": "The second hit of d+3,4 is HIGH! Duck under the 2nd kick and launch with ws+2! Interrupt Flamingo flow with a DICKJAB (db+1).",
            "parry": "Low parry the 1st hit of d+3,4 with df. Standard kick parries catch his telegraphed high kicks."
        },
        "claudio": {
            "lore": "Leader of the Archers of Sirius, an ancient order of exorcists allied with Jin to banish the Devil Gene.",
            "poking": "Poking Buttons: 1, 2, df+1 (Fast mid check), b+3 (Safe knee), f+3 (Long range mid).",
            "pressure": "Pressure Moves: Superman Punch wr+2 (+6 on block into Starburst STB!), f+4 (Crouch-forcing mid: +4 on block).",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+3 or db+4,3. Mid: STB db+1+2 (Guard Break!) or uf+4 (Premier hopkick).",
            "trap": "The Trap Setup: wr+2 into Starburst, then frame-trap with STB df+1+2 or Guard Break db+1+2.",
            "step": "Sidestep Left (SSL) completely evades wr+2 Superman Punch and running attacks. Do not SSR due to b+1 tracking.",
            "minus": "-10 to -14 Punishable: b+3 (-13), df+1,2 (-13), f+2,2 (-12). -15+ Launch Punishable: Hopkick uf+4 (-13 pushback), STB d+2,2 (-15 Launch), STB f+1+2,1+2 (-15 Launch).",
            "duck": "When wr+2 is blocked, duck under high follow-ups. Duck his Starburst guard break db+1+2 on reaction.",
            "parry": "Claudio has no reversal. His wr+2 punch can be caught with high punch parries (Steve b+1+2, Bryan b+1+2)."
        },
        "zafina": {
            "lore": "Ancient Egyptian astrologer who sealed the spirit of the demon Azazel in her cursed left arm.",
            "poking": "Poking Buttons: 1, 3, df+1 (Mid check), db+3 (Low kick), b+1 (Mid check).",
            "pressure": "Pressure Moves: Scarecrow (SCR - 3+4), Tarantula (TRT - d+1+2), Mantis (MNT - d+3+4).",
            "mixup": "Upper/Mid/Low Mix-up: Low: TRT d+1+2 (Crawling low sweep) or SCR 4. Mid: SCR 2 or MNT 1 (Safe mid launcher).",
            "trap": "The Trap Setup: Crawl in Tarantula under highs and mids, then launch with TRT 2 or trip with TRT d+1+2.",
            "step": "Sidestep Left (SSL) evades Scarecrow and Tarantula forward lunges.",
            "minus": "-10 to -14 Punishable: df+1,4 (-12), b+1 (-13). -15+ Launch Punishable: d+3 sweep (-17 Launch), TRT d+1+2 (-18 Launch), SCR 4 (-16 Launch).",
            "duck": "In Tarantula stance she crawls on the floor: high strikes whiff! Use low stomps (d+4) or ground-hitting mids.",
            "parry": "Azazel cursed claw strikes cannot be parried. Block and punish accordingly."
        },
        "victor": {
            "lore": "French UN commander and founder of the Raven unit, wielding dual knives, high-tech katana, and pistols.",
            "poking": "Poking Buttons: 1, 1, df+1,1 (Mid check string), d+4 (Low poke), f+1+2.",
            "pressure": "Pressure Moves: Iai Stance (IAI - 3+4), Pistol shot (qcf+2), wr+2 (+5 on block sword slash).",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+4 (Sliding sword sweep) or IAI 4. Mid: IAI 2 (Safe mid launcher) or IAI 1+2.",
            "trap": "The Trap Setup: Fire pistol qcf+2 to condition standing block, then dash in with IAI 4 sweep or wr+2.",
            "step": "Sidestep Right (SSR) evades pistol shots, Iai stance slashes, and wr+2 approach tools.",
            "minus": "-10 to -14 Punishable: df+1,1 (-12), 2,2,2 (-13), 1+2 (-14). -15+ Launch Punishable: db+4 sword sweep (-18 Launch), IAI 4 (-16 Launch), teleport slash (-15 Launch).",
            "duck": "Pistol shots are HIGH: duck under them and launch with ws+2! Interrupt fake Iai stance transitions with a dickjab (db+1).",
            "parry": "Victor's SWORD and PISTOLS CANNOT be low-parried or caught with normal reversals! Block and punish."
        },
        "raven": {
            "lore": "Top-secret intelligence agent utilizing shadow clone ninjutsu to monitor the global clash between G-Corp and Yggdrasil.",
            "poking": "Poking Buttons: 1, 2, df+1 (Mid check), db+4 (Low sweep), 4,1 (High-mid check).",
            "pressure": "Pressure Moves: Shadow Clone dash (qcf+1+2), Soul Regalia (Heat clone rushes), b+1 (Armored clone strike).",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+4 (Sweep into tornado) or ws+1. Mid: uf+4 (Hopkick) or Hazan ws+2 (Mid launcher).",
            "trap": "The Trap Setup: Shadow clone teleport behind the opponent, forcing a quick high-low turn check.",
            "step": "Sidestep Left (SSL) evades shadow clone rushes and linear teleport strikes.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), 4,1 (-13). -15+ Launch Punishable: db+4 sweep (-17 Launch), Hazan ws+1 (-15 Launch), teleport dive (-16 Launch).",
            "duck": "Clone strikes have high properties: duck under clone teleports and float him out of the air with 1 jabs.",
            "parry": "Raven has a b+1+2 shadow substitution parry. Avoid multi-hit strings; rely on single heavy hits."
        },
        "alisa": {
            "lore": "Android combatant built by Dr. Bosconovitch; loyal bodyguard to Jin and Lars equipped with jet thrusters and chainsaws.",
            "poking": "Poking Buttons: 1, 1, df+1,1 (Mid check), d+3 (Low poke), b+1 (Homing mid), wr+2 (+ on block thruster).",
            "pressure": "Pressure Moves: Dual Chainsaws (DES - 1+2), wr+3,4 (Flying dive kicks: + on block), f+1+2 (Armored thrust).",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+3 (Low sweep) or DES d+1. Mid: DES f+1 (+3) or DES f+1+2 (Guard crush mid).",
            "trap": "The Trap Setup: Pin opponent with DES f+1 into DES d+1 low shredding. Without pushback, they cannot escape.",
            "step": "Sidestep Left (SSL) evades rocket punches, b+1, and wr+2. Avoid SSR against chainsaw mode.",
            "minus": "-10 to -14 Punishable: df+1,1 (-12), b+4,4 (-13). -15+ Launch Punishable: db+3 sweep (-17 Launch), fly 3+4 dive (-18 Launch), DES d+1 (-16 Launch).",
            "duck": "Rocket punch (1+2) is high: duck and launch with ws+2! Input a dickjab (db+1) against chainsaw pokes to break her DES stance.",
            "parry": "Alisa's CHAINSAWS CANNOT be parried! Do not attempt reversals; use Power Crush armor moves to disrupt her flow."
        },
        "nina": {
            "lore": "Legendary Irish assassin and former commander of G-Corporation's forces, armed with dual suppressed handguns.",
            "poking": "Poking Buttons: 1, 2, df+1,2 (Mid check string), d+4,1 (Low-high poke), b+1 (Safe homing check).",
            "pressure": "Pressure Moves: Hayashida Step (qcb), Butterfly loops (uf+4,3), Wipeout cancels (db+3), qcf+1 (+ on block high).",
            "mixup": "Upper/Mid/Low Mix-up: Low: d+3,2 or db+3 (Wipeout low sweep). Mid: df+3,2 (Mid launcher) or geisha roll 1+2.",
            "trap": "The Trap Setup: Continuous Hayashida cancels into df+1,2. If opponent tries to press, counter-hit with b+1.",
            "step": "Sidestep Right (SSR) evades Hayashida step cancels and df+1,2 strings.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), f+1+2 (-13). -15+ Launch Punishable: d+3,2 (-15 Launch), Wipeout db+3 (-17 Launch), geisha roll sweep (-18 Launch).",
            "duck": "The second hit of d+4,1 is HIGH! Duck under it and launch with ws+2. Interrupt Hayashida cancels with a dickjab (db+1).",
            "parry": "Nina has a standard b+1+3 / b+2+4 reversal. Break her reversal using Paul's df+1 elbow, Bryan's f+3 knee, or Feng's b+1+2 headbutt."
        },
        "jack-8": {
            "lore": "G-Corporation's flagship military cybernetic combatant, overhauled with heavy railguns and hydraulic thrusters.",
            "poking": "Poking Buttons: 1, 1, df+1,2 (Mid check), db+1 (Fast crouching low punch), ff+1 (Long reach mid).",
            "pressure": "Pressure Moves: Gamma Howl (GMH - 3+4), GMH 4 (+11 Guard Break!), f+1+2 (Armored double punch).",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+2 (Machine gun low sweep) or GMH 3. Mid: GMH 1 (Mid launcher) or GMH 2.",
            "trap": "The Trap Setup: At the wall, input GMH 4 (+11 Guard Break) for guaranteed follow-up punches and wall re-splats.",
            "step": "Sidestep Left (SSL) evades Gamma Howl lunges, db+1, and ff+1. Jack has a massive hurtbox; utilize maximum juggles.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), b+1,2 (-13), f+1+2 (-14). -15+ Launch Punishable: db+2 sweep (-18 Launch), GMH 2 (-16 Launch), Megaton punch (-17 Launch).",
            "duck": "Duck under GMH 4 guard break and launch with ws+2! Low parry db+1 low punch with df.",
            "parry": "Jack's brute punches can be parried, but his hydraulic rocket thrusts pierce through reversals."
        },
        "feng": {
            "lore": "Chinese Kempo master seeking ancient scrolls to attain the ultimate fighting state of the God Fist Dragon.",
            "poking": "Poking Buttons: 1, 2, df+1 (Tracks right, fast mid check), b+1 (i10 backfist check), d+2 (High-crushing low), db+3.",
            "pressure": "Pressure Moves: Kenpo Step (b+3+4), Shifting Clouds (STC - f+3+4), qcf+1 (+ on block palm strike).",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+4 (Sweeping low kick) or STC 4. Mid: STC 1 or f+3,4 (Safe mid launcher).",
            "trap": "The Trap Setup: Retreat with Kenpo Step. When opponent whiffs their attack in pursuit, launch with Kenpo 2.",
            "step": "Sidestep Left (SSL) evades Kenpo lunges, b+1, and STC mix-ups. Beware of df+1 which tracks right.",
            "minus": "-10 to -14 Punishable: b+1 (-12 punish), df+2,2 (-13), 1+2 (-14). -15+ Launch Punishable: db+4 sweep (-17 Launch), STC 4 sweep (-18 Launch), hopkick uf+4 (-13).",
            "duck": "Block db+4 sweep with db and launch for 80+ damage! Low parry d+2 low poke with df.",
            "parry": "Feng has 1+2 Sabaki and b+1+2 parries. Beat his parries with Knees (Bryan f+3, Lars b+4) or Weapons."
        },
        "dragunov": {
            "lore": "Russian Spetsnaz commander known as the 'White Angel of Death', ruthless and silent in neutral control.",
            "poking": "Poking Buttons: 1, 2, df+1,4 (Mid check string), d+2 (Premier high-crushing low poke), b+4,3 (Mid-high string).",
            "pressure": "Pressure Moves: Russian Assault wr+2 (+6 on block!), Sneak Stance (SNK - qcf), qcf+4 (Heavy plus-frame mid kick).",
            "mixup": "Upper/Mid/Low Mix-up: Low: d+2 or SNK 4 (Crouching low sweep). Mid: qcf+1 or qcf+2 (Safe mid launcher).",
            "trap": "The Trap Setup: Land wr+2 (+6 on block). If opponent presses any button, Counter-Hit with df+2 or throw with tackle.",
            "step": "Sidestep Right (SSR) is MANDATORY against Dragunov! wr+2, Sneak cancels, and qcf+4 all whiff cleanly against SSR. Do NOT SSL.",
            "minus": "-10 to -14 Punishable: 4,1 (-12), df+1,4 (-13), b+4,3 (-14). -15+ Launch Punishable: d+2 (-14 crouching punish), qcf+2 (-15 Launch), snake edge db+3 (-26 Launch).",
            "duck": "Never press buttons after blocking wr+2 (+6). Hold neutral guard or interrupt Sneak stance cancels with a dickjab (db+1).",
            "parry": "Dragunov has a b+1+3 reversal. Break it using Elbows (Paul df+1) or Knees. wr+2 can be caught with high punch parries."
        },
        "bryan": {
            "lore": "Cybernetic sociopath and former police detective turned anarchist, fueled by perpetual kinetic generators.",
            "poking": "Poking Buttons: 1, 2, df+1,1,1 (Mid check), 3+4 (Premier Range 2 keepout kick), d+2 (Safe mid check), b+1 (+3 on block).",
            "pressure": "Pressure Moves: Mach Punch (ff+2), b+1 (+3 on block!), Hatchet Kick (qcb+3: +5 on hit low!), Taunt (1+3+4).",
            "mixup": "Upper/Mid/Low Mix-up: Low: Hatchet Kick qcb+3 or Snake Edge df+3. Mid: Jet Upper fb+2 (i14 launcher) or f+3 (Knee).",
            "trap": "The Trap Setup: Taunt (1+3+4) against walled opponents grants unblockable +16 frames into free Jet Upper or Mach Punch.",
            "step": "Sidestep Left (SSL) evades Mach Punch ff+2, 3+4 keepout, and b+1. Beware of Hatchet Kick qcb+3 which clips SSR.",
            "minus": "-10 to -14 Punishable: df+1,1,1,1 (-13), f+4,1 (-13), 1+2 (-14). -15+ Launch Punishable: Snake Edge df+3 (-26 Stagger Low Launch!), qcb+4 (-15 Launch), Jet Upper fb+2 (-14 on block).",
            "duck": "Snake Edge (df+3) is slow and reactable: block with db and launch for 90+ damage! Stay grounded against Taunt setups.",
            "parry": "Bryan has a b+1+2 punch parry that counters with Mach Punch. Do NOT throw punches at him; use Knees (f+3) and Kicks."
        },
        "azucena": {
            "lore": "Peruvian MMA champion and 'Coffee Queen', using unorthodox dance-like evasions to promote her family farm.",
            "poking": "Poking Buttons: 1, 2, df+1,4 (Mid check string), d+3 (Low kick), 1,2,4, f+3 (Mid poke).",
            "pressure": "Pressure Moves: Running coffee charge wr+3,2 (+ on block), Libertador Stance (LIB - f+3+4: auto-evades highs/lows).",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+3 or LIB 4 (Low sweep). Mid: LIB 1+2 (Safe mid launcher) or LIB 2.",
            "trap": "The Trap Setup: Enter Libertador stance. When opponent instinctively throws a jab or low, auto-dodge and launch with LIB 1+2.",
            "step": "Sidestep Right (SSR) evades wr+3,2 running mix-ups and Libertador pokes.",
            "minus": "-10 to -14 Punishable: df+1,4 (-12), 1,2,4 (-13). -15+ Launch Punishable: db+3 sweep (-17 Launch), LIB 4 sweep (-16 Launch), hopkick uf+4 (-13).",
            "duck": "The 2nd hit of wr+3,2 is HIGH! Duck under it and launch with ws+2! Use MID BUTTONS (df+1, df+2) against Libertador stance.",
            "parry": "In Libertador stance, Azucena automatically parries Highs and Lows! ONLY attack her stance with MIDS or ELBOWS."
        },
        "king": {
            "lore": "Mexican masked luchador fighting to fund his orphanage, wielding legendary grappling techniques and chain throws.",
            "poking": "Poking Buttons: 1, 2, df+1 (Mid check), d+3 (Low poke), f,f+1 (Mid lunging check), b+1 (Fast counter-hit check).",
            "pressure": "Pressure Moves: Giant Swing (f,hcf+1), Shining Wizard (wr+2+4), Muscle Buster (qcb+1+2), Burning Knuckle (uf+1+2*).",
            "mixup": "The Grappler's Nightmare: Low: Ali Kicks (d+3+4) or low toe kick. Throw: Giant Swing (break 1) vs Shining Wizard (break 1+2). Mid: uf+4 hopkick.",
            "trap": "The Trap Setup: Condition opponent to stand with Giant Swing, then hopkick or crouch-grab (d+1+3) when they duck.",
            "step": "Sidestep Right (SSR) evades King's df+1, f,f+1, and running throw approaches. Duck under high throws.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), b+1,2 (-13), 1+2 (-14). -15+ Launch Punishable: Ali Kicks d+3+4 (-18 to -26 Stagger Low Launch!), hopkick uf+4 (-13), db+3 (-16 Launch).",
            "duck": "Low parry Ali Kicks on the 2nd kick with df! Break Giant Swing with 1, Shining Wizard with 1+2, and Tombstone with 2.",
            "parry": "King has separate parries: b+1+3 catches kicks (breaks leg); b+2+4 catches right punches (spins behind you). Use Elbows/Knees."
        },
        "paul": {
            "lore": "The hot-blooded American judo brawler striving to prove he is the absolute strongest fighter in the universe.",
            "poking": "Poking Buttons: 1, 2, df+1,1 (Mid check string), d+1 (Low checking palm), b+1 (Homing high check), f+2,3.",
            "pressure": "Pressure Moves: Phoenix Smasher Deathfist (qcf+2), b+1 (+3 on block homing), wr+2 (+ on block overhead).",
            "mixup": "The 50/50 Life Deletion: Low: Demoman (d+4,2:1+2 - clean hit knockdown sweep) vs Mid: Deathfist (qcf+2 - 55+ damage) or uf+4 hopkick.",
            "trap": "The Trap Setup: After wall splat, loop Demoman against standing guard, or launch with Deathfist when they crouch.",
            "step": "Sidestep Right (SSR) evades Deathfist qcf+2 and df+1. Beware of b+1 homing which clips sidesteps.",
            "minus": "-10 to -14 Punishable: df+1,1 (-12), b+1,2 (-13). -15+ Launch Punishable: Demoman d+4,2:1+2 (-17 Stagger Low Launch!), Deathfist qcf+2 (-17 Launch on block without pushback), hopkick uf+4 (-13).",
            "duck": "Block Demoman d+4 with db and launch with ws+2! The 2nd hit of 3,2 is high: duck and launch.",
            "parry": "Paul has a b+1+3 reversal. Break it using Elbows (df+1) and Knees (Bryan f+3)."
        },
        "law": {
            "lore": "Legendary martial arts master and chef inspired by Jeet Kune Do, competing to clear his restaurant debts.",
            "poking": "Poking Buttons: 1, 2, 3, df+1 (Fast mid check), d+2,3 (Low-high check), b+3 (Keepout kick), db+3 (Low kick).",
            "pressure": "Pressure Moves: Dragon Sign Stance (DSS), Junkyard Dog (b+2,3,4), wr+3 (+ on block flying dragon kick).",
            "mixup": "Upper/Mid/Low Mix-up: Low: Dragon Tail (db+4) or slide. Mid: Flip kick (uf+3,4) or DSS f+1 (Safe mid launcher).",
            "trap": "The Trap Setup: Pressure with Junkyard string. If opponent attempts to duck, switch to DSS mid launchers.",
            "step": "Sidestep Right (SSR) evades Dragon Sign pokes, 3+4, and DSS forward rushes.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), b+1,2 (-13). -15+ Launch Punishable: Dragon Tail db+4 (-26 Stagger Low Launch!), Flip Kick uf+3,4 (-15 Launch).",
            "duck": "The 2nd hit of Junkyard Dog (b+2,3,4) is LOW: immediately input df to LOW PARRY! Block Dragon Tail with db and launch for full combo.",
            "parry": "Law's Nunchucks and weapon moves cannot be parried. Normal kicks and punches can be deflected with standard parries."
        },
        "steve": {
            "lore": "British boxing champion and biological son of Nina Williams, fighting to discover the truth behind his origins.",
            "poking": "Poking Buttons: 1, 2, 1 (Fast jab strings), df+1 (Mid check), b+1 (Premier 13f Counter-Hit hook), d+1 (Low body blow).",
            "pressure": "Pressure Moves: Peekaboo Stance (PKB), Dempsey Roll (Heat), Sonic Fang (df+1+2), Ducking transitions (f+3 / f+4).",
            "mixup": "Upper/Mid/Low Mix-up: Low: PKB d+1 (Plus on hit low punch) or d+2. Mid: PKB 2 or Sonic Fang df+1+2.",
            "trap": "The Trap Setup: Throw b+1 hooks at Range 1. When opponent attempts to advance, b+1 scores a Counter-Hit full launch.",
            "step": "Sidestep Left (SSL) evades Peekaboo jabs and Sonic Fang df+1+2.",
            "minus": "-10 to -14 Punishable: Sonic Fang df+1+2 (-12 punish), b+1,2 (-13). -15+ Launch Punishable: d+2,1 (-15 Launch), PKB d+1 (-13), duck-in 2 (-14).",
            "duck": "Most of Steve's moves are HIGH! Duck under high hooks and launch with While Standing ws+2. Do not press buttons into b+1.",
            "parry": "Steve has a b+1+2 punch parry. Avoid throwing high punches; use Kicks, Knees, and Lows against him."
        },
        "asuka": {
            "lore": "Feisty Osaka high schooler and Kazama dojo master dedicated to keeping peace and purifying evil spirits.",
            "poking": "Poking Buttons: 1, 2, df+1 (Mid check), d+2 (Crouching mid check), db+3 (Low kick), b+3 (Evasive mid kick).",
            "pressure": "Pressure Moves: Naniwa Gusto (Heat charge), f+4 (Plus on block high kick), 1+2 (Power crush mid).",
            "mixup": "Upper/Mid/Low Mix-up: Low: Leg Cutter (db+4,4) or d+1+2 sweep. Mid: f+2 (Safe launcher on whiff) or b+3.",
            "trap": "The Trap Setup: Hesitate in neutral with b+3. When opponent dashes in, launch with f+2 or bait attacks into b+1+3 parry.",
            "step": "Sidestep Right (SSR) evades Asuka's f+2 launcher, b+3, and Leg Cutter db+4.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), 2,3 (-13), f+1+2 (-13). -15+ Launch Punishable: Leg Cutter db+4,4 (-18 Stagger Low Launch!), f+2 launcher (-18 on block!), Can-Can kicks d+3+4 (-15 Launch).",
            "duck": "Block Leg Cutter db+4 with db and launch for full combo! Duck under the 3rd hit of 1,2,4.",
            "parry": "Asuka's b+1+3 parry can be held for an extended active window! Crush her parry using ELBOWS (Paul df+1, Bryan b+1), KNEES, or WEAPONS."
        },
        "lili": {
            "lore": "Monaco billionaire heiress who incorporates ballet and rhythmic gymnastics into street fighting, obsessed with beating Asuka.",
            "poking": "Poking Buttons: 1, 2, df+1 (Mid check), d+3 (Low poke), f+2,3 (Mid-high string), 3,1.",
            "pressure": "Pressure Moves: Feisty Rabbit (RAB), Backturned Stance (BT), qcf+3 (Plus on block mid kick), wr+3.",
            "mixup": "Upper/Mid/Low Mix-up: Low: Matterhorn (d+3+4) or BT d+3+4 (Low sweep). Mid: Edelweiss (db+4) or BT 1+2.",
            "trap": "The Trap Setup: Backturned transitions into BT d+3+4 sweep vs BT 2 mid launcher.",
            "step": "Sidestep Left (SSL) evades Feisty Rabbit, Matterhorn, and qcf+3. Lili has an immense sidestep; use homing moves.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), f+2,3 (-13). -15+ Launch Punishable: Matterhorn d+3+4 (-24 Massive Launch!), BT d+3+4 sweep (-23 Stagger Low Launch!), Edelweiss db+4 (-26 Launch).",
            "duck": "Matterhorn and Edelweiss are slow, telegraphed sweeps: block with db and launch for 90+ damage! Interrupt BT stance with dickjabs.",
            "parry": "Lili's acrobatic kicks can be deflected with standard punch/kick parries."
        },
        "leo": {
            "lore": "German Bajiquan spelunker investigating G-Corporation and Kazuya to uncover the truth behind their mother's death.",
            "poking": "Poking Buttons: 1, 2, df+1 (Fast mid check), db+4 (Low sweep), b+1,4 (Mid-high string), f+4.",
            "pressure": "Pressure Moves: Fo Bu Stance (BOK - d+1+2), Jin Gang Stance (KNK), ff+2 (+ on block elbow).",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+4 or BOK 2 (Low sweep). Mid: BOK 1+2 or KNK 3,4 (Mid launcher).",
            "trap": "The Trap Setup: Transition into BOK stance. If opponent ducks expecting BOK 2, launch with BOK 1+2.",
            "step": "Sidestep Left (SSL) evades BOK stance lunges, df+1, and ff+2.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), b+1,4 (-13). -15+ Launch Punishable: db+4 sweep (-17 Launch), BOK 2 sweep (-18 Launch), hopkick uf+4 (-13).",
            "duck": "The 2nd hit of b+1,4 is high: duck and launch with ws+2! Interrupt BOK stance with a dickjab (db+1).",
            "parry": "Leo has b+1+3 / b+2+4 punch sabakis. Bajiquan elbows cannot be parried; use elbows against Leo."
        },
        "shaheen": {
            "lore": "Saudi military security specialist leading a private PMC, seeking justice for a friend assassinated by G-Corp.",
            "poking": "Poking Buttons: 1, 2, df+1 (Mid check), 4,1 (High-high counter check), db+2 (Low poke), d+4.",
            "pressure": "Pressure Moves: Stealth Dash (SNK - df+3), Slide (fc df,d,df+3), wr+2 (+ on block overhead).",
            "mixup": "Upper/Mid/Low Mix-up: Low: Slide fc df,d,df+3 or db+4. Mid: uf+4 (Hopkick) or SNK 2 (Safe mid launcher).",
            "trap": "The Trap Setup: Slide mix-up from full crouch. When opponent anticipates the slide and ducks, launch with uf+4.",
            "step": "Sidestep Left (SSL) evades Stealth Dash, 4,1 strings, and df+1.",
            "minus": "-10 to -14 Punishable: df+1 (-12 on spacing), 4,1 (-13), fb+2 (-14). -15+ Launch Punishable: Slide fc df,d,df+3 (-23 Stagger Low Launch!), hopkick uf+4 (-13), db+4 (-16 Launch).",
            "duck": "Block Slide with db and launch with maximum damage hopkicks! The 2nd hit of 4,1 is high: duck and launch.",
            "parry": "Shaheen has no special reversal. His kicks and pokes can be caught with standard parries."
        },
        "leroy": {
            "lore": "New York Wing Chun grandmaster who returned to take down the Mishima Zaibatsu and G-Corp alongside his pitbull Sugar.",
            "poking": "Poking Buttons: 1, 2, df+1,4 (Mid check string), d+3,2 (Low-mid check), b+3 (Mid kick), db+3.",
            "pressure": "Pressure Moves: Hermit Stance (HRM - 3+4), Twin Dragon Gate b+2 (Universal parry), wr+3.",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+3 or HRM 4 (Low sweep). Mid: HRM 1 or HRM 2 (Mid launcher).",
            "trap": "The Trap Setup: Enter Hermit stance with frame advantage. If opponent attacks, b+2 parries everything.",
            "step": "Sidestep Left (SSL) evades Hermit stance forward pokes and b+3.",
            "minus": "-10 to -14 Punishable: df+1,4 (-12), b+3 (-13). -15+ Launch Punishable: db+3 sweep (-17 Launch), HRM 4 sweep (-18 Launch), d+3,2 (-15 Launch).",
            "duck": "When Leroy enters Hermit stance (standing on one leg), immediately input a DICKJAB (db+1) to knock him out of stance.",
            "parry": "Leroy's b+2 Twin Dragon Gate deflects punches, kicks, elbows, and knees! Bypass it using LOW ATTACKS or WEAPONS."
        },
        "yoshimitsu": {
            "lore": "Mechanized leader of the chivalrous Manji Clan, wielding dual cursed katanas to redistribute wealth to the poor.",
            "poking": "Poking Buttons: 1, 1, df+1,2 (Mid check), d+2,2 (Mid low check), db+3,3,3 (Spinning low sweeps).",
            "pressure": "Pressure Moves: Flash (1+4: 6-frame parry hitbox!), Dragonfly (DGF - u+1+2), Kincho (KIN - 1+2), Bad Stomach poison.",
            "mixup": "Upper/Mid/Low Mix-up: Low: fc df+1 (Unblockable sword sweep) or db+3. Mid: ws+2,1 (Tornado launcher) or KIN 2.",
            "trap": "The Trap Setup: Flash (1+4) interrupts any opponent pressure at minus frames, converting into full launch.",
            "step": "Sidestep Left (SSL) evades Dragonfly and Kincho forward lunges. Never press buttons at -frames against Flash!",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), b+2,2 (-13). -15+ Launch Punishable: fc df+1 sword sweep (-23 Stagger Low Launch!), kangaroo kick 4~3 (-20 Launch), Flash 1+4 on block (-15 Launch).",
            "duck": "Jump or hopkick over unblockable fc df+1 sword sweep! Poison breath b+1+4 is high and duckable.",
            "parry": "Yoshimitsu's SWORD CANNOT be parried! Sword strikes ignore reversals completely; maintain spacing."
        },
        "kuma": {
            "lore": "Heihachi Mishima's loyal bodyguard and pet bear; learned Mishima style karate to avenge his fallen master.",
            "poking": "Poking Buttons: 2, 1 (10f string), df+1,2 (Mid check), db+2 (Fast low claw: +1 on hit), b+1 (Power crush mid).",
            "pressure": "Pressure Moves: Hunting Bear Stance (HBS - 3+4), f,f,f+1+2 (+5 on block into HBS!), Kuma Heat Electric (11f mid launcher in Heat!).",
            "mixup": "Upper/Mid/Low Mix-up: Low: HBS d+1+2 (Double low claw: +5 on hit) or HBS 2 (Roll). Mid: HBS 1+2 (Launcher). Throw: HBS f+1+2 (Bear bite).",
            "trap": "The Trap Setup: f,f,f+1+2 into Hunting Stance. Mix HBS d+1+2 low with HBS 1+2 mid launcher.",
            "step": "Sidestep Left (SSL) evades Hunting Bear Stance rushes and Bear Godfist.",
            "minus": "-10 to -14 Punishable: 2,1 (-12), df+1,2 (-12). -15+ Launch Punishable: db+2 (-15 Launch), HBS 2 roll (-18 Launch), d+1+2 bear sweep (-20 Launch).",
            "duck": "Kuma crawls on all fours in HBS: high punches whiff! Use ground-hitting mids (d+2, df+2). Break bear bite with 1+2.",
            "parry": "Kuma's headbutt and belly attacks cannot be parried. Claw attacks can be deflected."
        },
        "panda": {
            "lore": "Ling Xiaoyu's dedicated bodyguard and best friend; protects Xiaoyu as they search for Jin across the globe.",
            "poking": "Poking Buttons: 2, 1 (10f string), df+1,2 (Mid check), db+2 (Low claw), b+1 (Power crush).",
            "pressure": "Pressure Moves: Hunting Bear Stance (HBS - 3+4), f,f,f+1+2 (+5 on block into HBS!), Shochiku rolls.",
            "mixup": "Upper/Mid/Low Mix-up: Low: HBS d+1+2 (Double claw low) or HBS 2. Mid: HBS 1+2 (Launcher). Throw: HBS f+1+2 (Bite throw).",
            "trap": "The Trap Setup: Enter HBS stance with frame advantage. Opponent highs whiff over Panda's head; launch with HBS 1+2.",
            "step": "Sidestep Left (SSL) evades HBS rushes and Shochiku rolls.",
            "minus": "-10 to -14 Punishable: 2,1 (-12), df+1,2 (-12). -15+ Launch Punishable: db+2 (-15 Launch), HBS 2 roll (-18 Launch), d+1+2 sweep (-20 Launch).",
            "duck": "Do not throw highs at Panda in HBS stance; punish with mid launchers. Break bite throw with 1+2.",
            "parry": "Panda's belly flops and tail attacks cannot be parried. Claws can be deflected."
        },
        "heihachi": {
            "lore": "The legendary patriarch of the Mishima Zaibatsu; resurrected through mystical monks to reclaim his iron throne.",
            "poking": "Poking Buttons: 1, b+2 (-2 on block safe jab string), df+1 (Confirmable into df+1,2), f+3 (Fast mid knee).",
            "pressure": "Pressure Moves: EWGF (f,n,d,df:2: +5 on block high launcher!), f,f+2 (Demon Paw: safe mid gap-closer), 1,b+2.",
            "mixup": "Upper/Mid/Low Mix-up: Low: Hellsweep (cd+4,n,4) or db+2. Mid: EWGF or f,f+2 Demon Paw.",
            "trap": "The Trap Setup: Pressure with 1,b+2 into EWGF. If opponent attempts to challenge, Counter-Hit launch with f+3.",
            "step": "Sidestep Left (SSL) evades EWGF, f,f+2 Demon Paw, and 1,b+2. Beware of b+4 homing kick.",
            "minus": "-10 to -14 Punishable: 1,b+2 (-2 on block safe), df+1,2 (-13). -15+ Launch Punishable: Hellsweep cd+4,n,4 (-16 Launch), f,f+2 (-16 on block), hopkick uf+4 (-13).",
            "duck": "Block Hellsweep with db and launch for full combo! Do not counter hastily after 1,b+2.",
            "parry": "Heihachi has f+1+2 headbutt and b+1+2 parries. His headbutts are unparryable; use elbows and knees to break his parries."
        },
        "eddy": {
            "lore": "Capoeira prodigy who allied with Tekken Monks to atone for past misdeeds committed under G-Corporation.",
            "poking": "Poking Buttons: df+1,3, d+3 (Low into Negativa RLX), f,f+3 (Low kick into Handstand HSP + Mandinga level), 3,3,3,3.",
            "pressure": "Pressure Moves: Negativa Stance (RLX), Handstand Stance (HSP), Mandinga Level 2 empowerment.",
            "mixup": "Upper/Mid/Low Mix-up (RLX Negativa): Low: RLX 3,3 (50/50 low launcher at Mandinga Lv2!). Mid: RLX 4,3 (Safe mid tornado launcher!).",
            "trap": "The Trap Setup: Land f,f+3 to enter Handstand, build Mandinga level, then force 50/50 RLX 3,3 low vs RLX 4,3 mid.",
            "step": "Sidestep Left (SSL) evades Bananeira (HSP handstand) and Negativa (RLX) forward transitions.",
            "minus": "-10 to -14 Punishable: df+1,3 (-13), 3,3,3,3 string ender (-12). -15+ Launch Punishable: RLX 3,3 Mandinga low launcher (-18 Launch), HSP 4 sweep (-17 Launch), b+3,3 (-16 Launch).",
            "duck": "When Eddy sits in RLX or enters HSP handstand, immediately input a DICKJAB (db+1) to stop his flow! Duck under 3,3,3,3.",
            "parry": "Low parry Eddy's RLX ground kicks with df. Standard kick parries catch his acrobatic strikes."
        },
        "lidia": {
            "lore": "Prime Minister of Poland and traditional karate world champion, fighting to defend her homeland from Kazuya.",
            "poking": "Poking Buttons: 1, 2, 2 (Into Cat Stance), df+2 (Mid check into Horse Stance HRS), ff+2 (+5 on block into HRS!), db+3.",
            "pressure": "Pressure Moves: Horse Stance (HRS), Cat Stance (CAT), Heaven and Earth Stance (HAE in Heat: +12 Guard Break!).",
            "mixup": "Upper/Mid/Low Mix-up (HAE Stance in Heat): Unblockable High: HAE 1 (+12 guard break!). Mid: HAE 2 (+6 on block mid smash!).",
            "trap": "The Trap Setup: ff+2 (+5 on block) into HRS 2 mid or HRS 3 low sweep. In Heat, activate HAE 1 for guaranteed follow-up.",
            "step": "Sidestep Left (SSL) evades ff+2, Horse Stance, and Cat Stance forward lunges.",
            "minus": "-10 to -14 Punishable: 1,2,2 (-12), df+2 (-13). -15+ Launch Punishable: db+3 sweep (-17 Launch), HRS 4 sweep (-18 Launch), ff+2 (-14 pushback).",
            "duck": "HAE 1 guard break is high: DUCK under it and launch with ws+2! Interrupt Cat Stance with a dickjab (db+1).",
            "parry": "Lidia's traditional karate punches can be parried. Crush her own defensive parries using Elbows and Knees."
        },
        "clive": {
            "lore": "First Shield of Rosaria and Dominant of Ifrit (Final Fantasy XVI); master swordsman wielding Eikonic fire and steel.",
            "poking": "Poking Buttons: f+1+2 (Prominence: half-screen safe mid!), 1, 1, df+1,2, d+1 (Long range low sword poke).",
            "pressure": "Pressure Moves: Phoenix Shift (PHX - f+4), Titan Strike, Zantetsuken blade charges.",
            "mixup": "Upper/Mid/Low Mix-up (PHX Dash): Low: PHX 3 (Sliding sword sweep). Mid: PHX 2 / PHX 1+2 (Mid launcher). Throw: PHX 1+3 (Titan grab).",
            "trap": "The Trap Setup: Harass at mid-range with f+1+2 Prominence, then Phoenix Shift in with PHX 3 sweep or Titan grab.",
            "step": "Sidestep Right (SSR) evades Phoenix Shift dashes, Prominence f+1+2, and Titan slashes.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), 1,1 (-12). -15+ Launch Punishable: PHX 3 sliding sweep (-18 Launch), Prominence f+1+2 (-14 pushback), Titan smash (-16 Launch).",
            "duck": "Block PHX 3 low sliding sword sweep with db and launch! Duck under long range sword projectile attacks.",
            "parry": "Clive's INVICTUS SWORD CANNOT be low parried or caught with standard reversals! Block and punish."
        },
        "anna": {
            "lore": "Deadly assassin and former G-Corporation commander, locked in lifelong rivalry with her sister Nina.",
            "poking": "Poking Buttons: df+1,2 (Mid check string), d+4,1 (Low-high poke), qcf+1 (+ on block high CH launcher), b+2.",
            "pressure": "Pressure Moves: Chaos Judgment Stance (CJM - b+3: auto low reversals!), Full Crouch (FC) 50/50 cancels.",
            "mixup": "Full Crouch 50/50 Queen: Low: fc df+2 (Cold Blade: devastating low launcher!) vs Mid: ws+2 (15f mid launcher) or uf+1,3,3+4.",
            "trap": "The Trap Setup: Crouch into FC 50/50. Opponents cannot react between Cold Blade low launch and ws+2 mid launch.",
            "step": "Sidestep Right (SSR) evades Chaos Judgment stance entries, qcf+1, and df+1,2.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), f+1+2 (-13). -15+ Launch Punishable: Cold Blade fc df+2 (-18 Massive Launch!), d+4,1 (-13), ws+2 (-15 Launch).",
            "duck": "The 2nd hit of d+4,1 is high: duck and launch with ws+2! Block Cold Blade with db and launch for full combo.",
            "parry": "Anna auto-reverses low attacks in CJM stance (b+3)! Do NOT attack her stance with lows; use MIDS or ELBOWS."
        },
        "fahkumram": {
            "lore": "Legendary Muay Thai champion coerced into combat by the military to protect his captive family.",
            "poking": "Poking Buttons: bf+4 (Jet Kick: +6 on block!), 3 (Long range mid check with 3,1 and 3,4 extensions), d+4 (Fast shin low).",
            "pressure": "Pressure Moves: Charged strike strings (3,4~4* or f+3,2,4~3*: charged kick causes wall crush on block!), Ramasoon.",
            "mixup": "Upper/Mid/Low Mix-up: Low: 3,4~3 (Low kick sweep) vs Mid: 3,4~4* (Charged kick guard break).",
            "trap": "The Trap Setup: Push opponent to the wall, charge 3,4~4* for guaranteed wall crush, then follow with heavy mid combo.",
            "step": "Sidestep Left (SSL) evades Jet Kick bf+4, long range kicks, and charged guard breaks.",
            "minus": "-10 to -14 Punishable: 3,1 (-12), df+1,2 (-13). -15+ Launch Punishable: 3,4~3 low kick (-16 Launch), db+4 (-17 Launch), charged kick 3,4~4* (-14 on duck).",
            "duck": "Duck under charged kick 3,4~4* as it winds up and launch with ws+2! The 2nd hit of 3,1 is high: duck under it.",
            "parry": "Fahkumram's Muay Thai Elbows and Knees cannot be reversed! Low parry standard kicks with df."
        },
        "armor-king": {
            "lore": "Black Jaguar lucha libre wrestler seeking vengeance and personal score-settling against Marduk and King.",
            "poking": "Poking Buttons: df+1 (Premier grappler mid poke), d+3 (+1 on hit low), b+1 (12f CH launcher!), Dark Upper (cd+2), f,f,n,2.",
            "pressure": "Pressure Moves: Wave-dash into Giant Swing (f,hcf+1), Tombstone (db,f+2+4), Shining Black (wr+2+4), Dark Upper.",
            "mixup": "Wave-dash Grab/Mid Vortex: Wave-dash forward: mix Giant Swing / Tombstone grabs with Dark Upper (cd+2) or ws+1 mid launcher.",
            "trap": "The Trap Setup: Knock opponent down, wave-dash over their body, and mix f,f,n,2 low stun with Dark Upper.",
            "step": "Sidestep Left (SSL) evades Dark Upper cd+2, df+1, and f,f,n,2 low strikes. Tech or duck grabs.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), b+1,2 (-13). -15+ Launch Punishable: Dark Upper cd+2 (-15 Launch on block!), f,f,n,2 low stun (-18 Launch), hopkick uf+4 (-13).",
            "duck": "Block f,f,n,2 with db and launch! Break Giant Swing with 1, Tombstone with 2, and Shining Black with 1+2.",
            "parry": "Armor King has a b+1+3 / b+2+4 reversal. Break through his guard using Elbows (Paul df+1) or Knees (Bryan f+3)."
        },
        "miary-zo": {
            "lore": "Madagascan spiritual guardian fighting with traditional Morengy martial arts, channeling ancient primal energy.",
            "poking": "Poking Buttons: 1, 2, 4, df+1 (Mid check), d+3 (Fast low poke), f,f+3 (+ on block spiritual leap).",
            "pressure": "Pressure Moves: Primal Stance (PRM - d+3+4), Spiritual Leap (f,f+3), Ogre-style ancient guard break (PRM 1+2).",
            "mixup": "Upper/Mid/Low Mix-up (PRM Stance): Low: PRM 3 (Sweeping tail/leg low). Mid: PRM 2 (Mid launcher). Unblockable: PRM 1+2.",
            "trap": "The Trap Setup: Leap in with f,f+3 (+ on block) into Primal Stance, forcing 50/50 PRM 3 low vs PRM 2 mid.",
            "step": "Sidestep Left (SSL) evades Primal Stance lunges and spiritual leaps f,f+3.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), 1,2,4 (-13). -15+ Launch Punishable: PRM 3 sweeping tail/leg low (-18 Launch), PRM 1+2 guard break (-15 on duck), f,f+3 (-12).",
            "duck": "PRM 1+2 ancient guard break is high: duck and launch with ws+2! Block PRM 3 tail sweep with db and launch.",
            "parry": "Miary Zo's spiritual tail sweeps cannot be low parried. Standard punches and kicks can be deflected."
        },
        "kunimitsu": {
            "lore": "Fox-masked kunoichi and ninja thief, daughter of Kunimitsu I, continuing her family's treasure-hunting legacy.",
            "poking": "Poking Buttons: 2, 2, 2, 2 (Fast string into Setsuna SET dash), qcf+1 (Full-screen kunai throw!), df+1, db+3,3.",
            "pressure": "Pressure Moves: Setsuna Stance (SET), qcf+1 (Kunai throw), uf+3,4 (Acrobatic launcher), ws+3.",
            "mixup": "Upper/Mid/Low Mix-up: Low: SET 3 (Sliding low) or fc df+3 (Sweep launcher!). Mid: SET 2 (Safe mid) or ws+3 (Mid launcher).",
            "trap": "The Trap Setup: Fire qcf+1 kunai from full screen. If opponent blocks or hesitates, dash in with SET 3 low sweep.",
            "step": "Sidestep Left (SSL) evades Setsuna SET dash and qcf+1 kunai throws.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), 2,2,2,2 (-13). -15+ Launch Punishable: fc df+3 sweep (-20 Launch), SET 3 sliding low (-17 Launch), qcf+2 (-15 Launch).",
            "duck": "qcf+1 Kunai Throw is high: duck under it at full screen and dash in! Interrupt SET dash with a dickjab (db+1).",
            "parry": "Kunimitsu's thrown KUNAI DAGGER cannot be parried! Sword slashes bypass reversals; block and punish."
        },
        "bob": {
            "lore": "Freestyle karate bounty hunter who intentionally gained massive weight to achieve the ultimate blend of speed and mass.",
            "poking": "Poking Buttons: df+1 (Fast mid check), b+2,2, d+3+4 (Fast double low kicks), cd+1 (+ on block wave-dash high).",
            "pressure": "Pressure Moves: Spinner Ball Stance (BAL - f+3+4), Wave-dash, cd+1 (+ on block high punch).",
            "mixup": "Wave-dash 50/50: Low: cd+4,1+2 (Belly Hellsweep!) or db+3+4. Mid: uf+1+2,4 (Safe mid) or cd+2 (Mid launcher).",
            "trap": "The Trap Setup: Wave-dash into opponent's face: loop cd+4 Belly Hellsweep until they duck, then launch with cd+2.",
            "step": "Sidestep Right (SSR) evades Spinner Ball BAL, cd+1, and Belly Hellsweep cd+4.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), b+2,2 (-13). -15+ Launch Punishable: Belly Hellsweep cd+4,1+2 (-23 Stagger Low Launch!), db+3+4 (-17 Launch), BAL 3 (-16 Launch).",
            "duck": "Block Belly Hellsweep with db and launch for 85+ damage! Float Spinner Ball rolls out of the air with 1 jabs.",
            "parry": "Bob's heavy belly flops and shoulder tackles cannot be parried. Pokes can be deflected."
        },
        "roger-jr": {
            "lore": "Genetically modified boxing kangaroo created in G-Corp laboratories; fights alongside his mother from her pouch.",
            "poking": "Poking Buttons: 1, 2, 1 (Boxing jabs), d+3+4 (Tail low sweep), f,f+2 (Mid punch), b+1.",
            "pressure": "Pressure Moves: Animal Stance (ANM - b+3+4), Giant Swing (f,hcf+1), Animal Kicks (ANM 3,3,3).",
            "mixup": "Upper/Mid/Low Mix-up: Low: ANM 4 (Low sweep) or d+3+4 tail sweep. Mid: ANM 3,3,3 (Mid kick string) or Giant Swing.",
            "trap": "The Trap Setup: Mix up Giant Swing command grab with ANM 3,3,3 mid kicks against ducking opponents.",
            "step": "Sidestep Left (SSL) evades Animal Stance charges and tail sweeps.",
            "minus": "-10 to -14 Punishable: 1,2,1 (-12), f,f+2 (-13). -15+ Launch Punishable: d+3+4 tail low sweep (-20 Launch), ANM 4 sweep (-18 Launch), hopkick uf+4 (-13).",
            "duck": "Block d+3+4 tail sweep with db and launch with ws+2! Break Giant Swing throw with 1.",
            "parry": "Roger Jr.'s TAIL and marsupial kicks cannot be low parried! Boxing punches can be deflected."
        },
        "yujiro": {
            "lore": "'The Strongest Creature on Earth' (The Ogre from Baki); invincible martial artist who defeated modern armies barehanded.",
            "poking": "Poking Buttons: df+1 (Brute mid check), b+1 (Heavy chop: +5 on block!), d+2 (Crushing low punch), f+2.",
            "pressure": "Pressure Moves: Demon Back Awakening (Heat), Ear-drum slap (f,f+1+2*: Guard break -> Free combo!), b+1.",
            "mixup": "Upper/Mid/Low Mix-up: Low: db+4 (Leg-breaker sweep). Mid: df+2 / uf+2 (Brutal mid smash). Guard Break: f,f+1+2*.",
            "trap": "The Trap Setup: Push opponent to the wall, charge f,f+1+2* ear-drum slap for guard break into guaranteed full combo.",
            "step": "Sidestep Left (SSL) evades Heavy Chop b+1 and brute punches. Maintain safe distance.",
            "minus": "-10 to -14 Punishable: df+1,2 (-12), b+1 (-13). -15+ Launch Punishable: db+4 leg-breaker sweep (-24 Stagger Low Launch!), f,f+1+2* ear-slap (-16 on duck), df+2 (-15 Launch).",
            "duck": "f,f+1+2* Ear-drum slap is a high guard break: DUCK as it winds up and launch with ws+2! Block db+4 sweep with db.",
            "parry": "Yujiro's brute force strikes pierce through standard reversals! Do not attempt defensive parries against him."
        }
    }

    # Build character objects
    roster = []
    for meta in meta_list:
        cid, doc_num, slug, name, title, country, flag, faction, f_badge, season, style, weak_side, avatar = meta
        raw_name, block = raw_blocks[doc_num]
        sec = parse_sections(block)

        prof_line = sec.get('profile', '')
        height = ""
        weight = ""
        job_lore_ur = ""

        parts = [p.strip() for p in prof_line.split('|')]
        for p in parts:
            if p.startswith('Height:'):
                height = p.replace('Height:', '').strip()
            elif p.startswith('Weight:'):
                weight = p.replace('Weight:', '').strip()
            elif p.startswith('Job/History:'):
                job_lore_ur = p.replace('Job/History:', '').strip()

        if slug == "kuma":
            country = "Japan"
            flag = "🇯🇵"
            height = "290 cm (9'6\" - Standing)"
            weight = "360 kg"
            job_lore_ur = "Kuma Heihachi ka wafadar bodyguard aur pet hai; Heihachi ke marne ke baad Mishima style karate seekh kar Kazuya se badla lene aaya hai."
            avatar = "/assets/avatars/kuma.jpg"
        elif slug == "panda":
            country = "China"
            flag = "🇨🇳"
            height = "290 cm (9'6\" - Standing)"
            weight = "300 kg"
            job_lore_ur = "Ling Xiaoyu ki bodyguard aur best friend hai; Xiaoyu ki hifazat karte hue Jin ko dhoondne mein uski madad karti hai."
            avatar = "/assets/avatars/panda.jpg"

        poking_ur = sec.get('poking', '')
        pressure_ur = sec.get('pressure', '')
        mixup_ur = sec.get('mixup', '')
        jaal_ur = sec.get('jaal', '')

        if not pressure_ur and 'Poking & Pressure:' in poking_ur:
            content = poking_ur.replace('Poking & Pressure:', '').strip()
            poking_ur = f"Poking & Pressure: {content}"
            pressure_ur = f"Pressure & Stance Flows: {content}"

        if not jaal_ur:
            jaal_ur = f"Trap & Setup (Jaal): {mixup_ur}\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein."

        ed = english_dossiers[slug]

        char_obj = {
            "id": cid,
            "slug": slug,
            "name": name,
            "title": title,
            "country": country,
            "country_flag": flag,
            "faction": faction,
            "faction_badge": f_badge,
            "season": season,
            "style": style,
            "weak_side": weak_side,
            "avatar": avatar,
            "height": height,
            "weight": weight,
            # Primary English Fields (Default)
            "job_lore": ed["lore"],
            "poking_buttons": ed["poking"],
            "pressure_moves": ed["pressure"],
            "mixup_blender": ed["mixup"],
            "trap_setup": ed["trap"],
            # Bilingual Urdu Preservation
            "job_lore_ur": job_lore_ur,
            "poking_buttons_ur": poking_ur,
            "pressure_moves_ur": pressure_ur,
            "mixup_blender_ur": mixup_ur,
            "trap_setup_ur": jaal_ur,
            "anti_guide": {
                "weak_side": weak_side,
                # Primary English Fields (Default)
                "weak_side_detail": ed["step"],
                "minus_punishable_moves": ed["minus"],
                "bait_duck_interrupt": ed["duck"],
                "parry_vulnerabilities": ed["parry"],
                # Bilingual Urdu Preservation
                "weak_side_detail_ur": sec.get('step_ur', ed["step"]),
                "minus_punishable_moves_ur": sec.get('minus_ur', ed["minus"]),
                "bait_duck_interrupt_ur": sec.get('duck_ur', ed["duck"]),
                "parry_vulnerabilities_ur": sec.get('parry_ur', ed["parry"])
            }
        }
        roster.append(char_obj)

    print(f"Constructed {len(roster)} English-default character objects.")

    from build_strategy_data import build_universal_mechanics
    universal = build_universal_mechanics(raw_text)

    output_js_path = 'frontend/assets/js/tekken8MasterData.js'

    js_content = f"""/**
 * TEKKEN 8 MASTER STRATEGY HUB & ROSTER DATA LAYER
 * Authoritative Canonical Reference for 44 Characters (32 Base + 12 DLCs)
 * Universal Mechanics: Controls, Frame Data, Master Low Parry Matrix, Wall Traps & Escape Bible.
 * Primary Language: English (Default) with full bilingual Roman Urdu preservation.
 * Version: Tekken 8 Patch v3.00.02
 */

(function () {{
  'use strict';

  const UNIVERSAL_MECHANICS = {json.dumps(universal, indent=2, ensure_ascii=False)};

  const ROSTER_DATA = {json.dumps(roster, indent=2, ensure_ascii=False)};

  window.TEKKEN8_MASTER_DATA = {{
    universal: UNIVERSAL_MECHANICS,
    roster: ROSTER_DATA,
    getFighter: function (slug) {{
      if (!slug) return null;
      const s = String(slug).toLowerCase().trim();
      return ROSTER_DATA.find(f => f.slug === s || String(f.id) === s) || null;
    }},
    filterRoster: function (criteria) {{
      criteria = criteria || {{}};
      return ROSTER_DATA.filter(f => {{
        if (criteria.season && criteria.season !== 'ALL' && f.season !== criteria.season) return false;
        if (criteria.faction && criteria.faction !== 'ALL' && f.faction !== criteria.faction && f.faction_badge !== criteria.faction) return false;
        if (criteria.weak_side && criteria.weak_side !== 'ALL' && f.weak_side !== criteria.weak_side) return false;
        if (criteria.search) {{
          const q = criteria.search.toLowerCase().trim();
          const matchName = f.name.toLowerCase().includes(q);
          const matchCountry = f.country.toLowerCase().includes(q);
          const matchStyle = f.style.toLowerCase().includes(q);
          const matchTitle = f.title.toLowerCase().includes(q);
          if (!matchName && !matchCountry && !matchStyle && !matchTitle) return false;
        }}
        return true;
      }});
    }}
  }};

  console.log('✅ Tekken 8 Master Strategy Hub Data Layer Loaded: 44 Characters & Universal Mechanics (English Default).');
}})();
"""

    with open(output_js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Successfully generated {output_js_path} ({len(js_content)} bytes).")

if __name__ == '__main__':
    generate_file()
