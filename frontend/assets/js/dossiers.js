/**
 * TEKKEN 8 FIGHTER DOSSIERS ENGINE - AUTHORITATIVE CANONICAL REFERENCE
 * Complete physical, biographical, combat attribute, and tactical metrics for all 43 Fighters.
 * Version: Tekken 8 Patch v3.00.02
 */

(function () {
  'use strict';

  const DOSSIERS = {
    jin: {
      name: "Jin Kazama",
      title: "The Lightning of Fate",
      japanese_name: "風間 仁",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Traditional Karate • Kazama Style Self-Defense",
      height: "180 cm (5'11\")",
      weight: "75 kg (165 lbs)",
      age: "21",
      blood_type: "AB",
      status: "Leader of G-Corp Resistance",
      archetype: "All-Around / Mishima",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "Heir to the cursed Mishima bloodline and Kazama purifying heritage. Tormented by the global devastation he unleashed as head of the Mishima Zaibatsu, Jin embraces his mother Jun's teachings to purify his Devil Gene and destroy Kazuya once and for all.",
      pros: ["God-tier Range 2 keepout with f+4", "Unparryable electric d+2 low punch", "Versatile Zanshin stance cancels", "High-damage Heat Smash combo extensions"],
      cons: ["Demanding just-frame Electric Wind Hook Fist execution", "Linear key pokes easily stepped to SSL"],
      ratings: { offense: 92, defense: 90, range: 88, execution: 86, movement: 88, throw: 78 },
      top5: [
        { cmd: "2, 1, 4", role: "Safe String / Hit-Confirm", startup: "i10", block: "-6", dmg: 38, desc: "Universal 10f string with knockdown wall splat on counter-hit" },
        { cmd: "df+1", role: "Mid Check Poke", startup: "i13", block: "-3", dmg: 11, desc: "Essential mid poke to stop opponents ducking highs; tracks right" },
        { cmd: "f+4", role: "Keepout / CH Launcher", startup: "i16", block: "-7", dmg: 21, desc: "Legendary mid kick; safe on block, guarantees combo on Counter Hit" },
        { cmd: "d+2", role: "High-Crush Low Poke", startup: "i22", block: "-14", dmg: 22, desc: "Crushes highs instantly, forces crouch and leaves Jin at +4 on hit" },
        { cmd: "f,n,d,df+2", role: "Just-Frame Launcher", startup: "i14", block: "+5", dmg: 25, desc: "Electric Wind Hook Fist (EWHF); launcher with massive block advantage" }
      ],
      gameplan: "Dictate Range 2 spacing with f+4 and df+1. Force hesitations with d+2 and hellsweep (f,n,d,df+4). Punish whiffs decisively with EWHF into full aerial juggle.",
      launcher: "df+2 (Mid Launcher, i15, -12 on block, launches on normal hit)",
      standing_punish: [
        { frame: "10f", move: "2, 4", dmg: 25, adv: "+4" },
        { frame: "12f", move: "1+2", dmg: 28, adv: "KND" },
        { frame: "14f", move: "f,n,d,df+2", dmg: 25, adv: "+5 Launch" },
        { frame: "15f", move: "df+2 or d+3+4", dmg: 32, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 26, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 20, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,n,d,df+2 (EWHF)", startup: "i14", reach: "Far", dmg: 25, note: "Optimal launcher on any visible whiff" },
        { move: "f,f+2 (Demon Paw)", startup: "i15", reach: "Long", dmg: 24, note: "Safe gap-closer with extreme pushback" }
      ],
      stances: ["Zanshin (b+1+2)", "Zen (d+1+2 or df+1~F)", "Mental Alertness"],
      heat_breakdown: "Enters Awakened Devil state. Enhances f,f+2 into launcher and grants access to high-damage Heat Smash.",
      stage_synergy: "Excels on Wall stages (Coliseum, Urban Square) where Demon Paw and Zen 3+4 provide effortless splats."
    },

    kazuya: {
      name: "Kazuya Mishima",
      title: "The Cold-Blooded Oppressor",
      japanese_name: "三島 一八",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Mishima Style Fighting Karate",
      height: "181 cm (5'11\")",
      weight: "76 kg (168 lbs)",
      age: "49",
      blood_type: "AB",
      status: "G Corporation Supreme Executive",
      archetype: "50/50 Vortex / Mishima",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left / Walk Left)",
      lore: "Completely consumed by the Devil within. Following Heihachi's demise at the caldera, Kazuya utilized G Corporation's industrial warfare to subjugate the world, seeking absolute dominion through raw, unyielding demonic supremacy.",
      pros: ["Unmatched 50/50 Oki vortex (Hellsweep vs FF+3)", "Best 1,1,2 jab hit-confirm in Tekken history", "True 13f PEWGF normal-hit launcher", "Devastating high-damage counter-hit df+2"],
      cons: ["No generic 13f mid poke (df+1 is slow i15)", "Extremely steep execution curve", "Vulnerable to duck-and-launch against highs"],
      ratings: { offense: 96, defense: 94, range: 84, execution: 98, movement: 86, throw: 74 },
      top5: [
        { cmd: "1, 1, 2", role: "Hit-Confirm Knockdown", startup: "i10", block: "-17", dmg: 25, desc: "Essential 10f punish; hit-confirmable on visual cue, knocks down into vortex" },
        { cmd: "f,n,d,df+2", role: "Electric Wind God Fist", startup: "i11", block: "+5", dmg: 23, desc: "Signature EWGF; high launcher with frame advantage and immense pushback" },
        { cmd: "f,n,d,df+4, 1", role: "Knockdown Low Hellsweep", startup: "i16", block: "-23", dmg: 30, desc: "Feared unseeable low that knocks down and restarts the okizeme vortex" },
        { cmd: "f,f+3", role: "Safe Mid Launcher", startup: "i19", block: "-3", dmg: 20, desc: "Mid mixup companion to Hellsweep; safe on block and launches on normal hit" },
        { cmd: "df+2", role: "Counter-Hit Launcher", startup: "i15", block: "-12", dmg: 21, desc: "Fierce gut punch; crumple stuns on counter-hit for PEWGF launch" }
      ],
      gameplan: "Score a knockdown using 1,1,2 or EWGF. Wavedash directly in opponent face to enforce the 50/50 vortex: low Hellsweep or mid f,f+3.",
      launcher: "EWGF (f,n,d,df+2, i11-i14, +5 on block, high launcher) / f,f+3 (Mid, i19, -3 on block)",
      standing_punish: [
        { frame: "10f", move: "1, 1, 2", dmg: 25, adv: "KND / Vortex" },
        { frame: "11f", move: "b+1, 2", dmg: 27, adv: "+3" },
        { frame: "13f", move: "PEWGF (f,n,df+2)", dmg: 23, adv: "+5 Launch" },
        { frame: "15f", move: "df+1, 2 or df+2", dmg: 31, adv: "KND / Stun" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2 (Twin Pistons)", dmg: 28, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "EWGF", startup: "i11", reach: "Medium", dmg: 23, note: "Universal punish tool" },
        { move: "b+1, 2", startup: "i11", reach: "Medium", dmg: 27, note: "Fastest mid retaliator" }
      ],
      stances: ["Crouch Dash / Wavedash (f,n,d,df)"],
      heat_breakdown: "Unlocks True Devil form. Grants access to Devil Blaster beams and enhances Hellsweep followups.",
      stage_synergy: "Thrives in closed Wall stages like Arena and Underground where vortex corner traps are inescapable."
    },

    reina: {
      name: "Reina",
      title: "The Dusky Thunder",
      japanese_name: "麗奈",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Mishima Style Fighting Karate + Taido",
      height: "165 cm (5'5\")",
      weight: "52 kg (115 lbs)",
      age: "Unknown (~19)",
      blood_type: "Unknown",
      status: "Mishima High School Student",
      archetype: "Stance Rushdown / Mishima",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "A mysterious prodigy attending Mishima High School. Armed with both orthodox Taido acrobatics and the thunderous lightning of the Mishima style, she harbors an intimate, covert connection to Heihachi Mishima's dark legacy.",
      pros: ["Lightning-fast EWGF access with acrobatic Taido evasions", "Devastating Sentai and Wind God step mixups", "Strong wall carry and corner wall-break pressure", "Plus-frame Heat transitions"],
      cons: ["Lacks a conventional 15f normal-hit mid launcher", "Weak to SSR sidewalk against her core strings"],
      ratings: { offense: 95, defense: 84, range: 86, execution: 90, movement: 92, throw: 76 },
      top5: [
        { cmd: "f,n,d,df+2", role: "Electric Wind God Fist", startup: "i11", block: "+5", dmg: 23, desc: "High-speed Mishima electric launcher with crushing pushback" },
        { cmd: "df+1", role: "Mid Check Poke", startup: "i13", block: "-1", dmg: 12, desc: "One of the best df+1 pokes in the game; only -1 on block with Sentai cancel" },
        { cmd: "f,f+2", role: "Heat Engager / Stance", startup: "i15", block: "-9", dmg: 20, desc: "Long-range mid thrust that transitions smoothly into Sentai mixup" },
        { cmd: "db+2", role: "Low Harass", startup: "i20", block: "-13", dmg: 17, desc: "High crushing low kick that leaves Reina at +1 on hit" },
        { cmd: "1, 1, 2", role: "Mishima Knockdown Jab", startup: "i10", block: "-17", dmg: 25, desc: "Fastest 10f knockdown punish that sets up immediate oki pressure" }
      ],
      gameplan: "Use df+1 and f,f+2 to enter Sentai stance. Pressure opponents with plus frames, then catch sidesteps or ducking with EWGF.",
      launcher: "EWGF (f,n,d,df+2, i11, +5 on block) / Sentai 3+4",
      standing_punish: [
        { frame: "10f", move: "1, 1, 2", dmg: 25, adv: "KND" },
        { frame: "12f", move: "b+1, 2", dmg: 26, adv: "+4" },
        { frame: "14f", move: "EWGF", dmg: 23, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "15f", move: "WS+3, 4", dmg: 32, adv: "Knockdown / Wall Splat" }
      ],
      whiff_punish: [
        { move: "EWGF", startup: "i11", reach: "Far", dmg: 23, note: "Premier whiff punish" },
        { move: "f,f+2", startup: "i15", reach: "Long", dmg: 20, note: "Effortless dash-in punish" }
      ],
      stances: ["Sentai (SEN)", "Wrath of the Heavens (HW)", "Wind God Step"],
      heat_breakdown: "Enters Heihachi Awakening. Unlocks crushing guard breaks and electrified Taido leaps.",
      stage_synergy: "Excels on stages with breakable walls where her Sentai extensions shatter barriers with ease."
    },

    jun: {
      name: "Jun Kazama",
      title: "The Light of Hope",
      japanese_name: "風間 準",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Kazama Style Traditional Martial Arts",
      height: "170 cm (5'7\")",
      weight: "54 kg (119 lbs)",
      age: "43 (Preserved)",
      blood_type: "AB",
      status: "Wildlife Conservation Officer",
      archetype: "Defensive Keepout / Healing",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "Mother of Jin Kazama and bearer of ancient spiritual purification. Presumed lost following Ogre's attack years ago, Jun returns to forestall the catastrophic clash between father and son with compassionate yet formidable martial discipline.",
      pros: ["Self-healing mechanics using spiritual health expenditure", "Superior defensive parries and keepout strings", "Heavy damage from Izumo and Genjitsu stance flowcharts", "Safe mid launchers"],
      cons: ["Sacrifices recoverable health on special power moves", "Can be rushed down under continuous aggressive pacing"],
      ratings: { offense: 86, defense: 94, range: 90, execution: 78, movement: 82, throw: 80 },
      top5: [
        { cmd: "df+1", role: "Safe Mid Check", startup: "i13", block: "-3", dmg: 12, desc: "Safe mid poke with multiple followups and Izumo stance transitions" },
        { cmd: "b+3", role: "Evasive Hop Mid", startup: "i16", block: "-10", dmg: 20, desc: "Evades low attacks instantly; launches on Counter Hit and enters Genjitsu" },
        { cmd: "u+4", role: "Safe Can-Can Launcher", startup: "i15", block: "-13", dmg: 22, desc: "Premier mid launcher; low crushes on frame 9" },
        { cmd: "db+4, 4", role: "Low-High String", startup: "i20", block: "-12", dmg: 28, desc: "Deceptive low sweep into high roundhouse kick" },
        { cmd: "f+2", role: "Long Range Keepout", startup: "i17", block: "-7", dmg: 21, desc: "Safe mid thrust with immense range; absorbs spirit power" }
      ],
      gameplan: "Control distance with f+2 and b+3. Bait aggressive rushes into Jun parry (b+1+3). Enter Izumo stance to enforce low/mid mixups while regenerating gray health.",
      launcher: "u+4 (Mid Can-Can, i15, -13 OB) / Izumo 2",
      standing_punish: [
        { frame: "10f", move: "1, 2, 4", dmg: 28, adv: "+4" },
        { frame: "12f", move: "2, 1", dmg: 24, adv: "+6" },
        { frame: "14f", move: "f+1+2", dmg: 30, adv: "KND" },
        { frame: "15f", move: "u+4", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+3", dmg: 22, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 20, adv: "Launch" }
      ],
      whiff_punish: [
        { move: "f+2", startup: "i17", reach: "Long", dmg: 21, note: "Safest long-distance punish" },
        { move: "df+2, 1", startup: "i15", reach: "Medium", dmg: 28, note: "Knockdown punish" }
      ],
      stances: ["Izumo (IZM)", "Genjitsu (GEN)", "Matoi"],
      heat_breakdown: "Restores recoverable white health rapidly and empowers Genjitsu specials with purified spirit beams.",
      stage_synergy: "Great on infinite/hazard-free stages (Yakushima, Sanctum) where keepout and recovery dictate pace."
    },

    king: {
      name: "King",
      title: "The Beast Priest",
      japanese_name: "キング",
      country: "Mexico",
      country_flag: "🇲🇽",
      style: "Professional Wrestling / Lucha Libre",
      height: "200 cm (6'7\")",
      weight: "132 kg (291 lbs)",
      age: "30",
      blood_type: "A",
      status: "Pro Wrestler & Orphanage Caretaker",
      archetype: "Command Grappler",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The second-generation masked jaguar wrestler fighting to sustain the children of his orphanage. In Tekken 8, King steps into the ring with updated Lucha power, punishing opponent recklessness with brutal slams and aerial throws.",
      pros: ["Unmatched throw variety with true 3-way break tech mixups", "Unbreakable throws and armor tackles in Heat", "Giant Swing (i10 execution, 1 break with visual 1+2 disguise)", "Strong counter-hit mids and crouch dash mixups"],
      cons: ["Slower fundamental pokes", "Throw game can be ducked and heavily launched by knowledgeable players"],
      ratings: { offense: 94, defense: 88, range: 85, execution: 84, movement: 78, throw: 100 },
      top5: [
        { cmd: "f,b,db,d,df,f+1", role: "Giant Swing (1 Break)", startup: "i10", block: "Throw", dmg: 70, desc: "Legendary 10f command grab; 65-70 damage with wall splat capability" },
        { cmd: "f,f,f+2+4", role: "Shining Wizard (1+2 Break)", startup: "i15", block: "Throw", dmg: 45, desc: "Running knee into takedown slam; excellent oki and wall carry" },
        { cmd: "df+1", role: "Mid Check Poke", startup: "i12", block: "-1", dmg: 11, desc: "Fastest 12f mid check in the game; safe and halts ducking attempts" },
        { cmd: "df+2, 1", role: "CH Confirm Mid String", startup: "i15", block: "-6", dmg: 32, desc: "Normal hit knockdown and counter-hit combo starter" },
        { cmd: "d+3", role: "Low Harass Poke", startup: "i17", block: "-12", dmg: 14, desc: "Safe low kick that frustrates defensive blockers" }
      ],
      gameplan: "Use df+1 to freeze opponent standing guard. Buffer Giant Swing, Muscle Buster, and Tombstone. In Heat, activate armored running grabs to blow through incoming attacks.",
      launcher: "uf+4 (Hopkick, i15, -13 OB) / FC df+2",
      standing_punish: [
        { frame: "10f", move: "2, 1", dmg: 25, adv: "+6" },
        { frame: "12f", move: "b+1, 2", dmg: 28, adv: "KND" },
        { frame: "15f", move: "uf+4 (Hopkick)", dmg: 21, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "15f", move: "WS+1+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+1", startup: "i15", reach: "Long", dmg: 24, note: "Mid homing strike that forces crouch" },
        { move: "f,f,f+2+4", startup: "i15", reach: "Far", dmg: 45, note: "Running grab punish" }
      ],
      stances: ["Jaguar Step (JGS)", "Crouch Dash"],
      heat_breakdown: "Grants continuous Armor during command throw startups and upgrades Muscle Buster into an unbreakable takedown.",
      stage_synergy: "Monstrous on walled stages where Giant Swing wall splats deal up to 80+ damage."
    },

    paul: {
      name: "Paul Phoenix",
      title: "The Hot-Blooded Fighter",
      japanese_name: "ポール・フェニックス",
      country: "USA",
      country_flag: "🇺🇸",
      style: "Integrated Martial Arts based on Judo",
      height: "187 cm (6'2\")",
      weight: "91 kg (201 lbs)",
      age: "48",
      blood_type: "O",
      status: "Dojang Master & Veteran Fighter",
      archetype: "High Damage Brawler",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The self-proclaimed strongest fighter in the universe. Though plagued by bad luck and financial debt, Paul's thunderous fist can shatter walls, concrete, and tournament dreams in a single clean counter-hit blow.",
      pros: ["Absurd single-hit damage output with Deathfist (qcf+2)", "Feared Demolition Man low/mid mixup at close range", "Simple, devastating combo conversions with high floor damage", "Strong defensive keepout with safe pushback mids"],
      cons: ["Linear special moves prone to sidestepping", "Demolition Man requires clean hit to knock down"],
      ratings: { offense: 95, defense: 86, range: 82, execution: 75, movement: 80, throw: 82 },
      top5: [
        { cmd: "qcf+2", role: "Deathfist / Wall Splat", startup: "i15", block: "-17", dmg: 54, desc: "Iconic thunderous straight punch; massive damage with pushback" },
        { cmd: "d+4, 2:1+2", role: "Demolition Man", startup: "i15", block: "-17", dmg: 46, desc: "Close-range low sweep into mid knockdown; Paul's premier 50/50 weapon" },
        { cmd: "df+1", role: "Safe Mid Poke", startup: "i14", block: "-3", dmg: 13, desc: "Core mid check with sway and high-damage followups" },
        { cmd: "b+1, 2", role: "High-Damage Retaliator", startup: "i12", block: "-8", dmg: 32, desc: "Fast standing punish and safe interrupt" },
        { cmd: "uf+4", role: "Safe Hopkick Launcher", startup: "i15", block: "-13", dmg: 20, desc: "Jumping kick that evades low attacks and launches into full juggle" }
      ],
      gameplan: "Control spacing with df+1 and qcf+3. Once opponent respects your frames, close in for the 50/50: low Demolition Man or mid Deathfist.",
      launcher: "df+2 (Mid Launcher, i15, -8 OB, safe mid launcher!)",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "b+1, 2", dmg: 32, adv: "+2" },
        { frame: "14f", move: "b+3", dmg: 24, adv: "KND" },
        { frame: "15f", move: "df+2 or uf+4", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+3, 2", dmg: 28, adv: "KND" },
        { frame: "15f", move: "WS+2", dmg: 20, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "qcf+2 (Deathfist)", startup: "i15", reach: "Far", dmg: 54, note: "Devastating whiff punisher" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Safe mid juggle launch" }
      ],
      stances: ["Sway (qcb)", "Crouch Dash (qcf)"],
      heat_breakdown: "Grants maximum power to Deathfist, making it deal chip damage on block and wall-splatting from across the ring.",
      stage_synergy: "Deadly on walled arenas like Arena and Underground where Deathfist crushes opponents into splats."
    },

    hwoarang: {
      name: "Hwoarang",
      title: "Blood Talon",
      japanese_name: "ファラン",
      country: "South Korea",
      country_flag: "🇰🇷",
      style: "Taekwondo",
      height: "181 cm (5'11\")",
      weight: "71 kg (157 lbs)",
      age: "21",
      blood_type: "O",
      status: "Leader of Korean Resistance Gang",
      archetype: "Multi-Stance Pressure / Rushdown",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "Baek Doo San's premier student and Jin Kazama's fiercest rival. Fueled by pride and unrelenting ambition, Hwoarang commands fluid, unbroken kicks transitioning between four distinct stances that overwhelm opponent guard.",
      pros: ["Relentless plus-frame string pressure", "Four multi-layered stances (LFF, RFF, LFS, RFS)", "Unseeable low d3,4 sweep into stance vortex", "Deadly counter-hit Peacekeeper (f,f+4)"],
      cons: ["Stance transitions can be ducked or interrupted by observant foes", "Steep learning curve with intricate mental flowchart demands"],
      ratings: { offense: 98, defense: 80, range: 88, execution: 94, movement: 86, throw: 76 },
      top5: [
        { cmd: "d+3, 4", role: "Stance Starter Low-High", startup: "i16", block: "-12", dmg: 28, desc: "Cornerstone low harassment that transitions into Right Flamingo at +14" },
        { cmd: "f,f+4", role: "Peacekeeper / Keepout", startup: "i16", block: "-8", dmg: 24, desc: "Long-range mid kick that knocks back and launches on Counter Hit" },
        { cmd: "b+1", role: "Fast Safe Check", startup: "i12", block: "-7", dmg: 16, desc: "Fast standing 12f check with pushback" },
        { cmd: "1, 2", role: "Standard Jab String", startup: "i10", block: "+1", dmg: 17, desc: "High plus-frame jab leading into Flamingo stance" },
        { cmd: "RFF 2, 4~f", role: "Pressure Loop", startup: "i12", block: "+4", dmg: 32, desc: "Plus on block mid/high transition that keeps opponents pinned" }
      ],
      gameplan: "Initiate offensive momentum with d+3,4 into Right Flamingo. Cycle low and mid pokes to keep opponents guessing. Catch retaliations with f,f+4.",
      launcher: "df+2 (Safe Mid Launcher, i15, -8 OB)",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 17, adv: "+7" },
        { frame: "12f", move: "4, 3", dmg: 28, adv: "+4" },
        { frame: "14f", move: "f+1+2", dmg: 26, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4, 4", dmg: 28, adv: "KND" },
        { frame: "15f", move: "WS+2, 3", dmg: 32, adv: "Launch" }
      ],
      whiff_punish: [
        { move: "f,f+4 (Peacekeeper)", startup: "i16", reach: "Far", dmg: 24, note: "Long-range mid strike" },
        { move: "b+3", startup: "i16", reach: "Far", dmg: 25, note: "High damage normal launcher" }
      ],
      stances: ["Left Flamingo (LFS)", "Right Flamingo (RFS)", "Right Foot Forward (RFF)"],
      heat_breakdown: "Enhances Flamingo transitions with chip damage and guarantees plus frames on all major kick enders.",
      stage_synergy: "Thrives in small-to-medium wall stages where Flamingo pressure traps foes against barriers."
    },

    alisa: {
      name: "Alisa Bosconovitch",
      title: "The Destroying Automaton",
      japanese_name: "アリサ・ボスコノビッチ",
      country: "Russia",
      country_flag: "🇷🇺",
      style: "High-Mobility Thruster & Chainsaw Warfare",
      height: "168 cm (5'6\")",
      weight: "Mechanical (Classified)",
      age: "Cyborg",
      blood_type: "None",
      status: "Dr. Bosconovitch Creation",
      archetype: "Mobile Poke / Chainsaw Stance",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "An android engineered by Dr. Geppetto Bosconovitch in the likeness of his deceased daughter. Combining gentle humanity with devastating thruster engines and deployable arm chainsaws, Alisa serves as Lars Alexandersson's most faithful guardian.",
      pros: ["Exceptional lateral movement and backdash evasion", "Destructive Form chainsaws with relentless chip damage and plus frames", "Superb keepout with b+4 and f+4 rockets", "Great beginner-friendly fundamentals"],
      cons: ["Low defense during chainsaw transitions", "Predictable linear approach options"],
      ratings: { offense: 90, defense: 92, range: 92, execution: 74, movement: 96, throw: 75 },
      top5: [
        { cmd: "d+3", role: "Low Poke Harass", startup: "i16", block: "-12", dmg: 14, desc: "Fast, evasive low kick that leaves Alisa in full crouch with frame advantage" },
        { cmd: "b+4", role: "Keepout Mid", startup: "i16", block: "-6", dmg: 21, desc: "Safe mid kick with immense reach; stops aggressive forward dashes" },
        { cmd: "df+1", role: "Standard Mid Check", startup: "i13", block: "-2", dmg: 12, desc: "Safe mid poke with tracking to her weak side" },
        { cmd: "1+2 (DES)", role: "Destructive Form Stance", startup: "i14", block: "N/A", dmg: 0, desc: "Deploys chainsaws, turning every poke into chip-damaging plus frames" },
        { cmd: "f,f+3, 4", role: "Long Range Gap Closer", startup: "i17", block: "-10", dmg: 32, desc: "Thruster leap into mid strike; excellent whiff punisher" }
      ],
      gameplan: "Out-space opponents with backdashing and b+4 keepout. Once they whiff, punish with f,f+3,4. Deploy chainsaws (DES) to enforce relentless plus-frame block pressure.",
      launcher: "uf+4, 4 (Hopkick, i15, -13 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 1", dmg: 19, adv: "+6" },
        { frame: "12f", move: "2, 4", dmg: 28, adv: "+2" },
        { frame: "14f", move: "f+3, 2", dmg: 29, adv: "KND" },
        { frame: "15f", move: "uf+4, 4", dmg: 24, adv: "Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 24, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 20, adv: "Launch" }
      ],
      whiff_punish: [
        { move: "f,f+3, 4", startup: "i17", reach: "Far", dmg: 32, note: "Long range rocket dash" },
        { move: "b+4", startup: "i16", reach: "Far", dmg: 21, note: "Safe mid keepout" }
      ],
      stances: ["Destructive Form (DES)", "Dual Boot (DBO)", "Backup (BKU)"],
      heat_breakdown: "Chainsaw strikes do not consume gauge on block and inflict maximum guard damage.",
      stage_synergy: "Excels on expansive, open stages (Yakushima, Sanctum) where her top-tier movement shines."
    },

    asuka: {
      name: "Asuka Kazama",
      title: "The Spirited Peacemaker",
      japanese_name: "風間 飛鳥",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Kazama Style Traditional Martial Arts",
      height: "158 cm (5'2\")",
      weight: "49 kg (108 lbs)",
      age: "17",
      blood_type: "O",
      status: "High School Vigilante",
      archetype: "Defensive Counter / Whiff Punisher",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "Osaka's fiery peacemaker and Jin Kazama's cousin. Driven by an innate sense of justice, Asuka steps into the King of Iron Fist Tournament to reprimand the warmongers destabilizing Osaka and restore order to the family name.",
      pros: ["Best mid/high universal reversal parry (b+1+3)", "Exceptional whiff punishing with safe f+2 launcher", "Strong keepout with b+3 and db+3", "High comeback potential with Naniwa Gusto"],
      cons: ["Worst 10f standing punish in the game (1 jab is only +1, no good 10f knockdown)", "Weak against heavy low pressure"],
      ratings: { offense: 82, defense: 95, range: 88, execution: 72, movement: 84, throw: 82 },
      top5: [
        { cmd: "f+2", role: "Long Range Whiff Launcher", startup: "i17", block: "-8", dmg: 20, desc: "Safe mid lunging punch; one of the best whiff punishers in Tekken" },
        { cmd: "b+3", role: "Evasive Low-Crush Keepout", startup: "i16", block: "-19", dmg: 22, desc: "Backwards cartwheel kick; evades attacks and launches on hit" },
        { cmd: "b+1+3", role: "Universal Reversal Parry", startup: "i3", block: "Parry", dmg: 35, desc: "Catches enemy punches and kicks, throwing them overhead for heavy damage" },
        { cmd: "db+3", role: "High-Crush Low Poke", startup: "i21", block: "-12", dmg: 16, desc: "Safe low poke that ducks highs and leaves Asuka at +4" },
        { cmd: "df+1", role: "Mid Check", startup: "i13", block: "-3", dmg: 12, desc: "Standard mid poke to keep opponents honest" }
      ],
      gameplan: "Bait opponents into overextending, then punish with f+2 or b+1+3 reversal. Use db+3 to break defensive turtles and build Naniwa Gusto charges.",
      launcher: "f+2 (Safe Mid Launcher, i17, -8 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 2, 4", dmg: 28, adv: "+4" },
        { frame: "12f", move: "2, 3", dmg: 27, adv: "+3" },
        { frame: "14f", move: "f+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1, 4", dmg: 28, adv: "KND" },
        { frame: "15f", move: "WS+3", dmg: 22, adv: "Launch" }
      ],
      whiff_punish: [
        { move: "f+2", startup: "i17", reach: "Far", dmg: 20, note: "Premier safe launcher" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 21, note: "Fast mid launcher" }
      ],
      stances: ["Naniwa Gusto (Power Charge)", "Leg Cutter Transitions"],
      heat_breakdown: "Fully charges Naniwa Gusto automatically, empowering her mid strikes with crushing frame advantage.",
      stage_synergy: "Strong on open stages where her backdash and whiff punishing control the match."
    },

    azucena: {
      name: "Azucena Milagros",
      title: "The Perfect Blend / Coffee Queen",
      japanese_name: "アズセナ",
      country: "Peru",
      country_flag: "🇵🇪",
      style: "Rumi Maki (Indigenous Boxing) + Breakdance",
      height: "168 cm (5'6\")",
      weight: "55 kg (121 lbs)",
      age: "23",
      blood_type: "B",
      status: "Ortiz Farm Coffee Heiress",
      archetype: "Auto-Evade Stance Rushdown",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The energetic heiress of Peru's Ortiz Farm coffee plantation. Combining traditional Andean Rumi Maki boxing with infectious breakdance rhythms, Azucena enters the tournament to showcase Ortiz Farm beans to the global fighting stage.",
      pros: ["Libertador stance with built-in auto-evasion against highs and lows", "Devastating running 3,2 gap closer with massive plus frames", "Superb wall carry and corner mixups", "High mental pressure with taunting stances"],
      cons: ["Linear running tools can be sidestepped to SSR", "Vulnerable to well-timed mids while dancing in Libertador"],
      ratings: { offense: 96, defense: 84, range: 86, execution: 78, movement: 90, throw: 74 },
      top5: [
        { cmd: "f,f,f+3, 2", role: "Plus-Frame Running Mid", startup: "i15", block: "+4", dmg: 30, desc: "Premier approach tool; forces opponent to block and respect followups" },
        { cmd: "1+2 (LIB)", role: "Libertador Stance", startup: "i12", block: "N/A", dmg: 0, desc: "Auto-evades enemy highs and lows, countering with instant juggles" },
        { cmd: "df+1, 4", role: "Mid-High Check", startup: "i13", block: "-4", dmg: 24, desc: "Quick mid poke with delayable second hit" },
        { cmd: "db+3", role: "Low Harass", startup: "i20", block: "-12", dmg: 16, desc: "Safe low strike that transitions into Libertador at +5" },
        { cmd: "1, 2", role: "Standard Jab String", startup: "i10", block: "+1", dmg: 17, desc: "Fast 10f jab leading directly into Libertador dances" }
      ],
      gameplan: "Charge in with f,f,f+3,2 to establish plus frames. Transition into Libertador stance to bait desperate counter-attacks, auto-evade them, and launch into full juggles.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / LIB 2",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 17, adv: "+7" },
        { frame: "12f", move: "2, 3", dmg: 26, adv: "+4" },
        { frame: "14f", move: "f+1+2", dmg: 28, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 21, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f,f+3, 2", startup: "i15", reach: "Far", dmg: 30, note: "Fastest gap-closing punisher" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Standard mid launch" }
      ],
      stances: ["Libertador (LIB)"],
      heat_breakdown: "Libertador auto-dodges become active immediately and grant guaranteed free launchers on successful evasion.",
      stage_synergy: "Outstanding on Ortiz Farm and Arena where her running tools pin defenders against walls."
    },

    bryan: {
      name: "Bryan Fury",
      title: "The Harbinger of Chaos",
      japanese_name: "ブライアン・フューリー",
      country: "USA",
      country_flag: "🇺🇸",
      style: "Kickboxing / Cybernetic Violence",
      height: "186 cm (6'1\")",
      weight: "89 kg (196 lbs)",
      age: "31 (Cyborg)",
      blood_type: "B",
      status: "Autonomous Destructive Weapon",
      archetype: "Counter-Hit Specialist / Keepout",
      difficulty: "Master ★★★★★",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "A former police detective reanimated with a perpetual energy generator by Dr. Abel. Bryan thrives entirely on carnage and battle frenzy, wielding cybernetic kickboxing strikes that turn opponent mistakes into catastrophic counter-hit explosions.",
      pros: ["Highest counter-hit damage in Tekken (3+4, b+1, f+3, Hatchet Kick)", "Legendary Taunt Jet Upper unblockable setups", "Superior wall travel and brutal splat damage", "Dominant keepout presence with orbital heels"],
      cons: ["Requires deep counter-hit timing and patient defensive reading", "Lacks a generic 15f normal-hit mid launcher (relies on uf+4 or high Jet Upper)"],
      ratings: { offense: 94, defense: 92, range: 90, execution: 96, movement: 82, throw: 74 },
      top5: [
        { cmd: "3+4", role: "Long Range Keepout", startup: "i18", block: "-13", dmg: 26, desc: "Huge pushback mid kick; crumples on Counter Hit for 80+ damage combo" },
        { cmd: "b+1", role: "Plus-Frame Fist", startup: "i20", block: "+4", dmg: 24, desc: "Overhead fist; +4 on block with massive frame trap potential" },
        { cmd: "qcb+3", role: "Hatchet Kick", startup: "i19", block: "-13", dmg: 23, desc: "Crushing low sweep that leaves Bryan at +5 on hit" },
        { cmd: "f,b+2", role: "Jet Upper Launcher", startup: "i14", block: "-7", dmg: 22, desc: "14f high launcher; legendary whiff punisher and Taunt follow-up" },
        { cmd: "uf+4", role: "Orbital Heel", startup: "i24", block: "-5", dmg: 20, desc: "Safe mid jumping launcher that completely crushes incoming low attacks" }
      ],
      gameplan: "Frustrate opponent approach with 3+4 and orbital heel (uf+4). Enforce b+1 and Hatchet Kick (qcb+3). Catch eager retaliations with f+3 and counter-hit launchers.",
      launcher: "f,b+2 (Jet Upper, i14, -7 OB, High) / uf+4 (Orbital Heel, i24, -5 OB, Mid)",
      standing_punish: [
        { frame: "10f", move: "1, 4", dmg: 20, adv: "+5" },
        { frame: "12f", move: "2, 3", dmg: 26, adv: "+3" },
        { frame: "14f", move: "f,b+2 (Jet Upper)", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+3", dmg: 24, adv: "+6" },
        { frame: "15f", move: "WS+1", dmg: 20, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,b+2 (Jet Upper)", startup: "i14", reach: "Far", dmg: 22, note: "One of the best whiff punishers" },
        { move: "3+4", startup: "i18", reach: "Extreme", dmg: 26, note: "Long range keepout check" }
      ],
      stances: ["Snake Edge Transitions", "Taunt (1+3+4)"],
      heat_breakdown: "Armors up his cybernetic generator, adding guard break properties to b+1 and enhancing all Snake Edge extensions.",
      stage_synergy: "Deadly on all Walled stages where Taunt cancel setups at the wall guarantee round-ending damage."
    },

    claudio: {
      name: "Claudio Serafino",
      title: "The Purifier of Shadows",
      japanese_name: "クラウディオ・セラフィーノ",
      country: "Italy",
      country_flag: "🇮🇹",
      style: "Sirius Style Exorcism Sorcery",
      height: "182 cm (6'0\")",
      weight: "77 kg (170 lbs)",
      age: "33",
      blood_type: "AB",
      status: "Archers of Sirius Leader",
      archetype: "Mid-Range Starburst / Poke",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The debonair head of the Archers of Sirius, an ancient secret society of exorcists. Using celestial blue flames known as Starburst, Claudio manipulates the conflict between the Mishimas to purge demonic corruption from the mortal realm.",
      pros: ["Best hopkick in Tekken (uf+4, high-crushing, safe on block pushback)", "Empowered Starburst state unlocks devastating special moves", "Excellent fundamental Range 2 pokes with b+1 and f,f+4", "Straightforward, highly effective tournament gameplan"],
      cons: ["Limited low poke arsenal outside Starburst", "Linear key moves vulnerable to SSR"],
      ratings: { offense: 90, defense: 88, range: 92, execution: 70, movement: 84, throw: 76 },
      top5: [
        { cmd: "uf+4", role: "Signature Hopkick", startup: "i15", block: "-13", dmg: 20, desc: "Legendary hopkick with deceptive evasive hitbox and massive range" },
        { cmd: "b+1", role: "Long Range Mid Check", startup: "i18", block: "-5", dmg: 22, desc: "Homing mid thrust that knocks back and grants Starburst on hit" },
        { cmd: "f,f+4", role: "Running Mid Kick", startup: "i16", block: "+7", dmg: 25, desc: "Plus on block mid strike that sets up immediate frame traps" },
        { cmd: "db+3", role: "Low Check", startup: "i18", block: "-13", dmg: 14, desc: "Core low poke to annoy opponents blocking his mids" },
        { cmd: "STB d+2, 2", role: "Starburst Low Smasher", startup: "i20", block: "-14", dmg: 35, desc: "Empowered low sweep only accessible while in Starburst mode" }
      ],
      gameplan: "Dominate Range 2 with b+1 and f,f+4. Use uf+4 hopkick to crush low attempts. Once Starburst is activated, enforce heavy chip damage and unseeable low sweeps.",
      launcher: "uf+4 (Hopkick, i15, -13 OB) / df+1, 2",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "f+2, 2", dmg: 28, adv: "+4" },
        { frame: "15f", move: "uf+4 (Hopkick)", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "uf+4", startup: "i15", reach: "Far", dmg: 20, note: "Premier hopkick whiff punisher" },
        { move: "b+1", startup: "i18", reach: "Long", dmg: 22, note: "Safe homing strike" }
      ],
      stances: ["Starburst (STB)"],
      heat_breakdown: "Maintains permanent Starburst charges for the duration of Heat, unlocking unlimited access to STB specials.",
      stage_synergy: "Outstanding on arena stages where b+1 and STB specials send opponents hurtling into walls."
    },

    "devil-jin": {
      name: "Devil Jin",
      title: "The Black Wings of Ruin",
      japanese_name: "デビル仁",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Advanced Kazama Style & Devil Genetic Mutation",
      height: "180 cm (5'11\")",
      weight: "75 kg (165 lbs)",
      age: "21",
      blood_type: "AB",
      status: "Corrupted Devil Host",
      archetype: "Mixup Vortex / Aerial Dominance",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "The demonic manifestation taking complete possession of Jin Kazama. Unburdened by human morality, Devil Jin wields corrupted Mishima karate, dark telekinesis, and razor-sharp obsidian wings to pulverize all opposition into ash.",
      pros: ["True unseeable knockdown Hellsweep (f,n,d,df+4,4)", "Electric Wind God Fist with superior vertical launch height", "Aerial flight mobility and unblockable lasers", "Devastating wall travel with Mourning Crow transitions"],
      cons: ["High execution barrier for consistent wavedash pressure", "Vulnerable to SSL sidewalk against laser pokes"],
      ratings: { offense: 96, defense: 88, range: 92, execution: 96, movement: 90, throw: 78 },
      top5: [
        { cmd: "f,n,d,df+2", role: "Electric Wind God Fist", startup: "i11", block: "+5", dmg: 23, desc: "Classic Mishima high launcher; plus on block with massive aerial combo potential" },
        { cmd: "f,n,d,df+4, 4", role: "Knockdown Hellsweep", startup: "i16", block: "-26", dmg: 32, desc: "Premier low launcher that knocks down and guarantees oki" },
        { cmd: "df+1, 2", role: "Mid Check String", startup: "i13", block: "-8", dmg: 22, desc: "Quick mid poke with delayable second hit to catch ducking" },
        { cmd: "f,f+4", role: "Safe Mid Ground Smasher", startup: "i17", block: "-4", dmg: 24, desc: "Mid axe kick that crushes lows and hits grounded opponents" },
        { cmd: "b+4", role: "Counter-Hit Kick", startup: "i17", block: "-8", dmg: 22, desc: "Safe mid strike that launches on Counter Hit" }
      ],
      gameplan: "Wavedash into opponent face to force the deadly 50/50: Hellsweep or mid axe kick (f,f+4). Keep approachers at bay with EWGF.",
      launcher: "EWGF (f,n,d,df+2, i11, +5 OB) / Mourning Crow 2",
      standing_punish: [
        { frame: "10f", move: "1, 1, 2", dmg: 25, adv: "KND" },
        { frame: "12f", move: "b+1, 2", dmg: 26, adv: "+4" },
        { frame: "14f", move: "EWGF", dmg: 23, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "EWGF", startup: "i11", reach: "Far", dmg: 23, note: "Premier whiff punisher" },
        { move: "f,f+2", startup: "i15", reach: "Long", dmg: 24, note: "Safe demon paw gap closer" }
      ],
      stances: ["Mourning Crow (MC)", "Flight (FLY)"],
      heat_breakdown: "Unlocks demonic wing blades, making Mourning Crow 2 plus on block and granting full-screen lasers.",
      stage_synergy: "Thrives in Walled arenas where Hellsweep wall conversions finish rounds in two interactions."
    },

    dragunov: {
      name: "Sergei Dragunov",
      title: "The White Reaper",
      japanese_name: "セルゲイ・ドラグノフ",
      country: "Russia",
      country_flag: "🇷🇺",
      style: "Combat Sambo",
      height: "190 cm (6'3\")",
      weight: "88 kg (194 lbs)",
      age: "26",
      blood_type: "Unknown",
      status: "Spetsnaz Elite Field Commander",
      archetype: "Plus-Frame Pressure / Grapple",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "A mute military commander known across international battlefields as 'The White Reaper'. Dragunov utilizes cold, surgical Combat Sambo strikes and ground submissions to eliminate targets with merciless mechanical efficiency.",
      pros: ["Oppressive plus frames with running 2 (f,f,f+2)", "Superior Sneak stance transitions with guard breaks", "Dominant low harassment with d+2 high-crush", "Formidable command grabs (Blizzard Hammer, Reverse Arm Bar)"],
      cons: ["Linear running moves vulnerable to sharp SSR sidewalk", "Average standing punishment outside 10f"],
      ratings: { offense: 98, defense: 88, range: 90, execution: 76, movement: 86, throw: 90 },
      top5: [
        { cmd: "f,f,f+2", role: "Running Plus-Frame Strike", startup: "i15", block: "+6", dmg: 26, desc: "Iconic Russian Assault; forces crouch at +6 on block for immense pressure" },
        { cmd: "d+2", role: "High-Crush Low Poke", startup: "i18", block: "-13", dmg: 17, desc: "High-crushing low punch; forces opponent into crouch at -1" },
        { cmd: "df+1", role: "Mid Check", startup: "i13", block: "-2", dmg: 13, desc: "Fast mid poke with extensions that halt ducking" },
        { cmd: "qcf+4", role: "Sneak Mid Launcher", startup: "i16", block: "-8", dmg: 22, desc: "Safe mid kick that launches on Counter Hit and wall-splats" },
        { cmd: "b+4, 3", role: "Hit-Confirm Knee", startup: "i15", block: "-9", dmg: 30, desc: "Safe mid-high string that knocks down into ground oki" }
      ],
      gameplan: "Charge in with f,f,f+2 to claim +6 on block. Mix between low d+2, command grabs, and mid df+1. Use Sneak cancels to sustain relentless offense.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / qcf+2",
      standing_punish: [
        { frame: "10f", move: "1, 3", dmg: 21, adv: "+7" },
        { frame: "12f", move: "4, 1", dmg: 26, adv: "+4" },
        { frame: "14f", move: "f+1+2", dmg: 28, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "12f", move: "WS+1, 3", dmg: 26, adv: "+6" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f,f+2", startup: "i15", reach: "Far", dmg: 26, note: "Approaching whiff punisher" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Standard mid launch" }
      ],
      stances: ["Sneak (SNK / qcf)"],
      heat_breakdown: "Enters Tactical Overdrive. Enhances f,f,f+2 into a crushing wall splat and guarantees Sneak 4 guard break.",
      stage_synergy: "Deadly on all Walled stages where Russian Assault pins defenders into inescapable corner sequences."
    },

    feng: {
      name: "Feng Wei",
      title: "The God of Fist",
      japanese_name: "フェン・ウェイ",
      country: "China",
      country_flag: "🇨🇳",
      style: "God Fist Style Chinese Kempo",
      height: "185 cm (6'1\")",
      weight: "85 kg (187 lbs)",
      age: "26",
      blood_type: "AB",
      status: "Wandering Martial Arts Master",
      archetype: "Evasive Stance / Poking Master",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SWR (Walk Right)",
      lore: "A relentless martial artist whose insatiable quest for supreme strength drove him to murder his master and steal the God Fist scrolls. Armed with elusive Kempo stances, Feng Wei shatters enemy guards with surgical precision.",
      pros: ["Best evasive toolkit in the game (Kenpo Step, Shifting Clouds parry)", "Unmatched poke variety with safe frame data", "Fast 10f shoulder counter-hit punisher (b+1+2)", "High damage backturned mixups"],
      cons: ["Relatively short forward reach on standard jabs", "Slightly below-average combo damage from basic launchers"],
      ratings: { offense: 94, defense: 96, range: 82, execution: 76, movement: 92, throw: 82 },
      top5: [
        { cmd: "b+1", role: "Fast Counter-Hit Check", startup: "i10", block: "-12", dmg: 18, desc: "Fastest 10f counter-hit weapon in the game; crumples on CH for full juggle" },
        { cmd: "df+1", role: "Safe Mid Poke", startup: "i14", block: "0", dmg: 14, desc: "Neutral 0 on block mid check; allows Feng to immediately steal turns" },
        { cmd: "db+3", role: "High-Crush Low Sweep", startup: "i16", block: "-15", dmg: 17, desc: "Crushes highs instantly, hits low and leaves Feng at +4 on hit" },
        { cmd: "b+1+2", role: "Shoulder Punish", startup: "i13", block: "-19", dmg: 34, desc: "13f standing punisher and panic interrupt with massive knockdown" },
        { cmd: "f+3, 4", role: "Safe Mid String", startup: "i18", block: "-6", dmg: 32, desc: "Mid-mid string that catches sidestepping and wallsplats" }
      ],
      gameplan: "Weave in and out of range with Kenpo Step (b+3+4). Stop aggression with b+1 and b+1+2. Enforce db+3 lows and transition into backturned stances.",
      launcher: "f+1+2 (Mid Launcher, i15, -13 OB) / WS+3",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 19, adv: "+6" },
        { frame: "13f", move: "b+1+2 (Shoulder)", dmg: 34, adv: "KND" },
        { frame: "15f", move: "f+1+2", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 21, adv: "+7" },
        { frame: "15f", move: "WS+3", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f+1+2", startup: "i15", reach: "Medium", dmg: 22, note: "Standard mid launch" },
        { move: "f,f+3", startup: "i18", reach: "Long", dmg: 24, note: "Long range downward axe kick" }
      ],
      stances: ["Kenpo Step (KNP)", "Shifting Clouds (STC)", "Backturned (BT)"],
      heat_breakdown: "Empowers Kenpo strikes with guard breaks and allows automatic parry followups in Shifting Clouds.",
      stage_synergy: "Excels across all stage types thanks to flexible evasion and crushing wall splats."
    },

    "jack-8": {
      name: "Jack-8",
      title: "The Absolute Heavy Armament",
      japanese_name: "ジャック8",
      country: "Global (G-Corp)",
      country_flag: "🌐",
      style: "Military Brutal Force / Exoskeleton Combat",
      height: "235 cm (7'8\")",
      weight: "285 kg (628 lbs)",
      age: "0 (Model 8)",
      blood_type: "Synthetic Oil",
      status: "G-Corporation Assault Droid",
      archetype: "Heavy Keepout / Range Punisher",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "The latest iteration of G Corporation's terrifying humanoid tank. Engineered by Jane with an integrated energy railgun, high-density titanium chassis, and enhanced flight thrusters, Jack-8 levels entire city blocks on command.",
      pros: ["Absurd reach on long-range pokes (df+2, f+2, db+1)", "Formidable low harassment with db+1 and Megaton sweep", "High damage output from Gamma Howl stance", "Heavy block pushback on core tools"],
      cons: ["Large hurtbox susceptible to character-specific big-body juggles", "Weak sidestep mobility due to massive frame"],
      ratings: { offense: 90, defense: 86, range: 98, execution: 72, movement: 65, throw: 88 },
      top5: [
        { cmd: "df+2", role: "Long Range Mid Launcher", startup: "i15", block: "-14", dmg: 21, desc: "Premier mid launcher with the longest reach in the game" },
        { cmd: "db+1", role: "Low Machinegun Harass", startup: "i12", block: "-12", dmg: 14, desc: "Fastest low poke in Tekken; high crushes and chips at opponent feet" },
        { cmd: "f+2", role: "Heavy Mid Straight", startup: "i15", block: "-11", dmg: 26, desc: "Massive reach straight punch that knocks back and wallsplats" },
        { cmd: "b+1", role: "Mid Check", startup: "i14", block: "-4", dmg: 16, desc: "Safe mid check with Gamma Howl stance transition" },
        { cmd: "f,f+1", role: "Piston Punch", startup: "i15", block: "-12", dmg: 28, desc: "Forward lunging punch that causes heavy knockdown" }
      ],
      gameplan: "Keep opponents at Range 2.5 with df+2 and f+2. Chip away with low db+1. When opponents rush in, blow through them with Gamma Howl armor.",
      launcher: "df+2 (Mid Launcher, i15, -14 OB, Extreme Range)",
      standing_punish: [
        { frame: "10f", move: "2, 1", dmg: 22, adv: "+6" },
        { frame: "12f", move: "f+1, 2", dmg: 28, adv: "+4" },
        { frame: "15f", move: "df+2", dmg: 21, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 24, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "df+2", startup: "i15", reach: "Extreme", dmg: 21, note: "Longest normal mid launcher" },
        { move: "f+2", startup: "i15", reach: "Far", dmg: 26, note: "Heavy straight punch" }
      ],
      stances: ["Gamma Howl (GMH)", "Sit Down"],
      heat_breakdown: "Deploys railgun thrusters, turning Gamma Howl into an armored full-screen beam launcher.",
      stage_synergy: "Monstrous on wall stages where f+2 and piston punches wall-splat from half-screen."
    },

    lars: {
      name: "Lars Alexandersson",
      title: "The Iron Lion of Yggdrasil",
      japanese_name: "ラース・アレクサンダーソン",
      country: "Sweden",
      country_flag: "🇸🇪",
      style: "Tekken Forces Martial Arts",
      height: "183 cm (6'0\")",
      weight: "77 kg (170 lbs)",
      age: "28",
      blood_type: "AB",
      status: "Yggdrasil Resistance Commander",
      archetype: "High-Speed Stance Transition / Carry",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The illegitimate son of Heihachi Mishima and charismatic leader of the rebel faction Yggdrasil. Armed with lightning-infused military combat and dynamic dash transitions, Lars fights alongside Jin Kazama to save humanity from global destruction.",
      pros: ["Best corner-to-corner wall carry in Tekken 8", "High-speed stance flowcharts (Dynamic Entry, Silent Entry, Limited Entry)", "Devastating plus-frame Heat Smash", "Extremely evasive ducking entries"],
      cons: ["Stance mixups can be interrupted with well-timed generic jabs", "Lacks an unseeable knockdown low from standing neutral"],
      ratings: { offense: 94, defense: 86, range: 88, execution: 80, movement: 94, throw: 76 },
      top5: [
        { cmd: "f,f+2", role: "Approaching Stance Starter", startup: "i15", block: "-9", dmg: 20, desc: "Fast mid thrust that seamlessly enters Silent Entry with advantage" },
        { cmd: "df+1", role: "Safe Mid Poke", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid check with Dynamic Entry transitions" },
        { cmd: "db+1, 3", role: "Low-High String", startup: "i17", block: "-12", dmg: 26, desc: "High-crushing low poke into guaranteed high follow-up" },
        { cmd: "b+4", role: "Counter-Hit Knee", startup: "i15", block: "-8", dmg: 21, desc: "Safe mid knee that launches into full combo on Counter Hit" },
        { cmd: "fb+2, 1", role: "Heavy Punisher", startup: "i14", block: "-10", dmg: 32, desc: "14f standing punisher with high knockdown pushback" }
      ],
      gameplan: "Initiate momentum with f,f+2 and df+1. Transition into Silent Entry (SEN) to enforce mid launchers or low slides. Carry opponents to the nearest wall for massive splats.",
      launcher: "uf+4 (Hopkick, i15, -13 OB) / df+2, 1",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "2, 3", dmg: 27, adv: "+4" },
        { frame: "14f", move: "fb+2, 1", dmg: 32, adv: "KND" },
        { frame: "15f", move: "uf+4 (Hopkick)", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "15f", move: "WS+1", dmg: 21, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 20, note: "Long range dash thrust" },
        { move: "uf+4", startup: "i15", reach: "Medium", dmg: 20, note: "Standard hopkick" }
      ],
      stances: ["Dynamic Entry (DEN)", "Silent Entry (SEN)", "Limited Entry (LEN)"],
      heat_breakdown: "Grants continuous electric charge to all stance transitions, unlocking Limited Entry 2 guard crush.",
      stage_synergy: "Excels on large wall stages (Urban Square, Arena) where his wall carry delivers free corner conversions."
    },

    law: {
      name: "Marshall Law",
      title: "The Legendary Dragon",
      japanese_name: "マーシャル・ロウ",
      country: "USA",
      country_flag: "🇺🇸",
      style: "Martial Arts (Jeet Kune Do)",
      height: "179 cm (5'10\")",
      weight: "69 kg (152 lbs)",
      age: "48",
      blood_type: "B",
      status: "Marshall Dojo Master & Chef",
      archetype: "DSS Stance Pressure / Counter-Hit",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The legendary kung-fu restaurateur fighting to clear his son Forest's financial debts. In Tekken 8, Law's signature Dragon Sign Stance (DSS) has been streamlined, letting him unleash rapid-fire nunchaku strikes and acrobatic somersaults with blazing speed.",
      pros: ["Dominant close-range counter-hit fishing (magic 4, 3+4, b+4)", "DSS stance transitions now grant seamless plus frames and guard breaks", "Legendary slide mixup (FC df,d,df+3) with guaranteed followups", "High damage nunchaku Heat specials"],
      cons: ["Linear approach tools vulnerable to SSR", "Short reach on standard pokes outside nunchaku range"],
      ratings: { offense: 96, defense: 84, range: 82, execution: 88, movement: 88, throw: 82 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Premier mid check poke that cancels directly into DSS" },
        { cmd: "b+4", role: "Counter-Hit Knee", startup: "i15", block: "-7", dmg: 22, desc: "Safe mid knee that crumple-launches on Counter Hit" },
        { cmd: "FC df,d,df+3", role: "Dragon Slide", startup: "i18", block: "-23", dmg: 25, desc: "Unseeable low slide from crouch with guaranteed followups" },
        { cmd: "3+4", role: "Acrobic Somersault Launcher", startup: "i14", block: "-16", dmg: 28, desc: "Lightning-fast 14f mid launcher that crushes lows" },
        { cmd: "DSS f+1", role: "Dragon Sign Guard Break", startup: "i15", block: "+6", dmg: 26, desc: "Plus on block mid strike from DSS stance" }
      ],
      gameplan: "Pressure opponents at Range 0-1 with df+1 into DSS cancels. Condition them to stand with b+4, then slide under guard with FC df,d,df+3.",
      launcher: "df+2 (Safe Mid Launcher, i15, -7 OB) / 3+4",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "3+4", dmg: 28, adv: "Launch" },
        { frame: "14f", move: "f+2~1", dmg: 28, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 24, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "3+4", startup: "i14", reach: "Medium", dmg: 28, note: "Fastest somersault launcher" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Safe mid launch" }
      ],
      stances: ["Dragon Sign Stance (DSS)", "Dragon Charge"],
      heat_breakdown: "Empowers nunchaku attacks with impenetrable guard damage and makes DSS cancels instant.",
      stage_synergy: "Excels on wall stages where DSS extensions slam opponents into corners."
    },

    lee: {
      name: "Lee Chaolan",
      title: "The Silver Demon",
      japanese_name: "李 超狼",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Martial Arts & Violet Systems Gadgetry",
      height: "178 cm (5'10\")",
      weight: "67 kg (148 lbs)",
      age: "48",
      blood_type: "A",
      status: "Violet Systems CEO",
      archetype: "Just-Frame Counter-Hit / Keepout",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "The silver-haired prodigy and adopted son of Heihachi Mishima. Under his heroic alter-ego 'Violet', Lee leverages Violet Systems military exosuits to support Jin's resistance army while dispatching foes with 'Excellent' elegance.",
      pros: ["Unmatched just-frame counter-hit tools (b+4, 4,4, df+4)", "Best magic 4 counter-hit launcher in the game", "Infinite Hitman stance evasion and cancel loops", "Extremely high wall carry and stylish combo routes"],
      cons: ["Highest just-frame execution requirement across many core strings", "Weak low damage from standard standing neutral"],
      ratings: { offense: 90, defense: 95, range: 90, execution: 98, movement: 92, throw: 74 },
      top5: [
        { cmd: "b+4", role: "Premier Keepout Mid", startup: "i16", block: "-3", dmg: 22, desc: "Safe mid kick with huge pushback; launches on Counter Hit into full juggle" },
        { cmd: "4, 4:4", role: "Acid Rain Just-Frame", startup: "i10", block: "-10", dmg: 38, desc: "Legendary 10f just-frame standing punish that guarantees full combo" },
        { cmd: "df+1", role: "Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid poke with Hitman stance cancel" },
        { cmd: "d+3", role: "High-Crush Low Poke", startup: "i16", block: "-15", dmg: 15, desc: "High-crushing low kick with just-frame followup for Counter Hit launch" },
        { cmd: "f,f+3", role: "Long Range Approach", startup: "i20", block: "+2", dmg: 24, desc: "Plus on block mid axe kick that enforces frame traps" }
      ],
      gameplan: "Out-space opponents with b+4 and Hitman stance steps. Punish ducking with f,f+3. Punish standing errors with 10f Acid Rain into 'Excellent' combo conversions.",
      launcher: "df+2 (Safe Mid Launcher, i15, -7 OB) / uf+4",
      standing_punish: [
        { frame: "10f", move: "4, 4:4 (Acid Rain)", dmg: 38, adv: "Full Launch" },
        { frame: "12f", move: "4, 3", dmg: 26, adv: "+4" },
        { frame: "14f", move: "f+2, 1", dmg: 28, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "10f", move: "WS+3, 3", dmg: 24, adv: "+4" },
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+2, 3", dmg: 32, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+3", startup: "i20", reach: "Far", dmg: 24, note: "Approaching mid strike" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Safe mid launch" }
      ],
      stances: ["Hitman Stance (HMS)", "Mist Step (MS)"],
      heat_breakdown: "Simplifies just-frame execution to automatic timings and empowers Hitman strikes with blazing silver fire.",
      stage_synergy: "Dominates large arenas where Mist Step wall carries travel across the entire battlefield."
    },

    leo: {
      name: "Leo Kliesen",
      title: "The Seeker of Truth",
      japanese_name: "レオ・クリーゼン",
      country: "Germany",
      country_flag: "🇩🇪",
      style: "Baji Quan (Eight Extremities Fist)",
      height: "175 cm (5'9\")",
      weight: "63 kg (139 lbs)",
      age: "19",
      blood_type: "AB",
      status: "Spelunker & G-Corp Investigator",
      archetype: "Compact Mid Poke / Bökken Stance",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "A skilled spelunker investigating the suspicious circumstances surrounding their mother Emma Kliesen's death at G Corporation. Armed with authentic Chinese Baji Quan elbow and shoulder strikes, Leo seeks truth and justice amidst global conflict.",
      pros: ["Exceptional close-range mid checks with df+1 and b+1,4", "Bökken (BOK) and Fo Bu (FOB) stances provide continuous low/mid 50/50s", "Top-tier standing and crouch punishment", "Strong wall travel and floor hazard conversions"],
      cons: ["Low poke damage is moderate outside stance sweeps", "Predictable linear entry routes"],
      ratings: { offense: 92, defense: 90, range: 84, execution: 78, movement: 86, throw: 80 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "One of the best mid pokes; only -1 on block with multiple followups" },
        { cmd: "b+1, 4", role: "Counter-Hit Elbow String", startup: "i14", block: "-12", dmg: 34, desc: "Natural combo on hit that knocks down and splats" },
        { cmd: "db+4, 1", role: "Low Sweep String", startup: "i20", block: "-12", dmg: 26, desc: "Deceptive low sweep into mid chop that leaves Leo at advantage" },
        { cmd: "f+4", role: "Stance Starter Mid", startup: "i15", block: "-4", dmg: 18, desc: "Mid kick that cancels directly into Fo Bu stance at +6" },
        { cmd: "d+2", role: "High-Crush Low Poke", startup: "i18", block: "-13", dmg: 17, desc: "High-crushing low elbow strike that leaves Leo in full crouch" }
      ],
      gameplan: "Control the neutral with df+1 and b+1,4. Use f+4 to enter Fo Bu stance and force 50/50 mixups between the low sweep and mid elbow launcher.",
      launcher: "df+2 (Mid Launcher, i15, -13 OB) / uf+4",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "f+2, 2", dmg: 28, adv: "+4" },
        { frame: "14f", move: "b+1, 4", dmg: 34, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 21, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+3", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2", startup: "i16", reach: "Far", dmg: 24, note: "Forward lunging elbow strike" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 21, note: "Standard mid launch" }
      ],
      stances: ["Bökken (BOK)", "Fo Bu (FOB)"],
      heat_breakdown: "Empowers Baji Quan elbow strikes with shockwave bursts, guaranteeing guard breaks in Bökken stance.",
      stage_synergy: "Excels on floor-break stages (Descent into Subconscious) where downward stomps trigger multi-level juggles."
    },

    leroy: {
      name: "Leroy Smith",
      title: "The Grandmaster of Drip",
      japanese_name: "リロイ・スミス",
      country: "USA",
      country_flag: "🇺🇸",
      style: "Wing Chun Kung Fu",
      height: "175 cm (5'9\")",
      weight: "72 kg (159 lbs)",
      age: "53",
      blood_type: "A",
      status: "New York Purifier & Dog Companion",
      archetype: "Defensive Parry / Hermit Stance",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "A New York native whose family fell victim to gang violence half a century ago. Having mastered Wing Chun in Hong Kong alongside his loyal pitbull Sugar, Leroy returns to purge corporate syndicates from his hometown with unwavering style.",
      pros: ["Incredible universal Wing Chun auto-parry (b+1+2)", "Hermit stance auto-low parry with plus-frame punches", "One-time Sugar dog assist attack per match", "Safe, accessible punishment and counter-hit tools"],
      cons: ["Lower raw combo damage output compared to top brawlers", "Slower sidestep evasiveness"],
      ratings: { offense: 88, defense: 98, range: 84, execution: 70, movement: 82, throw: 82 },
      top5: [
        { cmd: "b+1+2", role: "Universal Wing Chun Parry", startup: "i3", block: "Parry", dmg: 24, desc: "Parries enemy high/mid attacks with guaranteed counter-punch" },
        { cmd: "df+1", role: "Safe Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid poke that cancels into Hermit stance" },
        { cmd: "db+3", role: "Low Harass", startup: "i16", block: "-13", dmg: 15, desc: "Safe low kick into Hermit stance at +4" },
        { cmd: "f,f+2, 2", role: "Long Range Punish", startup: "i15", block: "-9", dmg: 32, desc: "Double palm strike that wall splats from distance" },
        { cmd: "b+4", role: "Counter-Hit Mid", startup: "i16", block: "-7", dmg: 21, desc: "Safe mid kick that launches on Counter Hit" }
      ],
      gameplan: "Suffocate opponent offense with b+1+2 parries. Enter Hermit stance (HRM) using df+1 or db+3 to auto-parry low attacks and unleash rapid chain punches.",
      launcher: "uf+4 (Hopkick, i15, -13 OB) / HRM 2",
      standing_punish: [
        { frame: "10f", move: "1, 2, 4", dmg: 26, adv: "+4" },
        { frame: "12f", move: "2, 2", dmg: 26, adv: "+4" },
        { frame: "14f", move: "f+4, 4", dmg: 30, adv: "KND" },
        { frame: "15f", move: "uf+4 (Hopkick)", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 4", dmg: 28, adv: "KND" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2, 2", startup: "i15", reach: "Far", dmg: 32, note: "Long range double palm" },
        { move: "uf+4", startup: "i15", reach: "Medium", dmg: 20, note: "Standard hopkick" }
      ],
      stances: ["Hermit (HRM)"],
      heat_breakdown: "Empowers Wing Chun chain strikes with continuous chip damage and refreshes Sugar's summon ability.",
      stage_synergy: "Outstanding on arena stages where parry followups wall splat with ease."
    },

    lili: {
      name: "Lili (Emilie De Rochefort)",
      title: "The Radiant Aristocrat",
      japanese_name: "リリ",
      country: "Monaco",
      country_flag: "🇲🇨",
      style: "Self-Taught Gymnastics & Street Ballet",
      height: "173 cm (5'8\")",
      weight: "56 kg (123 lbs)",
      age: "17",
      blood_type: "A",
      status: "Rochefort Oil Co. Heiress",
      archetype: "Queen of Sidestep / Flowchart Mixup",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The pampered only daughter of a Monegasque oil magnate. Concealing her street fighting passions from her pacifist father, Lili wields graceful ballet acrobatics, high-flying cartwheels, and the single best sidestep in the entire Tekken roster.",
      pros: ["Best sidestep / lateral evasion in the entire game", "Matterhorn (d+3+4) high-crush launcher deals massive comeback damage", "Formidable Feisty Rabbit (RAB) and backturned mixups", "Long-range safe keepout with 3+4 and f+4"],
      cons: ["Matterhorn is -26 on block (launch punishable on read)", "Linear attacks can be stepped to SSR"],
      ratings: { offense: 92, defense: 96, range: 88, execution: 72, movement: 100, throw: 74 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Safe mid poke; allows Lili to immediately sidestep retaliations" },
        { cmd: "d+3+4", role: "Matterhorn High-Crush", startup: "i15", block: "-26", dmg: 32, desc: "Immense high-crushing mid launcher; launches into 85+ damage combos" },
        { cmd: "3+4", role: "Safe Keepout Flip", startup: "i18", block: "-9", dmg: 24, desc: "Safe jumping flip kick that knocks down and wall splats" },
        { cmd: "db+4", role: "Low Sweep Harass", startup: "i20", block: "-12", dmg: 18, desc: "Safe low sweep that leaves Lili in backturned stance at advantage" },
        { cmd: "f,f+3", role: "Long Range Gap Closer", startup: "i16", block: "-3", dmg: 22, desc: "Safe jumping knee with immense forward travel" }
      ],
      gameplan: "Sidestep opponent attacks with superior lateral movement, then launch with Matterhorn or df+2. Enforce Feisty Rabbit stances and backturned cartwheels.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / d+3+4 (Matterhorn, i15)",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "2, 4", dmg: 28, adv: "+4" },
        { frame: "14f", move: "f+2, 3", dmg: 32, adv: "KND" },
        { frame: "15f", move: "df+2 or d+3+4", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 26, adv: "+8" },
        { frame: "16f", move: "WS+2", dmg: 24, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 24, note: "Long range thrust" },
        { move: "d+3+4 (Matterhorn)", startup: "i15", reach: "Medium", dmg: 32, note: "Devastating whiff punisher" }
      ],
      stances: ["Feisty Rabbit (RAB)", "Backturned (BT)"],
      heat_breakdown: "Grants continuous plus frames on Feisty Rabbit flips and enhances Matterhorn with aerial recovery safety.",
      stage_synergy: "Excels on open infinite arenas where her unmatched lateral sidestep out-maneuvers all rivals."
    },

    nina: {
      name: "Nina Williams",
      title: "The Silent Assassin",
      japanese_name: "ニーナ・ウィリアムズ",
      country: "Ireland",
      country_flag: "🇮🇪",
      style: "Assassination Martial Arts & Koppojutsu",
      height: "161 cm (5'3\")",
      weight: "49 kg (108 lbs)",
      age: "43 (Cryo-Preserved ~24)",
      blood_type: "A",
      status: "Elite Freelance Contractor",
      archetype: "Butterfly Loop / Infinite Pressure",
      difficulty: "Master ★★★★★",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "A ruthless Irish assassin trained in Koppojutsu and bone-shattering joint locks. Working as an elite freelance contractor for G Corporation, Nina eliminates targets with dual-wielded handguns, lethal chain throws, and continuous butterfly-step pressure.",
      pros: ["Relentless plus-frame string pressure (Hayashida step, Butterfly cancel)", "Devastating multi-link chain throws (Betrayal, Arm Break, Spider Knee)", "Fastest 10f standing punishers with gun followup extensions", "High wall travel and corner pressure"],
      cons: ["Extremely demanding physical execution (iWS cancels, Hayashida loops)", "Short range on basic pokes"],
      ratings: { offense: 98, defense: 86, range: 82, execution: 98, movement: 90, throw: 94 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Core mid poke with Butterfly step cancels into infinite loops" },
        { cmd: "b+1", role: "Safe Mid Retaliator", startup: "i14", block: "-5", dmg: 20, desc: "Safe mid strike that launches on Counter Hit" },
        { cmd: "db+3", role: "Low Harass", startup: "i16", block: "-13", dmg: 16, desc: "Fast low kick that ducks under high jabs" },
        { cmd: "f,f+3", role: "Long Range Mid", startup: "i16", block: "-7", dmg: 24, desc: "Long range leaping kick that wall splats" },
        { cmd: "d+3, 4, 3", role: "Mixup String", startup: "i14", block: "-10", dmg: 32, desc: "Low-high-mid string with delayable gunshots" }
      ],
      gameplan: "Trap defenders against the wall with df+1 Butterfly cancels. Enforce chain throws on standing guards. Whiff punish with dual gunshots and f,f+3.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / uf+2, 1",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "2, 3", dmg: 26, adv: "+4" },
        { frame: "14f", move: "b+1", dmg: 20, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 4", dmg: 28, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+3", startup: "i16", reach: "Far", dmg: 24, note: "Fast forward leap" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Standard mid launch" }
      ],
      stances: ["Hayashida Step (HYS)", "Butterfly Cancel", "Swiping Claw"],
      heat_breakdown: "Equips dual firearms, converting handgun strings into unblockable chip damage sequences.",
      stage_synergy: "Monstrous on walled arenas where Butterfly cancels pin opponents indefinitely."
    },

    panda: {
      name: "Panda",
      title: "The Faithful Protector",
      japanese_name: "パンダ",
      country: "China",
      country_flag: "🇨🇳",
      style: "Heihachi Style Advanced Kuma Shin Ken",
      height: "277 cm (9'1\")",
      weight: "200 kg (441 lbs)",
      age: "9",
      blood_type: "None",
      status: "Ling Xiaoyu Bodyguard & Mascot",
      archetype: "Heavy Bear / Big Body Stance",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "Ling Xiaoyu's devoted pet and bodyguard. Trained in Heihachi Mishima's bear martial arts, Panda combines raw colossal strength with surprisingly nimble rolling charges, protecting Xiaoyu from all threats with endearing ferocity.",
      pros: ["Immense reach on bear paws and claw swipes", "Hunting stance (HBS) ducks under highs and mids", "Absurd low sweep damage with db+2 and rolling attacks", "Unique big-body combo properties"],
      cons: ["Large hurtbox susceptible to severe bear-specific juggles", "Extremely slow backdash and movement speed"],
      ratings: { offense: 90, defense: 78, range: 94, execution: 82, movement: 68, throw: 84 },
      top5: [
        { cmd: "df+2", role: "Long Range Mid Launcher", startup: "i15", block: "-13", dmg: 22, desc: "Colossal mid claw sweep that launches on normal hit" },
        { cmd: "b+1", role: "Fast Bear Swipe", startup: "i10", block: "-12", dmg: 20, desc: "10f standing counter-hit tool that catches forward rushers" },
        { cmd: "db+2", role: "Bear Low Sweep", startup: "i23", block: "-17", dmg: 26, desc: "Unseeable low claw sweep that knocks down for guaranteed oki" },
        { cmd: "f+1, 1, 1", role: "Bear Jab Barrage", startup: "i10", block: "-6", dmg: 32, desc: "Heavy 10f punish string that splats at the wall" },
        { cmd: "HBS 1+2", role: "Hunting Stance Smasher", startup: "i15", block: "+4", dmg: 28, desc: "Plus on block mid slam while prowling on all fours" }
      ],
      gameplan: "Control space with df+2 claw sweeps. Frustrate opponent high attacks with Hunting Stance (HBS). Punish whiffs with massive bear paw juggles.",
      launcher: "df+2 (Mid Launcher, i15, -13 OB) / uf+4",
      standing_punish: [
        { frame: "10f", move: "1, 2 or b+1", dmg: 20, adv: "+6" },
        { frame: "12f", move: "f+1, 1, 1", dmg: 32, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "df+2", startup: "i15", reach: "Far", dmg: 22, note: "Long range bear launcher" },
        { move: "f,f+2", startup: "i16", reach: "Far", dmg: 25, note: "Demon bear paw" }
      ],
      stances: ["Hunting Bear Stance (HBS)", "Sit Down"],
      heat_breakdown: "Enters Berserk Bear state, unlocking electrified bear swipes and enhanced Hunting stance speed.",
      stage_synergy: "Excels on hazard-rich stages where bear throws slam opponents through floors and walls."
    },

    kuma: {
      name: "Kuma",
      title: "The Roaring Bear",
      japanese_name: "クマ",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Heihachi Style Advanced Kuma Shin Ken",
      height: "280 cm (9'2\")",
      weight: "210 kg (463 lbs)",
      age: "10",
      blood_type: "None",
      status: "Mishima Zaibatsu Loyal Guardian",
      archetype: "High Damage Bear / Hunting Stance",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "Heihachi Mishima's beloved pet and most loyal discipline disciple. Wielding Heihachi's red belt and electrified Mishima techniques in memory of his departed master, Kuma unleashes thunderous electric bear claws upon G Corporation.",
      pros: ["Electric Wind God Fist bear claw (Wind God Paw)", "Hunting stance with crushing low and mid options", "Tremendous reach and heavy guard break tools", "High damage aerial juggles with fish weapons"],
      cons: ["Large hurtbox vulnerable to bear-specific extended combos", "Slow lateral sidestep agility"],
      ratings: { offense: 92, defense: 78, range: 94, execution: 84, movement: 68, throw: 86 },
      top5: [
        { cmd: "f,n,d,df+2", role: "Electric Wind God Paw", startup: "i11", block: "+5", dmg: 24, desc: "Kuma's Mishima electric; high launcher with massive frame advantage" },
        { cmd: "df+2", role: "Long Range Mid Launcher", startup: "i15", block: "-13", dmg: 22, desc: "Colossal mid claw sweep with extreme reach" },
        { cmd: "db+2", role: "Low Claw Sweep", startup: "i23", block: "-17", dmg: 26, desc: "Unseeable low sweep that knocks down into full oki" },
        { cmd: "f+1, 1, 1", role: "Bear 10f Punish", startup: "i10", block: "-6", dmg: 32, desc: "Heavy standing punish string with wall splat capability" },
        { cmd: "HBS 1+2", role: "Hunting Stance Slam", startup: "i15", block: "+4", dmg: 28, desc: "Plus on block mid slam while prowling on all fours" }
      ],
      gameplan: "Control the neutral with df+2 claw sweeps and Electric Wind God Paws. Enter Hunting Stance to evade enemy high attacks, then crush defense with low sweeps.",
      launcher: "f,n,d,df+2 (Electric Paw, i11, +5 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 2 or b+1", dmg: 20, adv: "+6" },
        { frame: "12f", move: "f+1, 1, 1", dmg: 32, adv: "KND" },
        { frame: "14f", move: "f,n,d,df+2", dmg: 24, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,n,d,df+2", startup: "i11", reach: "Far", dmg: 24, note: "Electric bear paw" },
        { move: "df+2", startup: "i15", reach: "Far", dmg: 22, note: "Long range claw launch" }
      ],
      stances: ["Hunting Bear Stance (HBS)", "Sit Down"],
      heat_breakdown: "Channels Heihachi's spirit, electrifying all bear strikes and granting infinite Electric Wind God Paws.",
      stage_synergy: "Monstrous on wall stages where Mishima bear electrics slam opponents through barriers."
    },

    raven: {
      name: "Raven",
      title: "The Shadow Agent",
      japanese_name: "レイヴン",
      country: "Global (UN Intelligence)",
      country_flag: "🌐",
      style: "Ninjutsu & Shadow Clone Espionage",
      height: "187 cm (6'2\")",
      weight: "86 kg (190 lbs)",
      age: "Unknown (~35)",
      blood_type: "B",
      status: "UN Secret Intelligence Operative",
      archetype: "Clone Teleport / Backturned Mixup",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "An elite shadow operative of the United Nations Independent Forces. Having completed arduous shadow ninjutsu retrainings, Raven wields physical shadow clones and spatial teleportation to disrupt G Corporation's global military operations.",
      pros: ["Shadow clones create multi-angled simultaneous mixup strikes", "Exceptional backturned evasion and teleport escapes", "Safe mid launchers with long forward reach", "Devastating wall hazard conversions"],
      cons: ["Backturned transitions require sharp situational awareness", "Predictable clone timings can be stepped or interrupted"],
      ratings: { offense: 94, defense: 88, range: 90, execution: 86, movement: 92, throw: 80 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i14", block: "-1", dmg: 13, desc: "Core mid poke with backturned transition" },
        { cmd: "ff+3", role: "Safe Long Range Mid", startup: "i16", block: "-6", dmg: 24, desc: "Acrobatic scissor kick that launches into full juggle" },
        { cmd: "db+4", role: "Low Harass", startup: "i18", block: "-12", dmg: 16, desc: "Safe low kick that ducks under incoming high strikes" },
        { cmd: "3~4", role: "Clone Teleport Leap", startup: "i20", block: "+2", dmg: 26, desc: "Shadow clone leap that creates plus frames on block" },
        { cmd: "BT f+4, 3", role: "Backturned Mixup", startup: "i15", block: "-10", dmg: 32, desc: "Fast mid strike from backturned stance leading to juggle" }
      ],
      gameplan: "Use shadow clones to confuse opponent guard at Range 2. Enter Backturned (BT) stance using df+1, then mix between low sweeps and mid clone launchers.",
      launcher: "ff+3 (Safe Mid Launcher, i16, -6 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "2, 4", dmg: 26, adv: "+4" },
        { frame: "14f", move: "4, 1", dmg: 28, adv: "KND" },
        { frame: "16f", move: "ff+3", dmg: 24, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "ff+3", startup: "i16", reach: "Far", dmg: 24, note: "Long range scissor kick launch" },
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 22, note: "Shadow straight punch" }
      ],
      stances: ["Backturned (BT)", "Shadow Clones", "Haze"],
      heat_breakdown: "Summons persistent shadow clones on all basic attacks, creating impossible-to-parry dual strikes.",
      stage_synergy: "Excels on multi-tiered stages where clone juggles trigger wall and floor breaks."
    },

    shaheen: {
      name: "Shaheen",
      title: "The Desert Falcon",
      japanese_name: "シャヒーン",
      country: "Saudi Arabia",
      country_flag: "🇸🇦",
      style: "Military Close Quarters Combat (CQC)",
      height: "183 cm (6'0\")",
      weight: "76 kg (168 lbs)",
      age: "Unknown (~29)",
      blood_type: "B",
      status: "Private Military Executive",
      archetype: "Fundamental Slide / Stealth Step",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "A bodyguard and military executive for a private security firm. Following the suspicious demise of his close friend, a prominent petroleum magnate, Shaheen enters the tournament to bring Kazuya Mishima and G Corporation to justice.",
      pros: ["Classic FC slide mixup (FC df,d,df+3) with safe followups", "Exceptional fundamental pokes (df+1, 4,1, b+1)", "Stealth Step stance provides effortless low/mid pressure", "Safe 15f hopkick launcher with high reach"],
      cons: ["Linear approach tools easily stepped to SSR", "Straightforward gameplan can be anticipated by seasoned veterans"],
      ratings: { offense: 90, defense: 92, range: 86, execution: 72, movement: 88, throw: 78 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Safe mid poke with multiple extensions and Stealth Step cancels" },
        { cmd: "uf+4", role: "Safe Hopkick", startup: "i15", block: "-13", dmg: 20, desc: "Classic hopkick launcher that crushes low attacks" },
        { cmd: "FC df,d,df+3", role: "Desert Slide", startup: "i18", block: "-23", dmg: 24, desc: "Unseeable low slide from crouch with guaranteed knockdown followups" },
        { cmd: "4, 1", role: "Counter-Hit High String", startup: "i11", block: "-3", dmg: 26, desc: "Fast 11f counter-hit string that knocks down on hit" },
        { cmd: "f,b+2", role: "Heavy Punisher", startup: "i14", block: "-10", dmg: 32, desc: "Fast standing 14f punisher with massive knockdown pushback" }
      ],
      gameplan: "Control space with df+1 and b+1. Drop into crouch to enforce the slide mixup (FC slide vs hopkick). Whiff punish with uf+4.",
      launcher: "uf+4 (Hopkick, i15, -13 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "2, 3", dmg: 26, adv: "+4" },
        { frame: "14f", move: "f,b+2", dmg: 32, adv: "KND" },
        { frame: "15f", move: "uf+4 (Hopkick)", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "uf+4", startup: "i15", reach: "Far", dmg: 20, note: "Premier hopkick" },
        { move: "f,f+3", startup: "i16", reach: "Long", dmg: 24, note: "Approaching kick" }
      ],
      stances: ["Stealth Step (SNK)"],
      heat_breakdown: "Empowers Desert Slide into an armored launcher and grants continuous plus frames in Stealth Step.",
      stage_synergy: "Thrives on all stage layouts thanks to rock-solid fundamentals."
    },

    steve: {
      name: "Steve Fox",
      title: "The Counter-Punching Genius",
      japanese_name: "スティーブ・フォックス",
      country: "United Kingdom",
      country_flag: "🇬🇧",
      style: "Orthodox & Peekaboo Boxing",
      height: "185 cm (6'1\")",
      weight: "75 kg (165 lbs)",
      age: "21",
      blood_type: "B",
      status: "Middleweight World Boxing Champion",
      archetype: "Stance Boxing / CH Fisher",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "The middleweight boxing champion of the world and biological son of Nina Williams. Utilizing rapid slip-weaves, Peekaboo guard, and swaying ducking steps, Steve dodges incoming attacks with surgical grace to deliver devastating counter-punches.",
      pros: ["Fastest counter-hit launch in Tekken (b+1, i13, safe on block)", "Formidable Peekaboo (PAB) and Flicker (FLK) stance pressure", "Superior defensive slipping and ducking evasions", "Extremely high safety across his core striking arsenal"],
      cons: ["No generic kick launchers (strictly punches)", "Low damage potential from standard low pokes outside counter-hit"],
      ratings: { offense: 94, defense: 96, range: 82, execution: 96, movement: 94, throw: 80 },
      top5: [
        { cmd: "b+1", role: "Premier Counter-Hit Punch", startup: "i13", block: "-1", dmg: 21, desc: "God-tier 13f high punch; safe on block and launches on Counter Hit" },
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Safe mid poke with Flicker stance cancel" },
        { cmd: "d+2, 1", role: "High-Crush Low String", startup: "i16", block: "-12", dmg: 24, desc: "Fast low punch string leading into Peekaboo stance" },
        { cmd: "PAB df+1", role: "Peekaboo Mid Check", startup: "i14", block: "0", dmg: 16, desc: "Neutral on block mid strike that sets up immediate frame traps" },
        { cmd: "f,f+2", role: "Approaching Straight", startup: "i16", block: "-9", dmg: 24, desc: "Long range straight punch that knocks down and wall splats" }
      ],
      gameplan: "Bait opponent attacks with b+1 counter-hit timing. Slip under highs using Ducking (DCK). Enter Peekaboo stance to enforce mid and low punch pressure.",
      launcher: "b+1 (CH Launcher, i13, -1 OB) / df+2 (Mid Launcher, i15)",
      standing_punish: [
        { frame: "10f", move: "1, 1, 2", dmg: 22, adv: "+6" },
        { frame: "12f", move: "1+2", dmg: 26, adv: "+4" },
        { frame: "14f", move: "b+1", dmg: 21, adv: "CH Launch" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+1, 2", dmg: 24, adv: "+6" },
        { frame: "14f", move: "WS+1, 1", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2", startup: "i16", reach: "Far", dmg: 24, note: "Long range straight punch" },
        { move: "b+1", startup: "i13", reach: "Medium", dmg: 21, note: "Fastest counter-hit launch" }
      ],
      stances: ["Peekaboo (PAB)", "Flicker (FLK)", "Sway / Weave"],
      heat_breakdown: "Enters Lion Heart stance automatically from heavy blows, granting unblockable punch guard breaks.",
      stage_synergy: "Excels on walled stages where Peekaboo frame traps pin opponents into corners."
    },

    victor: {
      name: "Victor Chevalier",
      title: "The Refined Vanguard",
      japanese_name: "ヴィクター・シュヴァリエ",
      country: "France",
      country_flag: "🇫🇷",
      style: "Super Spy CQB / Takemikazuchi Cyber Katana",
      height: "187 cm (6'2\")",
      weight: "84 kg (185 lbs)",
      age: "58",
      blood_type: "AB",
      status: "UN Raven Unit Supreme Commander",
      archetype: "Teleport Weapon / Iai Stance",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "A decorated French military veteran and supreme founder of the UN Raven Unit. Armed with the high-frequency cyber katana 'Takemikazuchi', stealth spatial teleporters, and tactical dual pistols, Victor executes battlefield missions with aristocratic refinement.",
      pros: ["Long-range sword strikes with massive hitboxes", "Spatial teleportation (Iai stance) evades incoming pressure", "Explosive shotgun blast Heat Engagers", "Simple, high-damage combo routes"],
      cons: ["Linear sword thrusts vulnerable to SSL sidewalk", "Several stance transitions carry high block risk"],
      ratings: { offense: 96, defense: 88, range: 94, execution: 74, movement: 88, throw: 78 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Safe mid sword thrust with Iai stance cancels" },
        { cmd: "f,f+2", role: "Long Range Gap Closer", startup: "i15", block: "-8", dmg: 24, desc: "Teleporting sword slash that closes distance instantly" },
        { cmd: "db+4", role: "Low Katana Sweep", startup: "i19", block: "-13", dmg: 18, desc: "Safe low slash that leaves Victor in Iai stance at advantage" },
        { cmd: "2, 2, 2", role: "Pistol String", startup: "i10", block: "-12", dmg: 32, desc: "Fast 10f punish string ending in handgun shots" },
        { cmd: "b+1+2", role: "Tactical Shotgun Blast", startup: "i16", block: "-9", dmg: 34, desc: "Close-range firearm strike that causes massive knockdown" }
      ],
      gameplan: "Control the mid-range with f,f+2 and df+1. Transition into Iai stance to enforce teleport mixups between low sweeps and high-damage katana launchers.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / Iai 2",
      standing_punish: [
        { frame: "10f", move: "2, 2, 2", dmg: 32, adv: "KND" },
        { frame: "12f", move: "f+2, 1", dmg: 26, adv: "+4" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 24, note: "Teleport sword slash" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Standard mid launch" }
      ],
      stances: ["Iai Stance (IAI)", "Perfume (PRF)"],
      heat_breakdown: "Overcharges the Takemikazuchi cyber katana, making all sword slashes inflict extreme chip damage on block.",
      stage_synergy: "Excels on wall stages where shotgun blasts shatter barriers effortlessly."
    },

    xiaoyu: {
      name: "Ling Xiaoyu",
      title: "The Dancing Phoenix",
      japanese_name: "凌 暁雨",
      country: "China",
      country_flag: "🇨🇳",
      style: "Baguazhang & Piguaquan",
      height: "157 cm (5'2\")",
      weight: "42 kg (93 lbs)",
      age: "18",
      blood_type: "A",
      status: "Mishima High School Student",
      archetype: "Evasion Artist / Art of Phoenix",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "A cheerful martial arts prodigy attending Mishima High School. Devoted to saving Jin Kazama from the curse of his demonic bloodline, Xiaoyu weaves through battle with playful yet deadly Baguazhang steps and evasive crouching stances.",
      pros: ["Art of Phoenix (AOP) evades almost all high and mid attacks", "Extremely elusive Rain Dance (RDS) backturned stance", "Hardest character in the game to hit with generic strings", "High-damage juggle conversions from crouch"],
      cons: ["Short attack reach on basic pokes", "Requires deep situational awareness of opponent hurtboxes"],
      ratings: { offense: 90, defense: 100, range: 76, execution: 94, movement: 98, throw: 76 },
      top5: [
        { cmd: "d+1+2 (AOP)", role: "Art of Phoenix Stance", startup: "i10", block: "N/A", dmg: 0, desc: "Ducks underneath high and mid strikes, making Xiaoyu completely untouchable" },
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Safe mid check poke with RDS backturned transition" },
        { cmd: "AOP 4~3", role: "Evasive Launcher", startup: "i17", block: "-13", dmg: 24, desc: "Cartwheel kick from AOP that launches into full juggle" },
        { cmd: "ff+3", role: "Approaching Mid", startup: "i16", block: "-3", dmg: 22, desc: "Safe leaping kick with heavy forward travel" },
        { cmd: "db+4", role: "Low Harass", startup: "i18", block: "-12", dmg: 15, desc: "Safe low kick that leaves Xiaoyu in AOP at advantage" }
      ],
      gameplan: "Frustrate opponent offense by entering Art of Phoenix (AOP). Whiff punish their missed strikes with AOP 4~3 or df+2. Flow into Rain Dance (RDS) for backturned mixups.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / AOP 4~3",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "f+1+2", dmg: 26, adv: "+4" },
        { frame: "14f", move: "3", dmg: 22, adv: "KND" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+2", dmg: 22, adv: "+8" },
        { frame: "15f", move: "WS+1+2", dmg: 24, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "ff+3", startup: "i16", reach: "Far", dmg: 24, note: "Approaching leaping kick" },
        { move: "AOP 4~3", startup: "i17", reach: "Medium", dmg: 24, note: "Evasive stance launcher" }
      ],
      stances: ["Art of Phoenix (AOP)", "Rain Dance (RDS)"],
      heat_breakdown: "Empowers Art of Phoenix with continuous auto-evasion and unlocks enhanced hypnotic strike loops.",
      stage_synergy: "Excels on open infinite arenas where her evasion frustrates opponents to exhaustion."
    },

    yoshimitsu: {
      name: "Yoshimitsu",
      title: "The Mechanical Space Ninja",
      japanese_name: "吉光",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Advanced Manji Ninjutsu",
      height: "178 cm (5'10\")",
      weight: "63 kg (139 lbs)",
      age: "Unknown",
      blood_type: "O",
      status: "Manji Clan 11th Master",
      archetype: "Flash Parry / Unorthodox Stances",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "The honorable master of the righteous Manji Clan robin-hood bandits. Clad in cybernetic armor and wielding the cursed demon blade Yoshimitsu, he enters the tournament to thwart Kazuya's global war machine and aid the destitute.",
      pros: ["Manji Flash (1+4, i6-i8 startup, fastest interrupt in fighting game history)", "Kincho and Flea stances bypass standard defense completely", "Self-healing in Indian Stance and life-stealing sword strikes", "Unblockable low sweeps and flying helicopter attacks"],
      cons: ["Demands eccentric, creative player mindset", "Self-harm mechanics (Harakiri) carry catastrophic risk if mistimed"],
      ratings: { offense: 92, defense: 98, range: 86, execution: 96, movement: 94, throw: 84 },
      top5: [
        { cmd: "1+4", role: "Manji Flash", startup: "i6", block: "-15", dmg: 25, desc: "Fastest interrupt in Tekken (6-8 frames); steals turns from plus frames" },
        { cmd: "df+1", role: "Safe Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid poke with Kincho stance cancel" },
        { cmd: "3~4", role: "Helicopter Spin", startup: "i18", block: "+2", dmg: 24, desc: "Airborne spinning blades with plus frames on block" },
        { cmd: "FC df+4", role: "Manji Low Sweep", startup: "i18", block: "-26", dmg: 24, desc: "Full knockdown sweep into guaranteed sword followups" },
        { cmd: "KIN 2", role: "Kincho Safe Mid", startup: "i15", block: "-4", dmg: 22, desc: "Mid sword thrust from Kincho that launches on Counter Hit" }
      ],
      gameplan: "Steal turns and interrupt opponent plus frames with Manji Flash (1+4). Use Flea and Indian stances to confuse defenders, then unleash unblockable sword strikes.",
      launcher: "df+2 (Safe Mid Launcher, i15, -7 OB) / uf+3",
      standing_punish: [
        { frame: "6f", move: "1+4 (Flash)", dmg: 25, adv: "Launch Interrupt" },
        { frame: "10f", move: "1, 1", dmg: 19, adv: "+6" },
        { frame: "12f", move: "2, 2", dmg: 26, adv: "+4" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1, 2", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2, 1", dmg: 32, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+4", startup: "i16", reach: "Far", dmg: 24, note: "Forward flying kick" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Safe mid sword launch" }
      ],
      stances: ["Kincho (KIN)", "Flea (FLA)", "Indian Stance (IND)", "Dragonfly (DGF)"],
      heat_breakdown: "Overcharges the cursed Yoshimitsu blade with dark souls, turning all sword strikes unblockable on hit.",
      stage_synergy: "Excels across all stages thanks to unblockable setups and Manji Flash interrupts."
    },

    zafina: {
      name: "Zafina",
      title: "The Mystic Astrologer",
      japanese_name: "ザフィーナ",
      country: "Egypt",
      country_flag: "🇪🇬",
      style: "Ancient Assassination Arts & Azazel Claws",
      height: "171 cm (5'7\")",
      weight: "53 kg (117 lbs)",
      age: "23",
      blood_type: "B",
      status: "Royal Tomb Guardian",
      archetype: "Stance Morphing / Low Profile",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "An Egyptian astrologer and guardian of an ancient royal tomb. Having sealed the spiritual remnant of the demon Azazel inside her left arm, Zafina fights to keep the beast contained while utilizing its monstrous power to extinguish Kazuya's dark ambitions.",
      pros: ["Three elusive animal stances (Tarantula, Scarecrow, Mantis)", "Tarantula (TRT) crawls underneath high and mid strikes", "Empowered Azazel demonic claw strikes in Heat", "High-frustration defensive keepout"],
      cons: ["Low damage from standard standing neutral", "Complex stance transitions require deep situational mastery"],
      ratings: { offense: 90, defense: 96, range: 88, execution: 92, movement: 96, throw: 74 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Safe mid poke with multiple animal stance transitions" },
        { cmd: "b+1+2", role: "Demon Claw Strike", startup: "i15", block: "-9", dmg: 26, desc: "Heavy mid strike utilizing Azazel's crystal claw" },
        { cmd: "d+3", role: "Low Poke Harass", startup: "i16", block: "-12", dmg: 14, desc: "Fast low kick leading into Tarantula crawl" },
        { cmd: "ff+3", role: "Approaching Axe Kick", startup: "i17", block: "-4", dmg: 22, desc: "Safe mid kick that knocks down on Counter Hit" },
        { cmd: "TRT d+1+2", role: "Tarantula Low Sweep", startup: "i18", block: "-14", dmg: 24, desc: "Creeping low sweep from full floor crawl" }
      ],
      gameplan: "Crawl under enemy attacks using Tarantula stance (TRT). Transition between Mantis and Scarecrow to keep opponents guessing. Punish mistakes with Azazel's claws.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / MNT 2",
      standing_punish: [
        { frame: "10f", move: "1, 3", dmg: 21, adv: "+6" },
        { frame: "12f", move: "f+2, 3", dmg: 26, adv: "+4" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "ff+3", startup: "i17", reach: "Far", dmg: 22, note: "Long range approaching kick" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Standard mid launch" }
      ],
      stances: ["Tarantula (TRT)", "Scarecrow (SCR)", "Mantis (MNT)"],
      heat_breakdown: "Unleashes Azazel's full power, expanding the demonic claw hitbox and adding extreme chip damage to Scarecrow strikes.",
      stage_synergy: "Excels on open stages where animal crawling confuses opponent spacing."
    },

    eddy: {
      name: "Eddy Gordo",
      title: "The Rhythmic Capoeirista",
      japanese_name: "エディ・ゴルド",
      country: "Brazil",
      country_flag: "🇧🇷",
      style: "Capoeira",
      height: "188 cm (6'2\")",
      weight: "75 kg (165 lbs)",
      age: "29",
      blood_type: "B",
      status: "Capoeira Master & Resistance Ally",
      archetype: "Mandinga Stance / Continuous Rhythm",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "The legendary Brazilian capoeirista seeking redemption after being coerced into serving Jin Kazama's Mishima Zaibatsu. Armed with fluid Mandinga rhythms and ground handstand transitions, Eddy fights to protect the innocent from G Corporation.",
      pros: ["Streamlined Bananeira (handstand) and Negativa (ground) stance flowcharts", "Mandinga charges grant high-damage special combo extensions", "Devastating low sweep mixups from relaxed stance", "Strong beginner-friendly rhythm pressure"],
      cons: ["Low defense during continuous ground flowcharts", "Can be interrupted by well-timed mids during handstand dances"],
      ratings: { offense: 96, defense: 82, range: 90, execution: 74, movement: 92, throw: 76 },
      top5: [
        { cmd: "3, 3", role: "Rhythm Kick String", startup: "i13", block: "-6", dmg: 28, desc: "Core capoeira kick string leading into Bananeira" },
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Safe mid poke with Negativa transition" },
        { cmd: "db+3", role: "Negativa Low Sweep", startup: "i18", block: "-14", dmg: 20, desc: "Ground sweep that knocks down into juggle conversions" },
        { cmd: "f,f+3", role: "Approaching Flying Kick", startup: "i16", block: "-4", dmg: 24, desc: "Long range gap-closer that transitions into handstand" },
        { cmd: "b+3, 3", role: "High-Crush Kicks", startup: "i15", block: "-9", dmg: 32, desc: "Evades incoming high jabs and launches on Counter Hit" }
      ],
      gameplan: "Enter Bananeira handstand and Negativa ground stances to build Mandinga charges. Force defenders to guess between unseeable low sweeps and mid cartwheel launchers.",
      launcher: "df+3+4 (Mid Launcher, i15, -13 OB) / Bananeira 2",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "4, 3", dmg: 26, adv: "+4" },
        { frame: "15f", move: "df+3+4", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 3", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+3", startup: "i16", reach: "Far", dmg: 24, note: "Long range flying kick" },
        { move: "df+3+4", startup: "i15", reach: "Medium", dmg: 22, note: "Standard mid launch" }
      ],
      stances: ["Bananeira (HSP)", "Negativa (RLX)", "Mandinga"],
      heat_breakdown: "Automatically maxes out Mandinga charges, allowing instant execution of his most devastating capoeira launchers.",
      stage_synergy: "Excels on open stages where continuous rhythm acrobatics create endless spacing headaches."
    },

    lidia: {
      name: "Lidia Sobieska",
      title: "The Warrior Prime Minister",
      japanese_name: "リディア・ソビエスカ",
      country: "Poland",
      country_flag: "🇵🇱",
      style: "Traditional Karate (Shotokan / Goju-Ryu Hybrid)",
      height: "174 cm (5'8\")",
      weight: "60 kg (132 lbs)",
      age: "29",
      blood_type: "O",
      status: "Prime Minister of Poland",
      archetype: "Heaven & Earth Stances / Plus-Frame Rushdown",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The courageous Prime Minister of Poland and world karate champion. In Tekken 8, Lidia enters the fray with renewed resolve, utilizing orthodox Seiei and Horse stances to defend her homeland from Mishima military aggression.",
      pros: ["Overwhelming plus-frame karate strikes (f,f+2, df+1,2)", "Heaven and Earth stances create true guard break opportunities", "Extremely high damage wall conversions with Horse stance", "Formidable mid pokes with strong pushback"],
      cons: ["Linear karate thrusts can be stepped to SSR", "Demands aggressive forward momentum to sustain stance advantage"],
      ratings: { offense: 96, defense: 88, range: 88, execution: 82, movement: 86, throw: 80 },
      top5: [
        { cmd: "f,f+2", role: "Premier Approach Thrust", startup: "i15", block: "-4", dmg: 22, desc: "High-speed karate punch leading into Cat stance at advantage" },
        { cmd: "df+1, 2", role: "Mid Check String", startup: "i13", block: "-6", dmg: 24, desc: "Safe mid poke string leading into Horse stance" },
        { cmd: "db+3", role: "Low Karate Kick", startup: "i17", block: "-12", dmg: 16, desc: "Safe low kick that leaves Lidia in full crouch with frame advantage" },
        { cmd: "f+1+2", role: "Heavy Mid Straight", startup: "i16", block: "-9", dmg: 28, desc: "Knocks down and wallsplats from distance" },
        { cmd: "b+1", role: "Fast Safe Check", startup: "i12", block: "-7", dmg: 16, desc: "Fast standing 12f check with pushback" }
      ],
      gameplan: "Charge forward with f,f+2 into Cat and Horse stances. Enforce guard break punches against defensive blockers. Whiff punish with f,f+2.",
      launcher: "uf+4 (Hopkick, i15, -13 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 2, 2", dmg: 26, adv: "+6" },
        { frame: "12f", move: "f+2, 4", dmg: 28, adv: "+4" },
        { frame: "14f", move: "f+1+2", dmg: 28, adv: "KND" },
        { frame: "15f", move: "uf+4 (Hopkick)", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 22, note: "Approaching karate thrust" },
        { move: "uf+4", startup: "i15", reach: "Medium", dmg: 20, note: "Standard hopkick" }
      ],
      stances: ["Cat Stance (CAT)", "Horse Stance (HRS)", "Heaven & Earth"],
      heat_breakdown: "Grants infinite Horse stance charges, making all karate strikes deal severe chip damage and guard breaks.",
      stage_synergy: "Deadly on walled arenas where Horse stance strikes wall-splat from across the ring."
    },

    heihachi: {
      name: "Heihachi Mishima",
      title: "The King of Iron Fist",
      japanese_name: "三島 平八",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Mishima Style Fighting Karate (True Ancestor)",
      height: "179 cm (5'10\")",
      weight: "80 kg (176 lbs)",
      age: "75 (Resurrected)",
      blood_type: "B",
      status: "Resurrected Patriarch of Mishima Clan",
      archetype: "Iron Dominance / Warrior Stance",
      difficulty: "Master ★★★★★",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "The indomitable patriarch who founded the King of Iron Fist Tournament. Defying death at the volcanic caldera, Heihachi returns to the living world imbued with ancient ascetic Warrior monk disciplines to reclaim his empire and crush Kazuya.",
      pros: ["Thunderous Electric Wind God Fist with maximum vertical launch height", "Warrior Stance flowcharts with crushing guard breaks", "Top-tier mid pokes (df+1,2, f,f+2, f+4)", "Highest single-hit damage output among Mishimas"],
      cons: ["No generic standing 15f mid launcher (relies on EWGF or delayed uf+4)", "Weak standing low poke damage outside Hellsweep"],
      ratings: { offense: 98, defense: 92, range: 86, execution: 96, movement: 88, throw: 82 },
      top5: [
        { cmd: "f,n,d,df+2", role: "Electric Wind God Fist", startup: "i11", block: "+5", dmg: 25, desc: "The definitive Mishima electric; launches into 85+ damage combos with +5 advantage" },
        { cmd: "f,f+2", role: "Demon God Fist", startup: "i15", block: "-16", dmg: 26, desc: "Long-range mid straight punch that launches into full juggle on hit" },
        { cmd: "df+1, 2", role: "Mid Check String", startup: "i13", block: "-13", dmg: 26, desc: "Heavy mid check with delayable second strike" },
        { cmd: "f+4", role: "Frame Advantage Axe Kick", startup: "i18", block: "+4", dmg: 22, desc: "Axe kick that forces crouch at +4 on block" },
        { cmd: "f,n,d,df+4, n, 4", role: "Hellsweep String", startup: "i16", block: "-11", dmg: 32, desc: "Classic low sweep into high roundhouse kick" }
      ],
      gameplan: "Control the pace with f,f+2 and f+4 axe kick. Wavedash into opponent face to bait whiffs, then launch instantly with EWGF.",
      launcher: "EWGF (f,n,d,df+2, i11, +5 OB) / f,f+2",
      standing_punish: [
        { frame: "10f", move: "1, 1, 2", dmg: 25, adv: "KND" },
        { frame: "12f", move: "2, 2", dmg: 28, adv: "+6" },
        { frame: "14f", move: "EWGF", dmg: 25, adv: "Full Launch" },
        { frame: "15f", move: "f,f+2", dmg: 26, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "18f", move: "WS+2", dmg: 24, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,n,d,df+2 (EWGF)", startup: "i11", reach: "Far", dmg: 25, note: "Premier whiff punisher" },
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 26, note: "Heavy mid launch" }
      ],
      stances: ["Warrior Stance", "Wind God Step", "Raijin Stance"],
      heat_breakdown: "Ignites the True Mishima Fire, converting all axe kicks into unblockable guard crushes.",
      stage_synergy: "Dominates on wall arenas where EWGF wall carries result in round-ending splat sequences."
    },

    clive: {
      name: "Clive Rosfield",
      title: "The First Shield of Rosaria",
      japanese_name: "クライヴ・ロズフィールド",
      country: "Valisthea / UK",
      country_flag: "🇬🇧",
      style: "Rosarian Royal Swordsmanship & Eikonic Flame",
      height: "180 cm (5'11\")",
      weight: "78 kg (172 lbs)",
      age: "33",
      blood_type: "Unknown",
      status: "First Shield & Dominant of Ifrit",
      archetype: "Greatsword Spacing / Precision Stance",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The First Shield of Rosaria and Dominant of the Eikon Ifrit. Transported across realms into the Iron Fist tournament, Clive wields the royal greatsword Invictus alongside primal Eikonic fire to shatter tyrannical warmongers.",
      pros: ["Extreme reach on broadsword slash strings (Invictus)", "Eikonic dash cancels allow high-mobility spacing", "Devastating flame chip damage in Heat", "High damage aerial juggle enders"],
      cons: ["Linear greatsword thrusts vulnerable to SSR", "Sword recoveries can be punished if whiffed up close"],
      ratings: { offense: 94, defense: 88, range: 96, execution: 84, movement: 86, throw: 76 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Sword Check", startup: "i13", block: "-2", dmg: 14, desc: "Safe mid sword thrust with broad reach" },
        { cmd: "f,f+2", role: "Stinger Gap Closer", startup: "i15", block: "-8", dmg: 24, desc: "Lunging sword thrust that closes half-screen distances" },
        { cmd: "db+3", role: "Low Sword Sweep", startup: "i18", block: "-13", dmg: 17, desc: "Safe low slash that ducks under high attacks" },
        { cmd: "b+1+2", role: "Rising Flames Launcher", startup: "i16", block: "-12", dmg: 26, desc: "Fiery upward slash that launches into aerial juggle" },
        { cmd: "3, 2", role: "Mid-High Check", startup: "i14", block: "-4", dmg: 28, desc: "Fast kick into broadsword swipe that wall splats" }
      ],
      gameplan: "Out-range opponents with broadsword pokes at Range 2. Close in with Stinger (f,f+2). Ignite Ifrit flames in Heat to burn through opponent guard.",
      launcher: "b+1+2 (Mid Launcher, i16, -12 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "2, 3", dmg: 26, adv: "+4" },
        { frame: "15f", move: "b+1+2", dmg: 26, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2 (Stinger)", startup: "i15", reach: "Far", dmg: 24, note: "Long range sword thrust" },
        { move: "b+1+2", startup: "i16", reach: "Medium", dmg: 26, note: "Fiery upward launcher" }
      ],
      stances: ["Precision Stance", "Eikonic Dash"],
      heat_breakdown: "Ignites the flames of Ifrit, adding hellfire explosion chip damage to all broadsword strikes.",
      stage_synergy: "Excels on open arena stages where sword reach dictates the pace."
    },

    anna: {
      name: "Anna Williams",
      title: "The Scarlet Lightning",
      japanese_name: "アンナ・ウィリアムズ",
      country: "Ireland",
      country_flag: "🇮🇪",
      style: "Assassination Martial Arts",
      height: "163 cm (5'4\")",
      weight: "49 kg (108 lbs)",
      age: "41 (Cryo-Preserved ~22)",
      blood_type: "A",
      status: "Syndicate Contractor & Rival Assassin",
      archetype: "Chaos Judgment / Seductress Mixup",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "Nina Williams' glamorous, flamboyant sister and eternal rival. Clad in high-fashion couture and wielding ruthless assassination techniques, Anna steps into the tournament to settle personal scores with Nina and G Corporation.",
      pros: ["Chaos Judgment (CJM) auto-parries low attacks and creates 50/50s", "Devastating high-damage counter-hit sweeps", "Formidable close-range slapping strings and bazooka specials", "High mental frame traps"],
      cons: ["Linear special moves vulnerable to SSR", "Risky on block if mixup reads are anticipated"],
      ratings: { offense: 94, defense: 84, range: 84, execution: 80, movement: 88, throw: 82 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid poke with Chaos Judgment transition" },
        { cmd: "qcf+1", role: "Approaching Palm", startup: "i15", block: "-4", dmg: 24, desc: "Safe mid palm strike that causes heavy knockdown" },
        { cmd: "db+3", role: "Low Sweep Harass", startup: "i18", block: "-13", dmg: 17, desc: "Safe low kick into CJM stance at advantage" },
        { cmd: "b+2, 2", role: "Hit-Confirm String", startup: "i14", block: "-8", dmg: 30, desc: "Mid-mid slap string that knocks down on hit" },
        { cmd: "CJM 2", role: "Chaos Launcher", startup: "i16", block: "-12", dmg: 24, desc: "Safe mid strike from CJM that launches into full juggle" }
      ],
      gameplan: "Enter Chaos Judgment (CJM) to nullify low pokes. Mix between low sweeps and mid launchers. Trap opponents with qcf+1 palm strikes.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / CJM 2",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "2, 3", dmg: 26, adv: "+4" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "qcf+1", startup: "i15", reach: "Far", dmg: 24, note: "Fast approaching palm" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Standard mid launch" }
      ],
      stances: ["Chaos Judgment (CJM)"],
      heat_breakdown: "Equips miniature bazooka rockets, converting CJM enders into unblockable explosions.",
      stage_synergy: "Excels on wall stages where CJM slap strings pin opponents to corners."
    },

    "armor-king": {
      name: "Armor King",
      title: "The Dark Champion",
      japanese_name: "アーマーキング",
      country: "Mexico",
      country_flag: "🇲🇽",
      style: "Shoot Wrestling / Black Mist Combat",
      height: "193 cm (6'4\")",
      weight: "105 kg (231 lbs)",
      age: "30",
      blood_type: "B",
      status: "Underground Circuit Legend",
      archetype: "Grappler-Brawler Hybrid / Mishima Wavedash",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "The fearsome masked jaguar wrestler seeking vengeance for his brother's demise. Combining brutal shoot wrestling throws with fluid Mishima wavedashing and toxic black mist, Armor King stands as a formidable dark champion.",
      pros: ["Mishima-style wavedash into Dark Upper launcher (f,n,d,df+1)", "Formidable Shining Wizard and Giant Swing command grabs", "Safe mid poke harassment with b+1 and df+1", "High-damage toxic black mist unblockables"],
      cons: ["Dark Upper is high and punishable on duck", "Lacks a generic 15f normal-hit mid launcher"],
      ratings: { offense: 95, defense: 90, range: 88, execution: 88, movement: 86, throw: 96 },
      top5: [
        { cmd: "f,n,d,df+1", role: "Dark Upper Launcher", startup: "i14", block: "-10", dmg: 24, desc: "High launcher with incredible reach; premier whiff punisher" },
        { cmd: "b+1", role: "Counter-Hit Straight", startup: "i12", block: "-5", dmg: 20, desc: "Safe 12f mid check that crumple-launches on Counter Hit" },
        { cmd: "f,f,f+2+4", role: "Shining Wizard", startup: "i15", block: "Throw", dmg: 45, desc: "Running knee slam; excellent wall carry and oki" },
        { cmd: "d+3", role: "Low Kick Harass", startup: "i16", block: "-12", dmg: 14, desc: "Safe low kick that leaves Armor King at advantage" },
        { cmd: "df+1", role: "Safe Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Standard mid poke to stop ducking" }
      ],
      gameplan: "Wavedash into opponent face to mix between Dark Upper, Giant Swing, and Shining Wizard. Catch retaliations with b+1 counter-hit straight.",
      launcher: "f,n,d,df+1 (Dark Upper, i14, -10 OB) / uf+4",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "b+1", dmg: 20, adv: "+4" },
        { frame: "14f", move: "f,n,d,df+1 (Dark Upper)", dmg: 24, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,n,d,df+1", startup: "i14", reach: "Far", dmg: 24, note: "Premier Dark Upper" },
        { move: "f,f+2", startup: "i15", reach: "Long", dmg: 24, note: "Fast straight punch" }
      ],
      stances: ["Shadow Step", "Crouch Dash"],
      heat_breakdown: "Enters Poison Mist rage, adding unblockable poison breath followups to all major command throws.",
      stage_synergy: "Excels on wall stages where Shining Wizard wall splats deal tremendous damage."
    },

    bob: {
      name: "Bob Richards",
      title: "Freestyle Karate Perfection",
      japanese_name: "ボブ",
      country: "USA",
      country_flag: "🇺🇸",
      style: "Freestyle Karate & High-Speed Acrobatics",
      height: "195 cm (6'5\")",
      weight: "152 kg (335 lbs)",
      age: "27",
      blood_type: "AB",
      status: "Vigilante Hero & Martial Perfectionist",
      archetype: "Heavy Weight Agility / Plus Frame Wave",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "A martial arts perfectionist who intentionally gained colossal weight to combine unstoppable mass with lightning agility ('Speed and Weight!'). Operating as a vigilante hero, Bob crushes criminal syndicates with acrobatic somersaults and wavedash pressure.",
      pros: ["Absurd forward wavedash agility despite massive weight", "Safe mid launchers (uf+3, df+2) with high hitboxes", "Strong low harassment with cd+4 (Hellcat sweep)", "Heavy plus frames on forward belly strikes"],
      cons: ["Large hurtbox makes him vulnerable to big-body juggles", "Approaches can be stepped to SSL"],
      ratings: { offense: 94, defense: 86, range: 88, execution: 76, movement: 90, throw: 82 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid poke with multiple extensions" },
        { cmd: "cd+4, 1", role: "Hellcat Sweep String", startup: "i16", block: "-14", dmg: 28, desc: "Wavedash low sweep into mid punch knockdown" },
        { cmd: "uf+3", role: "Acrobatic Mid Launcher", startup: "i15", block: "-13", dmg: 22, desc: "Jumping belly flip that launches on hit" },
        { cmd: "f,f+2", role: "Heavy Straight", startup: "i15", block: "-8", dmg: 24, desc: "Long range lunging punch that wall splats" },
        { cmd: "b+2, 2", role: "Counter-Hit String", startup: "i14", block: "-6", dmg: 30, desc: "Safe mid-mid check that knocks down" }
      ],
      gameplan: "Wavedash into opponent face to force Hellcat low sweeps or uf+3 mid belly launches. Push opponents into the corner with f,f+2.",
      launcher: "uf+3 (Mid Launcher, i15, -13 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "f+2, 3", dmg: 26, adv: "+4" },
        { frame: "15f", move: "uf+3", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 24, note: "Long range lunging punch" },
        { move: "uf+3", startup: "i15", reach: "Medium", dmg: 22, note: "Standard belly flip" }
      ],
      stances: ["Crouch Dash / Wavedash", "Roll"],
      heat_breakdown: "Channels Maximum Velocity, turning belly strikes into armored guard-crush battering rams.",
      stage_synergy: "Excels on wall stages where heavy body splats maximize juggle damage."
    },

    fahkumram: {
      name: "Fahkumram",
      title: "The Muay Thai Titan",
      japanese_name: "ファカムラム",
      country: "Thailand",
      country_flag: "🇹🇭",
      style: "Traditional Muay Thai & Muay Boran",
      height: "226 cm (7'5\")",
      weight: "145 kg (320 lbs)",
      age: "36",
      blood_type: "A",
      status: "Imprisoned Muay Thai Champion",
      archetype: "Crushing Knee & Elbow Keepout",
      difficulty: "Hard ★★★★☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "A legendary Muay Thai champion struck by lightning at age 12, gaining inhuman physique and electrical tattoo markings. Coerced into underground fights to protect his family from corrupt military captors, Fahkumram unleashes devastating kicks.",
      pros: ["Massive attack reach on knees, elbows, and low kicks", "Chargeable guard break strikes at the wall", "Fierce counter-hit confirm strings (3,1, 1,2, b+1)", "Devastating wall splat and floor break damage"],
      cons: ["Large hurtbox susceptible to extended juggle routes", "Linear charge attacks vulnerable to SSR sidewalk"],
      ratings: { offense: 96, defense: 86, range: 98, execution: 80, movement: 82, throw: 80 },
      top5: [
        { cmd: "3, 1", role: "Long Range Mid-High", startup: "i14", block: "-6", dmg: 26, desc: "Premier mid check with enormous forward reach" },
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Safe mid elbow that halts ducking" },
        { cmd: "db+4", role: "Low Shin Kick", startup: "i20", block: "-14", dmg: 20, desc: "Heavy low kick that forces crouch at +4" },
        { cmd: "f,f+3", role: "Approaching Flying Knee", startup: "i16", block: "-4", dmg: 26, desc: "High-flying knee that causes massive wall splats" },
        { cmd: "b+1", role: "Counter-Hit Elbow", startup: "i15", block: "-7", dmg: 22, desc: "Safe mid elbow that crumple-launches on Counter Hit" }
      ],
      gameplan: "Control space with 3,1 and db+4 shin kicks. Push opponents into the wall with f,f+3 flying knees. Charge heavy strikes to break their guard.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / uf+4",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "f+2, 1", dmg: 26, adv: "+4" },
        { frame: "15f", move: "df+2", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+3", dmg: 24, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+3", startup: "i16", reach: "Far", dmg: 26, note: "Long range flying knee" },
        { move: "df+2", startup: "i15", reach: "Far", dmg: 22, note: "Long reach mid launch" }
      ],
      stances: ["Muay Thai Clinch", "Ram Muay"],
      heat_breakdown: "Electrifies his lightning tattoos, turning all wall charge strikes into guaranteed unblockable guard breaks.",
      stage_synergy: "Deadly on walled arenas where knee strikes smash through barriers."
    },

    kunimitsu: {
      name: "Kunimitsu",
      title: "The Fox Blade",
      japanese_name: "州光",
      country: "Japan",
      country_flag: "🇯🇵",
      style: "Manji Ninjutsu & Dagger Arts",
      height: "160 cm (5'3\")",
      weight: "47 kg (104 lbs)",
      age: "19",
      blood_type: "O",
      status: "Second-Generation Fox Mask Thief",
      archetype: "Aerial Kunai / Setsunagake Dashes",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The second-generation thief donning the sacred fox mask. Seeking to heal her ailing mother by stealing Yoshimitsu's enchanted demon blade, Kunimitsu darts across the arena with aerial kunai throws, spatial dashes, and surgical dagger slashes.",
      pros: ["Full-screen kunai projectile pressure (qcf+2)", "Setsunagake forward dashes create unseeable low/mid 50/50s", "Exceptional aerial mobility and teleport escapes", "Fast standing and crouch whiff punishers"],
      cons: ["Linear kunai throws can be sidestepped or ducked at distance", "Low health scaling on basic trades"],
      ratings: { offense: 96, defense: 88, range: 94, execution: 80, movement: 96, throw: 74 },
      top5: [
        { cmd: "qcf+2", role: "Kunai Dagger Throw", startup: "i15", block: "-12", dmg: 22, desc: "Full-screen dagger projectile; launches into combo on hit" },
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid poke with Setsunagake cancel" },
        { cmd: "db+3", role: "Low Shin Slash", startup: "i17", block: "-12", dmg: 15, desc: "Safe low slash into stance at +4" },
        { cmd: "f,f+2", role: "Approaching Slash", startup: "i15", block: "-8", dmg: 24, desc: "High-speed dagger thrust with huge forward reach" },
        { cmd: "b+2", role: "Safe Mid Check", startup: "i14", block: "-6", dmg: 20, desc: "Safe mid strike that launches on Counter Hit" }
      ],
      gameplan: "Harass from full screen with qcf+2 kunai throws. Use Setsunagake dashes to close in for unseeable low sweeps or mid dagger launches.",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / qcf+2",
      standing_punish: [
        { frame: "10f", move: "1, 2, 2", dmg: 24, adv: "+6" },
        { frame: "12f", move: "f+2, 3", dmg: 26, adv: "+4" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "13f", move: "WS+1, 2", dmg: 26, adv: "+8" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "qcf+2 (Kunai)", startup: "i15", reach: "Full-Screen", dmg: 22, note: "Longest whiff punisher" },
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 24, note: "Fast dagger dash" }
      ],
      stances: ["Setsunagake (KAT)", "Tenchi Ruten"],
      heat_breakdown: "Empowers kunai daggers with explosive elemental burst damage that shatters guard on block.",
      stage_synergy: "Excels on open infinite arenas where full-screen projectiles dominate."
    },

    "miary-zo": {
      name: "Miary Zo",
      title: "The Malagasy Gale",
      japanese_name: "ミアリ・ゾ",
      country: "Madagascar",
      country_flag: "🇲🇬",
      style: "Moraingy (Traditional Malagasy Kickboxing)",
      height: "172 cm (5'8\")",
      weight: "62 kg (137 lbs)",
      age: "22",
      blood_type: "B",
      status: "Island Coastal Champion",
      archetype: "Sweeping Arc Strikes / Kinetic Momentum",
      difficulty: "Medium ★★★☆☆",
      weak_side: "SSL (Weak to Sidestep Left)",
      lore: "A coastal champion representing Madagascar's traditional bare-knuckle Moraingy martial arts. Combining sweeping rotational roundhouse kicks with dynamic kinetic momentum, Miary Zo enters the international arena to bring glory to her island homeland.",
      pros: ["Rotational momentum stance grants continuous plus frames", "Wide sweeping low arcs that track opponent sidesteps", "High burst damage on kinetic counter-hits", "Fluid back-sway evasions"],
      cons: ["Linear straight punches can be sidestepped to SSL", "Requires momentum rhythm management to sustain peak damage"],
      ratings: { offense: 92, defense: 86, range: 90, execution: 78, movement: 92, throw: 76 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid poke with rotational momentum transition" },
        { cmd: "f,f+3", role: "Gale Axe Kick", startup: "i16", block: "-4", dmg: 24, desc: "Long range descending kick that wall splats" },
        { cmd: "db+3", role: "Sweeping Arc Low", startup: "i18", block: "-13", dmg: 17, desc: "Wide tracking low sweep that catches sidestepping" },
        { cmd: "b+1+2", role: "Heavy Elbow Thrust", startup: "i15", block: "-9", dmg: 28, desc: "Knocks down and splats from mid-range" },
        { cmd: "3, 2", role: "Hit-Confirm String", startup: "i14", block: "-6", dmg: 28, desc: "Fast kick-punch combo that leads into aerial juggle" }
      ],
      gameplan: "Control the mid-range with sweeping Moraingy kicks. Catch sidesteps with db+3. When opponent freezes, rush in with Gale Axe Kick (f,f+3).",
      launcher: "df+2 (Mid Launcher, i15, -12 OB) / uf+4",
      standing_punish: [
        { frame: "10f", move: "1, 2", dmg: 18, adv: "+7" },
        { frame: "12f", move: "f+2, 1", dmg: 26, adv: "+4" },
        { frame: "15f", move: "df+2", dmg: 20, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+3", startup: "i16", reach: "Far", dmg: 24, note: "Long range axe kick" },
        { move: "df+2", startup: "i15", reach: "Medium", dmg: 20, note: "Standard mid launch" }
      ],
      stances: ["Moraingy Whirlwind", "Gale Step"],
      heat_breakdown: "Channels oceanic kinetic energy into all roundhouse kicks, adding massive guard pushback.",
      stage_synergy: "Excels on open island stages like Yakushima where lateral sweeping kicks dominate."
    },

    "roger-jr": {
      name: "Roger Jr.",
      title: "The Bounding Brawler",
      japanese_name: "ロジャーJr.",
      country: "Australia",
      country_flag: "🇦🇺",
      style: "Commando Boxing & Kangaroo Agility",
      height: "160 cm (5'3\")",
      weight: "80 kg (176 lbs)",
      age: "3",
      blood_type: "Marsupial",
      status: "Boxing Champion & Mother-Joey Duo",
      archetype: "Low Box / Tail Spring Launches",
      difficulty: "Easy ★★☆☆☆",
      weak_side: "SSR (Weak to Sidestep Right)",
      lore: "The feisty kangaroo duo fighting out of Australia. With Mama Kangaroo commanding the footwork and Joey coordinating rapid-fire boxing jabs from her pouch, Roger Jr. bounds across the tournament to teach bullies a lesson with marsupial power.",
      pros: ["Tail spring launches bypass low and mid attacks", "Fast command boxing jabs with high hitboxes", "Deceptive low tail sweeps with knockdown oki", "Entertaining, unpredictable acrobatics"],
      cons: ["Short punch reach on standard jabs", "Slightly unusual hurtbox timings"],
      ratings: { offense: 90, defense: 86, range: 82, execution: 70, movement: 90, throw: 82 },
      top5: [
        { cmd: "df+1", role: "Fast Mid Check", startup: "i13", block: "-1", dmg: 13, desc: "Fast mid boxing poke to check ducking" },
        { cmd: "uf+4", role: "Tail Spring Hopkick", startup: "i15", block: "-13", dmg: 22, desc: "Springs off her tail to deliver a high-flying launch" },
        { cmd: "db+3", role: "Tail Sweep Harass", startup: "i18", block: "-13", dmg: 16, desc: "Safe low tail sweep that knocks down on Counter Hit" },
        { cmd: "f,f+2", role: "Windmill Glove Strike", startup: "i15", block: "-8", dmg: 24, desc: "Fast approaching glove punch that wall splats" },
        { cmd: "1, 2, 1", role: "Fast Boxing Barrage", startup: "i10", block: "-4", dmg: 26, desc: "10f standing punish string with plus frames" }
      ],
      gameplan: "Hop over low pokes with tail springs (uf+4). Interrupt opponent rushdowns with fast boxing barrages. Sweep feet with db+3.",
      launcher: "uf+4 (Tail Spring Hopkick, i15, -13 OB) / df+2",
      standing_punish: [
        { frame: "10f", move: "1, 2, 1", dmg: 26, adv: "+6" },
        { frame: "12f", move: "f+2, 2", dmg: 26, adv: "+4" },
        { frame: "15f", move: "uf+4", dmg: 22, adv: "Full Launch" }
      ],
      ws_punish: [
        { frame: "11f", move: "WS+4", dmg: 16, adv: "+5" },
        { frame: "14f", move: "WS+1", dmg: 22, adv: "+7" },
        { frame: "15f", move: "WS+2", dmg: 22, adv: "Full Launch" }
      ],
      whiff_punish: [
        { move: "f,f+2", startup: "i15", reach: "Far", dmg: 24, note: "Fast forward glove strike" },
        { move: "uf+4", startup: "i15", reach: "Medium", dmg: 22, note: "Tail spring launch" }
      ],
      stances: ["Kangaroo Bounce", "Pouch Ready"],
      heat_breakdown: "Empowers kangaroo tail jumps with ground pound shockwaves that stagger blocking opponents.",
      stage_synergy: "Great on all arena stages where fast tail bounces keep rivals guessing."
    }
  };

  // Attach to global window
  window.FIGHTER_DOSSIERS = DOSSIERS;

  // Helper accessor with safe fallback
  window.getFighterDossier = function (slug) {
    if (!slug) return DOSSIERS.jin;
    const clean = String(slug).toLowerCase().trim();
    if (DOSSIERS[clean]) return DOSSIERS[clean];
    // Return generic fallback based on first matching or Jin
    return Object.assign({}, DOSSIERS.jin, {
      name: clean.charAt(0).toUpperCase() + clean.slice(1),
      title: "Iron Fist Competitor",
      style: "Martial Arts",
      country: "Global",
      country_flag: "🌐"
    });
  };
})();
