/**
 * TEKKEN 8 MASTER STRATEGY HUB & ROSTER DATA LAYER
 * Authoritative Canonical Reference for 44 Characters (32 Base + 12 DLCs)
 * Universal Mechanics: Controls, Frame Data, Master Low Parry Matrix, Wall Traps & Escape Bible.
 * Version: Tekken 8 Patch v3.00.02
 */

(function () {
  'use strict';

  const UNIVERSAL_MECHANICS = {
  "title": "Tekken 8 Universal Combat Mechanics & Tournament Science",
  "title_ur": "ٹیکن 8 کے بنیادی اصول، فریم ڈیٹا اور ایڈوانس سسٹمز",
  "controls_notation": {
    "title": "Button Notation & Attack Legend",
    "title_ur": "بٹنوں کی پہچان اور نوٹیشن",
    "desc_ur": "ٹیکن میں ہر موو کو عالمی نمبرز اور ڈائریکشنز سے لکھا جاتا ہے تاکہ پلے اسٹیشن، ایکس باکس اور پی سی پر کھیلنا آسان ہو۔",
    "buttons": [
      {
        "btn": "1",
        "name": "Left Punch (LP)",
        "ps": "Square ▢",
        "xb": "X",
        "desc_ur": "سب سے تیز رفتار بنیادی مکہ (10 فریم جاب)"
      },
      {
        "btn": "2",
        "name": "Right Punch (RP)",
        "ps": "Triangle △",
        "xb": "Y",
        "desc_ur": "بھاری سیدھا مکہ، کاؤنٹر ہٹ اور ہٹ کنفرم کے لیے بہترین"
      },
      {
        "btn": "3",
        "name": "Left Kick (LK)",
        "ps": "Cross ✕",
        "xb": "A",
        "desc_ur": "تیز رفتار بائیں ٹانگ کی کک، فاصلہ برقرار رکھنے کا ٹول"
      },
      {
        "btn": "4",
        "name": "Right Kick (RK)",
        "ps": "Circle ◯",
        "xb": "B",
        "desc_ur": "طاقتور دائیں لات، ہاپ کک، ہومنگ یا لانچر مووز"
      },
      {
        "btn": "1+2",
        "name": "Dual Punch",
        "ps": "▢ + △",
        "xb": "X + Y",
        "desc_ur": "دونوں مکے ایک ساتھ (پاور کرش، کمانڈ تھرو، یا بریک تھرو)"
      },
      {
        "btn": "3+4",
        "name": "Dual Kick",
        "ps": "✕ + ◯",
        "xb": "A + B",
        "desc_ur": "دونوں لاتیں ایک ساتھ (سٹانسز اور جمپنگ لانچرز)"
      }
    ],
    "directions": [
      {
        "dir": "f",
        "name": "Forward",
        "ur": "آگے بڑھنا"
      },
      {
        "dir": "b",
        "name": "Back / Block",
        "ur": "پیچھے ہٹنا / ہائی اور مڈ بلاک"
      },
      {
        "dir": "d",
        "name": "Down",
        "ur": "نیچے جھکنا"
      },
      {
        "dir": "u",
        "name": "Up",
        "ur": "اوپر اچھلنا"
      },
      {
        "dir": "df",
        "name": "Down-Forward",
        "ur": "آگے اور نیچے ترچھا (پوکس اور لو پیری df)"
      },
      {
        "dir": "db",
        "name": "Down-Back",
        "ur": "پیچھے اور نیچے ترچھا (لو بلاک اور ہائی ڈک db)"
      },
      {
        "dir": "uf",
        "name": "Up-Forward",
        "ur": "آگے اور اوپر (ہاپ کک uf+4)"
      },
      {
        "dir": "ff / f,f",
        "name": "Dash",
        "ur": "دو دفعہ تیز آگے دبانا (ڈیش)"
      },
      {
        "dir": "wr (f,f,f)",
        "name": "While Running",
        "ur": "تین دفعہ آگے دبا کر بھاگتے ہوئے حملہ کرنا (+ آن بلاک)"
      },
      {
        "dir": "ws",
        "name": "While Standing / Rising",
        "ur": "ڈک (نیچے بیٹھنے) کے بعد اٹھتے وقت حملہ کرنا"
      },
      {
        "dir": "CH",
        "name": "Counter Hit",
        "ur": "جب حریف حملہ کر رہا ہو اور آپ کا وار پہلے لگ جائے"
      }
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
      {
        "step": "1. The Poke",
        "cmd": "1 / df+1",
        "desc_ur": "آگے جا کر 1 (Jab +1 on block) یا df+1 (Fast Mid check) ماریں۔"
      },
      {
        "step": "2. The Low Annoyance",
        "cmd": "d+4 / db+3 / d+2",
        "desc_ur": "جب وہ کھڑا ہو کر بلاک کرے تو تیز لو پوک ماریں تاکہ وہ جھکنے یا جلد بازی میں بٹن دبانے پر مجبور ہو۔"
      },
      {
        "step": "3. The Frame Trap",
        "cmd": "wr+2 / f+4 -> CH Mid",
        "desc_ur": "پلس فریم موو (+4 سے +6) ماریں، اور جیسے ہی وہ بلاک کرے فوراً کاؤنٹر ہٹ مڈ بٹن (df+2 یا b+1) دبائیں!"
      },
      {
        "step": "4. Stance Blender",
        "cmd": "Flamingo / Sentai / Vortex",
        "desc_ur": "پلس فریمز لے کر سٹانس میں جائیں جہاں حریف کو 50/50 کا اندازہ لگانا پڑتا ہے!"
      }
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
      {
        "type": "Elbows (کہنیاں)",
        "examples": "Paul df+1, Bryan df+2 / b+1, Dragunov f+1+2",
        "rule": "نارمل ریورسل سے پیری نہیں ہوتیں"
      },
      {
        "type": "Knees (گھٹنے)",
        "examples": "Bryan f+3, Feng df+3, Lars/Asuka b+4, Shaheen uf+4",
        "rule": "ریورسل کو چیر کر منہ پر لگتے ہیں"
      },
      {
        "type": "Headbutts & Shoulders",
        "examples": "Feng b+1+2, Heihachi f+1+2, Paul d+1+2, King f+2+3",
        "rule": "باڈی ماس اٹیکس پیری نہیں ہو سکتے"
      },
      {
        "type": "Weapons & Projectiles",
        "examples": "Victor / Yoshimitsu / Clive swords, Devil Jin laser, Kunimitsu kunai",
        "rule": "تلواریں اور فائر بالز ریورسل سے نہیں رکتیں"
      },
      {
        "type": "Heat Smash & Rage Arts",
        "examples": "All characters Heat Smash and Rage Art finishers",
        "rule": "انسٹنٹ ان پیرایبل"
      }
    ],
    "character_parries_table": [
      {
        "char": "Jin Kazama",
        "cmd": "b+1+3 / b+2+4",
        "catches": "SAB KUCH! Punches, Kicks, Elbows, Knees, Weapons",
        "followup_ur": "ٹائم سلو ہوتا ہے: فوراً d+3+4 (Can-Can Kicks Full Launcher) ماریں!"
      },
      {
        "char": "Leroy Smith",
        "cmd": "b+2 (Twin Dragon Gate)",
        "catches": "Punches, Kicks, Elbows, Knees سب ڈیفلیکٹ کرتا ہے",
        "followup_ur": "پیری لگتے ہی 1+2 دبائیں، لیروئے خود مکھوں کی بارش کر دے گا!"
      },
      {
        "char": "Asuka & Jun Kazama",
        "cmd": "b+1+3 / b+2+4 (Hold to Charge)",
        "catches": "High / Mid Punches & Kicks",
        "followup_ur": "دبا کر رکھنے سے لمبا وقت ایکٹیو رہتی ہے، آٹومیٹک 40 ڈیمیج اٹیک!"
      },
      {
        "char": "Asuka / Feng / Lee",
        "cmd": "Sabaki Parries (Asuka b+2+3, Feng 1+2, Lee b+1+2)",
        "catches": "اٹیک روکنے کے ساتھ ساتھ خود وار کرتی ہیں",
        "followup_ur": "فینگ کا 1+2 پیری ہوتے ہی خود لانچ کر دیتا ہے، لی کے بعد 2 دبائیں۔"
      },
      {
        "char": "Paul / Nina / Dragunov",
        "cmd": "b+1+3 / b+2+4",
        "catches": "Standard High / Mid Punches & Kicks",
        "followup_ur": "آٹومیٹک ہڈی توڑنے والی ریورسل اینیمیشن چلتی ہے۔"
      },
      {
        "char": "King",
        "cmd": "b+1+3 (Kicks) & b+2+4 (Right Punches)",
        "catches": "b+1+3 ککس پکڑتی ہے، b+2+4 پنچز",
        "followup_ur": "کک پیری ٹانگ توڑ دیتی ہے، پنچ پیری کے بعد کنگ مخالف کی پشت پر آ جاتا ہے!"
      },
      {
        "char": "Steve Fox",
        "cmd": "b+1+2 (Punch Parry)",
        "catches": "High aur Mid Punches",
        "followup_ur": "1 یا 2 دبائیں، سٹیو ہک مار کر زمین پر گرا دے گا۔"
      },
      {
        "char": "Bryan Fury",
        "cmd": "b+1+2 (Punch Parry)",
        "catches": "High aur Mid Punches",
        "followup_ur": "پیری لگتے ہی 2 دبائیں، برائن مایک پنچ مار کر دیوار پر اڑا دے گا!"
      },
      {
        "char": "Reina / Heihachi",
        "cmd": "b+1+3 / b+2+4 & Heaven's Wrath",
        "catches": "Attacks seh kar bijli counter",
        "followup_ur": "رائنا ہیٹ میں HW سٹانس (d+1+2) میں آٹو پیری کرتی ہے!"
      },
      {
        "char": "Yoshimitsu",
        "cmd": "1+4 (Flash)",
        "catches": "6-frame hitbox جو ہر قریبی حملہ کاٹ دیتا ہے",
        "followup_ur": "فل کو مبو کے لیے فوراً d+2,2,2 یا b+2,2 دبائیں!"
      },
      {
        "char": "Azucena",
        "cmd": "Libertador (f+3+4)",
        "catches": "Auto-Parry Highs aur Lows",
        "followup_ur": "سٹانس میں کھڑے رہیں، ڈاج ہوتے ہی LIB 1+2 لانچر مار دیں!"
      }
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
      {
        "char": "Bryan Fury",
        "name": "The Taunt (1+3+4) Unblockable Trap",
        "desc_ur": "دیوار پر حریف اٹھنے لگے تو Taunt ماریں۔ یہ ان بلاک ایبل ہے اور +16 فریمز دیتا ہے جس کے بعد f,b+2 (Mach Punch) یا جیٹ اپر گارنٹیڈ فری ڈیمیج ہے!"
      },
      {
        "char": "King & Armor King",
        "name": "Burning Knuckle & Giant Swing Wall Loop",
        "desc_ur": "وال گرنے کے بعد uf+1+2* (Burning Knuckle) چارج کریں۔ اگر حریف لیٹا رہے تو 40 ڈیمیج، کھڑا ہو تو ان بلاک ایبل لانچ، اور بچنے کے لیے رول کرے تو جائنٹ سوئنگ پکڑ لیں!"
      },
      {
        "char": "Hwoarang",
        "name": "Chip-Death & Backturned Flamingo Loop",
        "desc_ur": "دیوار پر فلیمنگو لوپ چلائیں۔ چیپ ڈیمیج سے ہیلتھ گھٹتی رہے گی، اور اگر وہ ڈک کرے تو مڈ کک مار کر دوبارہ وال سپلیٹ کر دیں!"
      },
      {
        "char": "Kazuya, Devil Jin & Reina",
        "name": "The Mishima Wall Vortex",
        "desc_ur": "دیوار پر ہیل سویپ (Low) یا ڈیمن پا / الیکٹرک (Mid) کا 50/50 لگائیں۔ غلط اندازے پر حریف دوبارہ دیوار سے ٹکرا جائے گا۔"
      },
      {
        "char": "Paul Phoenix",
        "name": "The 50/50 Wall Deletion",
        "desc_ur": "وال سپلیٹ کے بعد ڈیمو مین (d+4,2:1+2) مڈ لو سویپ ماریں، یا ڈیتھ فسٹ (qcf+2) سے حریف کا آدھا لائف بار اڑا دیں!"
      },
      {
        "char": "Yoshimitsu",
        "name": "Unblockable Sword Sweep & Poison Trap",
        "desc_ur": "دیوار پر fc df+1 (ان بلاک ایبل لو سورڈ سویپ) ماریں۔ اگر وہ جمپ کرے تو ws+2,1 مڈ ٹورنیڈو لانچر سے دوبارہ دیوار پر چپکا دیں!"
      },
      {
        "char": "Jin Kazama",
        "name": "Scourge (d+2) & Electric Wall Trap",
        "desc_ur": "دیوار پر f,f,f+3 (+6 وال کرش) ماریں۔ اب حریف جم چکا ہے: d+2 لو ماریں یا df+1,4~4 مڈ مار کر دوبارہ وال سپلیٹ کریں!"
      },
      {
        "char": "Jack-8 & Alisa",
        "name": "Un-escapable Chip & Guard Break Loop",
        "desc_ur": "جیک-8 گاما ہاول GMH 4 (+11 گارڈ بریک) مارتا ہے، اور الیسا چین سا (DES) نکال کر دیوار پر پش بیک کے بغیر نان سٹاپ چیپ کٹنگ کرتی ہے!"
      }
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
    {
      "name": "The Dickjab (db+1 / d+1)",
      "desc_ur": "10 فریم کا کراؤچنگ پنچ جو حریف کے ہائی اٹیکس کے نیچے سے نکل کر نینا، ہوارنگ اور رائنا کے سٹانس فلو کو توڑ دیتا ہے!"
    },
    {
      "name": "Power Crush (Armor)",
      "desc_ur": "شیلڈ آئی کون والا موو (b+1+2 / f+1+2) جو ساتویں فریم سے ہائی اور مڈ مار کھا کر واپس کاؤنٹر کرتا ہے!"
    },
    {
      "name": "Heat Burst (2+3 / L2)",
      "desc_ur": "دیوار پر پھنسے ہوں تو ہیٹ برسٹ دبائیں، اس میں آرمر ہوتا ہے جو حملہ روک کر آپ کو +1 اپنی باری دیتا ہے!"
    },
    {
      "name": "Sidestep + Block (u,n,b / d,n,b)",
      "desc_ur": "سائیڈ سٹیپ کر کے فوراً بلاک دبائیں تاکہ ڈریگنوف کا wr+2 اور کازویا کا الیکٹرک ہوا میں نکل جائے!"
    },
    {
      "name": "Throw Breaks (پکڑ توڑنا)",
      "desc_ur": "بایاں ہاتھ آگے آئے تو 1، دایاں ہاتھ آگے آئے تو 2، اور دونوں ہاتھ ایک ساتھ آئیں تو 1+2 دبائیں!"
    }
  ]
};

  const ROSTER_DATA = [
  {
    "id": 1,
    "slug": "jin",
    "name": "Jin Kazama",
    "title": "The Lightning of Fate",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Yggdrasil Alliance",
    "season": "Base",
    "style": "Traditional Karate • Kazama Self-Defense",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/jin.jpg",
    "height": "183 cm (6'0\")",
    "weight": "87 kg",
    "job_lore_ur": "Former Head of Mishima Zaibatsu; duniya ko apni shuru ki gayi jang aur Kazuya se bachane ke liye larta hai.",
    "poking_buttons_ur": "Poking Buttons: 1,2 (Jabs), df+1 (Mid check), f+4 (Long range mid CH launcher), d+4 (Fast low), db+4 (Plus frame low).",
    "pressure_moves_ur": "Pressure Moves: 2,1,4 (Safe string), f,f,f+3 (Running mid kick: +6 on block!), Electric Wind Hook Fist (f,n,d,df:2 - +5 on block).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up: Zenshin Stance (ZEN - b+3+4 ya f+4~f):\nLow: ZEN 4 (Diving sweep जो ज़मीन पर गिराता ہے) ya Hellsweep (f,n,d,df+4).\nMid: ZEN 1+2 ya ZEN 3 (Homing mid).\nHigh/Throw: ZEN 1+3 (Unbreakable stance grab) ya ZEN u+1 (Evasive launcher).",
    "trap_setup_ur": "Jaal (Trap Setup): d+2 (Scourge - High-crushing low jo CH par launch karta hai) aur f+4 se paas aayein. Jab woh darr kar block kare, 2,1 mar kar ruk jayein aur uf+2 (evasive punch) ya Throw (uf+1+2) mar dein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) karein taake EWHF, 2,1, aur f+4 hawa mein nikal jayein. Lekin Jin ka df+1 right track karta hai is liye mid-range par step-block karein.",
      "minus_punishable_moves_ur": "-10 to -14: 2,1,4 (-6 safe magar 3rd hit duckable), df+1,4 (-13 punish), d+2 (-14 crouching punish). -15+ Launch: d+3+4 Can-Can (-15 Launch), db+4 (-15 Launch on block), ZEN 4 diving sweep (-26 Launch).",
      "bait_duck_interrupt_ur": "2,1,4 ka aakhri hit High hai: duck kar ke ws+2 launcher marein! d+2 ko duck kar ke block karein aur ws launch dein. ZEN 1+3 throw ko break ya duck karein. d+4 fast low poke ko df se Low Parry karein.",
      "parry_vulnerabilities_ur": "Jin ki b+1+3 parry har cheez (weapons, elbows, knees) deflect karti hai! Is se bachne ke liye delay timing karein ya low attacks marein jo b+1+3 se parry nahi hotay."
    }
  },
  {
    "id": 2,
    "slug": "kazuya",
    "name": "Kazuya Mishima",
    "title": "Cold-Blooded Overlord",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "G-Corporation & Kazuya's Allies",
    "faction_badge": "G-Corp",
    "season": "Base",
    "style": "Mishima Style Fighting Karate",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/kazuya.jpg",
    "height": "181 cm (5'11\")",
    "weight": "85 kg",
    "job_lore_ur": "Head of G Corporation; apne baap Heihachi ko marne ke baad duniya par apni hukoomat qaim karna chahta hai.",
    "poking_buttons_ur": "Poking Buttons: 1,1 (Hit-confirmable 1,1,2), df+4 (Mid check), db+4 (Stature kick low: +4 on hit!), df+1,2.",
    "pressure_moves_ur": "Pressure Moves: EWGF (f,n,d,df:2 - +5 on block), f+4 (Crouch-forcing mid: +4 on block), cd+1+2 (+5 on block).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (The Ultimate 50/50 Vortex): Wave-dash (f,n,d,df~f...) karte hue aage jayein:\nLow: Hellsweep (f,n,d,df+4,1) – Zameen par gira kar dobara mix-up shuru karta hai.\nMid: ff+3 (Left splits kick - Safe Mid Launcher!) ya ff+2 (Long range mid demon paw).",
    "trap_setup_ur": "Jaal (Trap Setup): Opponent ko db+4 ya f+4 (block par) marein. Ab aap +4 hain. Foran df+2 दबाएं—agar agle bande ne jab bhi dabaya toh CH df+2 (Perfect Electric) se uski 70% life khatam!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Kazuya ki sabse bari maut hai! EWGF, df+1, ff+3 aur cd+1+2 sab SSL par whiff ho jate hain. SSR ghalti se bhi mat karein warna Hellsweep clip karega.",
      "minus_punishable_moves_ur": "-10 to -14: 1,1,2 (-17 on block - launch!), df+1,2 (-12 punish), f+1+2 (-12). -15+ Launch: Hellsweep (cd+4,1 -23 Stagger Low Launch!), df+2 (-15 Mid Launcher), Twin Pistons ws+1,2 (-15 Launch).",
      "bait_duck_interrupt_ur": "Wave-dash dekh kar ghabrayein mat. Hellsweep ko db se BLOCK karein (df parry mat karein) aur ws+2 se 85+ damage ka combo dein! 1,1,2 agar hit na ho toh 3rd hit block kar ke launch karein.",
      "parry_vulnerabilities_ur": "Kazuya ke paas normal parry nahi hai. Uske db+4 stature kick ko df se low parry karein. Kazuya ke f,f+3 mid kick aur EWGF punch parry ho sakte hain."
    }
  },
  {
    "id": 3,
    "slug": "reina",
    "name": "Reina",
    "title": "The Purple Spark",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Mishima Bloodline & Enforcers",
    "faction_badge": "Mishima Bloodline",
    "season": "Base",
    "style": "Mishima Style Karate • Taido",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/reina.jpg",
    "height": "160 cm (5'3\")",
    "weight": "~54 kg",
    "job_lore_ur": "Mishima Polytechnical School ki student aur Heihachi ki khufiya beti jo Devil Gene jagane aayi hai.",
    "poking_buttons_ur": "Poking Buttons: 1,1 (Confirm into 1,1,2), df+1,1, f+4 (Mid crouching pressure), db+4 (Low poke), ss+4 (Sidestep low).",
    "pressure_moves_ur": "Pressure Moves: ff+2 (Demon breath into Sentai Stance SEN - Sabse best approach tool), f,f,f+3 (+6 on block into Heaven's Wrath HW).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Sentai Stance ff+2~f):\nMid: SEN 3 (Fast safe homing kick) ya SEN 2 (Safe mid).\nLow: SEN 3+4 (Double low sweep).\nUnblockable Throw: SEN 1+3 (Sirf duck kar ke bacha ja sakta hai, break nahi hota!).",
    "trap_setup_ur": "Jaal (Trap Setup): ff+2 spam karein. Jab woh block kare, SEN 3 (High) ya SEN 1+3 (Throw) marein. Jab woh duck karne lage, toh SEN 2 ya df+2 se launch kar dein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) karein. ff+2, EWGF, aur Sentai (SEN) transitions SSL par hawa mein nikal jate hain.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,1 (-12 punish), f+4 (-13). -15+ Launch: cd+4 Hellsweep (-23 Stagger Launch!), SEN 3 sweep (-20 Launch), HW 3+4 (-15 Launch).",
      "bait_duck_interrupt_ur": "ff+2 block hote hi foran DICKJAB (db+1) marein! Yeh Reina ke Sentai flow ko wahin tod deta hai aur uski saari fake 50/50 options band kar deta hai.",
      "parry_vulnerabilities_ur": "Reina Heat mein Heaven's Wrath (HW d+1+2) mein auto-parry karti hai! HW mein khari ho toh punches/kicks mat marein, balke Elbows, Knees, ya Lows chalayein."
    }
  },
  {
    "id": 4,
    "slug": "jun",
    "name": "Jun Kazama",
    "title": "Light of Sanctuary",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Kazama Clan",
    "season": "Base",
    "style": "Kazama Style Traditional Martial Arts",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/jun.jpg",
    "height": "170 cm (5'7\")",
    "weight": "54 kg",
    "job_lore_ur": "Wildlife Surveillance Officer (WWW.C); Jin ki maa jo Yakushima ke muqaddas jangal se lauti hai.",
    "poking_buttons_ur": "Poking Buttons: 1,2 (Into Izumo stance), df+1, b+4,2, db+3 (Plus on hit low), f+4 (Plus on block high).",
    "pressure_moves_ur": "Pressure Moves: ss+4 (+6 on block mid!), f+1+2 (Plus into Miare stance), 1,2,2 (+4 on block into Izumo).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Izumo Stance IZU & Genjitsu GEN):\nLow: GEN 1 (Low poke) ya fc df+2 (Crouch low).\nMid: IZU 3 (Mid launcher) ya GEN 2 (Safe mid).\nThrow: IZU 1+3 (Unbreakable grab).",
    "trap_setup_ur": "Jaal (Trap Setup): 1,2,2 ya u+2 se Izumo stance mein jayein. Agar opponent button dabaye toh IZU 1,1 usay CH launch karega; agar chup khara rahe toh IZU 1+3 throw ya low marein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) karein taake Genjitsu (GEN) aur Izumo (IZU) transitions aur f+2 whiff ho jayein.",
      "minus_punishable_moves_ur": "-10 to -14: f+2,1 (-13 punish), df+1,2 (-12). -15+ Launch: db+4 (-17 Stagger Launch!), can-can kicks d+3+4 (-15 Launch), Izumo 4 (-16 Launch).",
      "bait_duck_interrupt_ur": "1,2,2 aur b+4,2 strings mein high extensions hain: duck kar ke ws+2 launcher marein! db+3 low poke ko df se low parry karein.",
      "parry_vulnerabilities_ur": "Jun b+1+3 parry ko hold kar sakti hai! Parry todne ke liye Elbows (Paul df+1, Bryan b+1), Knees, ya Weapons chalayein."
    }
  },
  {
    "id": 5,
    "slug": "devil-jin",
    "name": "Devil Jin",
    "title": "Black Wings of Ruin",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Mishima Bloodline & Enforcers",
    "faction_badge": "Devil Entity",
    "season": "Base",
    "style": "Advanced Mishima Style • Devil Arts",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/devil-jin.jpg",
    "height": "183 cm (6'0\")",
    "weight": "87 kg",
    "job_lore_ur": "Jin Kazama ke andar ka Devil Gene jo mukammal tabahi chahta hai.",
    "poking_buttons_ur": "Poking Buttons: 1,1 (Confirm 1,1,2), df+1,2, db+2 (High-crushing low: +3 on hit), b+4 (Steel pedal mid).",
    "pressure_moves_ur": "Pressure Moves: EWGF (f,n,d,df:2), uf+1 (Shackles chain into Mourning Crow MC stance), f,f,f+3 (+6 on block).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up:\nLow: Hellsweep (cd+4,1+2) – Full combo launcher on normal hit!\nMid: cd+1+2 या uf+4 (Safe mid knockdown into MC).\nUnblockable: MC 1+3 (Flying grab) ya b+1+4 (Lightning dive).",
    "trap_setup_ur": "Jaal (Trap Setup): Wave-dash se Hellsweep ka khauf paida karein. Jaise hi agla banda Hellsweep block karne ke liye neeche bethe, ff+2 ya uf+4 mar kar usay deewar tak le jayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) karein. EWGF, b+4, aur laser scraper strings SSL par nikal jate hain. cd+3 homing se bach kar neutral rahein.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12 punish), b+1,2 (-13). -15+ Launch: Hellsweep (cd+4,4 -26 Stagger Launch!), cd+1 (-15 Launch), d+3+4 can-cans (-15 Launch).",
      "bait_duck_interrupt_ur": "Laser attacks (1+2 ya fly 1+2) ko duck karein ya sidestep karein. Hellsweep ko db se block kar ke full combo ws launcher marein! Flying mix-up par 1 jab se float karein.",
      "parry_vulnerabilities_ur": "Devil Jin ke lasers aur fly moves parry nahi hotay. Lekin uske normal punches/kicks standard parry se pakray ja sakte hain."
    }
  },
  {
    "id": 6,
    "slug": "lars",
    "name": "Lars Alexandersson",
    "title": "Lion of the Rebellion",
    "country": "Sweden",
    "country_flag": "🇸🇪",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Yggdrasil Leader",
    "season": "Base",
    "style": "Tekken Forces Martial Arts",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/lars.jpg",
    "height": "185 cm (6'1\")",
    "weight": "83 kg",
    "job_lore_ur": "Yggdrasil Rebel Army ka Commander; pehle Mishima Tekken Force ka officer tha.",
    "poking_buttons_ur": "Poking Buttons: df+1 (Ab iske extensions df+1,1 aur df+1,3 hain!), 2,1 (Safe mid-mid), db+1,3 (Fast low poke), b+4 (Knee CH).",
    "pressure_moves_ur": "Pressure Moves: Dynamic Entry (DEN - f+3), Silent Entry (SEN - f+3~f), aur Limited Entry (LEN - d+3+4). DEN 3 (Homing mid jo block par +5 deta hai aur SEN mein jata hai!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (LEN Stance - db+2,1~d ya ws+2~d ke baad):\nLow: LEN 1 (Heavy low knockdown).\nMid: LEN 2 (Safe mid launcher/heat engager!).",
    "trap_setup_ur": "Jaal (Trap Setup): DEN 3 marein (Block par +5 in SEN). Ab agla banda hila bhi toh SEN 1 (Heat engager) ya SEN 3 (Launcher) lagega. Agar woh khara raha toh SEN 2 (Low) mar dein.",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Lars ke khilaf bohot effective hai. Dynamic Entry (DEN) aur Silent Entry (SEN) ke attacks SSR par whiff hotay hain.",
      "minus_punishable_moves_ur": "-10 to -14: fb+2,1 (-12 punish), f+1+2 (-12), df+2,1 (-13). -15+ Launch: db+4 (-15 Stagger Launch), DEN 2 sweep (-18 Launch), orbital kick uf+3 (-16 on block).",
      "bait_duck_interrupt_ur": "Lars jab DEN ya SEN mein dash kare, toh foran DICKJAB (db+1) marein! Is se uski flashing movement aur high/mid mix-up foran cancel ho jata hai.",
      "parry_vulnerabilities_ur": "Lars ke paas koi special reversal nahi hai. Uske DEN kicks aur punch strings ko easy parry kiya ja sakta hai."
    }
  },
  {
    "id": 7,
    "slug": "lee",
    "name": "Lee Chaolan",
    "title": "Silver-Haired Demon",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Violet Systems",
    "season": "Base",
    "style": "Mishima Style Karate • Martial Arts",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/lee.jpg",
    "height": "180 cm (5'11\")",
    "weight": "67 kg",
    "job_lore_ur": "CEO of Violet Systems (Humanoid Robotics company); Heihachi ne bachpan mein adopt kiya tha.",
    "poking_buttons_ur": "Poking Buttons: df+1 (Best mid check), 2,2,3 (10f string), d+3 (High-crushing low CH launcher!), db+3+4 (Heavy low: +4 on hit).",
    "pressure_moves_ur": "Pressure Moves: f,f,f+3,4 (+3 on block into Hitman), b+3,3~f (Low-high into Mist Step: +4 on hit).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Crouch / Slide Mix-up):\nLow: Slide (fc df,d,df+3) – Neeche phisal kar tangon par lagta hai.\nMid: ws+2,3 (Safe mid launcher / Heat burst combo!).",
    "trap_setup_ur": "Jaal (Trap Setup): df+1 ya d+3 mar kar Hitman Stance (3+4) mein jayein, ya दूर se b+4 (Keep-out kick) marein. Jab agla banda gussa ho kar aage bhage, toh 4,4:4 ya b+4 se CH launch kar dein!\nB. The Main Story Heroes & Allies",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Lee ke b+4, f,f+3, aur Hitman (HMS) pokes ko aasani se evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: 1,2,4 (-13), df+1,2 (-12), b+1:1,2 (-14). -15+ Launch: Slide fc df,d,df+3 (-23 Stagger Launch!), d+4,4 (-16 Launch), HMS 3 sweep (-18 Launch).",
      "bait_duck_interrupt_ur": "Acid Rain aur 1,2,4 ke aakhri hits high hain: duck kar ke ws launcher marein! Slide ko db se block kar ke maximum damage hopkick marein.",
      "parry_vulnerabilities_ur": "Lee ke paas b+1+2 punch parry hai. Agar woh parry lagaye toh Knees (Bryan f+3, Lars b+4) ya Elbows marein jo Lee ki parry ko cheer deti hain."
    }
  },
  {
    "id": 8,
    "slug": "xiaoyu",
    "name": "Ling Xiaoyu",
    "title": "Dancing Phoenix",
    "country": "China",
    "country_flag": "🇨🇳",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Jin's Protector",
    "season": "Base",
    "style": "Baguazhang • Piguazhang",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/xiaoyu.jpg",
    "height": "159 cm (5'2.5\")",
    "weight": "45 kg",
    "job_lore_ur": "High School / College Student & Amusement Park enthusiast; Jin ko bachane ke liye safar par nikalti hai.",
    "poking_buttons_ur": "Poking Buttons: df+1 (Turns her Backturned BT), d+3 (Fast low), b+2 (Into Rain Dance RDS), 1,d+2.",
    "pressure_moves_ur": "Pressure Moves: Art of Phoenix (AOP - d+1+2) – Yeh stance Xiaoyu ko itna neeche jhuka deti hai ke agle bande ke Mids bhi miss ho jate hain! f,f+3 into RDS.",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Hypnotist HYP & Backturned BT):\nLow: HYP 3 (Low sweep) ya BT d+3 / RDS d+3,4 (Low launcher).\nMid: HYP 2 (Mid launcher/Massive chip damage in Heat - +5 on block!).\nThrow: BT f,f+1+3 / 2+4 (Jumping crouch throw).",
    "trap_setup_ur": "Jaal (Trap Setup): Heat on karein aur b+3 ya f+2,1,2 se Hypnotist (HYP) stance mein jayein. Do कदम chalne ke baad HYP 2 (Mid) aur HYP 3 (Low) ka unreactable 50/50 chalayein!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) AOP aur Rain Dance (RDS) ke sideway evasion ko track karta hai. Range 2 par safe spacing rakhein.",
      "minus_punishable_moves_ur": "-10 to -14: df+1 (-12 on bad spacing), 3,4 (-13). -15+ Launch: AOP 4 sweep (-17 Launch), RDS 4 (-16 Launch), Cali Roll ws+2 (-15 Launch).",
      "bait_duck_interrupt_ur": "AOP (d+1+2) mein Xiaoyu ke niche Mids bhi nikal jate hain! AOP todne ke liye GROUND-HITTING MIDS (jaise d+2, db+2, ya low sweeps) marein.",
      "parry_vulnerabilities_ur": "Xiaoyu ke paas b+1 parry aur evasive stances hain. Us par high punches mat phenkein; Knees aur heavy mids use karein."
    }
  },
  {
    "id": 9,
    "slug": "hwoarang",
    "name": "Hwoarang",
    "title": "Blood Talon",
    "country": "South Korea",
    "country_flag": "🇰🇷",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Rival Wildcard",
    "season": "Base",
    "style": "Taekwondo",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/hwoarang.jpg",
    "height": "184 cm (6'0\")",
    "weight": "80 kg",
    "job_lore_ur": "Street Gang Leader & Taekwondo Fighter; South Korean military se chhup kar Jin se larne aata hai.",
    "poking_buttons_ur": "Poking Buttons: 1,2,3 (Into Left Flamingo LFS), 1,2,4 (Into Right Flamingo RFS), df+1,3 (Safe mid-high into LFS), d+3,4 (Low-high natural combo into +14 on hit!).",
    "pressure_moves_ur": "Pressure Moves: Right Kick (4 / RFF) aur Flamingo Stances (LFS / RFS). RFS f+4 (8-frame fast double kick jo block par +4 deti hai!), RFS df+4 (Safe mid CH launcher).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Aapka Poocha Gaya Endless Blender):\nStep 1: d+3,4 marein (Low-High). Ab aap Right Flamingo (RFS) mein hain.\nStep 2 (If they stand): RFS d+4,3 (Hellfire low-mid) ya दोबारा d+3,4 marein!\nStep 3 (If they duck d+3,4): RFS df+4 (Mid kick) ya RFS b+3 (Mid tornado launcher!) mar कर उड़ा दें!\nStep 4 (If they try to punch): RFS f+4,4 (8-frame fast high kicks) ya b+1 (Evasive step punch) marein.",
    "trap_setup_ur": "Jaal (Trap Setup): d+3,4 -> RFS 2 (+5 on block!) -> RFF df+4~f (+7 on hit) -> RFS d+4,3 ya RFS b+3. Agle bande ko pata hi nahi chalega kab High aa raha hai, kab Low, aur kab Mid!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Right Flamingo (RFS) aur Peacekeeper ko evade karta hai. Left Flamingo par sidestep na karein balke duck karein.",
      "minus_punishable_moves_ur": "-10 to -14: b+3 (-19 on whiff, -12 on block), f+1+2 (-13). -15+ Launch: d+4,4 (-15 Launch), RFS d+4,3 (-16 Launch), backlash 3~4 (-10 pushback).",
      "bait_duck_interrupt_ur": "d+3,4 ka pehla hit Low aur 2nd hit HIGH hai! Pehle hit ke baad foran DUCK karein aur ws+2 se launch kar dein! Flamingo loop mein DICKJAB (db+1) lagayein.",
      "parry_vulnerabilities_ur": "Hwoarang ke d+3,4 ke low ko df se LOW PARRY karein. Uske sab kicks standard sabaki aur parries se pakray ja sakte hain."
    }
  },
  {
    "id": 10,
    "slug": "claudio",
    "name": "Claudio Serafino",
    "title": "Sirius Marksman",
    "country": "Italy",
    "country_flag": "🇮🇹",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Archers of Sirius",
    "season": "Base",
    "style": "Sirius Exorcism Sorcery",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/claudio.jpg",
    "height": "182 cm (6'0\")",
    "weight": "77 kg",
    "job_lore_ur": "Leader of the Archers of Sirius (Vatican se jura khufiya Exorcist group jo shaitano ka shikar karta hai).",
    "poking_buttons_ur": "Poking Buttons: b+1 (Homing mid knockdown), df+3,2, ss+4 (Low poke: +6 on hit!), 1,2.",
    "pressure_moves_ur": "Pressure Moves: Superman Punch (f,f,f+2 - +6 on block aur Starburst deta hai!), b+3 (Fast safe knee), f+4 (Crouch-forcing mid: +4 on block).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (With Starburst STB):\nLow: STB d+2,2 (Natural combo low launcher!) ya ss+4.\nMid: STB db+1+2 (Mid जो गार्ड तोड़ देता है - Guard Break!), uf+4 (Best Hopkick in Tekken).",
    "trap_setup_ur": "Jaal (Trap Setup): Door se f,f,f+2 marein. Agar woh duck kare toh uf+4 (Hopkick) ya b+1 (Mid) marein. Starburst milte hi STB f+1+2,1+2 ya STB db+1+2 (Guard Break) se free wall splat lein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) wr+2 (Superman Punch) aur running kicks ko pura whiff karwa deta hai. SSR mat karein kyunki b+1 track karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: b+3 (-13), df+1,2 (-13), f+2,2 (-12). -15+ Launch: Hopkick uf+4 (-13 heavy pushback), STB d+2,2 (-15 Launch), STB f+1+2,1+2 (-15 Launch).",
      "bait_duck_interrupt_ur": "wr+2 agar door se aaye toh SSL kar ke piche se launcher marein. Starburst (STB) active ho toh db+1+2 guard break se bachne ke liye interrupt karein.",
      "parry_vulnerabilities_ur": "Claudio ke paas koi reversal nahi hai. Uske superman punch wr+2 ko high punch parry (Steve b+1+2, Bryan b+1+2) se pakra ja sakta hai."
    }
  },
  {
    "id": 11,
    "slug": "zafina",
    "name": "Zafina",
    "title": "Mystic Astrologer",
    "country": "Egypt",
    "country_flag": "🇪🇬",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Azazel Sealer",
    "season": "Base",
    "style": "Ancient Assassination Arts",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/zafina.jpg",
    "height": "170 cm (5'7\")",
    "weight": "53 kg",
    "job_lore_ur": "Astrologer (Najoomi) & Ancient Tomb Guardian; apne bazu mein Azazel ko qaid rakhti hai.",
    "poking_buttons_ur": "Poking Buttons: df+1,4 / df+1,2, 1,3 (Into Scarecrow SCR), 1,4 (Into Tarantula TRT), db+3 (Into Mantis MNT).",
    "pressure_moves_ur": "Pressure Moves: f,f+3 (Plus on block mid into SCR!), f,f,f+3 (Plus into MNT), b+1+2 (Azazel claw long-range low!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Scarecrow SCR & Mantis MNT):\nLow: SCR df+4 (Power low), MNT 3,1 (Low-mid CH launcher), TRT 3 (Crawling low).\nMid: SCR 2,1 (Azazel mid smash), SCR 1+2 (Mid launcher), MNT df+2 (Mid launcher).",
    "trap_setup_ur": "Jaal (Trap Setup): 1,3 ya d+3~d se Scarecrow ya Mantis mein jayein. SCR 4 (Armored mid launcher!) se button mashers ko saza dein aur SCR df+4 (Low) se blockers ko torein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Scarecrow (SCR) aur Tarantula (TRT) ke straight attacks ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,4 (-12), b+1 (-13). -15+ Launch: d+3 sweep (-17 Launch), TRT d+1+2 (-18 Launch), SCR 4 (-16 Launch).",
      "bait_duck_interrupt_ur": "TRT stance mein zameen par crawl karti hai. Aise mein High punches bilkul miss ho jayenge; d+4 low stomps ya ground-hitting mids use karein.",
      "parry_vulnerabilities_ur": "Azazel claw attacks unparryable hain! Normal claw punches parry nahi hotay is liye block kar ke punish karein."
    }
  },
  {
    "id": 12,
    "slug": "victor",
    "name": "Victor Chevalier",
    "title": "Refined Striker",
    "country": "France",
    "country_flag": "🇫🇷",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "UN Independent Forces",
    "season": "Base",
    "style": "Super Spy CQB • French Swordsmanship",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/victor.jpg",
    "height": "188 cm (6'2\")",
    "weight": "82 kg",
    "job_lore_ur": "United Nations Independent Forces ka Founder aur Legend Spy; pehle French Navy Commando tha.",
    "poking_buttons_ur": "Poking Buttons: 1,1,2 (10f punish into Perfumer PRF), df+1, d+2 (Sword mid poke: 0 on block!), db+4 (Long range sword low CH launcher!).",
    "pressure_moves_ur": "Pressure Moves: f,f,f+2 (Running sword slash: +5 on block aur CH launcher!), 2,2,2 (Pistol string into Iai Stance IAI).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Iai Sword Stance IAI - 3+4):\nLow: IAI d+2 (Heavy sword low jo +4 deta hai aur Heat mein knockdown karta hai!).\nMid: IAI 1,1 / IAI 1,2,2 (Safe mid series) ya IAI 2 (Safe homing mid sword slash).",
    "trap_setup_ur": "Jaal (Trap Setup): f,f,f+2 ya 1,2,1 (CH trap) chalayein. Jab opponent darr jaye, d+1+2 (Perfumer stance) -> PRF 2,2 se Iai Stance mein jaa kar IAI d+2 (Low) aur IAI 2 (Mid) ka mix-up lagayein.",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Victor ke pistol shots, Iai stance slashes aur wr+2 ko aasani se dodges karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,1 (-12), 2,2,2 (-13), 1+2 (-14). -15+ Launch: db+4 sword sweep (-18 Launch), IAI 4 (-16 Launch), teleport slash (-15 Launch).",
      "bait_duck_interrupt_ur": "Pistol shots (qcf+2 ya string pistol) HIGH hotay hain: DUCK kar ke ws+2 launch karein! wr+2 block karne ke baad fake pressure ko dickjab karein.",
      "parry_vulnerabilities_ur": "Victor ki TALWAAR (Sword) aur PISTOL normal parry aur low parry se deflect NAHI hotay! Unko sirf block kar ke punish karein."
    }
  },
  {
    "id": 13,
    "slug": "raven",
    "name": "Raven",
    "title": "Shadow Agent",
    "country": "Unknown",
    "country_flag": "🌐",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "UN Intelligence",
    "season": "Base",
    "style": "Ninjutsu",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/raven.jpg",
    "height": "186 cm (6'1\")",
    "weight": "86 kg",
    "job_lore_ur": "Master Ninja & UN Intelligence Agent; Victor ke neeche kaam karta hai.",
    "poking_buttons_ur": "Poking Buttons: df+1 (-1 on block!), b+1 (Plus on block high into Backturned BT), db+2 (Mid check into BT), d+3 (Fast low).",
    "pressure_moves_ur": "Pressure Moves: Soul Zone (SZ - d+1+2 ya attacks ke baad ~f), f,f,f+3 (Plus on block knee).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Backturned BT & Crouch):\nLow: BT d+3 (Fast sweep), fc df+3+4 (Hellfire low sweep into clone follow-up!).\nMid: BT 3+4 (Safe mid launcher), ws+1 (Mid launcher), SZ 2 (Mid clone punch).",
    "trap_setup_ur": "Jaal (Trap Setup): db+2 ya b+1 mar kar peeth ghumayein (BT). Agar agla banda attack kare toh BT b+1+3 (Teleport Parry) ya BT 1+2 (Power Crush) marein; agar block kare toh BT d+3 (Low) aur BT 3+4 (Mid) se torein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) shadow clone gap-closers aur b+2 pokes ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), 4,1 (-13). -15+ Launch: db+4 sweep (-17 Launch), Hazan ws+1 (-15 Launch), teleport dive (-16 Launch).",
      "bait_duck_interrupt_ur": "Clone attacks par ghabrayein mat; clones high hit hotay hain jinko duck kiya ja sakta hai. Teleport dekh kar 1 jab se float combo lein.",
      "parry_vulnerabilities_ur": "Raven ke paas b+1+2 shadow clone substitution parry hai. Multi-hit strings na lagayein, single heavy moves lagayein."
    }
  },
  {
    "id": 14,
    "slug": "alisa",
    "name": "Alisa Bosconovitch",
    "title": "Destroying Angel",
    "country": "Russia",
    "country_flag": "🇷🇺",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Violet Systems",
    "season": "Base",
    "style": "High-Mobility Thruster Combat",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/alisa.jpg",
    "height": "165 cm (5'5\")",
    "weight": "~63 kg",
    "job_lore_ur": "Dr. Bosconovitch ki banayi hui Military Android; Jin ko protect karne ke liye banayi gayi thi magar ab Lars ke sath hai.",
    "poking_buttons_ur": "Poking Buttons: df+1 (With extensions df+1,1,2 aur df+1,4), db+3 (Long range low poke), b+1 (Crouch-inducing mid), f+2 (into Chainsaws!).",
    "pressure_moves_ur": "Pressure Moves: Destructive Form (DES - Chainsaws - d+1+2). f,f,f+2 (+6 on block into f+1+2 guaranteed!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Chainsaw Stance DES):\nHigh/Plus: DES f+1 (Fast chainsaw jab jo +3 on block hai aur chip damage deta hai!).\nLow: DES d+1 (Multi-hit chainsaw low!).\nMid: DES f+1+2 (Homing mid जो ब्लॉक पर भी प्लस है!) ya DES 1 (Mid).",
    "trap_setup_ur": "Jaal (Trap Setup): Heat on karein aur f+2,1+2 ya 1,1 ke baad Chainsaws (DES) nikal lein. Ab DES f+1 (High +3), DES d+1 (Low), aur DES f+1+2 (Mid) baar-baar marein—block karte-karte hi agle ki life khatam ho jayegi!\nC. G Corporation & Rivals",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) rocket punches, b+1, aur wr+2 ko evade karta hai. SSR par DES chainsaw clip karti hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,1 (-12), b+4,4 (-13). -15+ Launch: db+3 sweep (-17 Launch), fly 3+4 dive (-18 Launch), DES d+1 (-16 Launch).",
      "bait_duck_interrupt_ur": "Rocket punch 1+2 high hai: duck kar ke ws launch marein! Chainsaw (DES) mein f+1 block kar ke dickjab (db+1) se chainsaw band karwayein.",
      "parry_vulnerabilities_ur": "Alisa ki CHAINSAWS (DES) normal parry se deflect nahi hotin! Unko parry karne ki koshish mat karein, armor move ya power crush se torein."
    }
  },
  {
    "id": 15,
    "slug": "nina",
    "name": "Nina Williams",
    "title": "Silent Assassin",
    "country": "Ireland",
    "country_flag": "🇮🇪",
    "faction": "G-Corporation & Kazuya's Allies",
    "faction_badge": "G-Corp Commander",
    "season": "Base",
    "style": "Assassination Martial Arts",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/nina.jpg",
    "height": "174 cm (5'8.5\")",
    "weight": "57 kg",
    "job_lore_ur": "World-Class Assassin & G Corporation Commander; Anna Williams ki bari behen aur Steve Fox ki biological maa.",
    "poking_buttons_ur": "Poking Buttons: 1,2 (1,2,1,2 string), df+1,2 (Jab cancelable into sidestep df+1,2~u/d), d+3,4,3 (Low-high-mid string: +3 on block!).",
    "pressure_moves_ur": "Pressure Moves: Sidestep 1 Cancel (ss+1~b~u/d) – Yeh block par +10 tak advantage deta hai! f,f,f+1+2 (+4 on block).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up:\nLow: db+3 (Plus on hit low: +4), fc df+4 (Wipe the floor sweep).\nMid: df+3,2 / df+1,2, b+1+4 (Double knee launcher).\nThrows: Multi-chain grabs (qcf+1+2 یا df+1,2~f+1+2).",
    "trap_setup_ur": "Jaal (Trap Setup): Bilkul qareeb chipak kar df+1,2 aur d+4,1 (Low-high) spam karein. Jab woh high duck karne ki koshish kare, df+2 (Mid launcher) ya f+1+2 (Armor) mar dein.",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Hayashida step aur df+1,2 ko evade karta hai. Duck d+4,1 high string.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), f+1+2 (-13). -15+ Launch: d+3,2 (-15 Launch), wipeout db+3 (-17 Launch), Geisha roll sweep (-18 Launch).",
      "bait_duck_interrupt_ur": "d+4,1 string ka doosra hit High hai: duck kar ke ws+2 launcher marein! Hayashida cancel pressure ko dickjab (db+1) se interrupt karein.",
      "parry_vulnerabilities_ur": "Nina ke paas b+1+3 / b+2+4 reversal hai. Usay todne ke liye Paul df+1 elbow, Bryan f+3 knee, ya Feng b+1+2 headbutt marein."
    }
  },
  {
    "id": 16,
    "slug": "jack-8",
    "name": "Jack-8",
    "title": "Heavy Combat Automaton",
    "country": "G-Corp",
    "country_flag": "🤖",
    "faction": "G-Corporation & Kazuya's Allies",
    "faction_badge": "G-Corp Weapon",
    "season": "Base",
    "style": "Brute Force Power Combat",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/jack-8.jpg",
    "height": "240 cm (7'10\")",
    "weight": "222 kg",
    "job_lore_ur": "Heavy Super-Killing Robot; Jane ki hifazat aur G-Corp ki front-line tabahi ke liye banaya gaya.",
    "poking_buttons_ur": "Poking Buttons: 2 (11f long-range jab!), df+1 (Mid), db+1 (12-frame machine-gun low poke: +2 on hit!), fc db+1 (Crouching low: +6 on hit!).",
    "pressure_moves_ur": "Pressure Moves: Gamma Howl Stance (GMH - 3+4). b+1,2~d या f+3~d se GMH mein jayein.",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Gamma Howl & Crouch):\nGuard Break High: GMH 4 (Block par +11 deta hai -> free GMH 2 या 1,1!).\nMid: GMH 1 (Safe Homing Mid) ya GMH 2 (Power mid).\nLow: db+1,1 into fc db+1 (Low pressure) aur df+2+4 (Crouch throw!).",
    "trap_setup_ur": "Jaal (Trap Setup): db+1 -> fc db+1 (+6 on hit) -> ws+4 ya fc df+2,d,f+1 chalayein. Deewar ke paas f+3~d into GMH 4 (Guard Break) aur GMH 1 (Mid) ka un-escapable loop lagayein!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Gamma Howl (GMH) lunges, db+1, aur ff+1 ko evade karta hai. Jack ka hit-box bara hai is liye wide combos lagte hain.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), b+1,2 (-13), f+1+2 (-14). -15+ Launch: db+2 machine gun sweep (-18 Launch), GMH 2 (-16 Launch), Megaton punch (-17 Launch).",
      "bait_duck_interrupt_ur": "GMH 4 guard break (+11) se bachne ke liye duck karein aur ws launcher marein! db+1 fast low punch ko df se Low Parry karein.",
      "parry_vulnerabilities_ur": "Jack-8 ke heavy punches normal parries se deflect ho sakte hain, lekin uske rocket arm moves parry nahi hotay."
    }
  },
  {
    "id": 17,
    "slug": "feng",
    "name": "Feng Wei",
    "title": "God Fist",
    "country": "China",
    "country_flag": "🇨🇳",
    "faction": "Tekken Monks & Traditional Purifiers",
    "faction_badge": "Dragon Fist",
    "season": "Base",
    "style": "Chinese Kempo • God Fist Style",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/feng.jpg",
    "height": "187 cm (6'1.5\")",
    "weight": "88 kg",
    "job_lore_ur": "God Fist Kenpo Master; apne hi ustad ko qatal kar ke duniya ke har martial artist ko harane nikla hai.",
    "poking_buttons_ur": "Poking Buttons: df+1 (0 on block! Agla banda jab kare toh b+1 CH lagta hai!), b+4 (12f tracking mid!), d+2 (Fast low), db+3 (16f long-range high-crushing low!).",
    "pressure_moves_ur": "Pressure Moves: Shifting Clouds (STC - f+3+4), Kenpo Step (KNP - b+3+4), uf+2 (Evasive side-step punch).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Crouch & Backturned BT):\nLow: ss+4 (Clean-hit low sweep launcher!), BT d+3 (Clean-hit low launcher!), fc df+4,1 (Low-mid).\nMid: ws+1,2 (Mid string), b+1+2 (13f Shoulder ram!), df+3 (Safe mid tornado launcher!).",
    "trap_setup_ur": "Jaal (Trap Setup): df+1 marein (0 on block) aur foran b+1 (10f CH palm) daba dein—agar agle ne button chhua bhi toh zameen par girega aur b+1+2 (Shoulder) free milega! Phir db+3 (Low) aur df+3 (Mid launcher) se mix karein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Kenpo step pokes, b+1, aur STC mix-up ko evade karta hai. Lekin Feng ka df+1 right track karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: b+1 (-12 punish), df+2,2 (-13), 1+2 (-14). -15+ Launch: db+4 sweep (-17 Launch), STC 4 sweep (-18 Launch), uf+4 hopkick (-13).",
      "bait_duck_interrupt_ur": "Feng ke b+1 fast elbow ko block kar ke 12f punish dein. db+4 sweep ko db block kar ke 80+ damage ka launch karein. d+2 low poke ko df se Low Parry karein.",
      "parry_vulnerabilities_ur": "Feng ke paas 1+2 Sabaki parry aur b+1+2 parry hai. Feng ki parry todne ke liye Knees (Bryan f+3, Lars b+4) ya Weapons use karein."
    }
  },
  {
    "id": 18,
    "slug": "dragunov",
    "name": "Sergei Dragunov",
    "title": "White Angel of Death",
    "country": "Russia",
    "country_flag": "🇷🇺",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Red Army Spetsnaz",
    "season": "Base",
    "style": "Combat Sambo",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/dragunov.jpg",
    "height": "188 cm (6'2\")",
    "weight": "86 kg",
    "job_lore_ur": "Russian Spetsnaz Officer (\"The White Angel of Death\"); war-zone se chhutti le kar apne shauq poore kar raha hai.",
    "poking_buttons_ur": "Poking Buttons: 1,2,1 (CH launcher), df+1 (With df+1,4 extension), d+2 (Hatchet Low: -1 on hit magar dono crouch mein jate hain!), db+3+4 (Heavy low: +7 on hit!).",
    "pressure_moves_ur": "Pressure Moves: Running 2 (f,f,f+2 - +4 on block aur CH launcher!), b+1+2 (+6 on block axe handle!), Sneak Stance (SNK - qcf).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Sneak Stance SNK & Tackles):\nLow: db+3+4 या SNK 3 (Slide low grab).\nMid: SNK 4 (+7 on block axe kick into crouch!) ya SNK 2 (Mid launcher).\nThrow: SNK 1+2 (Unbreakable Tackle!), f+1+4 / f+2+3 (Command throws).",
    "trap_setup_ur": "Jaal (Trap Setup): f,f,f+2 ya df+3+4~df se Sneak (SNK) mein jayein -> SNK 4 marein (+7 on block!). Ab fc df+1,4 (Low-Mid into SNK) ya ws+1+2 (Mid wall-splat) marein!",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Dragunov ke khilaf zaroori hai! wr+2 (Russian Assault), sneak cancels, aur qcf+4 SSR par whiff ho jate hain. SSL par clip ho jayenge.",
      "minus_punishable_moves_ur": "-10 to -14: 4,1 (-12), df+1,4 (-13), b+4,3 (-14). -15+ Launch: d+2 low poke (-14 crouching punish), qcf+2 (-15 Launch), snake edge db+3 (-26 Launch).",
      "bait_duck_interrupt_ur": "wr+2 block hone ke baad +6 hota hai: ghalti se bhi button mat dabayein! Neutral block rakhein ya dickjab se sneak cancel torein.",
      "parry_vulnerabilities_ur": "Dragunov ke paas b+1+3 / b+2+4 reversal hai. Usay todne ke liye Elbows (Paul df+1) ya Knees marein. Dragunov ke wr+2 ko high punch parry kiya ja sakta hai."
    }
  },
  {
    "id": 19,
    "slug": "bryan",
    "name": "Bryan Fury",
    "title": "Harbinger of Chaos",
    "country": "USA",
    "country_flag": "🇺🇸",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Cybernetic Anarchist",
    "season": "Base",
    "style": "Kickboxing",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/bryan.jpg",
    "height": "186 cm (6'1\")",
    "weight": "90 kg",
    "job_lore_ur": "Former Interpol Officer turned Zombie Cyborg (Dr. Abel & Bosconovitch ne banaya); sirf tabahi aur khoon-kharaba chahta hai.",
    "poking_buttons_ur": "Poking Buttons: df+2,1 (Mid-high), df+1,1,1,1,2 (Machine gun mid checks), d+4 (Long range low), db+3 (High-crushing low).",
    "pressure_moves_ur": "Pressure Moves: b+1 (Chop mid: +4 on block aur CH launcher!), qcb+1 (Sway high: +5 on block aur CH launcher!), Hatchet Kick (qcb+3 - +5 on hit low!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up:\nLow: qcb+3 (Hatchet kick - bar-bar marne se 25+ damage deta hai!).\nMid: 3+4 (Keep-out CH launcher), qcb+2,4 (Mid-high), f+3 (16f knee CH launcher: 0 on block!).\nUnblockable: Taunt (1+3+4) – Deewar par block nahi hota aur b+4 ya f+2,1,4 guaranteed deta hai!",
    "trap_setup_ur": "Jaal (Trap Setup): qcb+3 (Low) ya b+1 (Block par +4) marein, aur foran f+3 (Knee) daba dein. Agar agla banda hila, toh f+3 CH launch karega aur deewar par Taunt (1+3+4) se khel khatam!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Bryan ke Mach Punch (ff+2), 3+4 keepout, aur b+1 ko evade karta hai. SSR par Hatchet kick qcb+3 clip karti hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,1,1,1 (-13), f+4,1 (-13), 1+2 (-14). -15+ Launch: Snake Edge df+3 (-26 Massive Launch!), qcb+4 (-15 Launch), Jet Upper fb+2 (-14 on block).",
      "bait_duck_interrupt_ur": "Snake Edge (df+3) dekhte hi db se BLOCK karein aur 90 damage ka full combo launch karein! Taunt (1+3+4) dekh kar delay wake-up karein ya jab se interrupt karein.",
      "parry_vulnerabilities_ur": "Bryan ke paas b+1+2 punch parry hai jo mach punch counter deti hai. Us par punches mat marein, Knees (f+3) aur Kicks use karein."
    }
  },
  {
    "id": 20,
    "slug": "azucena",
    "name": "Azucena Ortiz",
    "title": "Coffee Queen",
    "country": "Peru",
    "country_flag": "🇵🇪",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Ortiz Farm",
    "season": "Base",
    "style": "Rumi Maki • Mixed Martial Arts",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/azucena.jpg",
    "height": "170 cm (5'7\")",
    "weight": "57 kg",
    "job_lore_ur": "MMA Champion, Model & Coffee Farm Owner (Ortiz Farm); apni coffee duniya bhar mein bechne ke liye larti hai.",
    "poking_buttons_ur": "Poking Buttons: df+1,4 (Mid-high with dangerous df+1,4,1 CH extension!), 1,1 (Hit-confirmable into Libertador LIB), db+4 (Low), db+3 (Plus low into Backturned BT).",
    "pressure_moves_ur": "Pressure Moves: Libertador Stance (LIB - f+3+4) – Is stance mein Highs aur Lows khud-ba-khud miss ho jate hain! f,f,f+3,2 (+2 on block).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (LIB & BT Stance):\nLow: LIB d+4,4 (Hellsweep-type spinning low) ya BT d+3 (Low kick).\nMid: LIB 2 (Safe mid), LIB 1+2 (Mid launcher), BT 1+2 (Safe mid).\nHigh/Throw: LIB 3+4 (Power crush), BT 1+3 (Throw).",
    "trap_setup_ur": "Jaal (Trap Setup): db+3 (Low hit -> BT) -> BT 3 (Low) ya BT 1,2 (LIB stance). Jab aap LIB mein hon aur agla banda jab ya low mare, Azucena hans kar dodge karegi aur aapko free counter launch milega!\nD. The Classic Tournament Veterans",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) wr+3,2 running mix-up aur Libertador pokes ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,4 (-12), 1,2,4 (-13). -15+ Launch: db+3 sweep (-17 Launch), LIB 4 low sweep (-16 Launch), hopkick uf+4 (-13).",
      "bait_duck_interrupt_ur": "wr+3,2 ka dusra hit high hai: DUCK kar ke ws+2 launcher marein! Libertador (LIB) stance mein auto-dodge hota hai: aise mein MIDS ya ELBOWS marein.",
      "parry_vulnerabilities_ur": "Azucena Libertador stance mein khari ho kar Highs aur Lows auto-parry karti hai! Stance todne ke liye sirf MID BUTTONS (df+1, df+2) marein."
    }
  },
  {
    "id": 21,
    "slug": "king",
    "name": "King II",
    "title": "Anger of the Beast",
    "country": "Mexico",
    "country_flag": "🇲🇽",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Lucha Libre",
    "season": "Base",
    "style": "Pro-Wrestling • Lucha Libre",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/king.jpg",
    "height": "200 cm (6'7\")",
    "weight": "147 kg",
    "job_lore_ur": "Pro Wrestler & Orphanage Owner (King I ki maut ke baad uska mask pehen kar yateem bachon ki parwarish karta hai).",
    "poking_buttons_ur": "Poking Buttons: 2,1 (10f mid-high), df+1,2 (Delayable mid-mid), df+2,1 (13-frame CH confirmable launcher!), d+3 (+1 on hit low), f,f,n,2 (Low smash: +7 on hit aur CH par animation throw!).",
    "pressure_moves_ur": "Pressure Moves: Jaguar Sprint (JGS - f+3+4), Muscle Armor (db+1+2 - Damage absorb kar ke + rehta hai!).\nUpper/Mid/Low & Throw Mix-up (The Grappler's Nightmare):\n1-Break Throw: Giant Swing (f,hcf+1) – 10-frame startup! Dekhne mein 1+2 break lagta hai magar 1 se tootta hai!\n1+2-Break Throw: Shining Wizard (f,f,f+2+4) ya Tijuana Twister (f,hcf+2 - 2 break).\nMid (If they duck the throws!): uf+4 (Hopkick launcher), f,f+1 (Homing mid), df+2,1.",
    "mixup_blender_ur": "",
    "trap_setup_ur": "Jaal (Trap Setup): f,f,n,2 (Low) ya 1,2 marein. Jab woh khara ho kar block kare, Giant Swing (f,hcf+1) ya Shining Wizard lagayein. Jaise hi woh throw se bachne ke liye neeche bethe, uf+4 (Hopkick) ya Crouch Throw (d+1+3) mar dein!",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) King ke df+1, f,f+1, aur Giant Swing approach ko evade karta hai. Throws se bachne ke liye duck karein.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), b+1,2 (-13), 1+2 (-14). -15+ Launch: Ali kicks d+3+4 (-18 to -26 Stagger Launch!), hopkick uf+4 (-13), db+3 (-16 Launch).",
      "bait_duck_interrupt_ur": "Ali kicks (d+3+4,4...) ko doosre hit par df se LOW PARRY karein! Giant Swing par 1 daba kar throw break karein, Shining Wizard par 1+2 break karein.",
      "parry_vulnerabilities_ur": "King ke paas b+1+3 (Kick parry) aur b+2+4 (Punch parry) alag hain! Kick parry se bachne ke liye Punches marein, aur Punch parry se bachne ke liye Elbows/Knees marein."
    }
  },
  {
    "id": 22,
    "slug": "paul",
    "name": "Paul Phoenix",
    "title": "Hot-Blooded Destroyer",
    "country": "USA",
    "country_flag": "🇺🇸",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Indomitable Brawler",
    "season": "Base",
    "style": "Judobased Mixed Martial Arts",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/paul.jpg",
    "height": "187 cm (6'1.5\")",
    "weight": "98 kg",
    "job_lore_ur": "Martial Artist, Bouncer & Former Biker; \"Toughest in the Universe\" banne ka khwab rakhta hai (hamesha garib rehta hai).",
    "poking_buttons_ur": "Poking Buttons: df+1 (df+1~b into Sway!), d+1 (Mid hammer), ss+3 (Low ankle kick: +4 on hit aur CH par b+1,2 free!), qcb+3 (Sway low).",
    "pressure_moves_ur": "Pressure Moves: f+1+2 (+3 on block overhead smash!), qcb+1 (0 on block mid!), df+1~b into Sway options.",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Deewar Ke Paas 2-Hit Death):\nLow: Demoman (d+4,2:1+2) – Bilkul paas (Clean Hit) se neeche gira kar deewar par marta hai!\nMid: Deathfist (qcf+2) – Agar agle bande ne Demoman ke darr se duck kiya, toh Deathfist uski 35-40% health ek mukke mein ura dega!",
    "trap_setup_ur": "Jaal (Trap Setup): df+1~b (Back-sway) -> qcb+4 (Homing high CH launcher: +1 on block) ya qcb+3,2 (Low-mid). Deewar ke paas Demoman aur Deathfist/Safe Mid (qcf+1+2 या d+1,2 in Heat Guard Break!) chalayein.",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Deathfist (qcf+2) aur df+1 ko evade karta hai. Lekin b+1 homing se bach kar neutral block rakhein.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,1 (-12), b+1,2 (-13). -15+ Launch: Demoman d+4,2:1+2 (-17 Stagger Launch on block!), Deathfist qcf+2 (-17 Launch on block without pushback), uf+4 hopkick (-13).",
      "bait_duck_interrupt_ur": "Demoman (d+4) ko db se block kar ke ws+2 launcher marein! 3,2 high extension ko duck kar ke launch karein. Deathfist block ho toh long range launcher (f,f+2) marein.",
      "parry_vulnerabilities_ur": "Paul ke paas b+1+3 reversal hai. Reversal todne ke liye Paul ke apne jaise Elbows (df+1) aur Knees chalayein."
    }
  },
  {
    "id": 23,
    "slug": "law",
    "name": "Marshall Law",
    "title": "The Dragon",
    "country": "USA",
    "country_flag": "🇺🇸",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Martial Arts Chef",
    "season": "Base",
    "style": "Martial Arts (Jeet Kune Do)",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/law.jpg",
    "height": "179 cm (5'10.5\")",
    "weight": "77 kg",
    "job_lore_ur": "Martial Arts Dojo Owner & Chinese Restaurant Chef; apne bete Forest ke bike accident ka qarza chuka raha hai.",
    "poking_buttons_ur": "Poking Buttons: 1,2 (1,2,3), df+1, d+1,3 (Low-high), db+3 (Fast low: +3 on hit), 4,3~f (into Dragon Sign Stance DSS).",
    "pressure_moves_ur": "Pressure Moves: f+1+2 (Dragon Hammer: +3 on block aur crouch force karta hai!), Nunchucks (1+2 in Heat - Safe Mid Launcher!), ws+4~f (+5 on block in DSS!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Crouch / DSS Mix-up):\nLow: Slide (fc df,d,df+3) – Zameen par gira kar guaranteed 1+2 Nunchuck deta hai!\nMid: uf+3 (Armored mid flying kick / Heat Engager!) ya ws+2 (Mid launcher).",
    "trap_setup_ur": "Jaal (Trap Setup): db+3 ya f+1+2 marein -> ws+4~f (DSS mein +5 on block!). Agar opponent button dabaye toh DSS f+1 ya DSS 3 usay CH karega; agar chup rahe toh crouch mein jaa kar Slide mar dein!",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Dragon Sign pokes, 3+4, aur DSS rushes ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), b+1,2 (-13). -15+ Launch: Junkyard b+2,3,4 (2nd hit low: Low Parry karein!), Dragon Tail db+4 (-26 Stagger Launch!), flip kick uf+3,4 (-15 Launch).",
      "bait_duck_interrupt_ur": "Junkyard Dog (b+2,3,4) ka doosra hit Low hai: foran df dba kar LOW PARRY karein! Dragon Tail ko db se block kar ke full launch combo marein.",
      "parry_vulnerabilities_ur": "Law ke Nunchucks aur DSS weapon moves parry nahi hotay! Normal kicks aur punches parry ho sakte hain."
    }
  },
  {
    "id": 24,
    "slug": "steve",
    "name": "Steve Fox",
    "title": "Counter-Punching Ace",
    "country": "United Kingdom",
    "country_flag": "🇬🇧",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "World Middleweight Champion",
    "season": "Base",
    "style": "Boxing",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/steve.jpg",
    "height": "182 cm (6'0\")",
    "weight": "79 kg",
    "job_lore_ur": "World Middleweight Boxing Champion; G-Corp ke laboratory experiment se Nina ke eggs se paida hua tha.",
    "poking_buttons_ur": "Poking Buttons: 1,2,1 (~f into Peekaboo PKB ya ~b into Flicker FLK), df+1, d+2,1~b (Low-mid cancel into FLK - Completely Safe!), d+1 (Low poke).",
    "pressure_moves_ur": "Pressure Moves: b+1 (13f Counter-Hit King! ~b daba kar Flicker mein safe rehta hai), Lionheart Stance (LH - db+3+4), Peekaboo (PKB - f+3+4).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Peekaboo PKB & Lionheart LH):\nGuard Break High: LH 1+2 (Unblockable guard-break -> free 1,1,2 ya Heat Smash!).\nMid: LH 1 (Mid) / LH 2 (Mid launcher) / PKB df+1,2.\nLow: PKB d+1 (Fast low punch: +2 on hit!) aur PKB d+2 (Sweeping low).",
    "trap_setup_ur": "Jaal (Trap Setup): 1,2,1~b ya b+1~b mar kar Flicker mein jayein, aur jaise hi agla banda punch mare, 3 ya 4 daba kar Weave (Side Dodge) karein aur 1,2 se uske munh par counter punch marein!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Steve ke Peekaboo (PKB) jabs aur Sonic Fang (df+1+2) ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: Sonic Fang df+1+2 (-12 punish), b+1,2 (-13). -15+ Launch: d+2,1 (-15 Launch), PKB d+1 (-13), duck in 2 (-14).",
      "bait_duck_interrupt_ur": "Steve ke zyadatar attacks High hotay hain! High hooks ko DUCK kar ke While Standing ws+2 launcher marein. b+1 CH fish karne par forward moves mat dabayein.",
      "parry_vulnerabilities_ur": "Steve ke paas b+1+2 punch parry hai. Steve par punches ke bajaye Kicks, Knees, aur Lows use karein."
    }
  },
  {
    "id": 25,
    "slug": "asuka",
    "name": "Asuka Kazama",
    "title": "Spirited Peacemaker",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Kazama Dojo",
    "season": "Base",
    "style": "Kazama Style Traditional Martial Arts",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/asuka.jpg",
    "height": "167 cm (5'5.5\")",
    "weight": "56 kg",
    "job_lore_ur": "High School Student & Street Peacemaker; Jin ki cousin aur Kazama dojo ki waris.",
    "poking_buttons_ur": "Poking Buttons: 1,1 / 1,3, df+1,2, d+1+2 (Low knock-down sweep!), db+3 (Long range low), b+4 (Knee CH).",
    "pressure_moves_ur": "Pressure Moves: Naniwa Gusto (NW power-up), f,f,f+1+2 (+4 on block aur NW deta hai!), NW ff+1+2 (+9 on block!), 1+2 (16-frame SAFE mid launcher!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up:\nLow: d+1+2 (Point-blank knockdown low -> free f+2 या 1+2 follow-up!).\nMid: 1+2 (Safe double-palm mid launcher!) ya f+2 (Long range launcher).",
    "trap_setup_ur": "Jaal (Trap Setup): Pokes mar kar thora peeche hatein (b+3 Backflip ya b+2+4 Parry/Sabaki). Jaise hi agla banda josh mein aage attack kare, b+3 ya df+2 se launch kar dein!",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Asuka ke f+2 launcher, b+3, aur Leg Cutter db+4 ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), 2,3 (-13), f+1+2 (-13). -15+ Launch: Leg cutter db+4,4 (-18 Stagger Launch!), f+2 launcher (-18 on block!), can-can kicks d+3+4 (-15 Launch).",
      "bait_duck_interrupt_ur": "Leg Cutter (db+4,4) ko block kar ke ws launcher marein! 1,2,4 string ka 3rd hit high hai: duck kar ke launch karein.",
      "parry_vulnerabilities_ur": "Asuka ki b+1+3 parry bohot lambi hold hoti hai! Is par punches/kicks mat marein; ELBOWS (Paul df+1, Bryan b+1), KNEES, ya WEAPONS marein jo parry tod dete hain."
    }
  },
  {
    "id": 26,
    "slug": "lili",
    "name": "Lili Rochefort",
    "title": "Fighting Heiress",
    "country": "Monaco",
    "country_flag": "🇲🇨",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Rochefort Enterprises",
    "season": "Base",
    "style": "Self-Taught Gymnastic Street Fighting",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/lili.jpg",
    "height": "180 cm (5'11\")",
    "weight": "60 kg",
    "job_lore_ur": "Billionaire Oil Magnate ki इकलौती Beti; apne walid se chhup kar street fighting ka shauq poora karti hai.",
    "poking_buttons_ur": "Poking Buttons: 1,1 (Turns Backturned BT), df+1, d+3 (Long range low), ff+4 (Root of Evil: Heavy low stomp jo +4 deta hai aur BT mein jata hai!).",
    "pressure_moves_ur": "Pressure Moves: Feisty Rabbit (FR - b+3 ya b+4), df+3 (+3 on block axe kick!), f,f,f+3 (Plus on block diving kick).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Backturned BT Stance - b+3+4 या ff+4 ke baad):\nLow: BT d+2 (Fast low: +5 on hit in crouch!) ya BT d+3+4 (Snake-edge style low launcher!).\nMid: BT 1+2 (13-frame fast mid launcher!), BT 3,4 (Safe mid kicks).\nThrow: BT 1+3 / 2+4 (50/50 throw).",
    "trap_setup_ur": "Jaal (Trap Setup): df+1 ya 1,2 mar kar Sidestep (u ya d) karein (Lili ka sidestep sabse bara hai!). Agle ka attack miss hote hi df+2 ya 3,1 marein, ya ff+4 (Low) se BT mix-up mein daal dein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Feisty Rabbit, Matterhorn (d+3+4), aur qcf+3 ko evade karta hai. Lili ka apna sidestep bohot bara hai is liye homing moves use karein.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), f+2,3 (-13). -15+ Launch: Matterhorn d+3+4 (-24 Massive Launch!), Backturned BT d+3+4 sweep (-23 Stagger Launch!), Edelweiss db+4 (-26 Launch).",
      "bait_duck_interrupt_ur": "Matterhorn aur Edelweiss slow sweeps hain: db se BLOCK karein aur 90 damage ka full combo launch karein! BT stance mein dickjab se interrupt karein.",
      "parry_vulnerabilities_ur": "Lili ke jumpy acrobatic attacks standard punch/kick parry se pakray ja sakte hain."
    }
  },
  {
    "id": 27,
    "slug": "leo",
    "name": "Leo Kliesen",
    "title": "Spelunker of Truth",
    "country": "Germany",
    "country_flag": "🇩🇪",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Baji Explorer",
    "season": "Base",
    "style": "Bajiquan",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/leo.jpg",
    "height": "176 cm (5'9\")",
    "weight": "63 kg",
    "job_lore_ur": "Spelunker (Cave Explorer) & Archeologist's Apprentice; apni maa Emma Kliesen (G-Corp scientist) ke qatil Kazuya ki talash mein hai.",
    "poking_buttons_ur": "Poking Buttons: df+1, d+4 (Fast low), db+4,1 (High-crushing low sweep!), b+1,4 (Knee string into Jin Ji Du Li KNK stance!).",
    "pressure_moves_ur": "Pressure Moves: b+1,4 (Knee into KNK), f+4 (Direct KNK entry: + on block!), Bokuden Stance (BOK - d+1+2 - Highs ke neeche se nikal jata hai!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (KNK One-Leg Stance):\nLow: KNK 4 (Low stomp jo +3 deta hai!) ya KNK df crouch dash into ws+3.\nMid: KNK 2 (High/CH launcher), KNK 3,4 (Mid-mid launcher!), KNK 1+2 (Safe power mid).",
    "trap_setup_ur": "Jaal (Trap Setup): Deewar ke paas b+1,4 -> KNK 3+4 या KNK 4 (Low) chalayein. Agar agla banda jab se rokne ki koshish kare, d+1+2 (BOK stance) daba kar uske punch ke neeche se nikal jayein aur BOK 2 se aasman mein ura dein!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) BOK stance lunges, df+1, aur ff+2 ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), b+1,4 (-13). -15+ Launch: db+4 sweep (-17 Launch), BOK 2 sweep (-18 Launch), hopkick uf+4 (-13).",
      "bait_duck_interrupt_ur": "b+1,4 ka doosra hit high hai: duck kar ke ws+2 launcher marein! BOK stance mein aate hi dickjab (db+1) se attack interrupt karein.",
      "parry_vulnerabilities_ur": "Leo ke paas b+1+3 / b+2+4 punch sabakis hain. Bajiquan elbows parry nahi hotin, is liye Leo ke khilaf elbows use karein."
    }
  },
  {
    "id": 28,
    "slug": "shaheen",
    "name": "Shaheen",
    "title": "Desert Falcon",
    "country": "Saudi Arabia",
    "country_flag": "🇸🇦",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "G-Corp Resistance",
    "season": "Base",
    "style": "Military Self-Defense (CQC)",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/shaheen.jpg",
    "height": "185 cm (6'1\")",
    "weight": "83 kg",
    "job_lore_ur": "Private Military Bodyguard Specialist; apne dost Salim (oil industry head) ke qatal ka badla Kazuya se lene aata hai.",
    "poking_buttons_ur": "Poking Buttons: 1,2,2 (CH string), df+1 (3-frame sidestep friendly mid), d+3 (Low into Stealth Step SNK!), d+4 (Low).",
    "pressure_moves_ur": "Pressure Moves: f,f,f+2 (+5 on block!), uf+1 (Jumping mid punch cancelable into SNK: +3 on block!), Guard Break (SNK 1+2 in Heat - +12 on block!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (Crouch / Stealth Step):\nLow: Slide (fc df,d,df+3) – Knockdown aur SNK 2 follow-up!\nMid: ws+2 (16-frame Mid Launcher!) ya uf+4 (Hopkick).",
    "trap_setup_ur": "Jaal (Trap Setup): d+3~df (Low into crouch) ya df+4,1~df se crouch mein jayein. Ab agle ko Slide (Low) aur ws+2 (Mid Launcher) ke 50/50 mein daal dein. Heat mein SNK 1+2 (Guard Break) se free launcher lein!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Stealth Dash, 4,1, aur df+1 ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1 (-12 on spacing), 4,1 (-13), fb+2 (-14). -15+ Launch: Slide fc df,d,df+3 (-23 Stagger Launch!), hopkick uf+4 (-13), db+4 (-16 Launch).",
      "bait_duck_interrupt_ur": "Slide ko db se block kar ke hopkick launch marein! 4,1 string ka 2nd hit high hai: duck kar ke ws launcher marein.",
      "parry_vulnerabilities_ur": "Shaheen ke paas koi special reversal nahi hai. Uske kicks aur pokes standard parry se pakray ja sakte hain."
    }
  },
  {
    "id": 29,
    "slug": "leroy",
    "name": "Leroy Smith",
    "title": "Grandmaster of Drip",
    "country": "USA",
    "country_flag": "🇺🇸",
    "faction": "Tekken Monks & Traditional Purifiers",
    "faction_badge": "Wing Chun Master",
    "season": "Base",
    "style": "Wing Chun",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/leroy.jpg",
    "height": "181 cm (5'11\")",
    "weight": "79 kg",
    "job_lore_ur": "Wing Chun Grandmaster; 50 saal baad New York ke gangs aur Mishima Zaibatsu ko saaf karne wapas aaya tha.",
    "poking_buttons_ur": "Poking Buttons: 1,2 / 1,1, df+1, d+3,2 (Fast low-high natural combo into Hermit Stance HRM at +8!), db+3 (Sweeping low).",
    "pressure_moves_ur": "Pressure Moves: Hermit Stance (HRM - 3+4) – Is stance mein Leroy Low attacks ko automatically parry kar leta hai! b+2 (Twin Dragon Gate Parry - Kisi bhi punch ya kick ko parry karta hai!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (HRM Stance - d+3,2 ke baad):\nLow: HRM 4 (HRM 4,1+2 low-mid) ya HRM d+1 (Low punch).\nMid: HRM b+1 (+4 on block mid punch!), HRM 2,1 (Safe mid), HRM 1+2 (Mid).",
    "trap_setup_ur": "Jaal (Trap Setup): d+3,2 marein. Yeh hit hone par aap HRM mein +8 hain! Agla banda button dabayega toh HRM 1 (Parry punch) ya HRM 2 usay CH karega. Agar woh normal stance mein attack kare toh b+2 (Parry) daba kar uska har attack wapas mor dein!",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Hermit (HRM) stance transitions aur b+3 ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,4 (-12), b+3 (-13). -15+ Launch: db+3 sweep (-17 Launch), HRM 4 sweep (-18 Launch), d+3,2 (-15 Launch).",
      "bait_duck_interrupt_ur": "Hermit stance mein jab lero aik tang par khara ho, toh foran DICKJAB (db+1) marein! HRM mein woh block nahi kar sakta.",
      "parry_vulnerabilities_ur": "Leroy ki b+2 Twin Dragon Gate sab kuch (elbows, knees, punches) deflect karti hai! Is se bachne ke liye LOWS chalayein (b+2 lows deflect nahi karti) ya WEAPONS use karein."
    }
  },
  {
    "id": 30,
    "slug": "yoshimitsu",
    "name": "Yoshimitsu",
    "title": "Mechanized Space Ninja",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Manji Clan Leader",
    "season": "Base",
    "style": "Advanced Manji Ninjutsu",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/yoshimitsu.jpg",
    "height": "178 cm (5'10\")",
    "weight": "63 kg",
    "job_lore_ur": "Leader of the Manji Clan (Chori kar ke garibon mein baantne wale Robin-Hood ninjas); apni shaitani talwar Yoshimitsu ko qaboo rakhta hai.",
    "poking_buttons_ur": "Poking Buttons: df+1, 1,1 (CH confirm), d+2,2 (Mid string), db+3,3,3 (Spinning low kicks), b+2,2 (Sword slash Heat Engager).",
    "pressure_moves_ur": "Pressure Moves: Flash (1+4 - 6-Frame Launcher! Jab aap NSS No-Sword Stance mein hon toh 8-frame aur zyada range!), Dragonfly (DGF - u+1+2 Helicopter).\nUpper/Mid/Low & Unblockable Mix-up:\nUnblockable Low: fc df+1 (Sword Sweep!) – Yeh block nahi hota, seedha launch karta hai! (Sirf low-parry ya jump se bacha ja sakta hai).\nMid: ws+2,1 (Mid tornado launcher from crouch!) ya df+2 (Safe launcher).\nUnblockable High: DGF 3+4 (Helicopter grab).",
    "mixup_blender_ur": "",
    "trap_setup_ur": "Jaal (Trap Setup): Jab agla banda aap par Plus frames (+1 se +4) le kar attack karne lage, toh block karne ke bajaye 1+4 (Flash) daba dein—6 frames mein agla banda hawa mein ur jayega! Crouch mein jaa kar Unblockable Low (fc df+1) aur ws+2,1 (Mid) ka mix-up lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Dragonfly (DGF) aur Kincho (KIN) dashes ko evade karta hai. Qareeb mein minus frames par button dabane se bachein warna 1+4 Flash lag jayega!",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), b+2,2 (-13). -15+ Launch: fc df+1 sword sweep (-23 Stagger Launch!), kangaroo kick 4~3 (-20 Launch), flash 1+4 whiff/block (-15 Launch).",
      "bait_duck_interrupt_ur": "fc df+1 unblockable sword sweep ko jump kar ke hopkick marein ya interrupt karein! Poison breath b+1+4 duckable hai.",
      "parry_vulnerabilities_ur": "Yoshimitsu ki TALWAAR (Sword) normal parry se deflect nahi hoti! Sword moves ko sirf block karein ya Flash se door spacing banayein."
    }
  },
  {
    "id": 31,
    "slug": "kuma",
    "name": "Kuma II",
    "title": "Master of Salmon",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Mishima Bloodline & Enforcers",
    "faction_badge": "Heihachi's Guard",
    "season": "Base",
    "style": "Heihachi-Style Advanced Kuma Shin Ken",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/kuma.jpg",
    "height": "290 cm (9'6\" - Standing)",
    "weight": "360 kg",
    "job_lore_ur": "Kuma Heihachi ka wafadar bodyguard aur pet hai; Heihachi ke marne ke baad Mishima style karate seekh kar Kazuya se badla lene aaya hai.",
    "poking_buttons_ur": "Poking Buttons: 2,1 (10f string), df+1,2, db+2 (Fast low claw: +1 on hit), b+1 (Power Crush mid).",
    "pressure_moves_ur": "Pressure Moves: Hunting Bear Stance (HBS - 3+4), f,f,f+1+2 (+5 on block into HBS!), Kuma's Heat Electric (f,n,d,df+2 - 11-frame mid launcher in Heat!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (HBS Stance - Four-Legged Crawl):\nLow: HBS d+1+2 (Double low claw: +5 on hit!) ya HBS 2 (Low roll).\nMid: HBS 1+2 (Mid launcher) ya HBS df+2 (Mid launch).\nThrow: HBS f+1+2 (Bear bite throw - khare aur bethe dono ko pakarta hai!).",
    "trap_setup_ur": "Jaal (Trap Setup): f,f,f+1+2 ya db+2 se Hunting Stance (HBS) mein jayein (is mein Highs aur kuch Mids miss ho jate hain). Wahan se HBS d+1+2 (Low), HBS 1+2 (Mid), aur HBS f+1+2 (Bite Throw) chalayein.\nE. Season 1, 2 & 3 DLC Fighters",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Hunting Bear Stance (HBS) lunges aur Bear Godfist ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: 2,1 (-12), df+1,2 (-12). -15+ Launch: db+2 (-15 Launch), HBS 2 roll (-18 Launch), d+1+2 bear sweep (-20 Launch).",
      "bait_duck_interrupt_ur": "Hunting Stance (HBS) mein Kuma chaar taangon par crawl karta hai: High attacks miss ho jayenge! Ground-hitting mids (d+2, df+2) marein. Bear bite throw f+1+2 ko 1+2 se break karein.",
      "parry_vulnerabilities_ur": "Kuma ke claw attacks parry ho sakte hain, lekin uske Headbutt aur Belly attacks normal reversal se deflect nahi hotay!"
    }
  },
  {
    "id": 32,
    "slug": "panda",
    "name": "Panda",
    "title": "Pretty in Pink",
    "country": "China",
    "country_flag": "🇨🇳",
    "faction": "Yggdrasil & Jin's Allies",
    "faction_badge": "Xiaoyu's Bodyguard",
    "season": "Base",
    "style": "Heihachi-Style Advanced Kuma Shin Ken",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/panda.jpg",
    "height": "290 cm (9'6\" - Standing)",
    "weight": "300 kg",
    "job_lore_ur": "Ling Xiaoyu ki bodyguard aur best friend hai; Xiaoyu ki hifazat karte hue Jin ko dhoondne mein uski madad karti hai.",
    "poking_buttons_ur": "Poking Buttons: 2,1 (10f string), df+1,2, db+2 (Fast low claw: +1 on hit), b+1 (Power Crush mid).",
    "pressure_moves_ur": "Pressure Moves: Hunting Bear Stance (HBS - 3+4), f,f,f+1+2 (+5 on block into HBS!), Kuma's Heat Electric (f,n,d,df+2 - 11-frame mid launcher in Heat!).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up (HBS Stance - Four-Legged Crawl):\nLow: HBS d+1+2 (Double low claw: +5 on hit!) ya HBS 2 (Low roll).\nMid: HBS 1+2 (Mid launcher) ya HBS df+2 (Mid launch).\nThrow: HBS f+1+2 (Bear bite throw - khare aur bethe dono ko pakarta hai!).",
    "trap_setup_ur": "Jaal (Trap Setup): f,f,f+1+2 ya db+2 se Hunting Stance (HBS) mein jayein (is mein Highs aur kuch Mids miss ho jate hain). Wahan se HBS d+1+2 (Low), HBS 1+2 (Mid), aur HBS f+1+2 (Bite Throw) chalayein.\nE. Season 1, 2 & 3 DLC Fighters",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Hunting Bear Stance (HBS) lunges aur Shochiku rolls ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: 2,1 (-12), df+1,2 (-12). -15+ Launch: db+2 (-15 Launch), HBS 2 roll (-18 Launch), d+1+2 panda sweep (-20 Launch).",
      "bait_duck_interrupt_ur": "Panda ke HBS stance mein high attacks na phenkein; mid launchers se punish karein. Panda bite throw f+1+2 ko 1+2 se break karein.",
      "parry_vulnerabilities_ur": "Panda ke pet (belly) aur tail attacks parry nahi hotay. Claws parry ho sakti hain."
    }
  },
  {
    "id": 33,
    "slug": "heihachi",
    "name": "Heihachi Mishima",
    "title": "The King of Iron Fist",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Mishima Bloodline & Enforcers",
    "faction_badge": "Mishima Patriarch",
    "season": "Season 1",
    "style": "Mishima Style Fighting Karate",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/heihachi.jpg",
    "height": "179 cm (5'10\")",
    "weight": "84 kg",
    "job_lore_ur": "Former Zaibatsu Leader; Tekken Monks ke zariye bacha aur wapas \"King of Iron Fist\" banne lauta hai.",
    "poking_buttons_ur": "Poking Buttons: 1,b+2 (-2 on block!), df+1 (Confirm into df+1,2), f+3 (Fast mid knee).",
    "pressure_moves_ur": "Pressure Moves: f+4 (+4 on block; crouching opponent ko guaranteed df+1,2 deta hai!), uf+3,4 (Hunting Hawk: +5 on block).",
    "mixup_blender_ur": "Upper/Mid/Low Mix-up:\nMid: ff+2 (Demon Uppercut launcher), b+4 (Homing CH launcher).\nLow: db+2 (High-crushing heavy low) ya cd+4,4,1 (Hellsweep).",
    "trap_setup_ur": "Jaal (Trap Setup): f+4 mar kar agle bande ko duck karne se darayein, phir Raijin Stance (b+1+2) ya Fujin Stance (d+1+2) se guard-breaks aur plus frames ki barish kar dein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) EWGF, f,f+2 Demon Paw, aur 1,b+2 ko evade karta hai. b+4 homing move se bachne ke liye neutral block karein.",
      "minus_punishable_moves_ur": "-10 to -14: 1,b+2 (-2 on block safe), df+1,2 (-13). -15+ Launch: Hellsweep cd+4,n,4 (-16 Launch), f,f+2 (-16 on block), uf+4 hopkick (-13).",
      "bait_duck_interrupt_ur": "Hellsweep ko db se block kar ke full combo ws launcher marein! 1,b+2 block kar ke jaldi mein counter na karein kyunki Heihachi ka recovery fast hai.",
      "parry_vulnerabilities_ur": "Heihachi f+1+2 headbutt aur b+1+2 parry karta hai. Uske headbutts unparryable hain, is liye elbows aur knees se uski parry torein."
    }
  },
  {
    "id": 34,
    "slug": "eddy",
    "name": "Eddy Gordo",
    "title": "Capoeira Prodigy",
    "country": "Brazil",
    "country_flag": "🇧🇷",
    "faction": "Tekken Monks & Traditional Purifiers",
    "faction_badge": "Reformed Fighter",
    "season": "Season 1",
    "style": "Capoeira",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/eddy.jpg",
    "height": "188 cm (6'2\")",
    "weight": "85 kg",
    "job_lore_ur": "Capoeira Master; G-Corp se apni ghaltiyon ka kaffara ada karne ke liye Tekken Monks ke sath milta hai.",
    "poking_buttons_ur": "Poking & Pressure: df+1,3, d+3 (Low into Negativa RLX), f,f+3 (Low kick into Handstand HSP + Mandinga level!), 3,3,3,3 (Beginner-friendly pressure string into stances).",
    "pressure_moves_ur": "Pressure & Stance Flows: df+1,3, d+3 (Low into Negativa RLX), f,f+3 (Low kick into Handstand HSP + Mandinga level!), 3,3,3,3 (Beginner-friendly pressure string into stances).",
    "mixup_blender_ur": "Mix-up (RLX Negativa Stance): Low: RLX 3,3 (Mandinga Level 2 par 50/50 low launcher!) | Mid: RLX 4,3 (Safe mid tornado launcher!).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (RLX Negativa Stance): Low: RLX 3,3 (Mandinga Level 2 par 50/50 low launcher!) | Mid: RLX 4,3 (Safe mid tornado launcher!).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Bananeira (HSP handstand) aur Negativa (RLX) transitions ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,3 (-13), 3,3,3,3 string ender (-12). -15+ Launch: RLX 3,3 Mandinga low launcher (-18 Launch), HSP 4 sweep (-17 Launch), b+3,3 (-16 Launch).",
      "bait_duck_interrupt_ur": "Eddy jab RLX zameen par baithe ya HSP handstand par jaye, toh foran DICKJAB (db+1) marein! Yeh uske flow ko wahi rok deta hai. 3,3,3,3 beginner string ko duck kar ke launch karein.",
      "parry_vulnerabilities_ur": "Eddy ke RLX ground kicks ko df se LOW PARRY karein. Uske acrobatic kicks standard kick parry se pakray ja sakte hain."
    }
  },
  {
    "id": 35,
    "slug": "lidia",
    "name": "Lidia Sobieska",
    "title": "Prime Minister of Poland",
    "country": "Poland",
    "country_flag": "🇵🇱",
    "faction": "Tekken Monks & Traditional Purifiers",
    "faction_badge": "Polish Government",
    "season": "Season 1",
    "style": "Traditional Karate",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/lidia.jpg",
    "height": "172 cm (5'7.5\")",
    "weight": "62 kg",
    "job_lore_ur": "Prime Minister of Poland & Traditional Karate World Champion; apne mulk aur duniya ko Kazuya se bachane nikli hai.",
    "poking_buttons_ur": "Poking & Pressure: 1,2,2 (Into Cat Stance), df+2 (Mid check into Horse Stance HRS), ff+2 (+5 on block into HRS!), db+3 (Clean hit knockdown low!).",
    "pressure_moves_ur": "Pressure & Stance Flows: 1,2,2 (Into Cat Stance), df+2 (Mid check into Horse Stance HRS), ff+2 (+5 on block into HRS!), db+3 (Clean hit knockdown low!).",
    "mixup_blender_ur": "Mix-up (Heat Heaven and Earth HAE Stance): Unblockable High: HAE 1 (+12 guard break!) | Mid: HAE 2 (+6 on block mid smash!).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (Heat Heaven and Earth HAE Stance): Unblockable High: HAE 1 (+12 guard break!) | Mid: HAE 2 (+6 on block mid smash!).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) ff+2, Horse Stance (HRS), aur Cat Stance (CAT) pokes ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: 1,2,2 (-12), df+2 (-13). -15+ Launch: db+3 sweep (-17 Launch), HRS 4 sweep (-18 Launch), ff+2 (-14 pushback).",
      "bait_duck_interrupt_ur": "HAE 1 unblockable guard break high hai: DUCK kar ke ws launcher marein! Cat Stance mein aate hi dickjab (db+1) se attack interrupt karein.",
      "parry_vulnerabilities_ur": "Lidia ke traditional karate punches parry ho sakte hain. Lidia ki apni parry todne ke liye Elbows aur Knees use karein."
    }
  },
  {
    "id": 36,
    "slug": "clive",
    "name": "Clive Rosfield",
    "title": "First Shield of Rosaria",
    "country": "Valisthea",
    "country_flag": "⚔️",
    "faction": "Guest Legends",
    "faction_badge": "Dominant of Ifrit",
    "season": "Season 1",
    "style": "Rosarian Royal Swordsmanship • Eikonic Combat",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/clive.jpg",
    "height": "~185 cm (6'1\")",
    "weight": "~82 kg",
    "job_lore_ur": "First Shield of Rosaria & Dominant of Ifrit.",
    "poking_buttons_ur": "Poking & Pressure: f+1+2 (Prominence - Half-screen safe mid!), 1,1 / df+1,2, d+1 (Long-range sword low), Phoenix Shift (PHX - f+4).",
    "pressure_moves_ur": "Pressure & Stance Flows: f+1+2 (Prominence - Half-screen safe mid!), 1,1 / df+1,2, d+1 (Long-range sword low), Phoenix Shift (PHX - f+4).",
    "mixup_blender_ur": "Mix-up (PHX Dash): Low: PHX 3 (Sliding sword sweep build Zantetsuken meter!) | Mid: PHX 2 / PHX 1+2 (Mid sword launcher) | Throw: PHX 1+3 (Titan grab).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (PHX Dash): Low: PHX 3 (Sliding sword sweep build Zantetsuken meter!) | Mid: PHX 2 / PHX 1+2 (Mid sword launcher) | Throw: PHX 1+3 (Titan grab).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Phoenix Shift dash (PHX), Prominence (f+1+2), aur Titan slashes ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), 1,1 (-12). -15+ Launch: PHX 3 sliding sweep (-18 Launch), Prominence f+1+2 (-14 pushback), Titan smash (-16 Launch).",
      "bait_duck_interrupt_ur": "PHX dash se aane wale low sword sweep ko db se block kar ke launch karein! Clive ke long range projectile f+2 ko duck karein.",
      "parry_vulnerabilities_ur": "Clive ki TALWAAR (Invictus Sword) normal parry aur low parry se deflect NAHI hoti! Sword slashes ko sirf block kar ke punish karein."
    }
  },
  {
    "id": 37,
    "slug": "anna",
    "name": "Anna Williams",
    "title": "Scarlet Lightning",
    "country": "Ireland",
    "country_flag": "🇮🇪",
    "faction": "G-Corporation & Kazuya's Allies",
    "faction_badge": "G-Corp Commander",
    "season": "Season 2",
    "style": "Assassination Martial Arts",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/anna.jpg",
    "height": "171 cm (5'7\")",
    "weight": "56 kg",
    "job_lore_ur": "Assassin, Former G-Corp Commander & Nina ki choti behen / rival.",
    "poking_buttons_ur": "Poking & Pressure: df+1,2, d+4,1 (Low-high), qcf+1 (+ on block high CH launcher), Chaos Judgment Stance (CJM - b+3 - Auto-low reversals!).",
    "pressure_moves_ur": "Pressure & Stance Flows: df+1,2, d+4,1 (Low-high), qcf+1 (+ on block high CH launcher), Chaos Judgment Stance (CJM - b+3 - Auto-low reversals!).",
    "mixup_blender_ur": "Mix-up (Full Crouch 50/50 Queen): Low: fc df+2 (Cold Blade - Half-life low launcher!) | Mid: ws+2 (15f Mid Launcher) ya uf+1,3,3+4 (Mid knockdown).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (Full Crouch 50/50 Queen): Low: fc df+2 (Cold Blade - Half-life low launcher!) | Mid: ws+2 (15f Mid Launcher) ya uf+1,3,3+4 (Mid knockdown).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Chaos Judgment (CJM) stance entries, qcf+1, aur df+1,2 ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), f+1+2 (-13). -15+ Launch: Cold Blade fc df+2 (-18 Massive Launch!), d+4,1 (-13), ws+2 (-15 Launch).",
      "bait_duck_interrupt_ur": "d+4,1 string ka doosra hit High hai: duck kar ke ws+2 launcher marein! Full Crouch (FC) 50/50 mein Cold Blade ko db se block kar ke full combo lein.",
      "parry_vulnerabilities_ur": "Anna CJM stance (b+3) mein auto-low reversal karti hai! CJM mein low attacks mat marein, sirf MIDS ya ELBOWS chalayein."
    }
  },
  {
    "id": 38,
    "slug": "fahkumram",
    "name": "Fahkumram",
    "title": "Thunder Striker",
    "country": "Thailand",
    "country_flag": "🇹🇭",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Muay Thai Legend",
    "season": "Season 2",
    "style": "Muay Thai",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/fahkumram.jpg",
    "height": "215 cm (7'0.5\")",
    "weight": "130 kg",
    "job_lore_ur": "Legendary Muay Thai Champion; Thai Military ne uski biwi aur beti ko bandhi bana kar usay larne par majboor kiya hai.",
    "poking_buttons_ur": "Poking & Pressure: bf+4 (Jet Kick: +6 on block!), 3 (Long range mid poke with 3,1 aur 3,4 extensions), d+4 (Fast shin low).",
    "pressure_moves_ur": "Pressure & Stance Flows: bf+4 (Jet Kick: +6 on block!), 3 (Long range mid poke with 3,1 aur 3,4 extensions), d+4 (Fast shin low).",
    "mixup_blender_ur": "Mix-up (String Charge Guard-Breaks): 3,4~4* ya f+3,2,4~3* (Charged Kick jo block karne wale ko deewar par चिपका deta hai!) vs 3,4~3 (Low kick).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (String Charge Guard-Breaks): 3,4~4* ya f+3,2,4~3* (Charged Kick jo block karne wale ko deewar par चिपका deta hai!) vs 3,4~3 (Low kick).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Jet Kick (bf+4), long range knee pokes, aur string extensions ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: 3,1 (-12), df+1,2 (-13). -15+ Launch: 3,4~3 low kick (-16 Launch), db+4 (-17 Launch), charged kick 3,4~4* (-14 on duck).",
      "bait_duck_interrupt_ur": "Charged kick 3,4~4* ko charge hote dekh kar DUCK karein aur ws+2 se launch karein! 3,1 string ka second hit high hai: duck karein.",
      "parry_vulnerabilities_ur": "Fahkumram ke Elbows aur Knees normal reversal se deflect nahi hotay! Normal kicks ko df se low parry karein."
    }
  },
  {
    "id": 39,
    "slug": "armor-king",
    "name": "Armor King II",
    "title": "Dark Jaguar",
    "country": "Mexico",
    "country_flag": "🇲🇽",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Black Jaguar Circuit",
    "season": "Season 2",
    "style": "Lucha Libre • Street Brawling",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/armor-king.jpg",
    "height": "200 cm (6'7\")",
    "weight": "148 kg",
    "job_lore_ur": "Black Jaguar Pro-Wrestler (Armor King I ka chota bhai jo Marduk aur King se hisab barabar rakhta hai).",
    "poking_buttons_ur": "Poking & Pressure: df+1 (Best grappler poke), d+3 (+1 on hit low), b+1 (12f CH launcher!), Dark Upper (f,n,d,df+2), f,f,n,2 (Stun low).",
    "pressure_moves_ur": "Pressure & Stance Flows: df+1 (Best grappler poke), d+3 (+1 on hit low), b+1 (12f CH launcher!), Dark Upper (f,n,d,df+2), f,f,n,2 (Stun low).",
    "mixup_blender_ur": "Mix-up (Wave-dash Grab/Mid Vortex): Wave-dash (f,n,d,df...) se Giant Swing (f,hcf+1), Tombstone (db,f+2+4), aur Shining Black (f,f,f+2+4) lagayein; duck karne par Dark Upper (cd+2) ya ws+1 mar kar launch kar dein!",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (Wave-dash Grab/Mid Vortex): Wave-dash (f,n,d,df...) se Giant Swing (f,hcf+1), Tombstone (db,f+2+4), aur Shining Black (f,f,f+2+4) lagayein; duck karne par Dark Upper (cd+2) ya ws+1 mar kar launch kar dein!\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Dark Upper (cd+2), df+1, aur f,f,n,2 ko evade karta hai. Throws se bachne ke liye tech ya duck karein.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), b+1,2 (-13). -15+ Launch: Dark Upper cd+2 (-15 Launch on block!), f,f,n,2 low stun (-18 Launch), hopkick uf+4 (-13).",
      "bait_duck_interrupt_ur": "f,f,n,2 low ko db block kar ke ws launcher marein! Giant Swing par 1 break karein, Tombstone par 2 break karein, Shining Black par 1+2 break karein.",
      "parry_vulnerabilities_ur": "Armor King ke paas b+1+3 / b+2+4 reversal hai. Usay todne ke liye Elbows (Paul df+1) ya Knees (Bryan f+3) use karein."
    }
  },
  {
    "id": 40,
    "slug": "miary-zo",
    "name": "Miary Zo",
    "title": "Primal Fighting Spirit",
    "country": "Madagascar",
    "country_flag": "🇲🇬",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Spiritual Guardian",
    "season": "Season 2",
    "style": "Morengy • Ancient Primal Arts",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/miary-zo.jpg",
    "height": "~174 cm (5'8.5\")",
    "weight": "~62 kg",
    "job_lore_ur": "Morengy Fighter & Spiritual Guardian (\"Fighting God Reborn\" connected to Ogre's ancient power).",
    "poking_buttons_ur": "Poking & Pressure: 1,2,4, df+1, d+3 (Fast low), f,f+3 (Plus on block spiritual leap), Primal Stance (PRM - d+3+4).",
    "pressure_moves_ur": "Pressure & Stance Flows: 1,2,4, df+1, d+3 (Fast low), f,f+3 (Plus on block spiritual leap), Primal Stance (PRM - d+3+4).",
    "mixup_blender_ur": "Mix-up (PRM Stance): Low: PRM 3 (Sweeping tail/leg low) | Mid: PRM 2 (Mid launcher) | Unblockable: PRM 1+2 (Ogre-style ancient guard break!).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (PRM Stance): Low: PRM 3 (Sweeping tail/leg low) | Mid: PRM 2 (Mid launcher) | Unblockable: PRM 1+2 (Ogre-style ancient guard break!).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Primal Stance (PRM) lunges aur spiritual leaps (f,f+3) ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), 1,2,4 (-13). -15+ Launch: PRM 3 sweeping tail/leg low (-18 Launch), PRM 1+2 guard break (-15 on duck), f,f+3 (-12).",
      "bait_duck_interrupt_ur": "PRM 1+2 ancient guard break high hai: duck kar ke ws launcher marein! PRM 3 tail sweep ko db block kar ke full combo lein.",
      "parry_vulnerabilities_ur": "Miary Zo ke spiritual energy attacks aur tail moves low parry nahi hotay! Normal punches/kicks parry ho sakti hain."
    }
  },
  {
    "id": 41,
    "slug": "kunimitsu",
    "name": "Kunimitsu II",
    "title": "Fox-Masked Kunoichi",
    "country": "Japan",
    "country_flag": "🇯🇵",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Manji Renegade",
    "season": "Season 3",
    "style": "Manji Ninjutsu • Dagger Arts",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/kunimitsu.jpg",
    "height": "162 cm (5'4\")",
    "weight": "50 kg",
    "job_lore_ur": "Thief & Ninja Assassin (Kunimitsu I ki beti jo family business aage barha rahi hai).",
    "poking_buttons_ur": "Poking & Pressure: 2,2,2,2 (Fast string into Setsuna SET dash), qcf+1 (Full-screen Kunai Throw!), df+1, db+3,3 (Low).",
    "pressure_moves_ur": "Pressure & Stance Flows: 2,2,2,2 (Fast string into Setsuna SET dash), qcf+1 (Full-screen Kunai Throw!), df+1, db+3,3 (Low).",
    "mixup_blender_ur": "Mix-up (SET Dash & Crouch): Low: SET 3 (Sliding low) ya fc df+3 (Sweep launcher!) | Mid: SET 2 (Safe mid) ya ws+3 (Mid launcher).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (SET Dash & Crouch): Low: SET 3 (Sliding low) ya fc df+3 (Sweep launcher!) | Mid: SET 2 (Safe mid) ya ws+3 (Mid launcher).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Setsuna (SET) dash aur Kunai throws (qcf+1) ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), 2,2,2,2 (-13). -15+ Launch: fc df+3 sweep (-20 Launch), SET 3 sliding low (-17 Launch), qcf+2 (-15 Launch).",
      "bait_duck_interrupt_ur": "qcf+1 Kunai Throw high hai: full screen par duck karein aur dash in karein! SET dash par dickjab (db+1) se mix-up torein.",
      "parry_vulnerabilities_ur": "Kunimitsu ke KUNAI (Daggers) projectiles normal parry se deflect nahi hotay! Sword slashes ko block karein."
    }
  },
  {
    "id": 42,
    "slug": "bob",
    "name": "Bob Richards",
    "title": "Speed & Weight",
    "country": "USA",
    "country_flag": "🇺🇸",
    "faction": "Tournament Veterans & Wildcards",
    "faction_badge": "Freestyle Bounty Hunter",
    "season": "Season 3",
    "style": "Freestyle Karate",
    "weak_side": "SSR",
    "avatar": "/assets/avatars/bob.jpg",
    "height": "186 cm (6'1\")",
    "weight": "152 kg",
    "job_lore_ur": "Freestyle Karate Bounty Hunter (\"Speed and Weight\" philosophy ke liye apna wazan barhaya).",
    "poking_buttons_ur": "Poking & Pressure: df+1, b+2,2, d+3+4 (Fast double low), Spinner Ball (BAL - f+3+4), cd+1 (Wave-dash high: + on block).",
    "pressure_moves_ur": "Pressure & Stance Flows: df+1, b+2,2, d+3+4 (Fast double low), Spinner Ball (BAL - f+3+4), cd+1 (Wave-dash high: + on block).",
    "mixup_blender_ur": "Mix-up (Wave-dash 50/50): Low: cd+4,1+2 (Belly Hellsweep!) ya db+3+4 | Mid: uf+1+2,4 (Safe mid) ya cd+2 (Mid launcher).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up (Wave-dash 50/50): Low: cd+4,1+2 (Belly Hellsweep!) ya db+3+4 | Mid: uf+1+2,4 (Safe mid) ya cd+2 (Mid launcher).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSR",
      "weak_side_detail_ur": "Sidestep Right (SSR) Spinner Ball (BAL), cd+1, aur Belly Hellsweep (cd+4) ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), b+2,2 (-13). -15+ Launch: Belly Hellsweep cd+4,1+2 (-23 Stagger Launch!), db+3+4 (-17 Launch), BAL 3 (-16 Launch).",
      "bait_duck_interrupt_ur": "Wave-dash par db se BLOCK karein aur Belly Hellsweep ko ws+2 se full launch marein! Spinner Ball par 1 jab se float karein.",
      "parry_vulnerabilities_ur": "Bob ke Belly stomps aur heavy shoulder attacks normal parry se deflect nahi hotay. Pokes parry ho sakte hain."
    }
  },
  {
    "id": 43,
    "slug": "roger-jr",
    "name": "Roger Jr.",
    "title": "Marsupial Boxing Champ",
    "country": "Australia",
    "country_flag": "🇦🇺",
    "faction": "G-Corporation & Kazuya's Allies",
    "faction_badge": "G-Corp Bio-Lab",
    "season": "Season 3",
    "style": "Commando Animal Boxing",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/roger-jr.jpg",
    "height": "160 cm (5'3\")",
    "weight": "85 kg",
    "job_lore_ur": "Genetically Modified Boxing Kangaroo (Roger ki biwi aur uska beta jo pouch mein beth kar larta hai).",
    "poking_buttons_ur": "Poking & Pressure: 1,2,1 (Boxing jabs), d+3+4 (Tail low sweep), f,f+2 (Mid punch), Animal Stance (ANM - b+3+4).",
    "pressure_moves_ur": "Pressure & Stance Flows: 1,2,1 (Boxing jabs), d+3+4 (Tail low sweep), f,f+2 (Mid punch), Animal Stance (ANM - b+3+4).",
    "mixup_blender_ur": "Mix-up: King की तरह Giant Swing (f,hcf+1) और Animal Kick (ANM 3,3,3 Mid vs ANM 4 Low) का खतरनाक इस्तेमाल।",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up: King की तरह Giant Swing (f,hcf+1) और Animal Kick (ANM 3,3,3 Mid vs ANM 4 Low) का खतरनाक इस्तेमाल।\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Animal Stance (ANM) charges aur tail sweeps ko evade karta hai.",
      "minus_punishable_moves_ur": "-10 to -14: 1,2,1 (-12), f,f+2 (-13). -15+ Launch: d+3+4 tail low sweep (-20 Launch), ANM 4 sweep (-18 Launch), hopkick uf+4 (-13).",
      "bait_duck_interrupt_ur": "d+3+4 tail sweep ko db block kar ke ws launcher marein! Giant Swing throw par 1 daba kar break karein.",
      "parry_vulnerabilities_ur": "Roger Jr. ki DUM (Tail) aur Kangaroo kicks low parry nahi hotin! Normal boxing punches standard punch parry se pakray ja sakte hain."
    }
  },
  {
    "id": 44,
    "slug": "yujiro",
    "name": "Yujiro Hanma",
    "title": "The Strongest Creature on Earth",
    "country": "Japan",
    "country_flag": "👹",
    "faction": "Guest Legends",
    "faction_badge": "The Ogre",
    "season": "Season 3",
    "style": "Total Primal Combat • Demon Back",
    "weak_side": "SSL",
    "avatar": "/assets/avatars/yujiro.jpg",
    "height": "190 cm (6'3\")",
    "weight": "120 kg",
    "job_lore_ur": "\"The Strongest Creature on Earth\" (The Ogre); bina kisi weapon ya rule ke duniya ki fauj ko akele harane wala shaitan.",
    "poking_buttons_ur": "Poking & Pressure: df+1, b+1 (Heavy chop: +5 on block!), d+2 (Crushing low punch), Demon Back Awakening (1+2+3+4 in Heat).",
    "pressure_moves_ur": "Pressure & Stance Flows: df+1, b+1 (Heavy chop: +5 on block!), d+2 (Crushing low punch), Demon Back Awakening (1+2+3+4 in Heat).",
    "mixup_blender_ur": "Mix-up: Guard Break: f,f+1+2* (Ear-drum slap / Guard Break -> Free combo!) | Low: db+4 (Leg-breaker sweep) | Mid: df+2 / uf+2 (Brutal mid smash).",
    "trap_setup_ur": "Trap & Setup (Jaal): Mix-up: Guard Break: f,f+1+2* (Ear-drum slap / Guard Break -> Free combo!) | Low: db+4 (Leg-breaker sweep) | Mid: df+2 / uf+2 (Brutal mid smash).\nMix-up aur pressure se opponent ko corner karein aur Counter-Hit trap lagayein.",
    "anti_guide": {
      "weak_side": "SSL",
      "weak_side_detail_ur": "Sidestep Left (SSL) Heavy Chop (b+1) aur brute punches ko evade karta hai. Distance maintain rakhein.",
      "minus_punishable_moves_ur": "-10 to -14: df+1,2 (-12), b+1 (-13). -15+ Launch: db+4 leg-breaker sweep (-24 Stagger Launch!), f,f+1+2* ear-slap guard break (-16 on duck), df+2 (-15 Launch).",
      "bait_duck_interrupt_ur": "f,f+1+2* Ear-drum slap high guard break hai: dekhte hi DUCK karein aur ws+2 se launch kar dein! db+4 sweep ko db block kar ke 85+ damage lein.",
      "parry_vulnerabilities_ur": "Yujiro ka Demon Back awakening unblockable brute attacks deta hai jo normal reversal ko tor dete hain! Us par defensive parry ki koshish mat karein."
    }
  }
];

  // Expose on global window object
  window.TEKKEN8_MASTER_DATA = {
    universal: UNIVERSAL_MECHANICS,
    roster: ROSTER_DATA,
    getFighter: function (slug) {
      if (!slug) return null;
      const s = String(slug).toLowerCase().trim();
      return ROSTER_DATA.find(f => f.slug === s || String(f.id) === s) || null;
    },
    filterRoster: function (criteria) {
      criteria = criteria || {};
      return ROSTER_DATA.filter(f => {
        if (criteria.season && criteria.season !== 'ALL' && f.season !== criteria.season) return false;
        if (criteria.faction && criteria.faction !== 'ALL' && f.faction !== criteria.faction && f.faction_badge !== criteria.faction) return false;
        if (criteria.weak_side && criteria.weak_side !== 'ALL' && f.weak_side !== criteria.weak_side) return false;
        if (criteria.search) {
          const q = criteria.search.toLowerCase().trim();
          const matchName = f.name.toLowerCase().includes(q);
          const matchCountry = f.country.toLowerCase().includes(q);
          const matchStyle = f.style.toLowerCase().includes(q);
          const matchTitle = f.title.toLowerCase().includes(q);
          if (!matchName && !matchCountry && !matchStyle && !matchTitle) return false;
        }
        return true;
      });
    }
  };

  console.log('✅ Tekken 8 Master Strategy Hub Data Layer Loaded: 44 Characters & Universal Mechanics.');
})();
