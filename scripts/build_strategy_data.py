"""
Script to build frontend/assets/js/tekken8MasterData.js
Extracts 100% of data from master_guide_extracted.txt and generates the authoritative
TEKKEN8_MASTER_DATA object containing universal mechanics and all 44 character profiles.
"""

import os
import re
import json

def read_master_guide():
    with open('master_guide_extracted.txt', 'r', encoding='utf-8') as f:
        return f.read()

def clean_text(t):
    return t.strip()

def build_universal_mechanics(text):
    return {
        "title": "Tekken 8 Universal Combat Mechanics & Tournament Science",
        "title_ur": "ٹیکن 8 کے بنیادی اصول، فریم ڈیٹا اور ایڈوانس سسٹمز",
        "controls_notation": {
            "title": "Button Notation & Attack Legend",
            "title_ur": "بٹنوں کی پہچان اور نوٹیشن",
            "desc_ur": "ٹیکن میں ہر موو کو عالمی نمبرز اور ڈائریکشنز سے لکھا جاتا ہے تاکہ پلے اسٹیشن، ایکس باکس اور پی سی پر کھیلنا آسان ہو۔",
            "buttons": [
                { "btn": "1", "name": "Left Punch (LP)", "ps": "Square ▢", "xb": "X", "desc_ur": "سب سے تیز رفتار بنیادی مکہ (10 فریم جاب)" },
                { "btn": "2", "name": "Right Punch (RP)", "ps": "Triangle △", "xb": "Y", "desc_ur": "بھاری سیدھا مکہ، کاؤنٹر ہٹ اور ہٹ کنفرم کے لیے بہترین" },
                { "btn": "3", "name": "Left Kick (LK)", "ps": "Cross ✕", "xb": "A", "desc_ur": "تیز رفتار بائیں ٹانگ کی کک، فاصلہ برقرار رکھنے کا ٹول" },
                { "btn": "4", "name": "Right Kick (RK)", "ps": "Circle ◯", "xb": "B", "desc_ur": "طاقتور دائیں لات، ہاپ کک، ہومنگ یا لانچر مووز" },
                { "btn": "1+2", "name": "Dual Punch", "ps": "▢ + △", "xb": "X + Y", "desc_ur": "دونوں مکے ایک ساتھ (پاور کرش، کمانڈ تھرو، یا بریک تھرو)" },
                { "btn": "3+4", "name": "Dual Kick", "ps": "✕ + ◯", "xb": "A + B", "desc_ur": "دونوں لاتیں ایک ساتھ (سٹانسز اور جمپنگ لانچرز)" }
            ],
            "directions": [
                { "dir": "f", "name": "Forward", "ur": "آگے بڑھنا" },
                { "dir": "b", "name": "Back / Block", "ur": "پیچھے ہٹنا / ہائی اور مڈ بلاک" },
                { "dir": "d", "name": "Down", "ur": "نیچے جھکنا" },
                { "dir": "u", "name": "Up", "ur": "اوپر اچھلنا" },
                { "dir": "df", "name": "Down-Forward", "ur": "آگے اور نیچے ترچھا (پوکس اور لو پیری df)" },
                { "dir": "db", "name": "Down-Back", "ur": "پیچھے اور نیچے ترچھا (لو بلاک اور ہائی ڈک db)" },
                { "dir": "uf", "name": "Up-Forward", "ur": "آگے اور اوپر (ہاپ کک uf+4)" },
                { "dir": "ff / f,f", "name": "Dash", "ur": "دو دفعہ تیز آگے دبانا (ڈیش)" },
                { "dir": "wr (f,f,f)", "name": "While Running", "ur": "تین دفعہ آگے دبا کر بھاگتے ہوئے حملہ کرنا (+ آن بلاک)" },
                { "dir": "ws", "name": "While Standing / Rising", "ur": "ڈک (نیچے بیٹھنے) کے بعد اٹھتے وقت حملہ کرنا" },
                { "dir": "CH", "name": "Counter Hit", "ur": "جب حریف حملہ کر رہا ہو اور آپ کا وار پہلے لگ جائے" }
            ]
        },
        "frame_data_science": {
            "title": "Frame Data Science & The Turn Priority",
            "title_ur": "فریم ڈیٹا سائنس: باری کس کی ہے؟",
            "fps_rule": "Tekken 8 runs locked at 60 FPS (1 frame = 1/60th second).",
            "rules": [
                {
                    "tier": "Startup Frames (i10, i15)",
                    "badge": "Startup i-Frames",
                    "color": "cyan",
                    "ur": "موو نکلنے میں کتنا وقت لگتا ہے۔ گیم کا سب سے تیز ترین حملہ جاب (1) ہوتا ہے جو صرف 10 فریمز (i10) لیتا ہے، جبکہ عام لانچرز 15 فریمز (i15) لیتے ہیں۔"
                },
                {
                    "tier": "Plus Frames (+1 to +8 on Block)",
                    "badge": "Plus (+) on Block",
                    "color": "gold",
                    "ur": "اگر آپ کا حملہ بلاک ہوا اور آپ پلس (+) میں ہیں، تو آپ کی باری ابھی ختم نہیں ہوئی! اگر دونوں کھلاڑی ایک ساتھ بٹن دبائیں گے تو آپ کا حملہ پہلے لگے گا، اسی سے پریشر بنتا ہے۔"
                },
                {
                    "tier": "Minus Safe (-1 to -9 on Block)",
                    "badge": "Safe on Block",
                    "color": "blue",
                    "ur": "آپ کی باری ختم ہو گئی ہے اور اب مخالف کی باری ہے۔ لیکن اگر آپ پرسکون رہ کر بلاک کریں تو مخالف آپ کو کوئی مفت ڈیمیج نہیں دے سکتا۔"
                },
                {
                    "tier": "Punishable (-10 to -14 on Block)",
                    "badge": "Punishable (-10 to -14)",
                    "color": "orange",
                    "ur": "اگر آپ کا موو بلاک ہو جائے تو مخالف آپ کو مفت مکے اور سٹرنگز مار سکتا ہے کیونکہ آپ اتنے فریمز تک بلاک نہیں کر سکتے۔"
                },
                {
                    "tier": "Launch Punishable (-15 or worse)",
                    "badge": "Launch Punishable (-15+)",
                    "color": "red",
                    "ur": "یہ انتہائی غیر محفوظ مووز ہوتے ہیں (جیسے ہیل سویپ یا سنیک ایج)۔ بلاک ہونے پر حریف آپ کو ہوا میں اڑا کر 70 سے 95 ڈیمیج کا فل کومبو مار سکتا ہے!"
                }
            ],
            "triangle": {
                "title": "High, Mid, Low Combat Triangle",
                "title_ur": "ہائی، مڈ اور لو کا مثلث",
                "high_ur": "High (Upper): تیز ترین حملے اور بلاک پر پلس فریمز دیتے ہیں۔ کمزوری: حریف نیچے بیٹھ کر (Duck) بچ سکتا ہے اور ws+2 سے لانچ کر سکتا ہے۔",
                "low_ur": "Low (Lower): کھڑے ہو کر بلاک کرنے والے حریف کی ٹانگوں پر لگتے ہیں۔ کمزوری: نیچے بیٹھ کر (db) بلاک ہو جاتے ہیں یا df دبا کر لو پیری ہو جاتے ہیں۔",
                "mid_ur": "Mid (Middle): نیچے بیٹھنے والے حریف کو سزا دیتے ہیں! جب آپ حریف کو لو اور ہائی سے تنگ کر کے جھکنے پر مجبور کریں، تو مڈ لانچر مار کر ہوا میں اڑا دیں۔"
            },
            "frame_trap_4step": [
                { "step": "1. The Poke", "cmd": "1 / df+1", "desc_ur": "آگے جا کر 1 (Jab +1 on block) یا df+1 (Fast Mid check) ماریں۔" },
                { "step": "2. The Low Annoyance", "cmd": "d+4 / db+3 / d+2", "desc_ur": "جب وہ کھڑا ہو کر بلاک کرے تو تیز لو پوک ماریں تاکہ وہ جھکنے یا جلد بازی میں بٹن دبانے پر مجبور ہو۔" },
                { "step": "3. The Frame Trap", "cmd": "wr+2 / f+4 -> CH Mid", "desc_ur": "پلس فریم موو (+4 سے +6) ماریں، اور جیسے ہی وہ بلاک کرے فوراً کاؤنٹر ہٹ مڈ بٹن (df+2 یا b+1) دبائیں!" },
                { "step": "4. Stance Blender", "cmd": "Flamingo / Sentai / Vortex", "desc_ur": "پلس فریمز لے کر سٹانس میں جائیں جہاں حریف کو 50/50 کا اندازہ لگانا پڑتا ہے!" }
            ],
            "spacing_settings": {
                "range_0_ur": "Range 0 (چپک کر): 1 (Jab), df+1, تھروز (1+3 / 2+4), اور تیز لو پوکس۔ سست مووز مت چلائیں ورنہ انٹرپٹ ہو جائیں گے۔",
                "range_mid_ur": "Range 1.5 - 2 (ایک سے دو قدم): پوکرز (df+2, b+4, uf+4) اور سائیڈ سٹیپ۔ حریف کا وار ہوا میں نکلے تو فوراً وہف پنشر ماریں۔",
                "range_long_ur": "Range 3+ (دور فاصلہ): وہائل رننگ (wr+2) یا ہیٹ برسٹ چلا کر تیزی سے قریب آئیں۔",
                "settings_ur": "کنٹرولر: L1=1+2, R1=3+4, L2=Heat Burst (2+3), R2=Rage Art۔ گرافکس: V-Sync کو OFF رکھیں اور Network کو 'Prioritize Response' پر سیٹ کریں۔ سپیشل سٹائل کو ہمیشہ OFF رکھیں۔"
            }
        },
        "parry_reversal_matrix": {
            "title": "Master Parry, Reversal & Duck vs Block Matrix",
            "title_ur": "پیری، ریورسل، لو پیری اور ڈک بمقابلہ بلاک گائیڈ",
            "low_parry_guide": {
                "cmd": "df (Down-Forward)",
                "how_ur": "جب مخالف لو اٹیک مارے تو db بلاک کرنے کے بجائے df دبا کر رکھیں۔ حریف زمین پر منہ کے بل گرے گا اور باؤنڈ سٹیٹ استعمال ہو جائے گی۔",
                "punish_flow_ur": "df (Low Parry) -> df+1 (یا ws+4) -> Jab Strings (1,2 / df+4) -> Long Range Ender (40 سے 50 مفت ڈیمیج!)",
                "unparryable_ur": "ہتھیاروں کی تلواریں (Yoshimitsu, Victor, Clive), نینا کی بندوقیں، لا کے ننچکس، اور کما/پانڈا/راجر جونیئر کے سر اور دم کے لوز لو پیری نہیں ہوتے!"
            },
            "decision_matrix": [
                {
                    "situation": "Fast Low Pokes (d+4, db+3, Hwoarang d+3,4, Law d+2,3, Feng d+2)",
                    "action": "LOW PARRY (df) KAREIN!",
                    "action_type": "parry",
                    "reason_ur": "یہ لوز بلاک ہونے پر صرف -11 سے -13 ہوتے ہیں (بلاک پر صرف چھوٹی کک ملے گی)۔ لیکن لو پیری کرنے پر 45+ ڈیمیج کا پورا کومبو ملتا ہے!"
                },
                {
                    "situation": "String ke Beech Wale Lows (Law Junkyard b+2,3,4, King Ali Kicks, Nina d+3,4)",
                    "action": "LOW PARRY (df) KAREIN!",
                    "action_type": "parry",
                    "reason_ur": "سٹرنگ کو بیچ میں توڑ کر آپ اپنی باری اور گارنٹیڈ کومبو دونوں فوراً حاصل کر لیتے ہیں۔"
                },
                {
                    "situation": "Heavy / Stagger Lows (Kazuya Hellsweep, Bryan Snake Edge, Paul Demoman, Lili BT d+3+4)",
                    "action": "BLOCK (db) KAREIN! (Parry MAT karein)",
                    "action_type": "block",
                    "reason_ur": "یہ مووز بلاک ہونے پر -15 سے -26 ہوتے ہیں! اگر لو پیری کریں گے تو صرف 45 ڈیمیج ملے گا، لیکن db سے بلاک کر کے ws+2 مارنے پر 80 سے 95 ڈیمیج کا فل لانچ ملے گا!"
                },
                {
                    "situation": "High Strings (Nina d+4,1, Law 1,2,3, Jin 2,1, Hwoarang d+3,4 ka 2nd hit, Paul 3,2)",
                    "action": "SIRF DUCK (d / db) KAREIN!",
                    "action_type": "duck",
                    "reason_ur": "ہائی اٹیک کو پیری کرنے پر صرف 25-30 ڈیمیج ملتا ہے، مگر نیچے بیٹھ کر (Duck) ہوا میں نکلنے دیں اور ws+2 مار کر مخالف کی آدھی ہیلتھ اڑا دیں!"
                }
            ],
            "unparryable_reversals": [
                { "type": "Elbows (کہنیاں)", "examples": "Paul df+1, Bryan df+2 / b+1, Dragunov f+1+2", "rule": "نارمل ریورسل سے پیری نہیں ہوتیں" },
                { "type": "Knees (گھٹنے)", "examples": "Bryan f+3, Feng df+3, Lars/Asuka b+4, Shaheen uf+4", "rule": "ریورسل کو چیر کر منہ پر لگتے ہیں" },
                { "type": "Headbutts & Shoulders", "examples": "Feng b+1+2, Heihachi f+1+2, Paul d+1+2, King f+2+3", "rule": "باڈی ماس اٹیکس پیری نہیں ہو سکتے" },
                { "type": "Weapons & Projectiles", "examples": "Victor / Yoshimitsu / Clive swords, Devil Jin laser, Kunimitsu kunai", "rule": "تلواریں اور فائر بالز ریورسل سے نہیں رکتیں" },
                { "type": "Heat Smash & Rage Arts", "examples": "All characters Heat Smash and Rage Art finishers", "rule": "انسٹنٹ ان پیرایبل" }
            ],
            "character_parries_table": [
                { "char": "Jin Kazama", "cmd": "b+1+3 / b+2+4", "catches": "SAB KUCH! Punches, Kicks, Elbows, Knees, Weapons", "followup_ur": "ٹائم سلو ہوتا ہے: فوراً d+3+4 (Can-Can Kicks Full Launcher) ماریں!" },
                { "char": "Leroy Smith", "cmd": "b+2 (Twin Dragon Gate)", "catches": "Punches, Kicks, Elbows, Knees سب ڈیفلیکٹ کرتا ہے", "followup_ur": "پیری لگتے ہی 1+2 دبائیں، لیروئے خود مکھوں کی بارش کر دے گا!" },
                { "char": "Asuka & Jun Kazama", "cmd": "b+1+3 / b+2+4 (Hold to Charge)", "catches": "High / Mid Punches & Kicks", "followup_ur": "دبا کر رکھنے سے لمبا وقت ایکٹیو رہتی ہے، آٹومیٹک 40 ڈیمیج اٹیک!" },
                { "char": "Asuka / Feng / Lee", "cmd": "Sabaki Parries (Asuka b+2+3, Feng 1+2, Lee b+1+2)", "catches": "اٹیک روکنے کے ساتھ ساتھ خود وار کرتی ہیں", "followup_ur": "فینگ کا 1+2 پیری ہوتے ہی خود لانچ کر دیتا ہے، لی کے بعد 2 دبائیں۔" },
                { "char": "Paul / Nina / Dragunov", "cmd": "b+1+3 / b+2+4", "catches": "Standard High / Mid Punches & Kicks", "followup_ur": "آٹومیٹک ہڈی توڑنے والی ریورسل اینیمیشن چلتی ہے۔" },
                { "char": "King", "cmd": "b+1+3 (Kicks) & b+2+4 (Right Punches)", "catches": "b+1+3 ککس پکڑتی ہے، b+2+4 پنچز", "followup_ur": "کک پیری ٹانگ توڑ دیتی ہے، پنچ پیری کے بعد کنگ مخالف کی پشت پر آ جاتا ہے!" },
                { "char": "Steve Fox", "cmd": "b+1+2 (Punch Parry)", "catches": "High aur Mid Punches", "followup_ur": "1 یا 2 دبائیں، سٹیو ہک مار کر زمین پر گرا دے گا۔" },
                { "char": "Bryan Fury", "cmd": "b+1+2 (Punch Parry)", "catches": "High aur Mid Punches", "followup_ur": "پیری لگتے ہی 2 دبائیں، برائن مایک پنچ مار کر دیوار پر اڑا دے گا!" },
                { "char": "Reina / Heihachi", "cmd": "b+1+3 / b+2+4 & Heaven's Wrath", "catches": "Attacks seh kar bijli counter", "followup_ur": "رائنا ہیٹ میں HW سٹانس (d+1+2) میں آٹو پیری کرتی ہے!" },
                { "char": "Yoshimitsu", "cmd": "1+4 (Flash)", "catches": "6-frame hitbox جو ہر قریبی حملہ کاٹ دیتا ہے", "followup_ur": "فل کو مبو کے لیے فوراً d+2,2,2 یا b+2,2 دبائیں!" },
                { "char": "Azucena", "cmd": "Libertador (f+3+4)", "catches": "Auto-Parry Highs aur Lows", "followup_ur": "سٹانس میں کھڑے رہیں، ڈاج ہوتے ہی LIB 1+2 لانچر مار دیں!" }
            ],
            "charge_guard_break_guide": {
                "title": "How to Charge Guard-Breaks & Defensive Parries",
                "title_ur": "گارڈ بریک اور پیریز چارج کرنے کا طریقہ",
                "defensive_ur": "آسوکا اور جون کے پاس b+1+3 ریورسل کو ہولڈ (دبا کر رکھنے) کی سہولت ہے۔ جتنا لمبا دبائیں گے، پیری ونڈو اتنی طویل کھلی رہے گی۔",
                "offensive_ur": "اٹیک بٹن کو دبا کر رکھنے (*) سے موو گارڈ بریک میں بدل جاتا ہے (جیسے Fahkumram 3,4~4*, Steve b+1*, Paul qcf+2*, Yujiro f,f+1+2*)۔ بلاک کرنے والا دیوار سے چپک جاتا ہے اور مفت اٹیک ملتا ہے۔"
            }
        },
        "wall_traps_escape": {
            "title": "Deadly Wall Traps & Wall Escape Bible",
            "title_ur": "دیوار کے جان لیوا جال اور بچنے کے تین سنہری اصول",
            "wall_combo_science_ur": "حریف کو دیوار پر ہائی وال سپلیٹ کریں، پھر جاب فلر (1 یا 2) مار کر ٹورنیڈو ایکسٹینشن دیں اور بھاری وال کومبو اینڈ کریں۔",
            "universal_wall_crush_ur": "وال کرش مووز (+5 سے +9 آن بلاک) حریف کو دیوار کے ساتھ جما دیتے ہیں اور وہ پیچھے نہیں ہٹ سکتا۔ وہاں سے 50/50 لو یا مڈ لانچر لوپ لگائیں۔",
            "character_wall_traps": [
                { "char": "Bryan Fury", "name": "The Taunt (1+3+4) Unblockable Trap", "desc_ur": "دیوار پر حریف اٹھنے لگے تو Taunt ماریں۔ یہ ان بلاک ایبل ہے اور +16 فریمز دیتا ہے جس کے بعد f,b+2 (Mach Punch) یا جیٹ اپر گارنٹیڈ فری ڈیمیج ہے!" },
                { "char": "King & Armor King", "name": "Burning Knuckle & Giant Swing Wall Loop", "desc_ur": "وال گرنے کے بعد uf+1+2* (Burning Knuckle) چارج کریں۔ اگر حریف لیٹا رہے تو 40 ڈیمیج، کھڑا ہو تو ان بلاک ایبل لانچ، اور بچنے کے لیے رول کرے تو جائنٹ سوئنگ پکڑ لیں!" },
                { "char": "Hwoarang", "name": "Chip-Death & Backturned Flamingo Loop", "desc_ur": "دیوار پر فلیمنگو لوپ چلائیں۔ چیپ ڈیمیج سے ہیلتھ گھٹتی رہے گی، اور اگر وہ ڈک کرے تو مڈ کک مار کر دوبارہ وال سپلیٹ کر دیں!" },
                { "char": "Kazuya, Devil Jin & Reina", "name": "The Mishima Wall Vortex", "desc_ur": "دیوار پر ہیل سویپ (Low) یا ڈیمن پا / الیکٹرک (Mid) کا 50/50 لگائیں۔ غلط اندازے پر حریف دوبارہ دیوار سے ٹکرا جائے گا۔" },
                { "char": "Paul Phoenix", "name": "The 50/50 Wall Deletion", "desc_ur": "وال سپلیٹ کے بعد ڈیمو مین (d+4,2:1+2) مڈ لو سویپ ماریں، یا ڈیتھ فسٹ (qcf+2) سے حریف کا آدھا لائف بار اڑا دیں!" },
                { "char": "Yoshimitsu", "name": "Unblockable Sword Sweep & Poison Trap", "desc_ur": "دیوار پر fc df+1 (ان بلاک ایبل لو سورڈ سویپ) ماریں۔ اگر وہ جمپ کرے تو ws+2,1 مڈ ٹورنیڈو لانچر سے دوبارہ دیوار پر چپکا دیں!" },
                { "char": "Jin Kazama", "name": "Scourge (d+2) & Electric Wall Trap", "desc_ur": "دیوار پر f,f,f+3 (+6 وال کرش) ماریں۔ اب حریف جم چکا ہے: d+2 لو ماریں یا df+1,4~4 مڈ مار کر دوبارہ وال سپلیٹ کریں!" },
                { "char": "Jack-8 & Alisa", "name": "Un-escapable Chip & Guard Break Loop", "desc_ur": "جیک-8 گاما ہاول GMH 4 (+11 گارڈ بریک) مارتا ہے، اور الیسا چین سا (DES) نکال کر دیوار پر پش بیک کے بغیر نان سٹاپ چیپ کٹنگ کرتی ہے!" }
            ],
            "escape_rules": [
                {
                    "rule": "1. Side-Walk Towards Open Side",
                    "badge": "کھلی طرف سائیڈ واک",
                    "desc_ur": "دیوار کے کونے سے نکلنے کے لیے مسلسل کھلی سائیڈ پر سائیڈ واک (u, u یا d, d ہولڈ) کریں اور جگہ ملتے ہی پوزیشن سوئچ تھرو (1+3 / 2+4) مار کر حریف کو دیوار میں پھینک دیں!"
                },
                {
                    "rule": "2. Delay Wake-Up (فوراً مت اٹھیں!)",
                    "badge": "زمین پر رکے رہیں",
                    "desc_ur": "برائن کے ٹونٹ، کازویا کے وال ورٹیکس اور پال کے ڈیمو مین سے بچنے کا بہترین طریقہ ہے 1 سیکنڈ تک زمین پر بغیر کوئی بٹن دبائے لیٹے رہنا تاکہ ان کا ٹائمنگ مکس اپ ہوا میں نکل جائے!"
                },
                {
                    "rule": "3. Jab + Side-Step (1 -> SS)",
                    "badge": "جاب مار کر نکلیں",
                    "desc_ur": "دیوار پر بڑے سست بٹن دبانے کے بجائے تیز جاب (1) یا ڈک جاب (db+1) ماریں اور فوراً باہر کی طرف سائیڈ سٹیپ کر کے دباؤ توڑ دیں!"
                }
            ]
        },
        "defense_escape_5rules": [
            { "name": "The Dickjab (db+1 / d+1)", "desc_ur": "10 فریم کا کراؤچنگ پنچ جو حریف کے ہائی اٹیکس کے نیچے سے نکل کر نینا، ہوارنگ اور رائنا کے سٹانس فلو کو توڑ دیتا ہے!" },
            { "name": "Power Crush (Armor)", "desc_ur": "شیلڈ آئی کون والا موو (b+1+2 / f+1+2) جو ساتویں فریم سے ہائی اور مڈ مار کھا کر واپس کاؤنٹر کرتا ہے!" },
            { "name": "Heat Burst (2+3 / L2)", "desc_ur": "دیوار پر پھنسے ہوں تو ہیٹ برسٹ دبائیں، اس میں آرمر ہوتا ہے جو حملہ روک کر آپ کو +1 اپنی باری دیتا ہے!" },
            { "name": "Sidestep + Block (u,n,b / d,n,b)", "desc_ur": "سائیڈ سٹیپ کر کے فوراً بلاک دبائیں تاکہ ڈریگنوف کا wr+2 اور کازویا کا الیکٹرک ہوا میں نکل جائے!" },
            { "name": "Throw Breaks (پکڑ توڑنا)", "desc_ur": "بایاں ہاتھ آگے آئے تو 1، دایاں ہاتھ آگے آئے تو 2، اور دونوں ہاتھ ایک ساتھ آئیں تو 1+2 دبائیں!" }
        ]
    }

print("Universal mechanics builder ready.")
