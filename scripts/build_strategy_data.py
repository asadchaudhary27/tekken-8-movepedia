"""
Script to build universal combat mechanics with English by default and bilingual support.
"""

def build_universal_mechanics(text):
    return {
        "title": "Tekken 8 Universal Combat Mechanics & Tournament Science",
        "title_ur": "ٹیکن 8 کے بنیادی اصول، فریم ڈیٹا اور ایڈوانس سسٹمز",
        "controls_notation": {
            "title": "Button Notation & Attack Legend",
            "title_ur": "بٹنوں کی پہچان اور نوٹیشن",
            "desc": "Tekken utilizes universal numerical and directional notation to standardize execution across PlayStation, Xbox, and PC controllers.",
            "desc_ur": "ٹیکن میں ہر موو کو عالمی نمبرز اور ڈائریکشنز سے لکھا جاتا ہے تاکہ پلے اسٹیشن، ایکس باکس اور پی سی پر کھیلنا آسان ہو۔",
            "buttons": [
                { "btn": "1", "name": "Left Punch (LP)", "ps": "Square ▢", "xb": "X", "desc": "Fastest universal standing attack (i10 jab). Essential for turn checks.", "desc_ur": "سب سے تیز رفتار بنیادی مکہ (10 فریم جاب)" },
                { "btn": "2", "name": "Right Punch (RP)", "ps": "Triangle △", "xb": "Y", "desc": "Heavy straight punch; critical for hit-confirms and counter-hit combo routes.", "desc_ur": "بھاری سیدھا مکہ، کاؤنٹر ہٹ اور ہٹ کنفرم کے لیے بہترین" },
                { "btn": "3", "name": "Left Kick (LK)", "ps": "Cross ✕", "xb": "A", "desc": "Fast left leg thrust; controls neutral space and checks low/mid transitions.", "desc_ur": "تیز رفتار بائیں ٹانگ کی کک، فاصلہ برقرار رکھنے کا ٹول" },
                { "btn": "4", "name": "Right Kick (RK)", "ps": "Circle ◯", "xb": "B", "desc": "High-impact right kick; key for homing moves, hopkicks, and magic 4 launches.", "desc_ur": "طاقتور دائیں لات، ہاپ کک، ہومنگ یا لانچر مووز" },
                { "btn": "1+2", "name": "Dual Punch", "ps": "▢ + △", "xb": "X + Y", "desc": "Simultaneous punch input; triggers Power Crushes, command grabs, and Heat Burst.", "desc_ur": "دونوں مکے ایک ساتھ (پاور کرش، کمانڈ تھرو، یا بریک تھرو)" },
                { "btn": "3+4", "name": "Dual Kick", "ps": "✕ + ◯", "xb": "A + B", "desc": "Simultaneous kick input; activates acrobatic launchers and unique stance shifts.", "desc_ur": "دونوں لاتیں ایک ساتھ (سٹانسز اور جمپنگ لانچرز)" }
            ],
            "directions": [
                { "dir": "f", "name": "Forward", "desc": "Advance towards opponent", "ur": "آگے بڑھنا" },
                { "dir": "b", "name": "Back / Block", "desc": "Retreat / High & Mid neutral guard", "ur": "پیچھے ہٹنا / ہائی اور مڈ بلاک" },
                { "dir": "d", "name": "Down", "desc": "Crouch ducking state", "ur": "نیچے جھکنا" },
                { "dir": "u", "name": "Up", "desc": "Jump / Sidestep background", "ur": "اوپر اچھلنا" },
                { "dir": "df", "name": "Down-Forward", "desc": "Diagonal offensive low checks and Low Parry input", "ur": "آگے اور نیچے ترچھا (پوکس اور لو پیری df)" },
                { "dir": "db", "name": "Down-Back", "desc": "Crouch Guard: blocks incoming lows and ducks under highs", "ur": "پیچھے اور نیچے ترچھا (لو بلاک اور ہائی ڈک db)" },
                { "dir": "uf", "name": "Up-Forward", "desc": "Standard hopkick and aerial evasive jumping attacks", "ur": "آگے اور اوپر (ہاپ کک uf+4)" },
                { "dir": "ff / f,f", "name": "Dash", "desc": "Forward dash gap-closer", "ur": "دو دفعہ تیز آگے دبانا (ڈیش)" },
                { "dir": "wr (f,f,f)", "name": "While Running", "desc": "Triple forward sprint attack; massive frame advantage on block (+4 to +6)", "ur": "تین دفعہ آگے دبا کر بھاگتے ہوئے حملہ کرنا (+ آن بلاک)" },
                { "dir": "ws", "name": "While Standing / Rising", "desc": "Attacks executed while transitioning from crouch to standing guard", "ur": "ڈک (نیچے بیٹھنے) کے بعد اٹھتے وقت حملہ کرنا" },
                { "dir": "CH", "name": "Counter Hit", "desc": "Striking an opponent during their attack startup; unlocks bonus damage & launches", "ur": "جب حریف حملہ کر رہا ہو اور آپ کا وار پہلے لگ جائے" }
            ]
        },
        "frame_data_science": {
            "title": "Frame Data Science & Turn Priority",
            "title_ur": "فریم ڈیٹا سائنس: باری کس کی ہے؟",
            "fps_rule": "Tekken 8 runs locked at 60 FPS (1 frame = 1/60th of a second).",
            "rules": [
                {
                    "tier": "Startup Frames (i10, i15)",
                    "badge": "Startup i-Frames",
                    "color": "cyan",
                    "desc": "How quickly an attack becomes active. The fastest standing attack is the 10-frame Jab (i10), while standard mid orbital launchers activate at 15 frames (i15).",
                    "ur": "موو نکلنے میں کتنا وقت لگتا ہے۔ گیم کا سب سے تیز ترین حملہ جاب (1) ہوتا ہے جو صرف 10 فریمز (i10) لیتا ہے۔"
                },
                {
                    "tier": "Plus Frames (+1 to +8 on Block)",
                    "badge": "Plus (+) on Block",
                    "color": "gold",
                    "desc": "If your attack is blocked and you are at Plus frames, your offensive turn is still alive! If both players press a button simultaneously, yours hits first, creating relentless pressure.",
                    "ur": "اگر آپ کا حملہ بلاک ہوا اور آپ پلس (+) میں ہیں، تو آپ کی باری ابھی ختم نہیں ہوئی! دونوں بٹن دبائیں تو آپ کا وار پہلے لگے گا۔"
                },
                {
                    "tier": "Minus Safe (-1 to -9 on Block)",
                    "badge": "Safe on Block",
                    "color": "blue",
                    "desc": "Your offensive turn has ended, and your opponent now has priority. However, as long as you hold neutral block, your opponent cannot land any guaranteed damage.",
                    "ur": "آپ کی باری ختم ہو گئی ہے۔ لیکن اگر آپ پرسکون رہ کر بلاک کریں تو مخالف آپ کو کوئی مفت ڈیمیج نہیں دے سکتا۔"
                },
                {
                    "tier": "Punishable (-10 to -14 on Block)",
                    "badge": "Punishable (-10 to -14)",
                    "color": "orange",
                    "desc": "Unsafe moves that allow the defender to retaliate with guaranteed standing punishes (e.g., 10f jab strings, 12f heavy checks, or 14f knockdowns).",
                    "ur": "اگر آپ کا موو بلاک ہو جائے تو مخالف آپ کو مفت مکے اور سٹرنگز مار سکتا ہے کیونکہ آپ اتنے فریمز تک بلاک نہیں کر سکتے۔"
                },
                {
                    "tier": "Launch Punishable (-15 or worse)",
                    "badge": "Launch Punishable (-15+)",
                    "color": "red",
                    "desc": "Extremely unsafe moves on block (e.g., Hellsweeps, Snake Edges, Demoman). Blocking these guarantees a full While Standing or standing launcher for 70 to 95+ damage!",
                    "ur": "انتہائی غیر محفوظ مووز۔ بلاک ہونے پر حریف آپ کو ہوا میں اڑا کر 70 سے 95 ڈیمیج کا فل کومبو مار سکتا ہے!"
                }
            ],
            "triangle": {
                "title": "High, Mid, Low Combat Triangle",
                "title_ur": "ہائی، مڈ اور لو کا مثلث",
                "high": "High: Fastest attacks that grant strong plus frames on block. Weakness: Opponents can duck (db) under them and launch with While Standing ws+2.",
                "high_ur": "High (Upper): تیز ترین حملے اور بلاک پر پلس فریمز دیتے ہیں۔ کمزوری: نیچے بیٹھ کر (Duck) بچا جا سکتا ہے۔",
                "mid": "Mid: Beats ducking opponents. When opponents fear highs or annoying lows and crouch down, launch them into orbit with a safe mid launcher!",
                "mid_ur": "Mid (Middle): نیچے بیٹھنے والے حریف کو سزا دیتے ہیں! مڈ لانچر مار کر ہوا میں اڑا دیں۔",
                "low": "Low: Chips away at standing guard and hits legs. Weakness: Blocked in crouch (db) for heavy punishes, or low-parried with df for free combos.",
                "low_ur": "Low (Lower): کھڑے ہو کر بلاک کرنے والے کی ٹانگوں پر لگتے ہیں۔ کمزوری: db بلاک یا df لو پیری ہو جاتے ہیں۔"
            },
            "frame_trap_4step": [
                { "step": "1. The Poke", "cmd": "1 / df+1", "desc": "Step forward with a 1 jab (+1 on block) or a fast df+1 mid check to gauge their defensive habits.", "desc_ur": "آگے جا کر 1 (Jab +1 on block) یا df+1 (Fast Mid check) ماریں۔" },
                { "step": "2. The Low Annoyance", "cmd": "d+4 / db+3 / d+2", "desc": "When they turtle in standing guard, chip away with annoying low pokes to provoke panic button presses.", "desc_ur": "جب وہ کھڑا ہو کر بلاک کرے تو تیز لو پوک ماریں تاکہ وہ جلد بازی میں بٹن دبانے پر مجبور ہو۔" },
                { "step": "3. The Frame Trap", "cmd": "wr+2 / f+4 -> CH Mid", "desc": "Land a plus-on-block move (+4 to +6), then immediately buffer a fast Counter-Hit mid (df+2, b+1). If they press, they get launched!", "desc_ur": "پلس فریم موو ماریں، اور جیسے ہی وہ بلاک کرے فوراً کاؤنٹر ہٹ مڈ بٹن مار کر لانچ کریں!" },
                { "step": "4. Stance Blender", "cmd": "Flamingo / Sentai / Vortex", "desc": "Take your plus frame advantage into specialized stances, forcing a 50/50 high-low guessing game.", "desc_ur": "پلس فریمز لے کر سٹانس میں جائیں جہاں حریف کو 50/50 کا اندازہ لگانا پڑتا ہے!" }
            ],
            "spacing_settings": {
                "range_0": "Range 0 (Kissing Distance): Use rapid 1 jabs, df+1 checks, throws (1+3 / 2+4), and fast low pokes. Avoid slow start-up moves to prevent being interrupted.",
                "range_0_ur": "Range 0 (چپک کر): 1 (Jab), df+1, تھروز (1+3 / 2+4), اور تیز لو پوکس۔",
                "range_mid": "Range 1.5 - 2 (Mid-Range): Control space using keepout pokes (df+2, b+4, hopkicks uf+4) and sidesteps. Whiff punish any missed move with maximum damage.",
                "range_mid_ur": "Range 1.5 - 2 (ایک سے دو قدم): پوکرز (df+2, b+4, uf+4) اور سائیڈ سٹیپ۔",
                "range_long": "Range 3+ (Long Range): Close distances with While Running moves (wr+2, f,f,f+3) or Heat Burst to enforce frame traps.",
                "range_long_ur": "Range 3+ (دور فاصلہ): وہائل رننگ (wr+2) یا ہیٹ برسٹ چلا کر تیزی سے قریب آئیں۔",
                "settings": "Controller: L1 = 1+2, R1 = 3+4, L2 = Heat Burst (2+3), R2 = Rage Art. Graphics: V-Sync OFF, Network setting 'Prioritize Response' to minimize latency. Special Style disabled.",
                "settings_ur": "کنٹرولر: L1=1+2, R1=3+4, L2=Heat Burst, R2=Rage Art۔ V-Sync کو OFF رکھیں اور Special Style غیر فعال کریں۔"
            }
        },
        "parry_reversal_matrix": {
            "title": "Master Parry, Reversal & Duck vs. Block Matrix",
            "title_ur": "پیری، ریورسل، لو پیری اور ڈک بمقابلہ بلاک گائیڈ",
            "low_parry_guide": {
                "cmd": "df (Down-Forward)",
                "how": "When an opponent aims for your legs with a low attack, input and hold df (Down-Forward). The attacker faceplants onto the floor with the tornado bound state pre-consumed.",
                "how_ur": "جب مخالف لو اٹیک مارے تو db بلاک کرنے کے بجائے df دبا کر رکھیں۔ حریف زمین پر گرے گا۔",
                "punish_flow": "df (Low Parry) -> df+1 (or ws+4) -> Jab Strings (1,2 / df+4) -> Long Range Ender (40-50 Guaranteed Damage!)",
                "punish_flow_ur": "df (Low Parry) -> df+1 -> Jab Strings -> Long Range Ender (40 سے 50 مفت ڈیمیج!)",
                "unparryable": "Weapons (Yoshimitsu, Victor, Clive swords), Nina's gunshots, Law's nunchucks, and Kuma/Panda/Roger Jr. headbutts and tails CANNOT be low parried!",
                "unparryable_ur": "ہتھیاروں کی تلواریں، بندوقیں، ننچکس، اور جانوروں کے سر اور دم لو پیری نہیں ہوتے!"
            },
            "decision_matrix": [
                {
                    "situation": "Fast Low Pokes (d+4, db+3, Hwoarang d+3,4, Law d+2,3, Feng d+2)",
                    "action": "LOW PARRY (df)!",
                    "action_type": "parry",
                    "reason": "These fast lows are only -11 to -13 on block, yielding only minor standing punishes. Low parrying rewards you with a guaranteed 45+ juggle combo!",
                    "reason_ur": "یہ لوز بلاک پر صرف -11 سے -13 ہوتے ہیں۔ لو پیری کرنے پر 45+ ڈیمیج کا پورا کومبو ملتا ہے!"
                },
                {
                    "situation": "Mid-String Lows (Law Junkyard b+2,3,4, King Ali Kicks, Nina d+3,4)",
                    "action": "LOW PARRY (df)!",
                    "action_type": "parry",
                    "reason": "Low parrying interrupts the string's momentum immediately, snatching back offensive initiative and delivering a free combo.",
                    "reason_ur": "سٹرنگ کو بیچ میں توڑ کر آپ اپنی باری اور گارنٹیڈ کومبو دونوں فوراً حاصل کر لیتے ہیں۔"
                },
                {
                    "situation": "Heavy / Stagger Lows (Kazuya Hellsweep, Bryan Snake Edge, Paul Demoman, Lili BT d+3+4)",
                    "action": "BLOCK (db) & LAUNCH! (Do NOT Low Parry)",
                    "action_type": "block",
                    "reason": "These moves are -15 to -26 on block. Low parry gives only 45 damage, but blocking in crouch (db) guarantees a full While Standing launch for 80 to 95+ damage!",
                    "reason_ur": "یہ مووز بلاک پر -15 سے -26 ہوتے ہیں! db سے بلاک کر کے ws+2 مارنے پر 80 سے 95 ڈیمیج کا فل لانچ ملے گا!"
                },
                {
                    "situation": "High Strings (Nina d+4,1, Law 1,2,3, Jin 2,1, Hwoarang d+3,4 2nd hit, Paul 3,2)",
                    "action": "DUCK (d / db) & LAUNCH!",
                    "action_type": "duck",
                    "reason": "Parrying a high only grants modest advantage, but ducking allows the attack to whiff completely overhead, exposing them to a ws+2 launcher.",
                    "reason_ur": "ہائی اٹیک کو پیری کرنے کے بجائے نیچے بیٹھ کر (Duck) ہوا میں نکلنے دیں اور ws+2 سے لانچ کریں!"
                }
            ],
            "unparryable_reversals": [
                { "type": "Elbows", "examples": "Paul df+1, Bryan df+2 / b+1, Dragunov f+1+2", "rule": "Cannot be caught by standard high/mid reversals" },
                { "type": "Knees", "examples": "Bryan f+3, Feng df+3, Lars/Asuka b+4, Shaheen uf+4", "rule": "Blows straight through parries and strikes cleanly" },
                { "type": "Headbutts & Shoulders", "examples": "Feng b+1+2, Heihachi f+1+2, Paul d+1+2, King f+2+3", "rule": "Body-mass attacks cannot be deflected" },
                { "type": "Weapons & Projectiles", "examples": "Victor / Yoshimitsu / Clive swords, Devil Jin laser, Kunimitsu kunai", "rule": "Weapon strikes pierce through all standard reversals" },
                { "type": "Heat Smash & Rage Arts", "examples": "All character Heat Smashes and Rage Arts", "rule": "Instantly bypasses all parries with armor penetration" }
            ],
            "character_parries_table": [
                { "char": "Jin Kazama", "cmd": "b+1+3 / b+2+4", "catches": "EVERYTHING! Punches, Kicks, Elbows, Knees, and Weapons", "followup": "Slows time: immediately input d+3+4 (Can-Can Kicks Full Launcher)!", "followup_ur": "ٹائم سلو ہوتا ہے: فوراً d+3+4 کین کین ککس لانچر ماریں!" },
                { "char": "Leroy Smith", "cmd": "b+2 (Twin Dragon Gate)", "catches": "Deflects Punches, Kicks, Elbows, and Knees", "followup": "On success, mash 1+2 for Leroy's Sun & Moon rapid punch flurry.", "followup_ur": "پیری لگتے ہی 1+2 دبائیں، لیروئے خود مکھوں کی بارش کر دے گا۔" },
                { "char": "Asuka & Jun Kazama", "cmd": "b+1+3 / b+2+4 (Hold to Charge)", "catches": "High / Mid Punches & Kicks", "followup": "Can be held to extend active parry window; triggers automatic 40-damage bone snap.", "followup_ur": "دبا کر رکھنے سے لمبا وقت ایکٹیو رہتی ہے، آٹومیٹک 40 ڈیمیج اٹیک!" },
                { "char": "Asuka / Feng / Lee", "cmd": "Sabaki Parries (Asuka b+2+3, Feng 1+2, Lee b+1+2)", "catches": "Simultaneously blocks and attacks forward", "followup": "Feng 1+2 automatically launches on parry. Press 2 after Lee's b+1+2.", "followup_ur": "فینگ کا 1+2 پیری ہوتے ہی خود لانچ کر دیتا ہے، لی کے بعد 2 دبائیں۔" },
                { "char": "Paul / Nina / Dragunov", "cmd": "b+1+3 / b+2+4", "catches": "Standard High / Mid Punches & Kicks", "followup": "Automatic limb-breaking grappling animation with heavy knockdown.", "followup_ur": "آٹومیٹک ہڈی توڑنے والی ریورسل اینیمیشن چلتی ہے۔" },
                { "char": "King", "cmd": "b+1+3 (Kicks) & b+2+4 (Right Punches)", "catches": "b+1+3 catches kicks; b+2+4 catches right punches", "followup": "Kick parry breaks legs; punch parry spins King behind the opponent for a free throw.", "followup_ur": "کک پیری ٹانگ توڑ دیتی ہے، پنچ پیری کے بعد کنگ پشت پر آ جاتا ہے!" },
                { "char": "Steve Fox", "cmd": "b+1+2 (Punch Parry)", "catches": "High and Mid Punches only", "followup": "Press 1 or 2 immediately for Steve's knockdown body hook.", "followup_ur": "1 یا 2 دبائیں، سٹیو ہک مار کر زمین پر گرا دے گا۔" },
                { "char": "Bryan Fury", "cmd": "b+1+2 (Punch Parry)", "catches": "High and Mid Punches only", "followup": "Press 2 (b+1+2 ~ 2) for an instant Mach Punch wall splat!", "followup_ur": "پیری لگتے ہی 2 دبائیں، برائن مایک پنچ مار کر دیوار پر اڑا دے گا!" },
                { "char": "Reina / Heihachi", "cmd": "b+1+3 / b+2+4 & Heaven's Wrath", "catches": "Absorbs attack and counters with lightning strike", "followup": "Reina in Heat auto-parries while standing in Heaven's Wrath (d+1+2) stance.", "followup_ur": "رائنا ہیٹ میں HW سٹانس (d+1+2) میں آٹو پیری کرتی ہے!" },
                { "char": "Yoshimitsu", "cmd": "1+4 (Flash)", "catches": "6-frame close-range hitbox that cuts all incoming strikes", "followup": "Converts on hit into full launch: immediately input d+2,2,2 or b+2,2.", "followup_ur": "فل کومبو کے لیے فوراً d+2,2,2 یا b+2,2 دبائیں!" },
                { "char": "Azucena", "cmd": "Libertador (f+3+4)", "catches": "Auto-parries incoming Highs and Lows in stance", "followup": "Simply hold stance; once evasive roll triggers, input LIB 1+2 launcher.", "followup_ur": "سٹانس میں کھڑے رہیں، ڈاج ہوتے ہی LIB 1+2 لانچر مار دیں!" }
            ],
            "charge_guard_break_guide": {
                "title": "How to Charge Guard-Breaks & Defensive Parries",
                "title_ur": "گارڈ بریک اور پیریز چارج کرنے کا طریقہ",
                "defensive": "Characters like Asuka and Jun can hold b+1+3 to extend their active parry window, delaying the recovery and catching hesitant opponent strikes.",
                "defensive_ur": "آسوکا اور جون کے پاس b+1+3 ریورسل کو ہولڈ (دبا کر رکھنے) کی سہولت ہے۔",
                "offensive": "Holding down attack inputs (*) charges power moves into unblockable guard breaks (e.g. Fahkumram 3,4~4*, Steve b+1*, Paul qcf+2*, Yujiro f,f+1+2*). Blocking opponents are wall-crushed with massive frame advantage.",
                "offensive_ur": "اٹیک بٹن کو دبا کر رکھنے (*) سے موو گارڈ بریک میں بدل جاتا ہے اور حریف دیوار سے چپک جاتا ہے۔"
            }
        },
        "wall_traps_escape": {
            "title": "Deadly Wall Traps & Wall Escape Bible",
            "title_ur": "دیوار کے جان لیوا جال اور بچنے کے تین سنہری اصول",
            "wall_combo_science": "Secure a high wall splat, insert a rapid jab filler (1 or 2), convert through tornado extension, and execute your heaviest wall combo ender.",
            "wall_combo_science_ur": "حریف کو دیوار پر ہائی وال سپلیٹ کریں، پھر جاب فلر مار کر ٹورنیڈو ایکسٹینشن دیں اور بھاری وال کومبو اینڈ کریں۔",
            "universal_wall_crush": "Wall Crush moves (+5 to +9 on block) pin opponents against the brickwork, removing pushback and setting up inescapable 50/50 ground stomp vs mid re-splat loops.",
            "universal_wall_crush_ur": "وال کرش مووز (+5 سے +9 آن بلاک) حریف کو دیوار کے ساتھ جما دیتے ہیں اور وہ پیچھے نہیں ہٹ سکتا۔",
            "character_wall_traps": [
                { "char": "Bryan Fury", "name": "The Taunt (1+3+4) Unblockable Trap", "desc": "As the opponent recovers against the wall, execute Taunt. It is completely unblockable and grants +16 frames on contact, guaranteeing a free Jet Upper (fb+2) or Mach Punch!", "desc_ur": "دیوار پر حریف اٹھنے لگے تو Taunt ماریں۔ یہ ان بلاک ایبل ہے اور +16 فریمز دیتا ہے جس کے بعد جیٹ اپر فری ڈیمیج ہے!" },
                { "char": "King & Armor King", "name": "Burning Knuckle & Giant Swing Wall Loop", "desc": "Charge uf+1+2* (Burning Knuckle) after wall knockdown. If they stay down, take 40 damage; if they stand, launch unblockable; if they roll, Giant Swing catches them!", "desc_ur": "وال گرنے کے بعد uf+1+2* چارج کریں۔ لیٹا رہے تو 40 ڈیمیج، کھڑا ہو تو ان بلاک ایبل لانچ، رول کرے تو جائنٹ سوئنگ!" },
                { "char": "Hwoarang", "name": "Chip-Death & Backturned Flamingo Loop", "desc": "Loop Flamingo pressure against walled opponents. Heavy chip damage continuously drains life, and ducking results in an instant mid wall-splat re-juggle.", "desc_ur": "دیوار پر فلیمنگو لوپ چلائیں۔ چیپ ڈیمیج سے ہیلتھ گھٹتی رہے گی، اور ڈک کرنے پر مڈ وال سپلیٹ مل جائے گا!" },
                { "char": "Kazuya, Devil Jin & Reina", "name": "The Mishima Wall Vortex", "desc": "Force a brutal 50/50 wall loop: Hellsweep (Low) knockdowns into another setup, while safe Demon Paw (ff+2) or EWGF (Mid/High) crushes ducking attempts.", "desc_ur": "دیوار پر ہیل سویپ (Low) یا ڈیمن پا / الیکٹرک (Mid) کا 50/50 لگائیں۔ غلط اندازے پر حریف دوبارہ دیوار سے ٹکرا جائے گا۔" },
                { "char": "Paul Phoenix", "name": "The 50/50 Wall Deletion", "desc": "After wall splat, force the ultimate guessing game: Demoman (d+4,2:1+2) sweep vs Deathfist (qcf+2) which deletes over 50% of the opponent's lifebar.", "desc_ur": "وال سپلیٹ کے بعد ڈیمو مین مڈ لو سویپ ماریں، یا ڈیتھ فسٹ سے حریف کا آدھا لائف بار اڑا دیں!" },
                { "char": "Yoshimitsu", "name": "Unblockable Sword Sweep & Poison Trap", "desc": "Use fc df+1 (Unblockable Low Sword Sweep). If they jump or parry, ws+2,1 mid tornado launcher immediately re-splats them into the wall.", "desc_ur": "دیوار پر fc df+1 ان بلاک ایبل لو سورڈ سویپ ماریں۔ جمپ کرے تو ws+2,1 سے دوبارہ دیوار پر چپکا دیں!" },
                { "char": "Jin Kazama", "name": "Scourge (d+2) & Electric Wall Trap", "desc": "Pin opponents with f,f,f+3 (+6 Wall Crush), then mix d+2 (low punch that hits grounded opponents and counter-hit launches) with safe mid df+1,4~4.", "desc_ur": "دیوار پر f,f,f+3 (+6 وال کرش) ماریں۔ d+2 لو ماریں یا df+1,4~4 مڈ مار کر دوبارہ وال سپلیٹ کریں!" },
                { "char": "Jack-8 & Alisa", "name": "Un-escapable Chip & Guard Break Loop", "desc": "Jack-8 uses Gamma Howl GMH 4 (+11 guard break) into free punches; Alisa activates Chainsaws (DES) for relentless, zero-pushback chip shredding.", "desc_ur": "جیک-8 گاما ہاول GMH 4 (+11 گارڈ بریک) مارتا ہے، اور الیسا چین سا نکال کر زیرو پش بیک چیپ کٹنگ کرتی ہے!" }
            ],
            "escape_rules": [
                {
                    "rule": "1. Side-Walk Towards Open Side",
                    "badge": "Side-Walk Open Side",
                    "desc": "Side-walk continuously (double-tap and hold u or d) toward the open stage direction. As soon as space opens, land a position-switch throw (1+3 / 2+4) to fling the opponent into the wall!",
                    "desc_ur": "دیوار کے کونے سے نکلنے کے لیے مسلسل کھلی سائیڈ پر سائیڈ واک کریں اور پوزیشن سوئچ تھرو مار کر حریف کو دیوار میں پھینک دیں!"
                },
                {
                    "rule": "2. Delay Wake-Up (Stay Grounded)",
                    "badge": "Stay Grounded",
                    "desc": "The most effective defense against Bryan's Taunt, Kazuya's Vortex, and Paul's Demoman is to remain grounded for a full second. Their timed mix-ups whiff harmlessly overhead.",
                    "desc_ur": "برائن کے ٹونٹ، کازویا کے وال ورٹیکس اور پال کے ڈیمو مین سے بچنے کا بہترین طریقہ ہے 1 سیکنڈ تک زمین پر بغیر کوئی بٹن دبائے لیٹے رہنا!"
                },
                {
                    "rule": "3. Quick Jab + Sidestep",
                    "badge": "Jab & Sidestep",
                    "desc": "Instead of throwing slow, high-risk panic launchers, throw a rapid 1 jab or db+1 dickjab, then immediately sidestep outward into open arena space.",
                    "desc_ur": "دیوار پر سست بٹن دبانے کے بجائے تیز جاب (1) یا ڈک جاب (db+1) ماریں اور فوراً باہر کی طرف سائیڈ سٹیپ کر کے دباؤ توڑ دیں!"
                }
            ]
        },
        "defense_escape_5rules": [
            { "name": "The Dickjab (db+1 / d+1)", "desc": "10-frame crouching punch that crushes highs and instantly halts relentless stance flows (Flamingo, Sentai, Hayashida).", "desc_ur": "10 فریم کا کراؤچنگ پنچ جو حریف کے ہائی اٹیکس کے نیچے سے نکل کر نینا، ہوارنگ اور رائنا کے سٹانس فلو کو توڑ دیتا ہے!" },
            { "name": "Power Crush (Armor)", "desc": "Armor attacks (b+1+2 / f+1+2) that absorb high and mid attacks starting from frame 7 to reverse offensive pressure.", "desc_ur": "شیلڈ آئی کون والا موو جو ساتویں فریم سے ہائی اور مڈ مار کھا کر واپس کاؤنٹر کرتا ہے!" },
            { "name": "Heat Burst (2+3 / L2)", "desc": "Armored universal activator that interrupts oppressive wall pressure and gives you +1 frame advantage.", "desc_ur": "دیوار پر پھنسے ہوں تو ہیٹ برسٹ دبائیں، اس میں آرمر ہوتا ہے جو حملہ روک کر آپ کو +1 اپنی باری دیتا ہے!" },
            { "name": "Sidestep + Block (u,n,b / d,n,b)", "desc": "Step slightly and immediately cancel into neutral block; allows linear moves (wr+2, Electrics) to whiff without risking counter-hits.", "desc_ur": "سائیڈ سٹیپ کر کے فوراً بلاک دبائیں تاکہ ڈریگنوف کا wr+2 اور کازویا کا الیکٹرک ہوا میں نکل جائے!" },
            { "name": "Throw Breaks (Tech Grabs)", "desc": "Left hand extends forward = break with 1; Right hand extends = break with 2; Both hands extend = break with 1+2.", "desc_ur": "بایاں ہاتھ آگے آئے تو 1، دایاں ہاتھ آگے آئے تو 2، اور دونوں ہاتھ ایک ساتھ آئیں تو 1+2 دبائیں!" }
        ]
    }
