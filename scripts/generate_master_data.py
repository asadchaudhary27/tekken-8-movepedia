"""
Authoritative generator for frontend/assets/js/tekken8MasterData.js
Combines 100% of the raw data from master_guide_extracted.txt with rich
anti-character frame metrics, weak sides, punishers, and bilingual tactical notes.
"""

import os
import re
import json

def generate_file():
    with open('master_guide_extracted.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Part 3 text
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

    print(f"Loaded {len(raw_blocks)} raw character blocks.")

    # We will build the 44 characters dataset
    roster = []

    # Helper to parse block text
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
    # (id, num_in_doc, slug, name, title, country, flag, faction, faction_badge, season, style, weak_side, avatar)
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

    # Detailed Anti-Character tactical packages tailored for Tekken 8 competitive play
    anti_packages = {
        "jin": {
            "step_ur": "Sidestep Left (SSL) karein taake EWHF, 2,1, aur f+4 hawa mein nikal jayein. Lekin Jin ka df+1 right track karta hai is liye mid-range par step-block karein.",
            "minus_punish_ur": "-10 to -14: 2,1,4 (-6 safe magar 3rd hit duckable), df+1,4 (-13 punish), d+2 (-14 crouching punish). -15+ Launch: d+3+4 Can-Can (-15 Launch), db+4 (-15 Launch on block), ZEN 4 diving sweep (-26 Launch).",
            "bait_duck_ur": "2,1,4 ka aakhri hit High hai: duck kar ke ws+2 launcher marein! d+2 ko duck kar ke block karein aur ws launch dein. ZEN 1+3 throw ko break ya duck karein. d+4 fast low poke ko df se Low Parry karein.",
            "parry_vuln_ur": "Jin ki b+1+3 parry har cheez (weapons, elbows, knees) deflect karti hai! Is se bachne ke liye delay timing karein ya low attacks marein jo b+1+3 se parry nahi hotay."
        },
        "kazuya": {
            "step_ur": "Sidestep Left (SSL) Kazuya ki sabse bari maut hai! EWGF, df+1, ff+3 aur cd+1+2 sab SSL par whiff ho jate hain. SSR ghalti se bhi mat karein warna Hellsweep clip karega.",
            "minus_punish_ur": "-10 to -14: 1,1,2 (-17 on block - launch!), df+1,2 (-12 punish), f+1+2 (-12). -15+ Launch: Hellsweep (cd+4,1 -23 Stagger Low Launch!), df+2 (-15 Mid Launcher), Twin Pistons ws+1,2 (-15 Launch).",
            "bait_duck_ur": "Wave-dash dekh kar ghabrayein mat. Hellsweep ko db se BLOCK karein (df parry mat karein) aur ws+2 se 85+ damage ka combo dein! 1,1,2 agar hit na ho toh 3rd hit block kar ke launch karein.",
            "parry_vuln_ur": "Kazuya ke paas normal parry nahi hai. Uske db+4 stature kick ko df se low parry karein. Kazuya ke f,f+3 mid kick aur EWGF punch parry ho sakte hain."
        },
        "reina": {
            "step_ur": "Sidestep Left (SSL) karein. ff+2, EWGF, aur Sentai (SEN) transitions SSL par hawa mein nikal jate hain.",
            "minus_punish_ur": "-10 to -14: df+1,1 (-12 punish), f+4 (-13). -15+ Launch: cd+4 Hellsweep (-23 Stagger Launch!), SEN 3 sweep (-20 Launch), HW 3+4 (-15 Launch).",
            "bait_duck_ur": "ff+2 block hote hi foran DICKJAB (db+1) marein! Yeh Reina ke Sentai flow ko wahin tod deta hai aur uski saari fake 50/50 options band kar deta hai.",
            "parry_vuln_ur": "Reina Heat mein Heaven's Wrath (HW d+1+2) mein auto-parry karti hai! HW mein khari ho toh punches/kicks mat marein, balke Elbows, Knees, ya Lows chalayein."
        },
        "jun": {
            "step_ur": "Sidestep Left (SSL) karein taake Genjitsu (GEN) aur Izumo (IZU) transitions aur f+2 whiff ho jayein.",
            "minus_punish_ur": "-10 to -14: f+2,1 (-13 punish), df+1,2 (-12). -15+ Launch: db+4 (-17 Stagger Launch!), can-can kicks d+3+4 (-15 Launch), Izumo 4 (-16 Launch).",
            "bait_duck_ur": "1,2,2 aur b+4,2 strings mein high extensions hain: duck kar ke ws+2 launcher marein! db+3 low poke ko df se low parry karein.",
            "parry_vuln_ur": "Jun b+1+3 parry ko hold kar sakti hai! Parry todne ke liye Elbows (Paul df+1, Bryan b+1), Knees, ya Weapons chalayein."
        },
        "devil-jin": {
            "step_ur": "Sidestep Left (SSL) karein. EWGF, b+4, aur laser scraper strings SSL par nikal jate hain. cd+3 homing se bach kar neutral rahein.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12 punish), b+1,2 (-13). -15+ Launch: Hellsweep (cd+4,4 -26 Stagger Launch!), cd+1 (-15 Launch), d+3+4 can-cans (-15 Launch).",
            "bait_duck_ur": "Laser attacks (1+2 ya fly 1+2) ko duck karein ya sidestep karein. Hellsweep ko db se block kar ke full combo ws launcher marein! Flying mix-up par 1 jab se float karein.",
            "parry_vuln_ur": "Devil Jin ke lasers aur fly moves parry nahi hotay. Lekin uske normal punches/kicks standard parry se pakray ja sakte hain."
        },
        "lars": {
            "step_ur": "Sidestep Right (SSR) Lars ke khilaf bohot effective hai. Dynamic Entry (DEN) aur Silent Entry (SEN) ke attacks SSR par whiff hotay hain.",
            "minus_punish_ur": "-10 to -14: fb+2,1 (-12 punish), f+1+2 (-12), df+2,1 (-13). -15+ Launch: db+4 (-15 Stagger Launch), DEN 2 sweep (-18 Launch), orbital kick uf+3 (-16 on block).",
            "bait_duck_ur": "Lars jab DEN ya SEN mein dash kare, toh foran DICKJAB (db+1) marein! Is se uski flashing movement aur high/mid mix-up foran cancel ho jata hai.",
            "parry_vuln_ur": "Lars ke paas koi special reversal nahi hai. Uske DEN kicks aur punch strings ko easy parry kiya ja sakta hai."
        },
        "lee": {
            "step_ur": "Sidestep Left (SSL) Lee ke b+4, f,f+3, aur Hitman (HMS) pokes ko aasani se evade karta hai.",
            "minus_punish_ur": "-10 to -14: 1,2,4 (-13), df+1,2 (-12), b+1:1,2 (-14). -15+ Launch: Slide fc df,d,df+3 (-23 Stagger Launch!), d+4,4 (-16 Launch), HMS 3 sweep (-18 Launch).",
            "bait_duck_ur": "Acid Rain aur 1,2,4 ke aakhri hits high hain: duck kar ke ws launcher marein! Slide ko db se block kar ke maximum damage hopkick marein.",
            "parry_vuln_ur": "Lee ke paas b+1+2 punch parry hai. Agar woh parry lagaye toh Knees (Bryan f+3, Lars b+4) ya Elbows marein jo Lee ki parry ko cheer deti hain."
        },
        "xiaoyu": {
            "step_ur": "Sidestep Left (SSL) AOP aur Rain Dance (RDS) ke sideway evasion ko track karta hai. Range 2 par safe spacing rakhein.",
            "minus_punish_ur": "-10 to -14: df+1 (-12 on bad spacing), 3,4 (-13). -15+ Launch: AOP 4 sweep (-17 Launch), RDS 4 (-16 Launch), Cali Roll ws+2 (-15 Launch).",
            "bait_duck_ur": "AOP (d+1+2) mein Xiaoyu ke niche Mids bhi nikal jate hain! AOP todne ke liye GROUND-HITTING MIDS (jaise d+2, db+2, ya low sweeps) marein.",
            "parry_vuln_ur": "Xiaoyu ke paas b+1 parry aur evasive stances hain. Us par high punches mat phenkein; Knees aur heavy mids use karein."
        },
        "hwoarang": {
            "step_ur": "Sidestep Left (SSL) Right Flamingo (RFS) aur Peacekeeper ko evade karta hai. Left Flamingo par sidestep na karein balke duck karein.",
            "minus_punish_ur": "-10 to -14: b+3 (-19 on whiff, -12 on block), f+1+2 (-13). -15+ Launch: d+4,4 (-15 Launch), RFS d+4,3 (-16 Launch), backlash 3~4 (-10 pushback).",
            "bait_duck_ur": "d+3,4 ka pehla hit Low aur 2nd hit HIGH hai! Pehle hit ke baad foran DUCK karein aur ws+2 se launch kar dein! Flamingo loop mein DICKJAB (db+1) lagayein.",
            "parry_vuln_ur": "Hwoarang ke d+3,4 ke low ko df se LOW PARRY karein. Uske sab kicks standard sabaki aur parries se pakray ja sakte hain."
        },
        "claudio": {
            "step_ur": "Sidestep Left (SSL) wr+2 (Superman Punch) aur running kicks ko pura whiff karwa deta hai. SSR mat karein kyunki b+1 track karta hai.",
            "minus_punish_ur": "-10 to -14: b+3 (-13), df+1,2 (-13), f+2,2 (-12). -15+ Launch: Hopkick uf+4 (-13 heavy pushback), STB d+2,2 (-15 Launch), STB f+1+2,1+2 (-15 Launch).",
            "bait_duck_ur": "wr+2 agar door se aaye toh SSL kar ke piche se launcher marein. Starburst (STB) active ho toh db+1+2 guard break se bachne ke liye interrupt karein.",
            "parry_vuln_ur": "Claudio ke paas koi reversal nahi hai. Uske superman punch wr+2 ko high punch parry (Steve b+1+2, Bryan b+1+2) se pakra ja sakta hai."
        },
        "zafina": {
            "step_ur": "Sidestep Left (SSL) Scarecrow (SCR) aur Tarantula (TRT) ke straight attacks ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,4 (-12), b+1 (-13). -15+ Launch: d+3 sweep (-17 Launch), TRT d+1+2 (-18 Launch), SCR 4 (-16 Launch).",
            "bait_duck_ur": "TRT stance mein zameen par crawl karti hai. Aise mein High punches bilkul miss ho jayenge; d+4 low stomps ya ground-hitting mids use karein.",
            "parry_vuln_ur": "Azazel claw attacks unparryable hain! Normal claw punches parry nahi hotay is liye block kar ke punish karein."
        },
        "victor": {
            "step_ur": "Sidestep Right (SSR) Victor ke pistol shots, Iai stance slashes aur wr+2 ko aasani se dodges karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,1 (-12), 2,2,2 (-13), 1+2 (-14). -15+ Launch: db+4 sword sweep (-18 Launch), IAI 4 (-16 Launch), teleport slash (-15 Launch).",
            "bait_duck_ur": "Pistol shots (qcf+2 ya string pistol) HIGH hotay hain: DUCK kar ke ws+2 launch karein! wr+2 block karne ke baad fake pressure ko dickjab karein.",
            "parry_vuln_ur": "Victor ki TALWAAR (Sword) aur PISTOL normal parry aur low parry se deflect NAHI hotay! Unko sirf block kar ke punish karein."
        },
        "raven": {
            "step_ur": "Sidestep Left (SSL) shadow clone gap-closers aur b+2 pokes ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), 4,1 (-13). -15+ Launch: db+4 sweep (-17 Launch), Hazan ws+1 (-15 Launch), teleport dive (-16 Launch).",
            "bait_duck_ur": "Clone attacks par ghabrayein mat; clones high hit hotay hain jinko duck kiya ja sakta hai. Teleport dekh kar 1 jab se float combo lein.",
            "parry_vuln_ur": "Raven ke paas b+1+2 shadow clone substitution parry hai. Multi-hit strings na lagayein, single heavy moves lagayein."
        },
        "alisa": {
            "step_ur": "Sidestep Left (SSL) rocket punches, b+1, aur wr+2 ko evade karta hai. SSR par DES chainsaw clip karti hai.",
            "minus_punish_ur": "-10 to -14: df+1,1 (-12), b+4,4 (-13). -15+ Launch: db+3 sweep (-17 Launch), fly 3+4 dive (-18 Launch), DES d+1 (-16 Launch).",
            "bait_duck_ur": "Rocket punch 1+2 high hai: duck kar ke ws launch marein! Chainsaw (DES) mein f+1 block kar ke dickjab (db+1) se chainsaw band karwayein.",
            "parry_vuln_ur": "Alisa ki CHAINSAWS (DES) normal parry se deflect nahi hotin! Unko parry karne ki koshish mat karein, armor move ya power crush se torein."
        },
        "nina": {
            "step_ur": "Sidestep Right (SSR) Hayashida step aur df+1,2 ko evade karta hai. Duck d+4,1 high string.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), f+1+2 (-13). -15+ Launch: d+3,2 (-15 Launch), wipeout db+3 (-17 Launch), Geisha roll sweep (-18 Launch).",
            "bait_duck_ur": "d+4,1 string ka doosra hit High hai: duck kar ke ws+2 launcher marein! Hayashida cancel pressure ko dickjab (db+1) se interrupt karein.",
            "parry_vuln_ur": "Nina ke paas b+1+3 / b+2+4 reversal hai. Usay todne ke liye Paul df+1 elbow, Bryan f+3 knee, ya Feng b+1+2 headbutt marein."
        },
        "jack-8": {
            "step_ur": "Sidestep Left (SSL) Gamma Howl (GMH) lunges, db+1, aur ff+1 ko evade karta hai. Jack ka hit-box bara hai is liye wide combos lagte hain.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), b+1,2 (-13), f+1+2 (-14). -15+ Launch: db+2 machine gun sweep (-18 Launch), GMH 2 (-16 Launch), Megaton punch (-17 Launch).",
            "bait_duck_ur": "GMH 4 guard break (+11) se bachne ke liye duck karein aur ws launcher marein! db+1 fast low punch ko df se Low Parry karein.",
            "parry_vuln_ur": "Jack-8 ke heavy punches normal parries se deflect ho sakte hain, lekin uske rocket arm moves parry nahi hotay."
        },
        "feng": {
            "step_ur": "Sidestep Left (SSL) Kenpo step pokes, b+1, aur STC mix-up ko evade karta hai. Lekin Feng ka df+1 right track karta hai.",
            "minus_punish_ur": "-10 to -14: b+1 (-12 punish), df+2,2 (-13), 1+2 (-14). -15+ Launch: db+4 sweep (-17 Launch), STC 4 sweep (-18 Launch), uf+4 hopkick (-13).",
            "bait_duck_ur": "Feng ke b+1 fast elbow ko block kar ke 12f punish dein. db+4 sweep ko db block kar ke 80+ damage ka launch karein. d+2 low poke ko df se Low Parry karein.",
            "parry_vuln_ur": "Feng ke paas 1+2 Sabaki parry aur b+1+2 parry hai. Feng ki parry todne ke liye Knees (Bryan f+3, Lars b+4) ya Weapons use karein."
        },
        "dragunov": {
            "step_ur": "Sidestep Right (SSR) Dragunov ke khilaf zaroori hai! wr+2 (Russian Assault), sneak cancels, aur qcf+4 SSR par whiff ho jate hain. SSL par clip ho jayenge.",
            "minus_punish_ur": "-10 to -14: 4,1 (-12), df+1,4 (-13), b+4,3 (-14). -15+ Launch: d+2 low poke (-14 crouching punish), qcf+2 (-15 Launch), snake edge db+3 (-26 Launch).",
            "bait_duck_ur": "wr+2 block hone ke baad +6 hota hai: ghalti se bhi button mat dabayein! Neutral block rakhein ya dickjab se sneak cancel torein.",
            "parry_vuln_ur": "Dragunov ke paas b+1+3 / b+2+4 reversal hai. Usay todne ke liye Elbows (Paul df+1) ya Knees marein. Dragunov ke wr+2 ko high punch parry kiya ja sakta hai."
        },
        "bryan": {
            "step_ur": "Sidestep Left (SSL) Bryan ke Mach Punch (ff+2), 3+4 keepout, aur b+1 ko evade karta hai. SSR par Hatchet kick qcb+3 clip karti hai.",
            "minus_punish_ur": "-10 to -14: df+1,1,1,1 (-13), f+4,1 (-13), 1+2 (-14). -15+ Launch: Snake Edge df+3 (-26 Massive Launch!), qcb+4 (-15 Launch), Jet Upper fb+2 (-14 on block).",
            "bait_duck_ur": "Snake Edge (df+3) dekhte hi db se BLOCK karein aur 90 damage ka full combo launch karein! Taunt (1+3+4) dekh kar delay wake-up karein ya jab se interrupt karein.",
            "parry_vuln_ur": "Bryan ke paas b+1+2 punch parry hai jo mach punch counter deti hai. Us par punches mat marein, Knees (f+3) aur Kicks use karein."
        },
        "azucena": {
            "step_ur": "Sidestep Right (SSR) wr+3,2 running mix-up aur Libertador pokes ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,4 (-12), 1,2,4 (-13). -15+ Launch: db+3 sweep (-17 Launch), LIB 4 low sweep (-16 Launch), hopkick uf+4 (-13).",
            "bait_duck_ur": "wr+3,2 ka dusra hit high hai: DUCK kar ke ws+2 launcher marein! Libertador (LIB) stance mein auto-dodge hota hai: aise mein MIDS ya ELBOWS marein.",
            "parry_vuln_ur": "Azucena Libertador stance mein khari ho kar Highs aur Lows auto-parry karti hai! Stance todne ke liye sirf MID BUTTONS (df+1, df+2) marein."
        },
        "king": {
            "step_ur": "Sidestep Right (SSR) King ke df+1, f,f+1, aur Giant Swing approach ko evade karta hai. Throws se bachne ke liye duck karein.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), b+1,2 (-13), 1+2 (-14). -15+ Launch: Ali kicks d+3+4 (-18 to -26 Stagger Launch!), hopkick uf+4 (-13), db+3 (-16 Launch).",
            "bait_duck_ur": "Ali kicks (d+3+4,4...) ko doosre hit par df se LOW PARRY karein! Giant Swing par 1 daba kar throw break karein, Shining Wizard par 1+2 break karein.",
            "parry_vuln_ur": "King ke paas b+1+3 (Kick parry) aur b+2+4 (Punch parry) alag hain! Kick parry se bachne ke liye Punches marein, aur Punch parry se bachne ke liye Elbows/Knees marein."
        },
        "paul": {
            "step_ur": "Sidestep Right (SSR) Deathfist (qcf+2) aur df+1 ko evade karta hai. Lekin b+1 homing se bach kar neutral block rakhein.",
            "minus_punish_ur": "-10 to -14: df+1,1 (-12), b+1,2 (-13). -15+ Launch: Demoman d+4,2:1+2 (-17 Stagger Launch on block!), Deathfist qcf+2 (-17 Launch on block without pushback), uf+4 hopkick (-13).",
            "bait_duck_ur": "Demoman (d+4) ko db se block kar ke ws+2 launcher marein! 3,2 high extension ko duck kar ke launch karein. Deathfist block ho toh long range launcher (f,f+2) marein.",
            "parry_vuln_ur": "Paul ke paas b+1+3 reversal hai. Reversal todne ke liye Paul ke apne jaise Elbows (df+1) aur Knees chalayein."
        },
        "law": {
            "step_ur": "Sidestep Right (SSR) Dragon Sign pokes, 3+4, aur DSS rushes ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), b+1,2 (-13). -15+ Launch: Junkyard b+2,3,4 (2nd hit low: Low Parry karein!), Dragon Tail db+4 (-26 Stagger Launch!), flip kick uf+3,4 (-15 Launch).",
            "bait_duck_ur": "Junkyard Dog (b+2,3,4) ka doosra hit Low hai: foran df dba kar LOW PARRY karein! Dragon Tail ko db se block kar ke full launch combo marein.",
            "parry_vuln_ur": "Law ke Nunchucks aur DSS weapon moves parry nahi hotay! Normal kicks aur punches parry ho sakte hain."
        },
        "steve": {
            "step_ur": "Sidestep Left (SSL) Steve ke Peekaboo (PKB) jabs aur Sonic Fang (df+1+2) ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: Sonic Fang df+1+2 (-12 punish), b+1,2 (-13). -15+ Launch: d+2,1 (-15 Launch), PKB d+1 (-13), duck in 2 (-14).",
            "bait_duck_ur": "Steve ke zyadatar attacks High hotay hain! High hooks ko DUCK kar ke While Standing ws+2 launcher marein. b+1 CH fish karne par forward moves mat dabayein.",
            "parry_vuln_ur": "Steve ke paas b+1+2 punch parry hai. Steve par punches ke bajaye Kicks, Knees, aur Lows use karein."
        },
        "asuka": {
            "step_ur": "Sidestep Right (SSR) Asuka ke f+2 launcher, b+3, aur Leg Cutter db+4 ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), 2,3 (-13), f+1+2 (-13). -15+ Launch: Leg cutter db+4,4 (-18 Stagger Launch!), f+2 launcher (-18 on block!), can-can kicks d+3+4 (-15 Launch).",
            "bait_duck_ur": "Leg Cutter (db+4,4) ko block kar ke ws launcher marein! 1,2,4 string ka 3rd hit high hai: duck kar ke launch karein.",
            "parry_vuln_ur": "Asuka ki b+1+3 parry bohot lambi hold hoti hai! Is par punches/kicks mat marein; ELBOWS (Paul df+1, Bryan b+1), KNEES, ya WEAPONS marein jo parry tod dete hain."
        },
        "lili": {
            "step_ur": "Sidestep Left (SSL) Feisty Rabbit, Matterhorn (d+3+4), aur qcf+3 ko evade karta hai. Lili ka apna sidestep bohot bara hai is liye homing moves use karein.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), f+2,3 (-13). -15+ Launch: Matterhorn d+3+4 (-24 Massive Launch!), Backturned BT d+3+4 sweep (-23 Stagger Launch!), Edelweiss db+4 (-26 Launch).",
            "bait_duck_ur": "Matterhorn aur Edelweiss slow sweeps hain: db se BLOCK karein aur 90 damage ka full combo launch karein! BT stance mein dickjab se interrupt karein.",
            "parry_vuln_ur": "Lili ke jumpy acrobatic attacks standard punch/kick parry se pakray ja sakte hain."
        },
        "leo": {
            "step_ur": "Sidestep Left (SSL) BOK stance lunges, df+1, aur ff+2 ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), b+1,4 (-13). -15+ Launch: db+4 sweep (-17 Launch), BOK 2 sweep (-18 Launch), hopkick uf+4 (-13).",
            "bait_duck_ur": "b+1,4 ka doosra hit high hai: duck kar ke ws+2 launcher marein! BOK stance mein aate hi dickjab (db+1) se attack interrupt karein.",
            "parry_vuln_ur": "Leo ke paas b+1+3 / b+2+4 punch sabakis hain. Bajiquan elbows parry nahi hotin, is liye Leo ke khilaf elbows use karein."
        },
        "shaheen": {
            "step_ur": "Sidestep Left (SSL) Stealth Dash, 4,1, aur df+1 ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1 (-12 on spacing), 4,1 (-13), fb+2 (-14). -15+ Launch: Slide fc df,d,df+3 (-23 Stagger Launch!), hopkick uf+4 (-13), db+4 (-16 Launch).",
            "bait_duck_ur": "Slide ko db se block kar ke hopkick launch marein! 4,1 string ka 2nd hit high hai: duck kar ke ws launcher marein.",
            "parry_vuln_ur": "Shaheen ke paas koi special reversal nahi hai. Uske kicks aur pokes standard parry se pakray ja sakte hain."
        },
        "leroy": {
            "step_ur": "Sidestep Left (SSL) Hermit (HRM) stance transitions aur b+3 ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,4 (-12), b+3 (-13). -15+ Launch: db+3 sweep (-17 Launch), HRM 4 sweep (-18 Launch), d+3,2 (-15 Launch).",
            "bait_duck_ur": "Hermit stance mein jab lero aik tang par khara ho, toh foran DICKJAB (db+1) marein! HRM mein woh block nahi kar sakta.",
            "parry_vuln_ur": "Leroy ki b+2 Twin Dragon Gate sab kuch (elbows, knees, punches) deflect karti hai! Is se bachne ke liye LOWS chalayein (b+2 lows deflect nahi karti) ya WEAPONS use karein."
        },
        "yoshimitsu": {
            "step_ur": "Sidestep Left (SSL) Dragonfly (DGF) aur Kincho (KIN) dashes ko evade karta hai. Qareeb mein minus frames par button dabane se bachein warna 1+4 Flash lag jayega!",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), b+2,2 (-13). -15+ Launch: fc df+1 sword sweep (-23 Stagger Launch!), kangaroo kick 4~3 (-20 Launch), flash 1+4 whiff/block (-15 Launch).",
            "bait_duck_ur": "fc df+1 unblockable sword sweep ko jump kar ke hopkick marein ya interrupt karein! Poison breath b+1+4 duckable hai.",
            "parry_vuln_ur": "Yoshimitsu ki TALWAAR (Sword) normal parry se deflect nahi hoti! Sword moves ko sirf block karein ya Flash se door spacing banayein."
        },
        "kuma": {
            "step_ur": "Sidestep Left (SSL) Hunting Bear Stance (HBS) lunges aur Bear Godfist ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: 2,1 (-12), df+1,2 (-12). -15+ Launch: db+2 (-15 Launch), HBS 2 roll (-18 Launch), d+1+2 bear sweep (-20 Launch).",
            "bait_duck_ur": "Hunting Stance (HBS) mein Kuma chaar taangon par crawl karta hai: High attacks miss ho jayenge! Ground-hitting mids (d+2, df+2) marein. Bear bite throw f+1+2 ko 1+2 se break karein.",
            "parry_vuln_ur": "Kuma ke claw attacks parry ho sakte hain, lekin uske Headbutt aur Belly attacks normal reversal se deflect nahi hotay!"
        },
        "panda": {
            "step_ur": "Sidestep Left (SSL) Hunting Bear Stance (HBS) lunges aur Shochiku rolls ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: 2,1 (-12), df+1,2 (-12). -15+ Launch: db+2 (-15 Launch), HBS 2 roll (-18 Launch), d+1+2 panda sweep (-20 Launch).",
            "bait_duck_ur": "Panda ke HBS stance mein high attacks na phenkein; mid launchers se punish karein. Panda bite throw f+1+2 ko 1+2 se break karein.",
            "parry_vuln_ur": "Panda ke pet (belly) aur tail attacks parry nahi hotay. Claws parry ho sakti hain."
        },
        "heihachi": {
            "step_ur": "Sidestep Left (SSL) EWGF, f,f+2 Demon Paw, aur 1,b+2 ko evade karta hai. b+4 homing move se bachne ke liye neutral block karein.",
            "minus_punish_ur": "-10 to -14: 1,b+2 (-2 on block safe), df+1,2 (-13). -15+ Launch: Hellsweep cd+4,n,4 (-16 Launch), f,f+2 (-16 on block), uf+4 hopkick (-13).",
            "bait_duck_ur": "Hellsweep ko db se block kar ke full combo ws launcher marein! 1,b+2 block kar ke jaldi mein counter na karein kyunki Heihachi ka recovery fast hai.",
            "parry_vuln_ur": "Heihachi f+1+2 headbutt aur b+1+2 parry karta hai. Uske headbutts unparryable hain, is liye elbows aur knees se uski parry torein."
        },
        "eddy": {
            "step_ur": "Sidestep Left (SSL) Bananeira (HSP handstand) aur Negativa (RLX) transitions ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,3 (-13), 3,3,3,3 string ender (-12). -15+ Launch: RLX 3,3 Mandinga low launcher (-18 Launch), HSP 4 sweep (-17 Launch), b+3,3 (-16 Launch).",
            "bait_duck_ur": "Eddy jab RLX zameen par baithe ya HSP handstand par jaye, toh foran DICKJAB (db+1) marein! Yeh uske flow ko wahi rok deta hai. 3,3,3,3 beginner string ko duck kar ke launch karein.",
            "parry_vuln_ur": "Eddy ke RLX ground kicks ko df se LOW PARRY karein. Uske acrobatic kicks standard kick parry se pakray ja sakte hain."
        },
        "lidia": {
            "step_ur": "Sidestep Left (SSL) ff+2, Horse Stance (HRS), aur Cat Stance (CAT) pokes ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: 1,2,2 (-12), df+2 (-13). -15+ Launch: db+3 sweep (-17 Launch), HRS 4 sweep (-18 Launch), ff+2 (-14 pushback).",
            "bait_duck_ur": "HAE 1 unblockable guard break high hai: DUCK kar ke ws launcher marein! Cat Stance mein aate hi dickjab (db+1) se attack interrupt karein.",
            "parry_vuln_ur": "Lidia ke traditional karate punches parry ho sakte hain. Lidia ki apni parry todne ke liye Elbows aur Knees use karein."
        },
        "clive": {
            "step_ur": "Sidestep Right (SSR) Phoenix Shift dash (PHX), Prominence (f+1+2), aur Titan slashes ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), 1,1 (-12). -15+ Launch: PHX 3 sliding sweep (-18 Launch), Prominence f+1+2 (-14 pushback), Titan smash (-16 Launch).",
            "bait_duck_ur": "PHX dash se aane wale low sword sweep ko db se block kar ke launch karein! Clive ke long range projectile f+2 ko duck karein.",
            "parry_vuln_ur": "Clive ki TALWAAR (Invictus Sword) normal parry aur low parry se deflect NAHI hoti! Sword slashes ko sirf block kar ke punish karein."
        },
        "anna": {
            "step_ur": "Sidestep Right (SSR) Chaos Judgment (CJM) stance entries, qcf+1, aur df+1,2 ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), f+1+2 (-13). -15+ Launch: Cold Blade fc df+2 (-18 Massive Launch!), d+4,1 (-13), ws+2 (-15 Launch).",
            "bait_duck_ur": "d+4,1 string ka doosra hit High hai: duck kar ke ws+2 launcher marein! Full Crouch (FC) 50/50 mein Cold Blade ko db se block kar ke full combo lein.",
            "parry_vuln_ur": "Anna CJM stance (b+3) mein auto-low reversal karti hai! CJM mein low attacks mat marein, sirf MIDS ya ELBOWS chalayein."
        },
        "fahkumram": {
            "step_ur": "Sidestep Left (SSL) Jet Kick (bf+4), long range knee pokes, aur string extensions ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: 3,1 (-12), df+1,2 (-13). -15+ Launch: 3,4~3 low kick (-16 Launch), db+4 (-17 Launch), charged kick 3,4~4* (-14 on duck).",
            "bait_duck_ur": "Charged kick 3,4~4* ko charge hote dekh kar DUCK karein aur ws+2 se launch karein! 3,1 string ka second hit high hai: duck karein.",
            "parry_vuln_ur": "Fahkumram ke Elbows aur Knees normal reversal se deflect nahi hotay! Normal kicks ko df se low parry karein."
        },
        "armor-king": {
            "step_ur": "Sidestep Left (SSL) Dark Upper (cd+2), df+1, aur f,f,n,2 ko evade karta hai. Throws se bachne ke liye tech ya duck karein.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), b+1,2 (-13). -15+ Launch: Dark Upper cd+2 (-15 Launch on block!), f,f,n,2 low stun (-18 Launch), hopkick uf+4 (-13).",
            "bait_duck_ur": "f,f,n,2 low ko db block kar ke ws launcher marein! Giant Swing par 1 break karein, Tombstone par 2 break karein, Shining Black par 1+2 break karein.",
            "parry_vuln_ur": "Armor King ke paas b+1+3 / b+2+4 reversal hai. Usay todne ke liye Elbows (Paul df+1) ya Knees (Bryan f+3) use karein."
        },
        "miary-zo": {
            "step_ur": "Sidestep Left (SSL) Primal Stance (PRM) lunges aur spiritual leaps (f,f+3) ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), 1,2,4 (-13). -15+ Launch: PRM 3 sweeping tail/leg low (-18 Launch), PRM 1+2 guard break (-15 on duck), f,f+3 (-12).",
            "bait_duck_ur": "PRM 1+2 ancient guard break high hai: duck kar ke ws launcher marein! PRM 3 tail sweep ko db block kar ke full combo lein.",
            "parry_vuln_ur": "Miary Zo ke spiritual energy attacks aur tail moves low parry nahi hotay! Normal punches/kicks parry ho sakti hain."
        },
        "kunimitsu": {
            "step_ur": "Sidestep Left (SSL) Setsuna (SET) dash aur Kunai throws (qcf+1) ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), 2,2,2,2 (-13). -15+ Launch: fc df+3 sweep (-20 Launch), SET 3 sliding low (-17 Launch), qcf+2 (-15 Launch).",
            "bait_duck_ur": "qcf+1 Kunai Throw high hai: full screen par duck karein aur dash in karein! SET dash par dickjab (db+1) se mix-up torein.",
            "parry_vuln_ur": "Kunimitsu ke KUNAI (Daggers) projectiles normal parry se deflect nahi hotay! Sword slashes ko block karein."
        },
        "bob": {
            "step_ur": "Sidestep Right (SSR) Spinner Ball (BAL), cd+1, aur Belly Hellsweep (cd+4) ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), b+2,2 (-13). -15+ Launch: Belly Hellsweep cd+4,1+2 (-23 Stagger Launch!), db+3+4 (-17 Launch), BAL 3 (-16 Launch).",
            "bait_duck_ur": "Wave-dash par db se BLOCK karein aur Belly Hellsweep ko ws+2 se full launch marein! Spinner Ball par 1 jab se float karein.",
            "parry_vuln_ur": "Bob ke Belly stomps aur heavy shoulder attacks normal parry se deflect nahi hotay. Pokes parry ho sakte hain."
        },
        "roger-jr": {
            "step_ur": "Sidestep Left (SSL) Animal Stance (ANM) charges aur tail sweeps ko evade karta hai.",
            "minus_punish_ur": "-10 to -14: 1,2,1 (-12), f,f+2 (-13). -15+ Launch: d+3+4 tail low sweep (-20 Launch), ANM 4 sweep (-18 Launch), hopkick uf+4 (-13).",
            "bait_duck_ur": "d+3+4 tail sweep ko db block kar ke ws launcher marein! Giant Swing throw par 1 daba kar break karein.",
            "parry_vuln_ur": "Roger Jr. ki DUM (Tail) aur Kangaroo kicks low parry nahi hotin! Normal boxing punches standard punch parry se pakray ja sakte hain."
        },
        "yujiro": {
            "step_ur": "Sidestep Left (SSL) Heavy Chop (b+1) aur brute punches ko evade karta hai. Distance maintain rakhein.",
            "minus_punish_ur": "-10 to -14: df+1,2 (-12), b+1 (-13). -15+ Launch: db+4 leg-breaker sweep (-24 Stagger Launch!), f,f+1+2* ear-slap guard break (-16 on duck), df+2 (-15 Launch).",
            "bait_duck_ur": "f,f+1+2* Ear-drum slap high guard break hai: dekhte hi DUCK karein aur ws+2 se launch kar dein! db+4 sweep ko db block kar ke 85+ damage lein.",
            "parry_vuln_ur": "Yujiro ka Demon Back awakening unblockable brute attacks deta hai jo normal reversal ko tor dete hain! Us par defensive parry ki koshish mat karein."
        }
    }

    # Generate each character object
    for meta in meta_list:
        cid, doc_num, slug, name, title, country, flag, faction, f_badge, season, style, weak_side, avatar = meta
        raw_name, block = raw_blocks[doc_num]
        sec = parse_sections(block)

        # Profile parsing
        prof_line = sec.get('profile', '')
        height = ""
        weight = ""
        job_lore = ""

        # Parse 'Country: ... | Height: ... | Weight: ... | Job/History: ...'
        parts = [p.strip() for p in prof_line.split('|')]
        for p in parts:
            if p.startswith('Height:'):
                height = p.replace('Height:', '').strip()
            elif p.startswith('Weight:'):
                weight = p.replace('Weight:', '').strip()
            elif p.startswith('Job/History:'):
                job_lore = p.replace('Job/History:', '').strip()

        # Handle Kuma vs Panda distinction
        if slug == "kuma":
            country = "Japan"
            flag = "🇯🇵"
            height = "290 cm (9'6\" - Standing)"
            weight = "360 kg"
            job_lore = "Kuma Heihachi ka wafadar bodyguard aur pet hai; Heihachi ke marne ke baad Mishima style karate seekh kar Kazuya se badla lene aaya hai."
            avatar = "/assets/avatars/kuma.jpg"
        elif slug == "panda":
            country = "China"
            flag = "🇨🇳"
            height = "290 cm (9'6\" - Standing)"
            weight = "300 kg"
            job_lore = "Ling Xiaoyu ki bodyguard aur best friend hai; Xiaoyu ki hifazat karte hue Jin ko dhoondne mein uski madad karti hai."
            avatar = "/assets/avatars/panda.jpg"

        poking_ur = sec.get('poking', '')
        pressure_ur = sec.get('pressure', '')
        mixup_ur = sec.get('mixup', '')
        jaal_ur = sec.get('jaal', '')

        # If DLC had combined poking & pressure
        if not pressure_ur and 'Poking & Pressure:' in poking_ur:
            # Clean up
            content = poking_ur.replace('Poking & Pressure:', '').strip()
            poking_ur = f"Poking & Pressure: {content}"
            pressure_ur = f"Pressure & Stance Flows: {content}"

        if not jaal_ur:
            jaal_ur = f"Trap & Setup (Jaal): {mixup_ur}\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein."

        anti = anti_packages.get(slug, {
            "step_ur": f"Sidestep {weak_side} ({weak_side}) is character ke main linear moves ko evade karta hai.",
            "minus_punish_ur": "-10 to -14 standing punish, -15+ launch punishable on unsafe sweeps.",
            "bait_duck_ur": "High attacks ko duck kar ke ws+2 launch karein aur fake stance flow par dickjab (db+1) marein.",
            "parry_vuln_ur": "Normal punches aur kicks standard parry se deflect hotay hain; elbows aur knees unparryable hain."
        })

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
            "job_lore_ur": job_lore,
            "poking_buttons_ur": poking_ur,
            "pressure_moves_ur": pressure_ur,
            "mixup_blender_ur": mixup_ur,
            "trap_setup_ur": jaal_ur,
            "anti_guide": {
                "weak_side": weak_side,
                "weak_side_detail_ur": anti["step_ur"],
                "minus_punishable_moves_ur": anti["minus_punish_ur"],
                "bait_duck_interrupt_ur": anti["bait_duck_ur"],
                "parry_vulnerabilities_ur": anti["parry_vuln_ur"]
            }
        }
        roster.append(char_obj)

    print(f"Constructed {len(roster)} character objects.")

    # Build universal mechanics
    from build_strategy_data import build_universal_mechanics
    universal = build_universal_mechanics(raw_text)

    # Output javascript file
    output_js_path = 'frontend/assets/js/tekken8MasterData.js'
    
    js_content = f"""/**
 * TEKKEN 8 MASTER STRATEGY HUB & ROSTER DATA LAYER
 * Authoritative Canonical Reference for 44 Characters (32 Base + 12 DLCs)
 * Universal Mechanics: Controls, Frame Data, Master Low Parry Matrix, Wall Traps & Escape Bible.
 * Version: Tekken 8 Patch v3.00.02
 */

(function () {{
  'use strict';

  const UNIVERSAL_MECHANICS = {json.dumps(universal, indent=2, ensure_ascii=False)};

  const ROSTER_DATA = {json.dumps(roster, indent=2, ensure_ascii=False)};

  // Expose on global window object
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

  console.log('✅ Tekken 8 Master Strategy Hub Data Layer Loaded: 44 Characters & Universal Mechanics.');
}})();
"""

    with open(output_js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Successfully generated {output_js_path} ({len(js_content)} bytes).")

if __name__ == '__main__':
    generate_file()
