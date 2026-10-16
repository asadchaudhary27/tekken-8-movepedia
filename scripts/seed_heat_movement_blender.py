"""
Seed Complete Heat Smashes Matrix, Movement Bible & Blender Protocol.
Populates:
1. character_heat_smashes (All 43 Fighters with full frame data, properties, counters)
2. movement_techniques (7 advanced movement techniques with SOCD shortcuts and sway warnings)
3. blender_scenarios (20 high-pressure vortex scenarios with frame situations, panic triggers, verified safe responses, risk/reward ratings, and practice drills)
Syncs SQLite tekken8_fyp.db and data/knowledge/master_compendium.json.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("tekken8_fyp.db")
COMPENDIUM_PATH = Path("data/knowledge/master_compendium.json")

# 1. SIX COMPETITIVE HEAT SMASH CATEGORIES (DANGER MATRIX)
HEAT_SMASH_CATEGORIES = [
    {
        "category": "Fastest Heat Smashes (i10–i14 Punish Tools)",
        "category_en": "Fastest Heat Smashes (i10–i14 Punish Tools)",
        "category_ur": "Sabse Tez Heat Smashes (i10–i14 Punishers)",
        "characters": "Jack-8 (i10!), Steve (i12), Lee (i12), Jun (i13), Victor (i13), Law (i14), Nina (i14), Clive (i14), Kunimitsu (i14)",
        "advantage_on_block": "-9 (Safe) / i10–i14 Punishers",
        "properties": "Startup: i10–i14 | Block: -9 (Safe) | Punishes any -10 to -14 move on reaction with full cinematic heat damage",
        "properties_en": "Startup: i10–i14 | Block: -9 (Safe) | Punishes any -10 to -14 move on reaction with full cinematic heat damage",
        "properties_ur": "Startup: i10–i14 | Block: -9 (Safe) | Opponent ke har -10 se -14 move ko reaction par full damage se punish karta hai",
        "counter_strategy": "Never throw unsafe pokes or -10 checks when these fighters are in Heat. Jack-8's Heat Smash is an i10 jab-speed punisher! Block is safe (-9), so do not attempt heavy launch punish; take your turn back with an i10 jab check.",
        "counter_strategy_en": "Never throw unsafe pokes or -10 checks when these fighters are in Heat. Jack-8's Heat Smash is an i10 jab-speed punisher! Block is safe (-9), so do not attempt heavy launch punish; take your turn back with an i10 jab check.",
        "counter_strategy_ur": "Jab yeh fighters Heat mein hon toh unsafe attacks ya -10 moves bilkul na karein. Jack-8 ka Heat Smash i10 jab ki speed se aata hai! Block par yeh -9 (Safe) hain, heavy launch punish ki koshish na karein.",
        "danger_and_counter": "Jack-8 (i10) aur Steve (i12) frame punishers hain. Block par -9 safe hain, is liye patient guard rakhein."
    },
    {
        "category": "Low Heat Smashes (Must Duck / Launch Punish)",
        "category_en": "Low Heat Smashes (Must Duck / Launch Punish)",
        "category_ur": "Low Heat Smashes (Crouch Duck / Launch Punish Zaroori!)",
        "characters": "Kazuya Mishima, Eddy Gordo, Claudio Serafino, Paul Phoenix, Lee Chaolan, Jin Kazama (ZEN.2+3)",
        "advantage_on_block": "-14 to -15 (Full Launch Punishable)",
        "properties": "Hit Level: Low | Block: -14 to -15 (Full Launch Punishable) | Pierces standing guard completely",
        "properties_en": "Hit Level: Low | Block: -14 to -15 (Full Launch Punishable) | Pierces standing guard completely",
        "properties_ur": "Hit Level: Low | Block: -14 se -15 (Full Launch Punishable) | Khare rehne par poora damage lagta hai",
        "counter_strategy": "These Heat Smashes hit Low! If you stand guard, you take 50+ unscaled damage. Read the startup timing or visual crouch dash cue and hold d/b (Crouch Guard). On block, they are -14 to -15: execute your character's optimal While Standing launcher (ws2, ws1,2, or hopkick) for a full round-winning launch combo!",
        "counter_strategy_en": "These Heat Smashes hit Low! If you stand guard, you take 50+ unscaled damage. Read the startup timing or visual crouch dash cue and hold d/b (Crouch Guard). On block, they are -14 to -15: execute your character's optimal While Standing launcher (ws2, ws1,2, or hopkick) for a full round-winning launch combo!",
        "counter_strategy_ur": "Yeh Heat Smashes Low hain! Agar aap khare block karenge toh poora damage lag jayega. Inke aate hi d/b (Crouch Guard) hold karein—block hone par yeh -14 se -15 Launch Punishable hain, apne character ka best While Standing (WS) launcher maarein!",
        "danger_and_counter": "Low hit level pierces standing block. Crouch block grants guaranteed WS launch punish."
    },
    {
        "category": "Long-Range / Fullscreen Projectile Heat Smashes",
        "category_en": "Long-Range / Fullscreen Projectile Heat Smashes",
        "category_ur": "Door Se Aane Wale / Projectile Heat Smashes",
        "characters": "Devil Jin (Psyche Laser), Victor Chevalier (Pistol Shot), Alisa Bosconovitch (Rocket Thruster), Jun Kazama (Light Beam), Clive Rosfield (Eikonic Flame), Raven (Shadow Clone Warp), Kunimitsu (Kunai Warp)",
        "advantage_on_block": "-9 (Safe) at Fullscreen / Huge Whiff Punish Threat",
        "properties": "Range: Range 3.0+ to Fullscreen | Hit Level: Mid or High/Mid | Evades neutral keepout",
        "properties_en": "Range: Range 3.0+ to Fullscreen | Hit Level: Mid or High/Mid | Evades neutral keepout",
        "properties_ur": "Range: Poori Screen (Range 3.0+) | Hit Level: Mid ya High/Mid | Neutral mein door se punish karta hai",
        "counter_strategy": "Never whiff attacks at long range when these fighters have Heat active! Jun and Clive can punish any whiff from across the entire arena. Maintain patient standing guard; linear projectiles like Devil Jin's laser and Victor's pistol can also be stepped with SSL/SSR outside close range.",
        "counter_strategy_en": "Never whiff attacks at long range when these fighters have Heat active! Jun and Clive can punish any whiff from across the entire arena. Maintain patient standing guard; linear projectiles like Devil Jin's laser and Victor's pistol can also be stepped with SSL/SSR outside close range.",
        "counter_strategy_ur": "Fullscreen par whiff karne ki ghalti hargiz na karein! Jun, Clive aur Victor poori screen ke doosre kone se whiff punish kar dete hain. Patient guard rakhein aur Devil Jin ke laser ko SSL karke dodge karein.",
        "danger_and_counter": "Fullscreen coverage snipes whiffs. Stay grounded and step linear beams at range."
    },
    {
        "category": "Massive Plus-on-Block into Stance Mixup (+6 to +12 on Block)",
        "category_en": "Massive Plus-on-Block into Stance Mixup (+6 to +12 on Block)",
        "category_ur": "Block Par Massive Plus (+6 se +12) Stance Mixup",
        "characters": "Reina (Heavens Wrath HW +8), Lars (DEN +6), Hwoarang (RFS +6), Lidia (HAE +8), Leo (BOK +6), Azucena (LIB +6), Miary Zo (BAO +6), Law (DSS +6), Lili (RAB +4), Xiaoyu (AOP +6), Shaheen (SNK +6), Yoshimitsu (KIN +5), Bob (SPB +6), Roger Jr (+6)",
        "advantage_on_block": "+6 to +12 (Forced Stance 50/50 Transition)",
        "properties": "Block: +6 to +12 (Automatic Stance Shift) | Opponent maintains active turn with guaranteed frame traps",
        "properties_en": "Block: +6 to +12 (Automatic Stance Shift) | Opponent maintains active turn with guaranteed frame traps",
        "properties_ur": "Block: +6 se +12 (Automatic Stance Shift) | Opponent ki baari rehti hai aur lethal frame traps bante hain",
        "counter_strategy": "NEVER press regular buttons after blocking these Heat Smashes! They are +6 to +12 on block and transition into lethal 50/50 stance options. Defensive Option Select: Use Raw Heat Burst (2+3) or an armored Power Crush to absorb their follow-up, or fuzzy guard the High/Mid options.",
        "counter_strategy_en": "NEVER press regular buttons after blocking these Heat Smashes! They are +6 to +12 on block and transition into lethal 50/50 stance options. Defensive Option Select: Use Raw Heat Burst (2+3) or an armored Power Crush to absorb their follow-up, or fuzzy guard the High/Mid options.",
        "counter_strategy_ur": "Inka Heat Smash block karne ke baad kabhi normal buttons na dabayein! Yeh block par +6 se +12 hote hain aur automatic stance mein chale jaate hain. Tod: 2+3 (Raw Heat Burst) ya Power Crush use karein warna patient guard rakhein.",
        "danger_and_counter": "Forced stance 50/50 at +6 to +12. Interrupt only with Armor / Heat Burst or fuzzy guard."
    },
    {
        "category": "Throw-on-Block / Unblockable Transition Heat Smashes",
        "category_en": "Throw-on-Block / Unblockable Transition Heat Smashes",
        "category_ur": "Throw-on-Block / Unblockable Transition Heat Smashes",
        "characters": "King (+10 into Jaguar Sprint JGS throw mixup), Nina Williams (+6 gunshot throw sequence), Jack-8 (Tackle cancel), Sergei Dragunov (Tackle / Floor Break loop), Armor King (+10 Shadow Step throw)",
        "advantage_on_block": "+10 into Stance (Guaranteed Unbreakable Throw Hazard)",
        "properties": "Properties: Triggers automatic cinematic throw transition or +10 sprint into unbreakable grapple",
        "properties_en": "Properties: Triggers automatic cinematic throw transition or +10 sprint into unbreakable grapple",
        "properties_ur": "Properties: Block hone par bhi automatic throw transition ya +10 unbreakable grapple sequence chalta hai",
        "counter_strategy": "King's Heat Smash deals 65 raw damage and enters Jaguar Sprint (JGS) at +10 where an unbreakable throw can land. You must Sidestep Right (SSR) or jab float the sprint on reaction! For Nina, duck the high gunshot follow-up to launch.",
        "counter_strategy_en": "King's Heat Smash deals 65 raw damage and enters Jaguar Sprint (JGS) at +10 where an unbreakable throw can land. You must Sidestep Right (SSR) or jab float the sprint on reaction! For Nina, duck the high gunshot follow-up to launch.",
        "counter_strategy_ur": "King ka Heat Smash 65 damage deta hai aur block hone par seedha Jaguar Sprint (+10) mein aata hai jahan se unbreakable throw lag sakta hai—foran Sidestep Right (SSR) karein ya jab float karein!",
        "danger_and_counter": "Blocks trigger grapple sequences. Sidestep the sprint or duck the follow-up."
    },
    {
        "category": "Wall Break / Floor Break / Balcony Break Heat Smashes",
        "category_en": "Wall Break / Floor Break / Balcony Break Heat Smashes",
        "category_ur": "Wall Break / Floor Break / Balcony Break Heat Smashes",
        "characters": "Bryan Fury (Hard Wall Break), Heihachi Mishima (Wall Splat/Break), Feng Wei (Wall Break), Fahkumram (Wall Break), Kuma (Wall Break), Panda (Wall Break), King (Floor Break on Sanctum/Descent), Kazuya (Floor Break), Dragunov (Floor Break)",
        "advantage_on_block": "Hard Stage Destruction on Hit / Wall Splat",
        "properties": "Stage Hazard Trigger: Shatters destructible walls, floors, and balconies for extended +30 DMG combo follow-ups",
        "properties_en": "Stage Hazard Trigger: Shatters destructible walls, floors, and balconies for extended +30 DMG combo follow-ups",
        "properties_ur": "Stage Hazard Trigger: Deewar aur zameen ko tod kar +30 damage ka extra combo deta hai",
        "counter_strategy": "On stages with destructible walls (e.g. Ortiz Farm, Rebel Hangar) or floors (Sanctum, Descent into Subconscious), these Heat Smashes lead to 80+ damage rounds. Never back yourself into a breakable wall when opponent is in Heat; maintain lateral movement.",
        "counter_strategy_en": "On stages with destructible walls (e.g. Ortiz Farm, Rebel Hangar) or floors (Sanctum, Descent into Subconscious), these Heat Smashes lead to 80+ damage rounds. Never back yourself into a breakable wall when opponent is in Heat; maintain lateral movement.",
        "counter_strategy_ur": "Deewar aur floor break stages par yeh Heat Smashes 80+ damage dete hain. Jab opponent Heat mein ho toh breakable deewar ke samnay khare na hon, sidestep se center stage par shift hon.",
        "danger_and_counter": "Triggers stage destruction. Avoid breakable walls when opponent has Heat active."
    }
]

# 2. ALL 43 FIGHTERS INDIVIDUAL HEAT SMASH ARSENAL DATA
CHARACTER_HEAT_SMASHES_DATA = [
    ("jin", "Jin Kazama", "in Heat 2+3 (or ZEN.2+3)", "i16 (ZEN i20)", "m, m (ZEN Low)", "50 DMG", "+5 Force Crouch (ZEN -15)", "Plus on Block Stance Mixup", "ZEN", "Floor Break", "Standard is +5 force crouch; ZEN is low sweep", "Standard block par +5 force crouch hai; ZEN version low sweep hai", "Stand block standard; duck ZEN low for full launch", "Standard ko stand block karein; ZEN low ko duck karke launch karein"),
    ("kazuya", "Kazuya Mishima", "in Heat 2+3", "i16", "l", "50 DMG", "-15 (Launch Punishable)", "Low (Must Duck / Launch Punish)", "None", "Floor Break", "Fast low hellsweep that pierces standing guard", "Tez low hellsweep jo standing guard ko todta hai", "Hold d/b on read; block grants guaranteed WS launch punish", "d/b crouch block karein; block par guaranteed WS launch punish lagayein"),
    ("reina", "Reina", "in Heat 2+3", "i16", "m, h, m", "50 DMG", "+8 into HW", "Massive Plus on Block Stance Mixup", "HW", "Wall Splat", "Forces Heavens Wrath stance at +8 on block", "Block par +8 Heavens Wrath stance mein jati hai", "Do not press buttons; use Raw Heat Burst or Power Crush", "Button na dabayein; Raw Heat Burst ya Power Crush se todien"),
    ("jun", "Jun Kazama", "in Heat 2+3", "i13", "m, m", "52 DMG", "-9 (Safe)", "Long-Range / Projectile", "None", "None", "i13 fullscreen light beam that recovers white health", "i13 poori screen ka light beam jo white health heal karta hai", "Never whiff at range; stand block or step left at distance", "Door se whiff na karein; stand block karein ya SSL karein"),
    ("king", "King", "in Heat 2+3", "i16", "m, m", "65 DMG", "+10 into JGS", "Throw-on-Block Transition", "JGS", "Floor Break / Wall Break", "Highest raw damage in T8; enters +10 Jaguar Sprint on block", "T8 ka sabse zyada damage; block par +10 Jaguar Sprint mein aata hai", "Sidestep Right (SSR) or jab float the sprint immediately", "Sidestep Right (SSR) karein ya foran jab float karein"),
    ("paul", "Paul Phoenix", "in Heat 2+3", "i20", "l", "55 DMG", "-15 (Launch Punishable)", "Low (Must Duck / Launch Punish)", "None", "Wall Break", "Heavy low tackle sweep with massive clean-hit damage", "Bari low sweep tackle jo clean hit par massive damage deti hai", "Crouch block on reaction/read; WS launch punish", "Crouch block karein aur WS launch punish lagayein"),
    ("hwoarang", "Hwoarang", "in Heat 2+3", "i16", "m, m", "50 DMG", "+6 into RFS", "Massive Plus on Block Stance Mixup", "RFS", "Wall Splat", "Forces Right Flamingo Stance at +6 on block", "Block par +6 Right Flamingo Stance mein aata hai", "Do not jab mash; fuzzy guard or use dickjab db+1", "Jab mash na karein; fuzzy guard ya dickjab db+1 use karein"),
    ("alisa", "Alisa Bosconovitch", "in Heat 2+3", "i16", "h, m", "50 DMG", "+4 into DES", "Long-Range / Projectile", "DES", "None", "Long-range rocket thrust into Dual Chainsaws", "Door se rocket thrust jo Dual Chainsaws mein jati hai", "Block and prepare for chainsaw mixup; step left in neutral", "Block karein aur chainsaw mixup ke liye tayar rahein"),
    ("asuka", "Asuka Kazama", "in Heat 2+3", "i16", "m, m", "52 DMG", "-9 (Safe)", "Fastest Punisher (i10-i14)", "None", "Wall Splat", "Safe on block; activates full Naniwa Gusto charge on hit", "Block par safe hai; hit hone par Naniwa Gusto charge deti hai", "Stand block is safe; take your turn with i10 jab poke", "Stand block safe hai; block ke baad i10 jab se turn lein"),
    ("azucena", "Azucena Milagros", "in Heat 2+3", "i16", "m, m", "50 DMG", "+6 into LIB", "Massive Plus on Block Stance Mixup", "LIB", "Wall Splat", "Transitions into Libertador auto-dodge stance at +6", "Block par +6 Libertador auto-dodge stance mein jati hai", "Do not press highs or mids; use low poke or armor", "High ya mid na marein; low poke ya armor move use karein"),
    ("bryan", "Bryan Fury", "in Heat 2+3", "i16", "m, m", "55 DMG", "-9 (Safe)", "Wall Break / Floor Break / Balcony Break Heat Smashes", "None", "Hard Wall Break", "Safe mid smash that activates Snake Eyes and breaks walls", "Safe mid smash jo Snake Eyes activate karta hai aur deewar todta hai", "Stand block; avoid having your back to destructible walls", "Stand block karein; deewar ke paas khare na hon"),
    ("claudio", "Claudio Serafino", "in Heat 2+3", "i20", "l", "50 DMG", "-14 (WS Punishable)", "Low (Must Duck / Launch Punish)", "None", "Wall Splat", "Low-sweeping Starburst strike that pierces guard", "Low Starburst sweep jo guard ko todti hai", "Duck on read; punish with i14 WS launcher or ws1,2", "Duck karein aur i14 WS launcher se punish karein"),
    ("devil-jin", "Devil Jin", "in Heat 2+3", "i16", "m, m", "53 DMG", "-9 (Safe)", "Long-Range / Projectile", "None", "Wall Break", "Fullscreen demonic laser sweep that catches whiffs", "Fullscreen demonic laser sweep jo door se pakarti hai", "Stand block or Sidestep Left (SSL) at long range", "Stand block karein ya long range par SSL karein"),
    ("dragunov", "Sergei Dragunov", "in Heat 2+3", "i16", "m, m", "54 DMG", "+6 into SNK", "Throw-on-Block Transition", "SNK", "Floor Break / Wall Break", "Enters Sneak stance at +6 or triggers tackle grapple", "Sneak stance mein +6 par jata hai aur tackle lagata hai", "Use Power Crush or backdash; duck high extensions", "Power Crush use karein ya backdash karein"),
    ("feng", "Feng Wei", "in Heat 2+3", "i16", "m, m", "52 DMG", "-9 (Safe)", "Wall Break / Floor Break / Balcony Break Heat Smashes", "None", "Wall Break", "Safe mid punch that causes massive pushback and wall splat", "Safe mid punch jo heavy pushback aur wall splat deta hai", "Stand block is safe; do not whiff against his keepout", "Stand block safe hai; keepout ke samnay whiff na karein"),
    ("jack-8", "Jack-8", "in Heat 2+3", "i10", "h", "50 DMG", "-9 (Safe)", "Fastest Heat Smashes (i10–i14 Punish Tools)", "None", "Floor Break", "i10 fastest Heat Smash in Tekken 8! Frame punishes jabs", "Tekken 8 ka sabse tez i10 Heat Smash! Jabs ko punish karta hai", "Never execute -10 moves when Jack has Heat; stand block", "Jack Heat mein ho toh -10 moves na karein; stand block karein"),
    ("lars", "Lars Alexandersson", "in Heat 2+3", "i16", "m, m", "50 DMG", "+6 into DEN", "Massive Plus on Block Stance Mixup", "DEN", "Wall Splat", "Enters Dynamic Entry at +6 on block with lightning speed", "Block par +6 Dynamic Entry mein bijli ki tarah jata hai", "Interrupt with dickjab db+1 or hold patient guard", "Dickjab db+1 se interrupt karein ya patient guard rakhein"),
    ("law", "Marshall Law", "in Heat 2+3", "i14", "m, m", "50 DMG", "+6 into DSS", "Fastest Heat Smashes (i10–i14 Punish Tools)", "DSS", "Wall Splat", "i14 fast punisher into Dragon Sign Stance +6", "i14 tez punisher jo Dragon Sign Stance mein +6 par jata hai", "Do not press buttons; block mid or duck high nunchaku", "Button na dabayein; mid block karein ya high duck karein"),
    ("lee", "Lee Chaolan", "in Heat 2+3", "i12", "l", "50 DMG", "-15 (Launch Punishable)", "Fastest Heat Smashes (i10–i14 Punish Tools)", "None", "Wall Splat", "i12 fast low sweep; excellent fast punisher", "i12 tez low sweep; fastest low punisher", "Crouch block on read; on block it is -15 for full WS launch", "Crouch block karein; block par -15 launch punish lagayein"),
    ("leo", "Leo Kliesen", "in Heat 2+3", "i16", "m, m", "50 DMG", "+6 into BOK", "Massive Plus on Block Stance Mixup", "BOK", "Wall Splat", "Transitions into Bokaho stance at +6 on block", "Block par +6 Bokaho stance mein jata hai", "Dickjab db+1 interrupts slow stance options", "Dickjab db+1 se slow stance options ko interrupt karein"),
    ("leroy", "Leroy Smith", "in Heat 2+3", "i16", "m, m", "52 DMG", "-9 (Safe)", "Fastest Punisher (i10-i14)", "None", "Wall Splat", "Safe mid staff strike; summons cane strike on command", "Safe mid chhari strike jo cane attack trigger karta hai", "Stand block is safe; do not press into his parry", "Stand block safe hai; uske parry ke andar attack na karein"),
    ("lili", "Lili", "in Heat 2+3", "i16", "m, m", "50 DMG", "+4 into RAB", "Massive Plus on Block Stance Mixup", "RAB", "Wall Splat", "Flips into Feisty Rabbit stance at +4 on block", "Block par +4 Feisty Rabbit stance mein flip karti hai", "Side-walk left or use fast mid check", "Side-walk left karein ya fast mid check maarein"),
    ("xiaoyu", "Ling Xiaoyu", "in Heat 2+3", "i16", "m, m", "50 DMG", "+6 into AOP", "Massive Plus on Block Stance Mixup", "AOP", "Wall Splat", "Enters Art of Phoenix (AOP) under-crush stance at +6", "Block par +6 Art of Phoenix stance mein jati hai", "Never press highs; use low-hitting mid or low poke", "High attacks bilkul na marein; low-hitting mid attack karein"),
    ("shaheen", "Shaheen", "in Heat 2+3", "i16", "m, m", "50 DMG", "+6 into SNK", "Massive Plus on Block Stance Mixup", "SNK", "Wall Splat", "Surfs into Stealth Step at +6 on block", "Block par +6 Stealth Step slide mein surf karta hai", "Hold standing guard; duck high slide extension on read", "Stand guard rakhein; high extension ko read karke duck karein"),
    ("steve", "Steve Fox", "in Heat 2+3", "i12", "h, m", "50 DMG", "-9 (Safe)", "Fastest Heat Smashes (i10–i14 Punish Tools)", "None", "Wall Splat", "i12 ultra-fast boxing punch combination punisher", "i12 nihayat tez boxing punisher", "Do not execute unsafe moves; stand block and take turn", "Unsafe moves na karein; stand block karke turn wapas lein"),
    ("victor", "Victor Chevalier", "in Heat 2+3", "i13", "m, m", "52 DMG", "-9 (Safe)", "Long-Range / Projectile", "None", "Wall Splat", "i13 fullscreen pistol shot into katana slash", "i13 poori screen ka pistol shot into katana slash", "Stand block; sidestep right at range to avoid tracking", "Stand block karein; door se SSR karke dodge karein"),
    ("yoshimitsu", "Yoshimitsu", "in Heat 2+3", "i16", "m, m", "50 DMG", "+5 into KIN", "Massive Plus on Block Stance Mixup", "KIN", "Wall Splat", "Transitions into Kincho stance at +5 on block", "Block par +5 Kincho stance mein transition karta hai", "Beware of Flash; use patient guard or backdash", "Flash se bach kar rahein; patient guard ya backdash karein"),
    ("zafina", "Zafina", "in Heat 2+3", "i16", "m, m", "50 DMG", "+6 into TRT", "Massive Plus on Block Stance Mixup", "TRT", "Wall Splat", "Crawls into Tarantula stance at +6 on block", "Block par +6 Tarantula crawl stance mein jati hai", "Use low-hitting mid; do not whiff highs over her head", "Low-hitting mid use karein; uske sar ke upar whiff na karein"),
    ("kuma", "Kuma", "in Heat 2+3", "i16", "m, m", "55 DMG", "+4 into SIT", "Wall Break / Floor Break / Balcony Break Heat Smashes", "SIT", "Wall Break", "Fresh salmon slash that breaks walls and enters Sit stance", "Taaza machhli ka slash jo deewar todta hai aur Sit mein aata hai", "Hold standing block; step left outside close range", "Stand block hold karein; SSL se side evade karein"),
    ("panda", "Panda", "in Heat 2+3", "i16", "m, m", "55 DMG", "+4 into SIT", "Wall Break / Floor Break / Balcony Break Heat Smashes", "SIT", "Wall Break", "Fresh bamboo slash that breaks walls and enters Sit stance", "Taaza baans ka slash jo deewar todta hai aur Sit mein aata hai", "Hold standing block; step left outside close range", "Stand block hold karein; SSL se side evade karein"),
    ("eddy", "Eddy Gordo", "in Heat 2+3", "i16", "l", "50 DMG", "-14 (WS Punishable)", "Low (Must Duck / Launch Punish)", "None", "Wall Splat", "Low Capoeira ground sweep that pierces standing guard", "Low Capoeira zameeni sweep jo standing guard ko todti hai", "Hold d/b crouch block; punish with i14 WS launcher", "d/b crouch block karein aur i14 WS launcher se punish karein"),
    ("lidia", "Lidia Sobieska", "in Heat 2+3", "i16", "m, m", "52 DMG", "+8 into HAE", "Massive Plus on Block Stance Mixup", "HAE", "Wall Splat", "Karate rush that enters Heaven & Earth stance at +8", "Karate rush jo block par +8 Heaven & Earth stance mein aata hai", "Do not press buttons; use Raw Heat Burst or Power Crush", "Button na dabayein; Raw Heat Burst ya Power Crush se todien"),
    ("heihachi", "Heihachi Mishima", "in Heat 2+3", "i16", "m, m", "55 DMG", "+6 into WGS", "Wall Break / Floor Break / Balcony Break Heat Smashes", "WGS", "Hard Wall Break", "Thunderous demon palm that breaks walls and enters Wind God", "Zabardast demon palm jo deewar todti hai aur Wind God mein aati hai", "Stand block; beware of wall destruction follow-ups", "Stand block karein; deewar tootne se hoshiyar rahein"),
    ("clive", "Clive Rosfield", "in Heat 2+3", "i14", "m, m", "52 DMG", "-9 (Safe)", "Long-Range / Projectile", "None", "Wall Splat", "i14 fullscreen Eikonic Fire blade that catches whiffs", "i14 poori screen ki Eikonic Fire blade jo door se punish karti hai", "Stand block; sidestep left at distance to evade", "Stand block karein; door se SSL karke evade karein"),
    ("anna", "Anna Williams", "in Heat 2+3", "i14", "m, m", "50 DMG", "+6 into CJM", "Fastest Heat Smashes (i10–i14 Punish Tools)", "CJM", "Wall Splat", "i14 fast assassin strike into Chaos Judgment at +6", "i14 tez assassin strike jo Chaos Judgment mein +6 par jati hai", "Hold standing guard or use dickjab db+1", "Stand guard rakhein ya dickjab db+1 use karein"),
    ("armor-king", "Armor King", "in Heat 2+3", "i16", "m, m", "58 DMG", "+10 into Step", "Throw-on-Block Transition", "Step", "Floor Break / Wall Break", "Black mist into +10 Shadow Step throw vortex", "Black mist into +10 Shadow Step throw vortex", "Sidestep right or jab check the forward step", "Sidestep right karein ya forward step ko jab check karein"),
    ("bob", "Bob Richards", "in Heat 2+3", "i16", "m, m", "52 DMG", "+6 into SPB", "Massive Plus on Block Stance Mixup", "SPB", "Wall Splat", "Super-heavy forward rush into Spinner Ball at +6", "Bhaari forward rush jo Spinner Ball mein +6 par jata hai", "Sidestep left or use armored Power Crush", "Sidestep left karein ya armored Power Crush use karein"),
    ("fahkumram", "Fahkumram", "in Heat 2+3", "i16", "m, m", "55 DMG", "-9 (Safe)", "Wall Break / Floor Break / Balcony Break Heat Smashes", "None", "Hard Wall Break", "Muay Thai ram head strike with massive wall splat", "Muay Thai ram head strike jo bhari wall splat deta hai", "Stand block; do not get pinned near corners", "Stand block karein; corner ke paas na phansein"),
    ("kunimitsu", "Kunimitsu", "in Heat 2+3", "i14", "m, m", "50 DMG", "+4 into SET", "Long-Range / Projectile", "SET", "Wall Splat", "i14 kunai teleport slash into Setsuna stance at +4", "i14 kunai teleport slash jo Setsuna stance mein +4 par jata hai", "Stand block and step left against linear dagger pokes", "Stand block karein aur linear pokes par SSL karein"),
    ("miary-zo", "Miary Zo", "in Heat 2+3", "i15", "m, m", "50 DMG", "+6 into BAO", "Massive Plus on Block Stance Mixup", "BAO", "Wall Splat", "African staff flurry into Bao stance at +6 on block", "African staff flurry jo block par +6 Bao stance mein aati hai", "Interrupt with dickjab db+1 or patient high guard", "Dickjab db+1 se interrupt karein ya patient guard rakhein"),
    ("roger-jr", "Roger Jr.", "in Heat 2+3", "i16", "m, m", "52 DMG", "+6 into Animal", "Massive Plus on Block Stance Mixup", "Animal", "Wall Splat", "Boxing glove frenzy into Animal Stance at +6", "Boxing glove frenzy jo Animal Stance mein +6 par jati hai", "Stand block and use i10 jab check or dickjab", "Stand block karein aur i10 jab check ya dickjab use karein"),
    ("nina", "Nina Williams", "in Heat 2+3", "i14", "m, m", "52 DMG", "+6 into Guns", "Throw-on-Block Transition", "Guns", "Wall Splat", "i14 fast gunshot string into guard break throw transition", "i14 tez gunshot string jo guard break throw transition deti hai", "Duck the high gunshot follow-up and launch", "High gunshot follow-up ko duck karke launch karein"),
    ("raven", "Raven", "in Heat 2+3", "i16", "m, m", "50 DMG", "+6 into Shadow", "Long-Range / Projectile", "Shadow", "Wall Splat", "Shadow clone teleport into backturned mixup at +6", "Shadow clone teleport jo backturned mixup mein +6 par jata hai", "Turn around check with mid or hold standing guard", "Mid check lagayein ya standing guard hold karein")
]

# 3. EXPANDED MOVEMENT BIBLE (7 COMPREHENSIVE ADVANCED TECHNIQUES)
MOVEMENT_TECHNIQUES = [
    {
        "technique": "Korean Backdash (KBD — Infinite Safe Spacing)",
        "technique_en": "Korean Backdash (KBD — Infinite Safe Spacing)",
        "technique_ur": "Korean Backdash (KBD — Mehfooz Aur Tez Spacing)",
        "technique_slug": "korean-backdash",
        "input": "b, n, b, d/b, b, n, b...",
        "input_execution": "b, n, b, d/b, b, n, b, d/b, b...",
        "socd_shortcut": "Hold Back (B), then rhythmically tap Down (D) + Forward (F)",
        "socd_shortcut_en": "Hold Back (B), then rhythmically tap Down (D) + Forward (F)",
        "socd_shortcut_ur": "Back (B) hold rakhein, aur rhythm ke sath Down (D) + Forward (F) tap karein",
        "why": "Normal backdash (b,b) has an ending recovery window where you cannot block. Inputting d/b puts your character into a 1-frame crouch state that immediately cancels backdash end-lag, while releasing d/b to neutral registers a free 'b' input from the neutral buffer, allowing seamless infinite backdashing in constant guard state.",
        "why_en": "Normal backdash (b,b) has an ending recovery window where you cannot block. Inputting d/b puts your character into a 1-frame crouch state that immediately cancels backdash end-lag, while releasing d/b to neutral registers a free 'b' input from the neutral buffer, allowing seamless infinite backdashing in constant guard state.",
        "why_ur": "Aam backdash (b,b) ke aakhir mein recovery pause hota hai jahan block nahi ho sakta. d/b (crouch) karne se backdash ki recovery foran cancel ho jati hai aur release karte hi neutral se agla backdash guard state mein nikalta hai.",
        "execution_breakdown": "1. Double tap back (b, B) to start first backdash. 2. Slide thumb/lever to d/b to cancel recovery. 3. Release to neutral (n) — the engine sees b -> n. 4. Tap b again: the engine registers [b, n, b] and executes the next backdash. Repeat [d/b, n, b] indefinitely.",
        "execution_breakdown_en": "1. Double tap back (b, B) to start first backdash. 2. Slide thumb/lever to d/b to cancel recovery. 3. Release to neutral (n) — the engine sees b -> n. 4. Tap b again: the engine registers [b, n, b] and executes the next backdash. Repeat [d/b, n, b] indefinitely.",
        "execution_breakdown_ur": "1. Pehla backdash b, B karein. 2. Thumb/lever ko d/b par slide karke recovery cancel karein. 3. Release to neutral karein. 4. Dobara b tap karein: engine [b, n, b] read karke agla backdash chala dega. Rhythm: [b, b] -> [db, n, b] -> [db, n, b].",
        "tactical_use": "Creates instant whiff punish opportunities at Range 1.5 to 2.5. Forces aggressive opponents to whiff attacks in neutral, leaving them wide open for your launcher.",
        "tactical_use_en": "Creates instant whiff punish opportunities at Range 1.5 to 2.5. Forces aggressive opponents to whiff attacks in neutral, leaving them wide open for your launcher.",
        "tactical_use_ur": "Range 1.5 se 2.5 par opponent ke attacks ko whiff karwata hai, jahan se aap apna optimal launcher maar kar 70+ combo le sakte hain.",
        "warning": "CRITICAL BACKSWAY WARNING: For backsway characters (Bryan, Paul, Nina, Steve, Lee), NEVER use a sloppy qcb (d, d/b, b) motion! A 'd' input will accidentally trigger Backsway stance and leave you completely vulnerable. Use the clean b -> d/b -> b method, or the reverse sway shortcut (b, b, u/b).",
        "warning_en": "CRITICAL BACKSWAY WARNING: For backsway characters (Bryan, Paul, Nina, Steve, Lee), NEVER use a sloppy qcb (d, d/b, b) motion! A 'd' input will accidentally trigger Backsway stance and leave you completely vulnerable. Use the clean b -> d/b -> b method, or the reverse sway shortcut (b, b, u/b).",
        "warning_ur": "KHABARDAAR (Backsway Characters): Bryan, Paul, Nina, Steve, aur Lee ke sath ghalti se qcb (d, db, b) motion na karein warna Backsway nikal aayega aur aap launch ho jayenge! Clean b -> db -> b ya b, b, ub use karein."
    },
    {
        "technique": "Mishima Wavedash & Crouch Dash Cancel (CD Cancel)",
        "technique_en": "Mishima Wavedash & Crouch Dash Cancel (CD Cancel)",
        "technique_ur": "Mishima Wavedash Aur CD Cancel Loop",
        "technique_slug": "mishima-wavedash",
        "input": "f, n, d, d/f, f, n, d, d/f...",
        "input_execution": "f, n, d, d/f, f, n, d, d/f, f...",
        "socd_shortcut": "Tap F, tap D, then hold D while pressing F to slide into d/f",
        "socd_shortcut_en": "Tap F, tap D, then hold D while pressing F to slide into d/f",
        "socd_shortcut_ur": "Forward tap karein, Down tap karein, phir Down hold karke Forward dabayein",
        "why": "Wavedash closes distance at blistering speed while continually realigning your character to track the opponent's sidesteps. It places the opponent into mental freeze due to the threat of the lethal Mishima 50/50 mixup (EWGF / Mid vs Hellsweep).",
        "why_en": "Wavedash closes distance at blistering speed while continually realigning your character to track the opponent's sidesteps. It places the opponent into mental freeze due to the threat of the lethal Mishima 50/50 mixup (EWGF / Mid vs Hellsweep).",
        "why_ur": "Wavedash nihayat tezi se distance cover karta hai aur opponent ke sidesteps ko auto-realign karta hai, jis se opponent 50/50 mixup (Hellsweep vs Mid) ke khauf se freeze ho jata hai.",
        "execution_breakdown": "1. Input Crouch Dash: f, n, d, d/f. 2. Slide d/f to forward (f) to cancel the crouch dash into a forward dash. 3. Input neutral then immediately repeat: n, d, d/f, f... Repeat rhythmically for smooth fluid waves.",
        "execution_breakdown_en": "1. Input Crouch Dash: f, n, d, d/f. 2. Slide d/f to forward (f) to cancel the crouch dash into a forward dash. 3. Input neutral then immediately repeat: n, d, d/f, f... Repeat rhythmically for smooth fluid waves.",
        "execution_breakdown_ur": "1. Pehle Crouch Dash karein: f, n, d, df. 2. df ko slide karke f par le jayein jo crouch dash ko forward dash mein cancel karta hai. 3. Neutral karke dobara d, df, f karein. Tezi se loop karein.",
        "tactical_use": "Wavedash into Block (CD~B): While wavedashing, suddenly tap and hold Back (B). The opponent anticipates an attack and executes an unsafe panic move which whiffs right in front of your guard! Wavedash into WS: Tap Up (u) or Back (b) during crouch dash to immediately access While Standing launchers (e.g. Kazuya WS+2).",
        "tactical_use_en": "Wavedash into Block (CD~B): While wavedashing, suddenly tap and hold Back (B). The opponent anticipates an attack and executes an unsafe panic move which whiffs right in front of your guard! Wavedash into WS: Tap Up (u) or Back (b) during crouch dash to immediately access While Standing launchers (e.g. Kazuya WS+2).",
        "tactical_use_ur": "Wavedash into Block (CD~B): Wavedash karte hue achanak Back hold kar lein—opponent dar kar keepout attack marega jo block ya whiff ho jayega! Wavedash into WS: Wavedash mein u tap karke foran WS moves (jaise Kazuya WS+2) maar sakenge.",
        "warning": "Do not wavedash in close range without blocking (CD~B); opponents can interrupt raw wavedashes with fast i10 jabs or hopkicks.",
        "warning_en": "Do not wavedash in close range without blocking (CD~B); opponents can interrupt raw wavedashes with fast i10 jabs or hopkicks.",
        "warning_ur": "Close range mein bina block kiye wavedash na karein; opponent i10 jab ya hopkick se interrupt kar sakta hai."
    },
    {
        "technique": "Crouch Cancel (CC — Standing Launchers from Crouch)",
        "technique_en": "Crouch Cancel (CC — Standing Launchers from Crouch)",
        "technique_ur": "Crouch Cancel (CC — Crouch Se Standing Launcher)",
        "technique_slug": "crouch-cancel",
        "input": "In Full Crouch (FC) -> tap u, n (or f, n) -> Standing Move",
        "input_execution": "FC -> u, n -> Standing Move (e.g. cc EWGF, cc df+2)",
        "socd_shortcut": "Tap Up (U) for 1 frame to snap to neutral standing instantly",
        "socd_shortcut_en": "Tap Up (U) for 1 frame to snap to neutral standing instantly",
        "socd_shortcut_ur": "Up (U) ko 1 frame ke liye tap karein jo foran standing position deta hai",
        "why": "When you block a heavy low attack, you are left in full crouch (FC). Many characters have mediocre While Standing (WS) launchers but possess god-tier standing launchers (e.g. Mishima cc EWGF, Bryan cc Jet Upper f,b+2, Paul cc df+2). Crouch Cancel lets you bypass WS recovery in exactly 1 frame.",
        "why_en": "When you block a heavy low attack, you are left in full crouch (FC). Many characters have mediocre While Standing (WS) launchers but possess god-tier standing launchers (e.g. Mishima cc EWGF, Bryan cc Jet Upper f,b+2, Paul cc df+2). Crouch Cancel lets you bypass WS recovery in exactly 1 frame.",
        "why_ur": "Jab aap opponent ka heavy low block karte hain toh aap crouch state mein hote hain. Kuch characters ke WS moves weak hote hain lekin standing launchers (EWGF, Jet Upper) bohot powerful hote hain. CC se aap 1 frame mein standing moves nikaal sakte hain.",
        "execution_breakdown": "While blocking in crouch or recovering from a low hit, tap Up (u) or Forward (f) for exactly 1 frame, release to neutral, and immediately input your standing launcher (e.g. u, n, f,b+2 for Bryan Jet Upper or u, n, f,n,df+2 for Mishima EWGF).",
        "execution_breakdown_en": "While blocking in crouch or recovering from a low hit, tap Up (u) or Forward (f) for exactly 1 frame, release to neutral, and immediately input your standing launcher (e.g. u, n, f,b+2 for Bryan Jet Upper or u, n, f,n,df+2 for Mishima EWGF).",
        "execution_breakdown_ur": "Crouch block ke foran baad Up (u) ya Forward (f) ko sirf 1 frame ke liye tap karein, neutral release karein, aur foran standing launcher input karein (jaise cc EWGF ya cc df+2).",
        "tactical_use": "Max-damage punishment on heavy -15 to -20 stagger lows (e.g. Kazuya Hellsweep, Bryan Snake Edge, Law Dragon Tail). Delivers 15-20 more combo damage than standard WS twin pistons.",
        "tactical_use_en": "Max-damage punishment on heavy -15 to -20 stagger lows (e.g. Kazuya Hellsweep, Bryan Snake Edge, Law Dragon Tail). Delivers 15-20 more combo damage than standard WS twin pistons.",
        "tactical_use_ur": "Bhaari lows (Snake Edge, Hellsweep) block karke standard WS punisher ki jagah standing launcher maar kar round-ending 80+ damage combo lein.",
        "warning": "Holding 'u' too long will cause your character to jump. It must be a crisp 1-frame micro tap.",
        "warning_en": "Holding 'u' too long will cause your character to jump. It must be a crisp 1-frame micro tap.",
        "warning_ur": "Up ko hold na karein warna character hawa mein jump kar jayega; sirf aik halka sa micro tap karein."
    },
    {
        "technique": "Instant While Running (iWR — Point-Blank Running Moves at Range 0)",
        "technique_en": "Instant While Running (iWR — Point-Blank Running Moves at Range 0)",
        "technique_ur": "Instant While Running (iWR — Point-Blank Running Moves)",
        "technique_slug": "instant-while-running",
        "input": "f, n, f, F + Button (e.g. iWR+2, iWR+3,2, iWR+2+4)",
        "input_execution": "f, n, f, F+2 (buffered at Range 0)",
        "socd_shortcut": "Tap F, tap F, hold F + Attack button with strict rhythmic cadence",
        "socd_shortcut_en": "Tap F, tap F, hold F + Attack button with strict rhythmic cadence",
        "socd_shortcut_ur": "Forward tap, Forward tap, phir Forward hold + Attack button dabayein",
        "why": "While Running (WR) moves are among the strongest offensive tools in Tekken 8 (e.g. Dragunov wr2, Claudio wr2, Victor wr2, Azucena wr3,2, King Shining Wizard f,f,F+2+4). iWR enables you to execute these moves directly in your opponent's face at Range 0.",
        "why_en": "While Running (WR) moves are among the strongest offensive tools in Tekken 8 (e.g. Dragunov wr2, Claudio wr2, Victor wr2, Azucena wr3,2, King Shining Wizard f,f,F+2+4). iWR enables you to execute these moves directly in your opponent's face at Range 0.",
        "why_ur": "While Running (WR) moves Tekken 8 ke sabse khatarnak plus-frame weapons hain (jaise Dragunov wr2, Claudio wr2, King Shining Wizard). iWR se aap zero distance (point-blank) par bhi running moves nikaal sakte hain.",
        "execution_breakdown": "Tekken 8 allows input buffering: tap forward (f), release to neutral (n), tap forward (f), then press and hold forward on the 3rd tap alongside the attack button (f, n, f, F+Button). Rhythm: 'tap... tap-HOLD+2'.",
        "execution_breakdown_en": "Tekken 8 allows input buffering: tap forward (f), release to neutral (n), tap forward (f), then press and hold forward on the 3rd tap alongside the attack button (f, n, f, F+Button). Rhythm: 'tap... tap-HOLD+2'.",
        "execution_breakdown_ur": "Tekken 8 mein buffer aasan hai: pehla f dabayein, neutral, doosra f dabayein, aur teesre f par forward hold karke attack button dabayein. Rhythm: 'f... f, F+2'.",
        "tactical_use": "Forces massive plus frames on block (+5 to +7) directly in neutral or after blocked jabs. King players use iWR to execute instant Shining Wizard (f,f,F+2+4) anywhere on screen.",
        "tactical_use_en": "Forces massive plus frames on block (+5 to +7) directly in neutral or after blocked jabs. King players use iWR to execute instant Shining Wizard (f,f,F+2+4) anywhere on screen.",
        "tactical_use_ur": "Point-blank range par opponent ke guard par +5 se +7 plus frames force karta hai. King players screen ke kisi bhi hissay se instant Shining Wizard lagate hain.",
        "warning": "If you press the attack button before holding the 3rd 'f', you will get a generic f+2 or f,f+2 instead of the While Running move.",
        "warning_en": "If you press the attack button before holding the 3rd 'f', you will get a generic f+2 or f,f+2 instead of the While Running move.",
        "warning_ur": "Agar teesre forward se pehle button dab gaya toh normal f+2 ya ff+2 nikal aayega aur WR move nahi banega."
    },
    {
        "technique": "Defensive Option-Select: Sidestep to Guard (SS~B & SS~d/b)",
        "technique_en": "Defensive Option-Select: Sidestep to Guard (SS~B & SS~d/b)",
        "technique_ur": "Defensive Option-Select: Sidestep to Guard (SS~B)",
        "technique_slug": "sidestep-to-guard",
        "input": "u (or d) tap for 6f~8f -> immediately hold B (or d/b)",
        "input_execution": "u ~ B (SSL to Guard) / d ~ B (SSR to Guard)",
        "socd_shortcut": "Tap Up/Down, then immediately transition to holding Back",
        "socd_shortcut_en": "Tap Up/Down, then immediately transition to holding Back",
        "socd_shortcut_ur": "Up/Down tap karein aur foran Back hold kar lein",
        "why": "Raw sidestepping is risky: if the opponent throws a tracking/homing attack, you take counter-hit damage. SS~B (Sidestep Cancel into Guard) gives you the lateral evasion of a sidestep against fast linear pokes while guaranteeing you block slower homing moves or mids.",
        "why_en": "Raw sidestepping is risky: if the opponent throws a tracking/homing attack, you take counter-hit damage. SS~B (Sidestep Cancel into Guard) gives you the lateral evasion of a sidestep against fast linear pokes while guaranteeing you block slower homing moves or mids.",
        "why_ur": "Seedha sidestep karne se agar opponent homing attack kare toh hit lag jati hai. SS~B se aap sidestep ka dodge bhi le lete hain aur foran back hold karke homing ya tracking moves ko block bhi kar lete hain.",
        "execution_breakdown": "Tap 'u' or 'd' to initiate the sidestep. After 6 to 8 frames of lateral movement, immediately transition your hand to hold Back (B). If the opponent pressed a linear move (e.g. Dragunov wr2, Mishima EWGF), it whiffs clean. If they threw a homing move (i18+), you block it safely.",
        "execution_breakdown_en": "Tap 'u' or 'd' to initiate the sidestep. After 6 to 8 frames of lateral movement, immediately transition your hand to hold Back (B). If the opponent pressed a linear move (e.g. Dragunov wr2, Mishima EWGF), it whiffs clean. If they threw a homing move (i18+), you block it safely.",
        "execution_breakdown_ur": "u ya d tap karein. 6 se 8 frames sidestep hone ke baad foran Back (B) hold kar lein. Linear moves whiff ho jayenge aur slow homing moves aapke guard par block ho jayenge.",
        "tactical_use": "The single most essential defensive option select in professional competitive Tekken. Neutralizes 85% of aggressive rushdown without risking counter-hit launches.",
        "tactical_use_en": "The single most essential defensive option select in professional competitive Tekken. Neutralizes 85% of aggressive rushdown without risking counter-hit launches.",
        "tactical_use_ur": "Professional tournament players ka sabse bara defensive hathyar. 85% linear rushdown attacks ko bina risk liye whiff karwata hai.",
        "warning": "Do not cancel the sidestep too early (under 4 frames) or you will cancel before moving off the centerline.",
        "warning_en": "Do not cancel the sidestep too early (under 4 frames) or you will cancel before moving off the centerline.",
        "warning_ur": "Sidestep ko bohot jaldi cancel na karein (4 frames se pehle) warna character centerline se bahar nahi nikal payega."
    },
    {
        "technique": "Fuzzy Guard & Low Duck Timing (Fuzzy Duck)",
        "technique_en": "Fuzzy Guard & Low Duck Timing (Fuzzy Duck)",
        "technique_ur": "Fuzzy Guard Aur Low Duck Timing",
        "technique_slug": "fuzzy-guard",
        "input": "Hold d/b for 3~5 frames -> immediately release to neutral/B",
        "input_execution": "d/b (3-5f tap) -> B (Stand Guard)",
        "socd_shortcut": "Micro-tap Down-Back then return to holding Back",
        "socd_shortcut_en": "Micro-tap Down-Back then return to holding Back",
        "socd_shortcut_ur": "Down-Back ko 3 frames ke liye tap karke wapas Back par shift karein",
        "why": "Strings in Tekken often branch between a fast High extension (e.g. 1,2 or df+1,2) and a slower Mid extension (e.g. df+1,4 or 1,2,3). Fuzzy ducking ducks the fast High on reaction/rhythm and immediately stands up in time to block the slower Mid.",
        "why_en": "Strings in Tekken often branch between a fast High extension (e.g. 1,2 or df+1,2) and a slower Mid extension (e.g. df+1,4 or 1,2,3). Fuzzy ducking ducks the fast High on reaction/rhythm and immediately stands up in time to block the slower Mid.",
        "why_ur": "Tekken mein strings mein aksar fast High aur slow Mid ka mixup hota hai. Fuzzy ducking se aap fast High ko duck karke guzar dete hain aur foran khare ho kar slow Mid ko block kar lete hain.",
        "execution_breakdown": "After blocking the first hit of a string, tap down-back (d/b) for 3-5 frames. If they pressed the fast High, it whiffs harmlessly over your head. If they pressed the delayed Mid, your character stands up before the mid impacts, blocking it safely.",
        "execution_breakdown_en": "After blocking the first hit of a string, tap down-back (d/b) for 3-5 frames. If they pressed the fast High, it whiffs harmlessly over your head. If they pressed the delayed Mid, your character stands up before the mid impacts, blocking it safely.",
        "execution_breakdown_ur": "Pehla hit block karne ke baad d/b ko 3-5 frames ke liye dabayein. Fast High whiff ho jayega aur slow Mid aane tak aap khare ho kar block kar chuke honge.",
        "tactical_use": "Solves knowledge checks against Hwoarang (d+3,4), Nina (d+4,1), Law (b+2,3,4), and Mishima 1,1,2 string pressure.",
        "tactical_use_en": "Solves knowledge checks against Hwoarang (d+3,4), Nina (d+4,1), Law (b+2,3,4), and Mishima 1,1,2 string pressure.",
        "tactical_use_ur": "Hwoarang d+3,4, Nina d+4,1, aur Law ke multi-hit strings ko neutralize karne ka sabse behtareen tareeqa hai.",
        "warning": "Fuzzy timing requires matchup familiarity; ducking too long will cause you to eat the mid launcher.",
        "warning_en": "Fuzzy timing requires matchup familiarity; ducking too long will cause you to eat the mid launcher.",
        "warning_ur": "Agar zyada der crouch mein rahe toh mid launcher lag jayega; micro timing zaroori hai."
    },
    {
        "technique": "Dash Blocking (f, f, b) & Deep Sidewalking (SS, hold u/d)",
        "technique_en": "Dash Blocking (f, f, b) & Deep Sidewalking (SS, hold u/d)",
        "technique_ur": "Dash Blocking Aur Deep Sidewalking",
        "technique_slug": "dash-blocking-sidewalking",
        "input": "f, f, b (Dash Block) / u, u (hold) or d, d (hold) (Sidewalk)",
        "input_execution": "f, F ~ b / u, U (hold) / d, D (hold)",
        "socd_shortcut": "Forward dash cancelled immediately with Back",
        "socd_shortcut_en": "Forward dash cancelled immediately with Back",
        "socd_shortcut_ur": "Forward dash ko foran Back se cancel karein",
        "why": "Dash Blocking lets you push forward and take stage control without getting hit by keepout attacks (Jet Upper, EWGF, magic 4). Sidewalking (SWL/SWR) provides sustained lateral movement to completely get behind opponents executing long strings.",
        "why_en": "Dash Blocking lets you push forward and take stage control without getting hit by keepout attacks (Jet Upper, EWGF, magic 4). Sidewalking (SWL/SWR) provides sustained lateral movement to completely get behind opponents executing long strings.",
        "why_ur": "Dash Blocking se aap aage barh kar stage control lete hain bina keepout hits khaye. Sidewalking se aap lambi multi-hit strings ke peeche chale jate hain aur free back-turned launcher milta hai.",
        "execution_breakdown": "For Dash Block: Input f, F to start forward run, and after 4-6 frames tap and hold B. For Sidewalk: Tap u or d, then immediately tap and hold u or d to enter sidewalk.",
        "execution_breakdown_en": "For Dash Block: Input f, F to start forward run, and after 4-6 frames tap and hold B. For Sidewalk: Tap u or d, then immediately tap and hold u or d to enter sidewalk.",
        "execution_breakdown_ur": "Dash block ke liye f, F karke 4 frames baad Back hold karein. Sidewalk ke liye u ya d ko double tap karke hold rakhein.",
        "tactical_use": "Cornering passive players at the wall and completely walking around running moves like Dragunov wr2 or Clive sword lunges.",
        "tactical_use_en": "Cornering passive players at the wall and completely walking around running moves like Dragunov wr2 or Clive sword lunges.",
        "tactical_use_ur": "Opponent ko deewar par dhakelna aur running attacks ke peeche nikal kar full combo lena.",
        "warning": "Sidewalking leaves you vulnerable to homing moves; always transition back to block if opponent doesn't attack.",
        "warning_en": "Sidewalking leaves you vulnerable to homing moves; always transition back to block if opponent doesn't attack.",
        "warning_ur": "Sidewalking ke dauran aap homing moves se hit ho sakte hain; safe rehne ke liye time par block karein."
    }
]

# 4. EXPANDED BLENDER EMERGENCY PROTOCOL (20 HIGH-PRESSURE VORTEX SCENARIOS)
BLENDER_SCENARIOS = [
    {
        "character": "Kazuya Mishima",
        "character_slug": "kazuya",
        "scenario": "Kazuya Wavedash 50/50 Vortex (ff+3 Mid vs Hellsweep CD+4 Low)",
        "scenario_en": "Kazuya Wavedash 50/50 Vortex (ff+3 Mid vs Hellsweep CD+4 Low)",
        "scenario_ur": "Kazuya Wavedash 50/50 Vortex (ff+3 Mid vs Hellsweep Low)",
        "situation": "+4 to +8 on knockdown/getup; Kazuya wavedashes directly into point-blank range.",
        "situation_en": "+4 to +8 on knockdown/getup; Kazuya wavedashes directly into point-blank range.",
        "situation_ur": "Knockdown ke baad Kazuya tezi se wavedash karke bilkul samnay aata hai.",
        "panic_trigger": "Mashing 10f jab checks or panic-rolling gets counter-hit launched by ff+3 or swept by Hellsweep.",
        "panic_trigger_en": "Mashing 10f jab checks or panic-rolling gets counter-hit launched by ff+3 or swept by Hellsweep.",
        "panic_trigger_ur": "Jab mash karna ya zameen par roll karna—Kazuya ka ff+3 ya Hellsweep foran launch kar dega.",
        "verified_safe_response": "Sidewalk Left (SWL): Kazuya's Hellsweep and ff+3 have zero tracking to his weak side (SSL/SWL). Walk left immediately upon getup to evade both options cleanly and launch him from behind!",
        "verified_safe_response_en": "Sidewalk Left (SWL): Kazuya's Hellsweep and ff+3 have zero tracking to his weak side (SSL/SWL). Walk left immediately upon getup to evade both options cleanly and launch him from behind!",
        "verified_safe_response_ur": "Sidewalk Left (SWL) karein! Kazuya ke Hellsweep aur ff+3 dono left side par zero tracking rakhte hain aur clean whiff ho jate hain.",
        "risk_reward": "Low Risk / High Reward (Full Back-Turn Launch)",
        "risk_reward_en": "Low Risk / High Reward (Full Back-Turn Launch)",
        "risk_reward_ur": "Low Risk / High Reward (Full Back-Turn Launch)",
        "drill": "Record Kazuya P2: Wavedash -> CD+4 vs Wavedash -> ff+3. Set P1: Wakeup -> Sidewalk Left -> Launch."
    },
    {
        "character": "Hwoarang",
        "character_slug": "hwoarang",
        "scenario": "Hwoarang Flamingo Kick Blender (d+3,4 into RFS/LFS loops)",
        "scenario_en": "Hwoarang Flamingo Kick Blender (d+3,4 into RFS/LFS loops)",
        "scenario_ur": "Hwoarang Flamingo Kick Blender (d+3,4 into Stance Loops)",
        "situation": "Hwoarang lands d+3,4 (+8 in RFS) and begins looping highs, mids, and sweeps.",
        "situation_en": "Hwoarang lands d+3,4 (+8 in RFS) and begins looping highs, mids, and sweeps.",
        "situation_ur": "Hwoarang d+3,4 hit karke RFS stance mein +8 par aa jata hai aur kicks chalaane lagta hai.",
        "panic_trigger": "Trying to jab check Hwoarang or ducking randomly eats RFS.b+3 or RFS.df+4 mid launchers.",
        "panic_trigger_en": "Trying to jab check Hwoarang or ducking randomly eats RFS.b+3 or RFS.df+4 mid launchers.",
        "panic_trigger_ur": "Kicks ke dauran jab dabana ya be-wajah duck karna—Hwoarang ka mid launcher CH kar dega.",
        "verified_safe_response": "1. Duck the 2nd hit of d+3,4 (the high kick) and launch him before he enters stance! 2. If stuck in stance block, use Dickjab (db+1) on RFS.2 high pokes, or Raw Heat Burst (2+3) to shatter the chain.",
        "verified_safe_response_en": "1. Duck the 2nd hit of d+3,4 (the high kick) and launch him before he enters stance! 2. If stuck in stance block, use Dickjab (db+1) on RFS.2 high pokes, or Raw Heat Burst (2+3) to shatter the chain.",
        "verified_safe_response_ur": "1. d+3,4 ka doosra hit High hai—foran Duck karke Launch karein! 2. Agar stance mein phans jayein toh Dickjab db+1 ya Raw Heat Burst 2+3 lagayein.",
        "risk_reward": "Guaranteed Launch Punish on 2nd hit Duck",
        "risk_reward_en": "Guaranteed Launch Punish on 2nd hit Duck",
        "risk_reward_ur": "Doosre hit par duck karke Guaranteed Launch Punish",
        "drill": "Record Hwoarang P2: d+3,4 -> RFS.2. Set P1: Crouch duck 2nd hit -> WS+2 launcher."
    },
    {
        "character": "Reina",
        "character_slug": "reina",
        "scenario": "Reina Sentai Pressure (f,f+2 Demon Paw on Block into SEN)",
        "scenario_en": "Reina Sentai Pressure (f,f+2 Demon Paw on Block into SEN)",
        "scenario_ur": "Reina Sentai Pressure (f,f+2 Block Hone Ke Baad SEN Mixup)",
        "situation": "Reina hits your guard with f,f+2 and transitions into Sentai (SEN) stance at only +2.",
        "situation_en": "Reina hits your guard with f,f+2 and transitions into Sentai (SEN) stance at only +2.",
        "situation_ur": "Reina door se f,f+2 maarti hai jo block hone par Sentai stance mein jati hai.",
        "panic_trigger": "Freezing in guard lets Reina get free Unbreakable Throws (SEN.1+2) or sweeping lows (SEN.3+4).",
        "panic_trigger_en": "Freezing in guard lets Reina get free Unbreakable Throws (SEN.1+2) or sweeping lows (SEN.3+4).",
        "panic_trigger_ur": "Dar kar khare rehne se Reina free Unbreakable Throw (SEN.1+2) ya low sweep maar deti hai.",
        "verified_safe_response": "Pro Secret: On BLOCK, Reina is ONLY +2! Execute an i13 Mid (df+1) or Dickjab (db+1). This interrupts her throw, low sweep, and slow mids! Only SEN.3 (High) and SEN.1 (Power Crush) beat df+1, which are duckable and -13 on block.",
        "verified_safe_response_en": "Pro Secret: On BLOCK, Reina is ONLY +2! Execute an i13 Mid (df+1) or Dickjab (db+1). This interrupts her throw, low sweep, and slow mids! Only SEN.3 (High) and SEN.1 (Power Crush) beat df+1, which are duckable and -13 on block.",
        "verified_safe_response_ur": "Pro Secret: Block par Reina sirf +2 hoti hai! Foran df+1 ya Dickjab db+1 maarein—Reina ka Throw, Low, aur slow Mids sab interrupt ho jayenge!",
        "risk_reward": "Low Risk / Breaks Stance Mixup 90% of the time",
        "risk_reward_en": "Low Risk / Breaks Stance Mixup 90% of the time",
        "risk_reward_ur": "Low Risk / 90% cases mein stance toot jati hai",
        "drill": "Record Reina P2: f,f+2 -> SEN.1+2 (Throw). Set P1: Block f,f+2 -> instant df+1 interrupt."
    },
    {
        "character": "King",
        "character_slug": "king",
        "scenario": "King Face-Down Oki Blender (Ground Throw vs Mid Stomp/Splash)",
        "scenario_en": "King Face-Down Oki Blender (Ground Throw vs Mid Stomp/Splash)",
        "scenario_ur": "King Face-Down Oki Blender (Zameen Par Throw vs Mid)",
        "situation": "You are knocked down face-down feet-away; King dashes in for ground throw or mid stomp.",
        "situation_en": "You are knocked down face-down feet-away; King dashes in for ground throw or mid stomp.",
        "situation_ur": "Aap zameen par ulte gire hue hain aur King daur kar ground throw lagane aata hai.",
        "panic_trigger": "Tech-rolling immediately or kicking from ground triggers King's 50 DMG ground grab.",
        "panic_trigger_en": "Tech-rolling immediately or kicking from ground triggers King's 50 DMG ground grab.",
        "panic_trigger_ur": "Foran tech roll karna ya paon marna—King ka ground throw pakar leta hai.",
        "verified_safe_response": "Stay grounded for 1 beat (hold down), then tech roll when King whiffs the throw, OR tap 1+2 to break the ground throw break window on reaction. If King jumps for body splash, roll right (1).",
        "verified_safe_response_en": "Stay grounded for 1 beat (hold down), then tech roll when King whiffs the throw, OR tap 1+2 to break the ground throw break window on reaction. If King jumps for body splash, roll right (1).",
        "verified_safe_response_ur": "Aik second zameen par rukein (Down hold), King ka throw whiff hone par uthein, ya 1+2 daba kar ground throw break karein.",
        "risk_reward": "Medium Risk / Avoids 50 DMG Ground Grab",
        "risk_reward_en": "Medium Risk / Avoids 50 DMG Ground Grab",
        "risk_reward_ur": "Medium Risk / 50 damage ground grab se bachata hai",
        "drill": "Record King P2: Ground throw d_db+2+4. Set P1: Face-down -> 1+2 break on reaction."
    },
    {
        "character": "Sergei Dragunov",
        "character_slug": "dragunov",
        "scenario": "Dragunov Running Plus-Frame Trap (wr+2 / qcf+4 into b+1+2 / d+2)",
        "scenario_en": "Dragunov Running Plus-Frame Trap (wr+2 / qcf+4 into b+1+2 / d+2)",
        "scenario_ur": "Dragunov Running Plus-Frame Trap (wr+2 / qcf+4 into b+1+2)",
        "situation": "Dragunov hits your block with wr+2 (+5) or qcf+4 (+7) and traps you at the wall.",
        "situation_en": "Dragunov hits your block with wr+2 (+5) or qcf+4 (+7) and traps you at the wall.",
        "situation_ur": "Dragunov block par wr+2 (+5) ya qcf+4 (+7) mar kar aapko deewar par bandh deta hai.",
        "panic_trigger": "Pressing any button after blocking wr+2 eats b+4,3 or b+1+2 for instant counter-hit wall splat.",
        "panic_trigger_en": "Pressing any button after blocking wr+2 eats b+4,3 or b+1+2 for instant counter-hit wall splat.",
        "panic_trigger_ur": "wr+2 block karne ke baad button dabana—Dragunov ka b+1+2 seedha CH wall splat kar dega.",
        "verified_safe_response": "1. Hold standing guard: Dragunov's d+2 deals chip but is -13 on block! 2. Sidewalk Left (SWL) at mid range to completely walk around wr+2 before it connects. 3. Power Crush on read.",
        "verified_safe_response_en": "1. Hold standing guard: Dragunov's d+2 deals chip but is -13 on block! 2. Sidewalk Left (SWL) at mid range to completely walk around wr+2 before it connects. 3. Power Crush on read.",
        "verified_safe_response_ur": "1. Stand guard hold karein: d+2 sirf chip damage deta hai aur block par -13 punishable hai! 2. Range par Sidewalk Left (SWL) karke wr+2 ko poora dodge karein.",
        "risk_reward": "Safe Guard Strategy / Minimizes Wall Splat",
        "risk_reward_en": "Safe Guard Strategy / Minimizes Wall Splat",
        "risk_reward_ur": "Safe Guard Strategy / Wall Splat se bachata hai",
        "drill": "Record Dragunov P2: wr+2 -> b+1+2. Set P1: Block wr+2 -> stand guard -> punish b+1+2."
    },
    {
        "character": "Jin Kazama",
        "character_slug": "jin",
        "scenario": "Jin Kazama d+2 Low Punch & ZEN Stance Blender",
        "scenario_en": "Jin Kazama d+2 Low Punch & ZEN Stance Blender",
        "scenario_ur": "Jin Kazama d+2 Low Punch Aur ZEN Stance Mixup",
        "situation": "Jin spams d+2 (Counter-Hit launcher low) or transitions into ZEN from 1,3,4 / 2,1,4.",
        "situation_en": "Jin spams d+2 (Counter-Hit launcher low) or transitions into ZEN from 1,3,4 / 2,1,4.",
        "situation_ur": "Jin d+2 low punch spam karta hai ya strings se seedha ZEN stance mein shift hota hai.",
        "panic_trigger": "Pressing buttons on d+2 gets counter-hit launched. Standing guard lets Jin chip away your life.",
        "panic_trigger_en": "Pressing buttons on d+2 gets counter-hit launched. Standing guard lets Jin chip away your life.",
        "panic_trigger_ur": "d+2 par button dabana—counter-hit launch ho jayenge.",
        "verified_safe_response": "Jin's d+2 is i22 startup and -14 on block! Crouch block on reaction to d+2 and execute an i14 WS launcher (Kazuya twin pistons, Bryan ws1, Jin ws2). On ZEN transitions on block, use an i10 jab check.",
        "verified_safe_response_en": "Jin's d+2 is i22 startup and -14 on block! Crouch block on reaction to d+2 and execute an i14 WS launcher (Kazuya twin pistons, Bryan ws1, Jin ws2). On ZEN transitions on block, use an i10 jab check.",
        "verified_safe_response_ur": "Jin ka d+2 i22 slow hai aur block par -14 hai! Reaction par crouch block karein aur i14 WS launcher maarein. Block par ZEN mein jaye toh i10 jab se check karein.",
        "risk_reward": "Guaranteed -14 WS Launch Punish",
        "risk_reward_en": "Guaranteed -14 WS Launch Punish",
        "risk_reward_ur": "Guaranteed -14 WS Launch Punish",
        "drill": "Record Jin P2: d+2. Set P1: Crouch block on visual red spark -> WS+2 launch."
    },
    {
        "character": "Lars Alexandersson",
        "character_slug": "lars",
        "scenario": "Lars Fake Stance Slide Rushdown (DEN / SEN Slides on Block)",
        "scenario_en": "Lars Fake Stance Slide Rushdown (DEN / SEN Slides on Block)",
        "scenario_ur": "Lars Fake Stance Slide Rushdown (DEN / SEN Slides)",
        "situation": "Lars hits your guard with b+1, df+1, or f+2,1 and lightning-slides into Dynamic Entry (DEN).",
        "situation_en": "Lars hits your guard with b+1, df+1, or f+2,1 and lightning-slides into Dynamic Entry (DEN).",
        "situation_ur": "Lars aapke guard par attacks marke bijli ki tarah DEN ya SEN stance mein slide karta hai.",
        "panic_trigger": "Freezing in guard allows Lars to execute DEN.3 (+5 homing) or SEN low sweep mixups.",
        "panic_trigger_en": "Freezing in guard allows Lars to execute DEN.3 (+5 homing) or SEN low sweep mixups.",
        "panic_trigger_ur": "Dar kar khare rehne se Lars free low sweep ya homing kick maar deta hai.",
        "verified_safe_response": "Lars transitions on block are 100% FAKE! Whenever Lars attacks your guard and slides, immediately press df+1 (Mid) or 1,2 Jab. He will be interrupted out of his slide every single time!",
        "verified_safe_response_en": "Lars transitions on block are 100% FAKE! Whenever Lars attacks your guard and slides, immediately press df+1 (Mid) or 1,2 Jab. He will be interrupted out of his slide every single time!",
        "verified_safe_response_ur": "Block par Lars ki stance slide 100% FAKE hai! Jaise hi guard par attack lagne ke baad woh slide kare, foran df+1 ya 1,2 Jab maarein—woh slide ke beech mein hi gir jayega!",
        "risk_reward": "Zero Risk Interrupt against Fake Slide",
        "risk_reward_en": "Zero Risk Interrupt against Fake Slide",
        "risk_reward_ur": "Zero Risk / Fake slide foran toot jati hai",
        "drill": "Record Lars P2: b+1 -> DEN slide. Set P1: Block b+1 -> instant df+1 interrupt."
    },
    {
        "character": "Bryan Fury",
        "character_slug": "bryan",
        "scenario": "Bryan Taunt & Hatchet Kick Trap (Taunt -> f,b+2 & qcb+3 Loop)",
        "scenario_en": "Bryan Fury Taunt & Hatchet Kick Trap (Taunt -> f,b+2 & qcb+3 Loop)",
        "scenario_ur": "Bryan Taunt Aur Hatchet Kick Trap (Taunt -> Jet Upper)",
        "situation": "Bryan corners you at the wall and uses Taunt (unblockable knee) or qcb+3 Hatchet Kick.",
        "situation_en": "Bryan corners you at the wall and uses Taunt (unblockable knee) or qcb+3 Hatchet Kick.",
        "situation_ur": "Bryan deewar par aapko Taunt (unblockable knee) ya qcb+3 Hatchet Kick se lock karta hai.",
        "panic_trigger": "Pressing slow buttons gets counter-hit by Jet Upper (f,b+2) or Mach Punch (ff+2).",
        "panic_trigger_en": "Pressing slow buttons gets counter-hit by Jet Upper (f,b+2) or Mach Punch (ff+2).",
        "panic_trigger_ur": "Slow moves dabane se Jet Upper ka counter-hit lagta hai aur 50% life khatam ho jati hai.",
        "verified_safe_response": "1. When Bryan starts Taunt, hit an i10 jab check or dickjab db+1 to interrupt the knee. 2. Hatchet Kick (qcb+3) is -13 on block: execute your i13 WS punisher. 3. Sidestep Right (SSR) beats his keepout.",
        "verified_safe_response_en": "1. When Bryan starts Taunt, hit an i10 jab check or dickjab db+1 to interrupt the knee. 2. Hatchet Kick (qcb+3) is -13 on block: execute your i13 WS punisher. 3. Sidestep Right (SSR) beats his keepout.",
        "verified_safe_response_ur": "1. Bryan Taunt shuru kare toh i10 jab ya db+1 se interrupt karein. 2. Hatchet kick (qcb+3) block par -13 hai—i13 WS punisher maarein. 3. Neutral mein SSR karein.",
        "risk_reward": "Interrupts Unblockable Taunt & Punishes -13 Low",
        "risk_reward_en": "Interrupts Unblockable Taunt & Punishes -13 Low",
        "risk_reward_ur": "Taunt ko interrupt karta hai aur -13 low ko punish karta hai",
        "drill": "Record Bryan P2: qcb+3. Set P1: Crouch block -> WS i13 punisher."
    },
    {
        "character": "Nina Williams",
        "character_slug": "nina",
        "scenario": "Nina Fast Hand Low-High Blender (d+4,1 & uf+4,3,4 Can Opener)",
        "scenario_en": "Nina Fast Hand Low-High Blender (d+4,1 & uf+4,3,4 Can Opener)",
        "scenario_ur": "Nina Fast Hand Low-High Blender (d+4,1 Aur Can Opener)",
        "situation": "Nina loops fast hand pokes, d+4,1 sweeps, and jumping Can Opener (uf+4,3,4) strings.",
        "situation_en": "Nina loops fast hand pokes, d+4,1 sweeps, and jumping Can Opener (uf+4,3,4) strings.",
        "situation_ur": "Nina fast hand pokes, d+4,1 aur jumping Can Opener kicks se continuous rushdown karti hai.",
        "panic_trigger": "Standing guard against d+4,1 allows Nina to maintain active frame trap momentum.",
        "panic_trigger_en": "Standing guard against d+4,1 allows Nina to maintain active frame trap momentum.",
        "panic_trigger_ur": "d+4 dekh kar khade rehna—Nina ka turn chalta rehta hai.",
        "verified_safe_response": "Pro Secret: 90% of Nina's aggressive strings end in a HIGH! On d+4,1: hold crouch after the low kick; the second hit (1 High) whiffs over your head for a free WS Launch! On uf+4,3,4: low block hit 2 and launch hit 3.",
        "verified_safe_response_en": "Pro Secret: 90% of Nina's aggressive strings end in a HIGH! On d+4,1: hold crouch after the low kick; the second hit (1 High) whiffs over your head for a free WS Launch! On uf+4,3,4: low block hit 2 and launch hit 3.",
        "verified_safe_response_ur": "Nina ki 90% strings HIGH par khatam hoti hain! d+4 ke baad khade na hon—crouch hold rakhein, uska 2nd hit (1 High) sar ke upar se whiff hoga aur free WS Launch milega!",
        "risk_reward": "Guaranteed WS Launch on 2nd hit Duck",
        "risk_reward_en": "Guaranteed WS Launch on 2nd hit Duck",
        "risk_reward_ur": "2nd hit par duck karke Guaranteed WS Launch",
        "drill": "Record Nina P2: d+4,1. Set P1: Block low d+4 -> hold crouch -> WS launcher."
    },
    {
        "character": "Marshall Law",
        "character_slug": "law",
        "scenario": "Marshall Law Panic Blender (1,2,3 into d+2,3 & Junkyard b+2,3,4)",
        "scenario_en": "Marshall Law Panic Blender (1,2,3 into d+2,3 & Junkyard b+2,3,4)",
        "scenario_ur": "Marshall Law Panic Blender (1,2,3 into d+2,3 & Junkyard)",
        "situation": "Law players execute 1,2,3 into d+2,3 (CH launcher) or spam b+2,3,4 Junkyard Kick.",
        "situation_en": "Law players execute 1,2,3 into d+2,3 (CH launcher) or spam b+2,3,4 Junkyard Kick.",
        "situation_ur": "Law players 1,2,3 block karwa kar foran d+2,3 launcher dabate hain ya Junkyard kick spamm karte hain.",
        "panic_trigger": "Mashing 1,2 Jab after blocking 1,2,3 gets crushed by d+2,3 for a full 75 DMG counter-hit launch!",
        "panic_trigger_en": "Mashing 1,2 Jab after blocking 1,2,3 gets crushed by d+2,3 for a full 75 DMG counter-hit launch!",
        "panic_trigger_ur": "1,2,3 block karke jab marna—d+2,3 jab ke neeche se nikal kar full combo launch kar dega!",
        "verified_safe_response": "1. NEVER press 1,2 Jab after blocking 1,2,3: use df+1 (Mid) or hold block for 1 second. If Law presses d+2,3, it is -15 on block for a full launch punish! 2. Junkyard (b+2,3,4): Low parry (d/f) hit 2 on reaction.",
        "verified_safe_response_en": "1. NEVER press 1,2 Jab after blocking 1,2,3: use df+1 (Mid) or hold block for 1 second. If Law presses d+2,3, it is -15 on block for a full launch punish! 2. Junkyard (b+2,3,4): Low parry (d/f) hit 2 on reaction.",
        "verified_safe_response_ur": "1. 1,2,3 block karke kabhi Jab na marein—df+1 marein ya 1 second block rakhein. Agar usne d+2,3 kiya toh woh -15 launch punishable hai! 2. Junkyard (b+2,3,4) ke 2nd hit par df hold karke Low Parry karein.",
        "risk_reward": "Converts Law's Bait into -15 Launch Punish",
        "risk_reward_en": "Converts Law's Bait into -15 Launch Punish",
        "risk_reward_ur": "Law ke trap ko -15 Launch Punish mein badal deta hai",
        "drill": "Record Law P2: 1,2,3 -> d+2,3. Set P1: Block 1,2,3 -> hold stand block -> launch d+2,3 (-15)."
    },
    {
        "character": "Eddy Gordo",
        "character_slug": "eddy",
        "scenario": "Eddy Gordo Ground Roll & Handstand Puzzle (RLX vs HSP Float)",
        "scenario_en": "Eddy Gordo Ground Roll & Handstand Puzzle (RLX vs HSP Float)",
        "scenario_ur": "Eddy Gordo Ground Roll Aur Handstand Puzzle (RLX vs HSP)",
        "situation": "Eddy drops to ground in Relax (RLX) or balances on hands in Handstand (HSP) to evade attacks.",
        "situation_en": "Eddy drops to ground in Relax (RLX) or balances on hands in Handstand (HSP) to evade attacks.",
        "situation_ur": "Eddy zameen par let jata hai (RLX) ya haathon ke bal khada hota hai (HSP) taake attacks whiff hon.",
        "panic_trigger": "Pressing standing high jabs (1,2) whiffs over Eddy, giving him a free launch combo.",
        "panic_trigger_en": "Pressing standing high jabs (1,2) whiffs over Eddy, giving him a free launch combo.",
        "panic_trigger_ur": "Standing high punches marna—hawa mein whiff honge aur Eddy seedha combo marega.",
        "verified_safe_response": "1. In Handstand (HSP): Eddy is airborne and CANNOT block! Hit any fast jab or df+1 for an instant float combo! 2. On Ground (RLX): Use low-hitting mids (e.g. Bryan df+2, Jin d+2, Kazuya df+2, King df+1).",
        "verified_safe_response_en": "1. In Handstand (HSP): Eddy is airborne and CANNOT block! Hit any fast jab or df+1 for an instant float combo! 2. On Ground (RLX): Use low-hitting mids (e.g. Bryan df+2, Jin d+2, Kazuya df+2, King df+1).",
        "verified_safe_response_ur": "1. Handstand (HSP) mein Eddy block nahi kar sakta! Fast df+1 ya jab marein—Eddy hawa mein float ho jayega aur full combo milega! 2. Zameen (RLX) par low-hitting mid marein.",
        "risk_reward": "Guaranteed Float Combo against Handstand",
        "risk_reward_en": "Guaranteed Float Combo against Handstand",
        "risk_reward_ur": "Handstand ke khilaf guaranteed Float Combo",
        "drill": "Record Eddy P2: HSP stance transition. Set P1: Hit df+1 -> full float juggle combo."
    },
    {
        "character": "Steve Fox",
        "character_slug": "steve",
        "scenario": "Steve Fox Peekaboo Corner Lock (PKB.d+1 / df+1,2 / PKB.2)",
        "scenario_en": "Steve Fox Peekaboo Corner Lock (PKB.d+1 / df+1,2 / PKB.2)",
        "scenario_ur": "Steve Fox Peekaboo Corner Lock (PKB Stance Loops)",
        "situation": "Steve enters Peekaboo (PKB) stance with both fists up and pins you to the wall with fast hooks.",
        "situation_en": "Steve enters Peekaboo (PKB) stance with both fists up and pins you to the wall with fast hooks.",
        "situation_ur": "Steve Peekaboo stance mein dono haath aage karke deewar par boxing pressure banata hai.",
        "panic_trigger": "Pressing 1,2 jab checks gets counter-hit by PKB.2 or b+1 for a 70 DMG combo.",
        "panic_trigger_en": "Pressing 1,2 jab checks gets counter-hit by PKB.2 or b+1 for a 70 DMG combo.",
        "panic_trigger_ur": "Jab mash karna—Steve ka b+1 ya PKB.2 seedha Counter-Hit launch kar dega.",
        "verified_safe_response": "1. Backdash (KBD) beats Peekaboo! Steve has very short forward range in PKB. Two backdashes make all his punches whiff. 2. At close range, use Dickjab (db+1) or armored Power Crush to break his rhythm.",
        "verified_safe_response_en": "1. Backdash (KBD) beats Peekaboo! Steve has very short forward range in PKB. Two backdashes make all his punches whiff. 2. At close range, use Dickjab (db+1) or armored Power Crush to break his rhythm.",
        "verified_safe_response_ur": "1. Backdash karein! Peekaboo mein Steve ki range bohot choti hoti hai, 2 backdashes se uske saare punches whiff honge. 2. Close range par Dickjab db+1 ya Power Crush use karein.",
        "risk_reward": "Whiff Punish via Spacing or Frame 10 High Crush",
        "risk_reward_en": "Whiff Punish via Spacing or Frame 10 High Crush",
        "risk_reward_ur": "Spacing se Whiff Punish ya Dickjab se turn lena",
        "drill": "Record Steve P2: PKB.d+1 -> PKB.df+1. Set P1: Double backdash -> whiff punish."
    },
    {
        "character": "Lidia Sobieska",
        "character_slug": "lidia",
        "scenario": "Lidia Horse & Cat Stance Rushes (ff+2 into HRS.2 / CAT Mixup)",
        "scenario_en": "Lidia Sobieska Horse & Cat Stance Rushes (ff+2 into HRS.2 / CAT Mixup)",
        "scenario_ur": "Lidia Horse & Cat Stance Rushes (ff+2 into HRS / CAT)",
        "situation": "Lidia hits your guard with ff+2 (+5) and shifts directly into Horse Stance (HRS).",
        "situation_en": "Lidia hits your guard with ff+2 (+5) and shifts directly into Horse Stance (HRS).",
        "situation_ur": "Lidia block par ff+2 (+5) mar kar seedha Horse Stance mein aati hai.",
        "panic_trigger": "Pressing buttons into Horse Stance eats HRS.2 (Mid launcher / Heat Engager).",
        "panic_trigger_en": "Pressing buttons into Horse Stance eats HRS.2 (Mid launcher / Heat Engager).",
        "panic_trigger_ur": "Stance mein button dabana—HRS.2 mid launcher se hit ho jayenge.",
        "verified_safe_response": "Sidestep Left (SSL): When Lidia enters Horse Stance after ff+2, step left immediately! Both HRS.2 and HRS.1 lack left tracking and whiff completely, leaving Lidia open for a full launch punish.",
        "verified_safe_response_en": "Sidestep Left (SSL): When Lidia enters Horse Stance after ff+2, step left immediately! Both HRS.2 and HRS.1 lack left tracking and whiff completely, leaving Lidia open for a full launch punish.",
        "verified_safe_response_ur": "Sidestep Left (SSL) karein! Lidia jab ff+2 ke baad Horse Stance mein aaye, foran left step karein—HRS.2 aur HRS.1 dono clean whiff ho jayenge!",
        "risk_reward": "Clean Whiff Launch Punish on SSL",
        "risk_reward_en": "Clean Whiff Launch Punish on SSL",
        "risk_reward_ur": "SSL par clean whiff launch punish",
        "drill": "Record Lidia P2: ff+2 -> HRS.2. Set P1: Block ff+2 -> Sidestep Left -> Launch."
    },
    {
        "character": "Claudio Serafino",
        "character_slug": "claudio",
        "scenario": "Claudio Starburst Running Loop (wr+2 into b+1 Plus-Frame Trap)",
        "scenario_en": "Claudio Serafino Starburst Running Loop (wr+2 into b+1 Plus-Frame Trap)",
        "scenario_ur": "Claudio Starburst Running Loop (wr+2 into b+1)",
        "situation": "Claudio activates Starburst (STB) and rushes in with running wr+2 (+6 on block).",
        "situation_en": "Claudio activates Starburst (STB) and rushes in with running wr+2 (+6 on block).",
        "situation_ur": "Claudio Starburst activate karke running wr+2 (+6) se attack karta hai.",
        "panic_trigger": "Challenging Claudio after blocked wr+2 eats f,f+4 or b+1 for a counter-hit launch.",
        "panic_trigger_en": "Challenging Claudio after blocked wr+2 eats f,f+4 or b+1 for a counter-hit launch.",
        "panic_trigger_ur": "wr+2 ke baad attack karna—Claudio ka b+1 ya ff+4 counter-hit launch kar dega.",
        "verified_safe_response": "1. Sidestep Left (SSL) in neutral: Claudio's wr+2 is strictly linear and tracks poorly to his left side. 2. On block: Hold standing guard and do not press buttons until he expends his Starburst.",
        "verified_safe_response_en": "1. Sidestep Left (SSL) in neutral: Claudio's wr+2 is strictly linear and tracks poorly to his left side. 2. On block: Hold standing guard and do not press buttons until he expends his Starburst.",
        "verified_safe_response_ur": "1. Neutral mein Sidestep Left (SSL) karein: Claudio ka wr+2 bilkul linear hai aur left side par whiff hota hai. 2. Block hone par stand guard rakhein.",
        "risk_reward": "Evades +6 Running Move via SSL",
        "risk_reward_en": "Evades +6 Running Move via SSL",
        "risk_reward_ur": "SSL se +6 running move dodge ho jata hai",
        "drill": "Record Claudio P2: wr+2 approach. Set P1: Sidestep Left -> whiff launch."
    },
    {
        "character": "Feng Wei",
        "character_slug": "feng",
        "scenario": "Feng Wei Kempo & Backturned Blender (b+3+4 into BT.1+2 / BT.d+3)",
        "scenario_en": "Feng Wei Kempo & Backturned Blender (b+3+4 into BT.1+2 / BT.d+3)",
        "scenario_ur": "Feng Wei Kempo Aur Backturned Blender (b+3+4 into BT)",
        "situation": "Feng retreats with Kempo Step (b+3+4) or enters Backturned (BT) stance at close range.",
        "situation_en": "Feng retreats with Kempo Step (b+3+4) or enters Backturned (BT) stance at close range.",
        "situation_ur": "Feng Kempo step se peeche hat-ta hai ya close range par Backturned stance mein aata hai.",
        "panic_trigger": "Running forward aggressively into Kempo gets counter-hit launched by Kempo 2 or shoulder b+1+2.",
        "panic_trigger_en": "Running forward aggressively into Kempo gets counter-hit launched by Kempo 2 or shoulder b+1+2.",
        "panic_trigger_ur": "Aage bhaag kar attack karna—Feng ka Kempo 2 ya shoulder b+1+2 counter-hit launch kar dega.",
        "verified_safe_response": "Do not chase Feng into Kempo! Hold your ground and wait for his Kempo sweep or punch to whiff, then execute an i12-i14 punish. In Backturned, watch for BT.d+3 low and crouch block (-15).",
        "verified_safe_response_en": "Do not chase Feng into Kempo! Hold your ground and wait for his Kempo sweep or punch to whiff, then execute an i12-i14 punish. In Backturned, watch for BT.d+3 low and crouch block (-15).",
        "verified_safe_response_ur": "Feng ka peecha na karein! Apni jagah khare rahein aur Kempo attack whiff hone par punish karein. Backturned mein BT.d+3 low par crouch block karein (-15).",
        "risk_reward": "Avoids Kempo Trap & Punishes BT.d+3 Low",
        "risk_reward_en": "Avoids Kempo Trap & Punishes BT.d+3 Low",
        "risk_reward_ur": "Kempo trap se bachata hai aur -15 low punish karta hai",
        "drill": "Record Feng P2: BT stance -> BT.d+3. Set P1: Crouch block -> WS launch."
    },
    {
        "character": "Yoshimitsu",
        "character_slug": "yoshimitsu",
        "scenario": "Yoshimitsu Flash Setup Trap (Negative-Edge Flash on Fake Block)",
        "scenario_en": "Yoshimitsu Flash Setup Trap (Negative-Edge Flash on Fake Block)",
        "scenario_ur": "Yoshimitsu Flash Setup Trap (Flash Frame 6 Parry)",
        "situation": "Yoshimitsu does a move with negative frames (e.g. 1,1 or df+1) and immediately inputs Flash (1+4).",
        "situation_en": "Yoshimitsu does a move with negative frames (e.g. 1,1 or df+1) and immediately inputs Flash (1+4).",
        "situation_ur": "Yoshimitsu minus frames par move karke foran Flash (1+4) daba deta hai.",
        "panic_trigger": "Rushing in to take your turn with close-range pokes gets swallowed by i6 Flash for a 65 DMG launch!",
        "panic_trigger_en": "Rushing in to take your turn with close-range pokes gets swallowed by i6 Flash for a 65 DMG launch!",
        "panic_trigger_ur": "Foran close-range punch marna—Yoshimitsu ka i6 Flash aapko absorb karke launch kar dega!",
        "verified_safe_response": "Flash has virtually ZERO forward range! When playing Yoshimitsu, punish with long-range weapons (e.g. df+2, f+4, or hopkick) rather than point-blank jabs, or backdash to let Flash whiff and launch him.",
        "verified_safe_response_en": "Flash has virtually ZERO forward range! When playing Yoshimitsu, punish with long-range weapons (e.g. df+2, f+4, or hopkick) rather than point-blank jabs, or backdash to let Flash whiff and launch him.",
        "verified_safe_response_ur": "Flash ki forward range bilkul zero hai! Close-range jabs ki jagah long-range attacks (df+2, f+4) use karein ya 1 backdash karke Flash ko whiff karwayein.",
        "risk_reward": "Bypasses i6 Flash Trap & Whiff Launches",
        "risk_reward_en": "Bypasses i6 Flash Trap & Whiff Launches",
        "risk_reward_ur": "i6 Flash se bachata hai aur whiff launch deta hai",
        "drill": "Record Yoshi P2: df+1 -> Flash 1+4. Set P1: Block df+1 -> backdash -> whiff launch."
    },
    {
        "character": "Victor Chevalier",
        "character_slug": "victor",
        "scenario": "Victor Chevalier Pistol & Teleport Shift (wr+2 into Iai Teleports)",
        "scenario_en": "Victor Chevalier Pistol & Teleport Shift (wr+2 into Iai Teleports)",
        "scenario_ur": "Victor Pistol Aur Teleport Shift (wr+2 into Iai)",
        "situation": "Victor rushes in with wr+2 or teleports into Iai stance with drawn katana.",
        "situation_en": "Victor rushes in with wr+2 or teleports into Iai stance with drawn katana.",
        "situation_ur": "Victor wr+2 mar kar aage aata hai ya katana nikaal kar Iai teleport mein jata hai.",
        "panic_trigger": "Standing still lets Victor fire unblockable gunshots or slice with safe mids.",
        "panic_trigger_en": "Standing still lets Victor fire unblockable gunshots or slice with safe mids.",
        "panic_trigger_ur": "Khare rehne se Victor unblockable gunshots ya safe katana slashes maar deta hai.",
        "verified_safe_response": "Sidestep Right (SSR): Victor's running wr+2 and teleport dashes track weakly to his right side. Step right to evade his forward thrust and execute a full combo punish.",
        "verified_safe_response_en": "Sidestep Right (SSR): Victor's running wr+2 and teleport dashes track weakly to his right side. Step right to evade his forward thrust and execute a full combo punish.",
        "verified_safe_response_ur": "Sidestep Right (SSR) karein! Victor ka wr+2 aur teleport dashes right side par weak tracking rakhte hain aur whiff ho jate hain.",
        "risk_reward": "Clean Whiff Launch on SSR",
        "risk_reward_en": "Clean Whiff Launch on SSR",
        "risk_reward_ur": "SSR par clean whiff launch",
        "drill": "Record Victor P2: wr+2. Set P1: Sidestep Right -> whiff launch."
    },
    {
        "character": "Alisa Bosconovitch",
        "character_slug": "alisa",
        "scenario": "Alisa Dual Chainsaw Chip Blender (DES Stance Pressure Loops)",
        "scenario_en": "Alisa Dual Chainsaw Chip Blender (DES Stance Pressure Loops)",
        "scenario_ur": "Alisa Dual Chainsaw Chip Blender (DES Stance Loops)",
        "situation": "Alisa activates chainsaws (DES) and inflicts heavy chip damage and plus frames on block.",
        "situation_en": "Alisa activates chainsaws (DES) and inflicts heavy chip damage and plus frames on block.",
        "situation_ur": "Alisa dono chainsaws nikaal kar block par heavy chip damage aur plus frames deti hai.",
        "panic_trigger": "Standing passive in block lets Alisa melt 40% of your life bar in chip damage alone.",
        "panic_trigger_en": "Standing passive in block lets Alisa melt 40% of your life bar in chip damage alone.",
        "panic_trigger_ur": "Passive block karte rehne se 40% life sirf chip damage se khatam ho jati hai.",
        "verified_safe_response": "1. Sidestep Left (SSL): Chainsaw attacks lose tracking to Sidestep Left. 2. Raw Heat Burst (2+3) or Power Crush: Alisa CANNOT block while in Chainsaw stance! Any hit knocks off her chainsaws instantly!",
        "verified_safe_response_en": "1. Sidestep Left (SSL): Chainsaw attacks lose tracking to Sidestep Left. 2. Raw Heat Burst (2+3) or Power Crush: Alisa CANNOT block while in Chainsaw stance! Any hit knocks off her chainsaws instantly!",
        "verified_safe_response_ur": "1. Sidestep Left (SSL) karein: Chainsaw attacks SSL par dodge hote hain. 2. Raw Heat Burst 2+3 ya Power Crush lagayein: Chainsaw stance mein Alisa block nahi kar sakti, aik hit se chainsaws gir jate hain!",
        "risk_reward": "Instant Stance Removal via Armor / SSL",
        "risk_reward_en": "Instant Stance Removal via Armor / SSL",
        "risk_reward_ur": "Armor ya SSL se chainsaws foran khatam ho jate hain",
        "drill": "Record Alisa P2: DES.f+1+2. Set P1: Raw Heat Burst 2+3 on block -> chainsaws stripped."
    },
    {
        "character": "Universal Defense",
        "character_slug": "universal",
        "scenario": "The Universal 'Dickjab' (db+1 or FC.1) — The Ultimate Blender Stopper",
        "scenario_en": "The Universal 'Dickjab' (db+1 or FC.1) — The Ultimate Blender Stopper",
        "scenario_ur": "Universal 'Dickjab' (db+1) — Har Blender Ko Todne Ka Formula",
        "situation": "You are trapped under relentless high-mid-low string pressure from an unfamiliar character.",
        "situation_en": "You are trapped under relentless high-mid-low string pressure from an unfamiliar character.",
        "situation_ur": "Kisi ajeeb character ki non-stop strings ke neeche aapka dimagh freeze ho jata hai.",
        "panic_trigger": "Trying to guess between high/mid/low or mashing standing jabs eats counter-hit launchers.",
        "panic_trigger_en": "Trying to guess between high/mid/low or mashing standing jabs eats counter-hit launchers.",
        "panic_trigger_ur": "Andaza lagana ya high punch marna—seedha counter-hit launch ho jayenge.",
        "verified_safe_response": "Execute db+1 (Down-Back + 1) or FC.1! Speed is i10 (fastest move in Tekken 8) with Frame 1 High Crush property. Opponent highs whiff over your head while mids/lows get interrupted. On hit, you are +6 to take your turn with ws4!",
        "verified_safe_response_en": "Execute db+1 (Down-Back + 1) or FC.1! Speed is i10 (fastest move in Tekken 8) with Frame 1 High Crush property. Opponent highs whiff over your head while mids/lows get interrupted. On hit, you are +6 to take your turn with ws4!",
        "verified_safe_response_ur": "db+1 (Down-Back + 1) dabayein! Yeh i10 speed ka move hai aur Frame 1 se High Crush karta hai. Opponent ke Highs sar ke upar se nikal jayenge aur slow moves interrupt ho jayenge! Hit par aap +6 hain.",
        "risk_reward": "Frame 1 High Crush / +6 Turn Reset",
        "risk_reward_en": "Frame 1 High Crush / +6 Turn Reset",
        "risk_reward_ur": "Frame 1 High Crush / +6 Turn Reset",
        "drill": "Practice Drill: Set training dummy to random strings -> practice interrupting with db+1."
    },
    {
        "character": "Universal Defense",
        "character_slug": "universal",
        "scenario": "Raw Heat Burst (2+3) — Emergency Invulnerable Freeze Breaker",
        "scenario_en": "Raw Heat Burst (2+3) — Emergency Invulnerable Freeze Breaker",
        "scenario_ur": "Raw Heat Burst (2+3) — Emergency Armor Freeze Breaker",
        "situation": "You are pinned in the corner or wall with less than 20% life and opponent is cycling plus frames.",
        "situation_en": "You are pinned in the corner or wall with less than 20% life and opponent is cycling plus frames.",
        "situation_ur": "Aap deewar par phans chuke hain, life 20% hai aur opponent continuous attack kar raha hai.",
        "panic_trigger": "Pressing regular buttons gets counter-hit wall splatted for round loss.",
        "panic_trigger_en": "Pressing regular buttons gets counter-hit wall splatted for round loss.",
        "panic_trigger_ur": "Normal button dabane se counter-hit wall splat lagta hai aur round khatam ho jata hai.",
        "verified_safe_response": "Execute Raw Heat Burst (2+3)! Heat Burst has full armor properties starting at Frame 8. It absorbs all incoming highs and mids, stops the opponent's momentum cold, and leaves you +2 on hit or +1 on block with Heat activated!",
        "verified_safe_response_en": "Execute Raw Heat Burst (2+3)! Heat Burst has full armor properties starting at Frame 8. It absorbs all incoming highs and mids, stops the opponent's momentum cold, and leaves you +2 on hit or +1 on block with Heat activated!",
        "verified_safe_response_ur": "2+3 (Raw Heat Burst) daba dein! Frame 8 se isme full armor hota hai jo opponent ke attack ko absorb karke sequence tod deta hai aur aapko +2 advantage deta hai!",
        "risk_reward": "Armor Break / Reverses Wall Pressure",
        "risk_reward_en": "Armor Break / Reverses Wall Pressure",
        "risk_reward_ur": "Armor Break / Wall pressure ko reverse karta hai",
        "drill": "Practice Drill: When cornered at wall, input 2+3 to absorb opponent rush and reset to neutral."
    }
]

def seed_database():
    print("Beginning seeding of Heat Smashes, Movement Bible, and Blender Protocol...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Create table character_heat_smashes
    c.execute("""
    CREATE TABLE IF NOT EXISTS character_heat_smashes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER NOT NULL,
        character_name TEXT NOT NULL,
        character_slug TEXT NOT NULL,
        command_input TEXT NOT NULL,
        startup_frames TEXT NOT NULL,
        hit_level TEXT NOT NULL,
        damage TEXT NOT NULL,
        block_frames TEXT NOT NULL,
        category TEXT NOT NULL,
        stance_transition TEXT,
        hazard_property TEXT,
        properties_notes TEXT,
        properties_notes_en TEXT,
        properties_notes_ur TEXT,
        tactical_counter TEXT,
        tactical_counter_en TEXT,
        tactical_counter_ur TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
    );
    """)

    # 2. Create table movement_techniques
    c.execute("""
    CREATE TABLE IF NOT EXISTS movement_techniques (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        technique_name TEXT NOT NULL,
        technique_slug TEXT NOT NULL,
        command_input TEXT NOT NULL,
        socd_shortcut TEXT,
        why_it_matters TEXT NOT NULL,
        why_it_matters_en TEXT,
        why_it_matters_ur TEXT,
        execution_breakdown TEXT NOT NULL,
        execution_breakdown_en TEXT,
        execution_breakdown_ur TEXT,
        tactical_application TEXT NOT NULL,
        tactical_application_en TEXT,
        tactical_application_ur TEXT,
        warning TEXT,
        warning_en TEXT,
        warning_ur TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Create table blender_scenarios
    c.execute("""
    CREATE TABLE IF NOT EXISTS blender_scenarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_name TEXT NOT NULL,
        character_slug TEXT NOT NULL,
        scenario_title TEXT NOT NULL,
        scenario_title_en TEXT,
        scenario_title_ur TEXT,
        frame_situation TEXT NOT NULL,
        frame_situation_en TEXT,
        frame_situation_ur TEXT,
        panic_trigger TEXT NOT NULL,
        panic_trigger_en TEXT,
        panic_trigger_ur TEXT,
        verified_safe_response TEXT NOT NULL,
        verified_safe_response_en TEXT,
        verified_safe_response_ur TEXT,
        risk_reward_rating TEXT NOT NULL,
        risk_reward_rating_en TEXT,
        risk_reward_rating_ur TEXT,
        practice_drill_input TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Fetch character ID map
    c.execute("SELECT slug, id FROM characters")
    char_map = dict(c.fetchall())

    # Clear previous seedings in these 3 tables to ensure idempotency
    c.execute("DELETE FROM character_heat_smashes")
    c.execute("DELETE FROM movement_techniques")
    c.execute("DELETE FROM blender_scenarios")

    # Insert character_heat_smashes
    for slug, name, cmd, startup, hit_lvl, dmg, blk, cat, stance, hazard, prop_en, prop_ur, counter_en, counter_ur in CHARACTER_HEAT_SMASHES_DATA:
        char_id = char_map.get(slug, 1)
        c.execute("""
        INSERT INTO character_heat_smashes (
            character_id, character_name, character_slug, command_input, startup_frames,
            hit_level, damage, block_frames, category, stance_transition, hazard_property,
            properties_notes, properties_notes_en, properties_notes_ur,
            tactical_counter, tactical_counter_en, tactical_counter_ur
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            char_id, name, slug, cmd, startup, hit_lvl, dmg, blk, cat, stance, hazard,
            prop_en, prop_en, prop_ur, counter_en, counter_en, counter_ur
        ))

    # Insert movement_techniques
    for m in MOVEMENT_TECHNIQUES:
        c.execute("""
        INSERT INTO movement_techniques (
            technique_name, technique_slug, command_input, socd_shortcut,
            why_it_matters, why_it_matters_en, why_it_matters_ur,
            execution_breakdown, execution_breakdown_en, execution_breakdown_ur,
            tactical_application, tactical_application_en, tactical_application_ur,
            warning, warning_en, warning_ur
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m["technique"], m["technique_slug"], m["input"], m["socd_shortcut"],
            m["why"], m["why_en"], m["why_ur"],
            m["execution_breakdown"], m["execution_breakdown_en"], m["execution_breakdown_ur"],
            m["tactical_use"], m["tactical_use_en"], m["tactical_use_ur"],
            m["warning"], m["warning_en"], m["warning_ur"]
        ))

    # Insert blender_scenarios
    for b in BLENDER_SCENARIOS:
        c.execute("""
        INSERT INTO blender_scenarios (
            character_name, character_slug, scenario_title, scenario_title_en, scenario_title_ur,
            frame_situation, frame_situation_en, frame_situation_ur,
            panic_trigger, panic_trigger_en, panic_trigger_ur,
            verified_safe_response, verified_safe_response_en, verified_safe_response_ur,
            risk_reward_rating, risk_reward_rating_en, risk_reward_rating_ur,
            practice_drill_input
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            b["character"], b["character_slug"], b["scenario"], b["scenario_en"], b["scenario_ur"],
            b["situation"], b["situation_en"], b["situation_ur"],
            b["panic_trigger"], b["panic_trigger_en"], b["panic_trigger_ur"],
            b["verified_safe_response"], b["verified_safe_response_en"], b["verified_safe_response_ur"],
            b["risk_reward"], b["risk_reward_en"], b["risk_reward_ur"],
            b["drill"]
        ))

    conn.commit()
    conn.close()
    print("SQLite tables populated successfully:")
    print(f"  - character_heat_smashes: {len(CHARACTER_HEAT_SMASHES_DATA)} rows")
    print(f"  - movement_techniques: {len(MOVEMENT_TECHNIQUES)} rows")
    print(f"  - blender_scenarios: {len(BLENDER_SCENARIOS)} rows")

    # Update master_compendium.json
    with open(COMPENDIUM_PATH, "r", encoding="utf-8") as f:
        comp = json.load(f)

    # 1. Update heat_smashes categories
    comp["heat_smashes"] = HEAT_SMASH_CATEGORIES

    # 2. Add full character_heat_smashes list into master_compendium.json
    char_heat_list = []
    for slug, name, cmd, startup, hit_lvl, dmg, blk, cat, stance, hazard, prop_en, prop_ur, counter_en, counter_ur in CHARACTER_HEAT_SMASHES_DATA:
        char_heat_list.append({
            "character": name,
            "character_slug": slug,
            "command_input": cmd,
            "startup_frames": startup,
            "hit_level": hit_lvl,
            "damage": dmg,
            "block_frames": blk,
            "advantage_on_block": blk,
            "category": cat,
            "category_en": cat,
            "category_ur": cat,
            "stance_transition": stance,
            "hazard_property": hazard,
            "properties": prop_en,
            "properties_en": prop_en,
            "properties_ur": prop_ur,
            "tactical_counter": counter_en,
            "counter_strategy": counter_en,
            "counter_strategy_en": counter_en,
            "counter_strategy_ur": counter_ur
        })
    comp["character_heat_smashes"] = char_heat_list

    # 3. Update movement_bible
    comp["movement_bible"] = MOVEMENT_TECHNIQUES

    # 4. Update blender_emergency_protocol
    blender_list = []
    for b in BLENDER_SCENARIOS:
        blender_list.append({
            "character": b["character"],
            "character_slug": b["character_slug"],
            "scenario": b["scenario"],
            "scenario_en": b["scenario_en"],
            "scenario_ur": b["scenario_ur"],
            "situation": b["situation"],
            "situation_en": b["situation_en"],
            "situation_ur": b["situation_ur"],
            "panic_trigger": b["panic_trigger"],
            "panic_trigger_en": b["panic_trigger_en"],
            "panic_trigger_ur": b["panic_trigger_ur"],
            "action": b["verified_safe_response"],
            "action_en": b["verified_safe_response_en"],
            "action_ur": b["verified_safe_response_ur"],
            "verified_safe_response": b["verified_safe_response"],
            "verified_safe_response_en": b["verified_safe_response_en"],
            "verified_safe_response_ur": b["verified_safe_response_ur"],
            "risk_reward": b["risk_reward"],
            "risk_reward_en": b["risk_reward_en"],
            "risk_reward_ur": b["risk_reward_ur"],
            "urgency": "CRITICAL" if "vortex" in b["scenario"].lower() or "blender" in b["scenario"].lower() else "HIGH",
            "practice_drill_input": b["drill"],
            "drill": b["drill"],
            "rule": b["scenario"],
            "rule_en": b["scenario_en"],
            "rule_ur": b["scenario_ur"],
            "detail": b["verified_safe_response"],
            "detail_en": b["verified_safe_response_en"],
            "detail_ur": b["verified_safe_response_ur"]
        })
    comp["blender_emergency_protocol"] = blender_list

    with open(COMPENDIUM_PATH, "w", encoding="utf-8") as f:
        json.dump(comp, f, indent=2, ensure_ascii=False)

    print("master_compendium.json updated successfully:")
    print(f"  - heat_smashes categories: {len(comp['heat_smashes'])}")
    print(f"  - character_heat_smashes: {len(comp['character_heat_smashes'])}")
    print(f"  - movement_bible: {len(comp['movement_bible'])}")
    print(f"  - blender_emergency_protocol: {len(comp['blender_emergency_protocol'])}")

if __name__ == "__main__":
    seed_database()
