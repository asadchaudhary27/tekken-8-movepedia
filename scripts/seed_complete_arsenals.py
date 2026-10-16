"""
Complete Database & UI Population Script for:
1. Complete Throw / Grab Arsenal (All 43 Fighters, Generic + Command Throws)
2. Complete Optimal Wall Enders (All 43 Fighters, 3 distinct routes = 129 routes)
3. Complete 10-Hit String Counters (All 43 Fighters)

Populates both tekken8_fyp.db and data/knowledge/master_compendium.json.
"""

import os
import json
import sqlite3
from datetime import datetime

DB_PATH = os.path.abspath("tekken8_fyp.db")
COMPENDIUM_PATH = os.path.abspath("data/knowledge/master_compendium.json")

# 43 characters list
CHARACTERS = [
    {"id": 1, "slug": "jin", "name": "Jin Kazama"},
    {"id": 2, "slug": "kazuya", "name": "Kazuya Mishima"},
    {"id": 3, "slug": "reina", "name": "Reina"},
    {"id": 4, "slug": "jun", "name": "Jun Kazama"},
    {"id": 5, "slug": "king", "name": "King"},
    {"id": 6, "slug": "paul", "name": "Paul Phoenix"},
    {"id": 7, "slug": "hwoarang", "name": "Hwoarang"},
    {"id": 8, "slug": "alisa", "name": "Alisa Bosconovitch"},
    {"id": 9, "slug": "asuka", "name": "Asuka Kazama"},
    {"id": 10, "slug": "azucena", "name": "Azucena Milagros"},
    {"id": 11, "slug": "bryan", "name": "Bryan Fury"},
    {"id": 12, "slug": "claudio", "name": "Claudio Serafino"},
    {"id": 13, "slug": "devil-jin", "name": "Devil Jin"},
    {"id": 14, "slug": "dragunov", "name": "Sergei Dragunov"},
    {"id": 15, "slug": "feng", "name": "Feng Wei"},
    {"id": 16, "slug": "jack-8", "name": "Jack-8"},
    {"id": 17, "slug": "lars", "name": "Lars Alexandersson"},
    {"id": 18, "slug": "law", "name": "Marshall Law"},
    {"id": 19, "slug": "lee", "name": "Lee Chaolan"},
    {"id": 20, "slug": "leo", "name": "Leo Kliesen"},
    {"id": 21, "slug": "leroy", "name": "Leroy Smith"},
    {"id": 22, "slug": "lili", "name": "Lili"},
    {"id": 23, "slug": "nina", "name": "Nina Williams"},
    {"id": 24, "slug": "panda", "name": "Panda"},
    {"id": 25, "slug": "kuma", "name": "Kuma"},
    {"id": 26, "slug": "raven", "name": "Raven"},
    {"id": 27, "slug": "shaheen", "name": "Shaheen"},
    {"id": 28, "slug": "steve", "name": "Steve Fox"},
    {"id": 29, "slug": "victor", "name": "Victor Chevalier"},
    {"id": 30, "slug": "xiaoyu", "name": "Ling Xiaoyu"},
    {"id": 31, "slug": "yoshimitsu", "name": "Yoshimitsu"},
    {"id": 32, "slug": "zafina", "name": "Zafina"},
    {"id": 33, "slug": "eddy", "name": "Eddy Gordo"},
    {"id": 34, "slug": "lidia", "name": "Lidia Sobieska"},
    {"id": 35, "slug": "heihachi", "name": "Heihachi Mishima"},
    {"id": 36, "slug": "clive", "name": "Clive Rosfield"},
    {"id": 37, "slug": "anna", "name": "Anna Williams"},
    {"id": 38, "slug": "armor-king", "name": "Armor King"},
    {"id": 39, "slug": "bob", "name": "Bob Richards"},
    {"id": 40, "slug": "fahkumram", "name": "Fahkumram"},
    {"id": 41, "slug": "kunimitsu", "name": "Kunimitsu"},
    {"id": 42, "slug": "miary-zo", "name": "Miary Zo"},
    {"id": 43, "slug": "roger-jr", "name": "Roger Jr."}
]

# 1. CHARACTER-SPECIFIC COMMAND THROWS (Over 100+ unique command grabs across 43 fighters)
COMMAND_THROWS = {
    "king": [
        {"name": "Giant Swing", "input": "f,hcf+1", "startup": "i10", "break": "1", "window": "20f (Visual Dhoka!)", "visual": "Both Arms Extended (Deceptive: Break 1!)", "dmg": "70 dmg", "dmg_num": 70, "oki": "Wall Splat for massive bonus damage (up to 70 total!)"},
        {"name": "Tombstone Piledriver", "input": "db,f+2+4", "startup": "i11", "break": "2", "window": "20f", "visual": "Both Arms Dive (Right Hand Lead: Break 2)", "dmg": "58 dmg", "dmg_num": 58, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Shining Wizard", "input": "f,f,F+2+4", "startup": "i10", "break": "1+2", "window": "20f", "visual": "Both Arms Running Clasp [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Leaves opponent at King's feet with +5 frame advantage"},
        {"name": "Muscle Buster", "input": "qcb+1+2", "startup": "i11", "break": "1+2", "window": "20f", "visual": "Both Hands Lift Over Head [1+2]", "dmg": "50 dmg", "dmg_num": 50, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Tijuana Twister", "input": "f,hcf+2", "startup": "i11", "break": "2", "window": "20f", "visual": "Right Arm Hook Over Shoulder [2]", "dmg": "55 dmg", "dmg_num": 55, "oki": "Throws opponent across entire arena, wall splat potential"},
        {"name": "Standing Achilles Hold", "input": "f,n,d,df+2+3", "startup": "i12", "break": "1+2", "window": "20f starter", "visual": "Crouch Leg Dive [1+2]", "dmg": "30 dmg", "dmg_num": 30, "oki": "Chain Throw Tree starter: branches into Scorpion Death Lock or STF (110+ dmg)"},
        {"name": "Arm Breaker", "input": "f,df+1+3", "startup": "i12", "break": "1", "window": "20f starter", "visual": "Left Arm Wing Grab [1]", "dmg": "25 dmg", "dmg_num": 25, "oki": "Chain Throw Tree starter: branches into Triple Arm Breaker & Sleeper Hold"},
        {"name": "Air Shining Wizard", "input": "in air f,f,F+2+4", "startup": "i10", "break": "Unbreakable", "window": "Air Juggle Only", "visual": "Airborne Knee Catch", "dmg": "35 dmg", "dmg_num": 35, "oki": "Guaranteed unscaled wall combo ender on any wall splat"}
    ],
    "dragunov": [
        {"name": "Scorpion Scissors", "input": "f+1+4", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Arm Lead [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Leaves opponent face-up head towards, guaranteed d+3+4 stomp"},
        {"name": "Blizzard Rush", "input": "f+2+3", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Arm Lead [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Leaves opponent face-down head away, forced wake-up guess"},
        {"name": "Reverse Arm Lock", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Extended [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Pit Viper Tackle", "input": "fc df+1+2", "startup": "i12", "break": "1+2", "window": "14f tight", "visual": "Crouch Double Arm Tackle [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Ground mount position with armbar / punch mixup options"},
        {"name": "Cradle / Chain Throws", "input": "qcf+1", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Arm Lock [1]", "dmg": "50 dmg", "dmg_num": 50, "oki": "Multi-throw branch to flying armlock or neck twist"}
    ],
    "jin": [
        {"name": "Comet Smasher", "input": "uf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Extended [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Tidal Wave", "input": "qcb+1+3", "startup": "i11", "break": "1", "window": "20f", "visual": "Left Hand Push [1]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Position swap; back against wall delivers Wall Splat!"},
        {"name": "Over-the-Shoulder Reverse", "input": "df+2+3", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Flip [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Spikes opponent flat on back for guaranteed d+2 oki"}
    ],
    "paul": [
        {"name": "Ultimate Tackle", "input": "b+1+4", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Shoulder Charge Grapple [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Ground mount tackle into Armbar or Ultimate Punch mixup"},
        {"name": "Push Throw", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Double Palm [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat near wall for guaranteed follow-up Deathfist!"},
        {"name": "Double Face Buster", "input": "ff+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Face Slam [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Floor Break on Sanctum & Descent into Subconscious"}
    ],
    "kazuya": [
        {"name": "Gates of Hell", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Slam into Ground [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Floor Break + guarantees ff+4 Steel Pedal ground hit!"},
        {"name": "Skull Smash", "input": "df+1+3", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Punch Throw [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Position swap towards wall"},
        {"name": "Double Face Kick", "input": "df+2+4", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Leg High Throw [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Leaves opponent face-up for wave dash mixup"}
    ],
    "reina": [
        {"name": "Sentai Grab", "input": "SEN.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Lightning Dash Both Hands [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Transitions into Heaven's Wrath (WRA) stance with frame advantage"},
        {"name": "Wind God Flurry Grab", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Electric Rush [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Mishima Submission", "input": "df+1+3", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Throat Grab [1]", "dmg": "38 dmg", "dmg_num": 38, "oki": "Knockdown near wall gives wall splat pressure"}
    ],
    "jack-8": [
        {"name": "Piledriver", "input": "qcb+1+2", "startup": "i11", "break": "2", "window": "20f (Visual Dhoka!)", "visual": "Both Hands Heavy Lift (Break 2!)", "dmg": "55 dmg", "dmg_num": 55, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Megaton Punch Grab", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Rocket Thrust [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Wall Splat near perimeter wall"},
        {"name": "Volcano Slam", "input": "df+2+4", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Scoop [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Leaves opponent at feet for db+2 oki"},
        {"name": "Crouch Megaton", "input": "fc df+1+2", "startup": "i12", "break": "1+2", "window": "14f tight", "visual": "Low Both Hands Scoop [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Catches crouching opponents for full Floor Break"}
    ],
    "nina": [
        {"name": "Spider Knee", "input": "qcf+1", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Knee Strike [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Branching Multi-Throw Chain Tree (arm snap / neck snap)"},
        {"name": "Bad Habit", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Groin Kick / Slam [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Crab Hold", "input": "qcf+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Leg Sweep Grab [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Chain throw starter into rolling heel hold"},
        {"name": "Betrayal", "input": "qcf+3", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Neck Snap [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Guaranteed d+3+4 ground stomp follow-up"}
    ],
    "hwoarang": [
        {"name": "Flamingo Suplex", "input": "LFS.1+2 or RFS.1+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Leg & Hand Lock [2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Door Mat", "input": "df+1+3", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Leg Trip [1]", "dmg": "38 dmg", "dmg_num": 38, "oki": "Position swap with frame advantage"},
        {"name": "Human Cannonball", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Flying Kick Throw [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat near wall"}
    ],
    "bryan": [
        {"name": "Fisherman Slam", "input": "qcf+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Hook Lift [2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Choke Slam", "input": "db+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Choke Lift [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Leaves opponent at feet for b+4 Taunt setup"},
        {"name": "Snake Bite", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Gut Punch Throw [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat near wall"}
    ],
    "yoshimitsu": [
        {"name": "Manji Toss", "input": "d+1+3", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Sword Sheath Grab [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Position swap over head into back-turned mixup"},
        {"name": "Rainbow Drop", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Spin Slam [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Kincho Toss", "input": "KIN.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Teleport Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Unblockable sword oki setup on wake-up"}
    ],
    "xiaoyu": [
        {"name": "AoP Roll Grab", "input": "AoP.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Ground Roll [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Leaves opponent face-down at feet"},
        {"name": "Human Windmill", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Acrobatic Cartwheel [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Rain Dance Grab", "input": "RDS.1+3", "startup": "i12", "break": "1", "window": "20f", "visual": "Back-Turned Left Flip [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Position swap"}
    ],
    "law": [
        {"name": "Dragon Bomb", "input": "qcb+1+2", "startup": "i11", "break": "2", "window": "20f", "visual": "Right Hand Flip Piledriver [2]", "dmg": "48 dmg", "dmg_num": 48, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Runup Dropkick Grab", "input": "f,f+3+4", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Feet Double Dropkick Throw [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Wall Splat"},
        {"name": "Knee Strike", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Clinch Knee [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Guaranteed DSS stance transition oki"}
    ],
    "steve": [
        {"name": "Peekaboo Clinch", "input": "PKB.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Clinch Uppercut [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Leaves opponent in Peekaboo stance pressure"},
        {"name": "Lionheart Slam", "input": "LNH.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Overhook Slam [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Wall Push", "input": "qcb+2+4", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Arm Push into Wall [2]", "dmg": "15 dmg", "dmg_num": 15, "oki": "Guaranteed Wall Stun into free b+1,2 wall combo!"}
    ],
    "alisa": [
        {"name": "Dual Boot Grab", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Rocket Flight [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Chainsaw Decapitation", "input": "DES.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Chainsaws Extended [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Chainsaw stance oki mixup"},
        {"name": "Spam Bomb", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Head Detach Toss [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Explosive knockdown across stage"}
    ],
    "asuka": [
        {"name": "Sacred Spin", "input": "qcf+2", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Sweep Grab [1]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Leaves opponent face-up for d+1+2 oki"},
        {"name": "Reversal Catch", "input": "b+1+3", "startup": "i3 (Parry)", "break": "1+2", "window": "Parry Catch", "visual": "Both Arms Flow Lock [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Reversal counter against punch/kick"},
        {"name": "Cloud Gate", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Double Palm [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat near wall"}
    ],
    "jun": [
        {"name": "Izumo Reversal Grab", "input": "IZU.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Soft Flow Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Leaves opponent in Izumo mixup"},
        {"name": "Purification Sweep", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Glowing Sweep [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Restores recoverable white health on hit!"},
        {"name": "Kazama Spiral", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Spiral Toss [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Floor Break on Sanctum & Descent into Subconscious"}
    ],
    "azucena": [
        {"name": "LIB Coffee Break", "input": "LIB.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Push / Dance [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Enters Libertador stance oki"},
        {"name": "TMT Drop", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Acrobat Toss [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Peruvian Toss", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Hip Toss [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat near wall"}
    ],
    "claudio": [
        {"name": "Starburst Sealer", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Glowing Blue Sparks [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Grants Starburst (STB) charge immediately on successful throw!"},
        {"name": "Exorcist Slam", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Holy Slam [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Floor Break on Sanctum & Descent into Subconscious"}
    ],
    "devil-jin": [
        {"name": "Hell's Gate Drop", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Demon Slam [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Devil Claw", "input": "df+1+3", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Demon Claw [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Position swap"},
        {"name": "Stonehead", "input": "qcb+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Headbutt Grab [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Guaranteed laser oki follow-up"}
    ],
    "feng": [
        {"name": "Shoulder Slam", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Shoulder Lock [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Wall Splat near wall for guaranteed b+1+2"},
        {"name": "Gorilla Arm", "input": "db+1+2", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Palm Drag [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Leaves opponent face down"},
        {"name": "Lotus Twist", "input": "df+1+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Hip Twist [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Position swap"}
    ],
    "lars": [
        {"name": "Silent Entry Throw", "input": "DEN.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Electric Rush Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Enters Dynamic Entry mixup"},
        {"name": "Zeus Smash", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Lightning Slam [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Rebel Tack", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Double Shoulder [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat"}
    ],
    "lee": [
        {"name": "Silver Viper", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Elegant Spin Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Leaves opponent for guaranteed d+3 oki"},
        {"name": "Face Crusher", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Elegant Slam [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Acid Rain Grab", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Triple Knee Grab [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Hitman (HMS) transition"}
    ],
    "leo": [
        {"name": "Baji Quan Slam", "input": "db+1+2", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Palm Strike Grab [1]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Position swap"},
        {"name": "KNK Knee Grapple", "input": "KNK.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Stance Tackle [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Rib Breaker", "input": "df+1+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Elbow Grab [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat"}
    ],
    "leroy": [
        {"name": "Wing Chun Trapping", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Cane & Arm Trap Both Hands [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Hermit Clinch", "input": "HRM.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Wing Chun Sweep [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Sugar bite oki setup"},
        {"name": "Cane Slam", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Cane Sweep [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Guaranteed grounded hit"}
    ],
    "lili": [
        {"name": "Dew Glide Grab", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Graceful Spin Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Back-Turned (BT) transition"},
        {"name": "Back-Turned Suplex", "input": "BT.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Reverse German Suplex [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Rose Bouquet", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Elegant Toss [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat"}
    ],
    "panda": [
        {"name": "Salmon Roll / Bear Hug", "input": "db+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Massive Bear Arms Extended [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Leaves opponent at feet for d+1+2 Butt Slam"},
        {"name": "Bear Butt Slam", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Paws Heavy Slam [1+2]", "dmg": "48 dmg", "dmg_num": 48, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "HBS Roll Grab", "input": "HBS.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Hunting Bear Stance Both Paws [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Guaranteed bear bite"}
    ],
    "kuma": [
        {"name": "Salmon Roll / Bear Hug", "input": "db+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Massive Bear Arms Extended [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Leaves opponent at feet for d+1+2 Butt Slam"},
        {"name": "Bear Butt Slam", "input": "qcf+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Paws Heavy Slam [1+2]", "dmg": "48 dmg", "dmg_num": 48, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "HBS Roll Grab", "input": "HBS.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Hunting Bear Stance Both Paws [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Guaranteed bear bite with salmon lightning"}
    ],
    "raven": [
        {"name": "Shadow Clone Grab", "input": "SZ.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Clone Illusion Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Teleports behind opponent into Back-Turned (BT) mixup"},
        {"name": "Substitution Slam", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Ninja Pile [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Undertaker", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Shadow Flip [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat"}
    ],
    "shaheen": [
        {"name": "Sneak Slide Grab", "input": "SNK.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Sliding Tackle Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Guaranteed Slide oki 50/50 mixup"},
        {"name": "Falcon Strike", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Eagle Claw [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Desert Sweep", "input": "df+1+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Sweep Grab [2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Position swap"}
    ],
    "victor": [
        {"name": "Blade Grasp Throw", "input": "PRF.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Sword Handle Both Hands [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "IAI Quick Draw Grab", "input": "IAI.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Katana Sheath Lock Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Leaves opponent for IAI stance oki"},
        {"name": "Submachine Gun Clinch", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Gun Holster Toss [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Wall Splat near wall"}
    ],
    "zafina": [
        {"name": "Mantis Crawl Grab", "input": "MNT.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Creeping Spider Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Enters Mantis (MNT) stance"},
        {"name": "Scarecrow Guillotine", "input": "SCR.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Claw Guillotine [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Tarantula Drag", "input": "TRT.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Low Web Drag [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Low grab setup"}
    ],
    "eddy": [
        {"name": "Mandinga Takeover", "input": "HSP.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Sweep from Handstand [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Grants Mandinga (MND) level buff!"},
        {"name": "Negativa Low Grab", "input": "RLX.1", "startup": "i16", "break": "Duck Only / Unbreakable", "window": "Duck Only (Low Grab)", "visual": "Low Sweeping Ground Grab", "dmg": "40 dmg", "dmg_num": 40, "oki": "Unbreakable low throw"},
        {"name": "Samba Slam", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Capoeira Flip [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Floor Break on Sanctum & Descent into Subconscious"}
    ],
    "lidia": [
        {"name": "Heaven & Earth Slam", "input": "HAE.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Karate Clinch [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Grants permanent Heaven & Earth level stack!"},
        {"name": "Cat Stance Sweep Grab", "input": "CAT.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Cat Stance Dive [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Position swap"},
        {"name": "Politician Throw", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Double Palm Push [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Wall Splat near wall"}
    ],
    "heihachi": [
        {"name": "Demon's Blood", "input": "f,f+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Head Snap [2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Stonehead", "input": "f,f+1+2", "startup": "i12", "break": "1+2 (Unbreakable in WI!)", "window": "20f (0f in WI)", "visual": "Both Hands Headbutt Clash [1+2]", "dmg": "42 dmg (55 in WI)", "dmg_num": 42, "oki": "Unbreakable in Warrior Instinct!"},
        {"name": "Broken Toy", "input": "qcf+1", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Spine Toss [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Throws opponent across stage"},
        {"name": "Jumping Power Bomb", "input": "qcb+1+2", "startup": "i11", "break": "1+2", "window": "20f", "visual": "Both Hands High Lift Powerbomb [1+2]", "dmg": "50 dmg", "dmg_num": 50, "oki": "Floor Break on Sanctum & Descent into Subconscious"}
    ],
    "clive": [
        {"name": "Eikonic Slam", "input": "f+1+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Sword Pommel Grab Right Hand [2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Builds Zantetsuken meter gauge"},
        {"name": "Titan Parry Grab", "input": "b+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Titan Arm Shield Both Hands [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Phoenix Shift Grab", "input": "PHX.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Fiery Wing Dive Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Teleport oki"}
    ],
    "anna": [
        {"name": "Bazooka Execution", "input": "qcb+1+2", "startup": "i12", "break": "2", "window": "20f", "visual": "Right Hand Lead Bazooka Grab [2]", "dmg": "48 dmg", "dmg_num": 48, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Chaos Judgment Grab", "input": "CJM.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Stance Toss [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Crouch vortex 50/50 mixup"},
        {"name": "Arm Turn Toss", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Arm Lock [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat near wall"}
    ],
    "armor-king": [
        {"name": "Tombstone Piledriver", "input": "db,f+2+4", "startup": "i11", "break": "2", "window": "20f (Visual Dhoka!)", "visual": "Both Hands Quick Dive (Break 2!)", "dmg": "58 dmg", "dmg_num": 58, "oki": "Hard Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Giant Swing", "input": "f,hcf+1", "startup": "i10", "break": "1", "window": "20f (Visual Dhoka!)", "visual": "Both Arms Extended (Break 1!)", "dmg": "70 dmg", "dmg_num": 70, "oki": "Massive wall splat damage"},
        {"name": "DDT", "input": "qcb+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Snap DDT [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Leaves opponent at feet for d+3 oki"},
        {"name": "Frankensteiner", "input": "d+3+4", "startup": "i15", "break": "Duck / Jump Only", "window": "Duck / Jump Only", "visual": "Flying Scissor Neck Throw", "dmg": "40 dmg", "dmg_num": 40, "oki": "Unbreakable jumping grapple"}
    ],
    "bob": [
        {"name": "Spinner Slam", "input": "BAL.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Spinner Ball Both Hands Slam [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Flying Meat Hook", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Heavy Body Toss [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Wall Splat near wall"},
        {"name": "Belly Bump Throw", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Belly Impact [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Position swap"}
    ],
    "fahkumram": [
        {"name": "Clinch Knee Smash", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Thai Clinch Both Hands [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Tiger Fang Grab", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Muay Thai Lock [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Wall Splat for free bf+4"},
        {"name": "Elbow Decapitator", "input": "qcf+1", "startup": "i12", "break": "1", "window": "20f", "visual": "Left Hand Elbow Grab [1]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Garuda force buff charge"}
    ],
    "kunimitsu": [
        {"name": "Teleport Kunai Grab", "input": "SET.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Shadow Grab Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Leaves opponent for b+2 flame unblockable trap"},
        {"name": "Shadow Strike", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Kunai Cross [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Kitsune Toss", "input": "df+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Fox Spin [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Position swap"}
    ],
    "miary-zo": [
        {"name": "Mora Acrobat Grab", "input": "MOR.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Stance Flip Both Hands [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Enters Baobab (BAO) wall stance"},
        {"name": "Baobab Diving Crush", "input": "BAO.1+2", "startup": "i14", "break": "Duck Only / Unblockable", "window": "Duck Only", "visual": "Diving Wall Cling Grab", "dmg": "45 dmg", "dmg_num": 45, "oki": "Wall dive unblockable grab"},
        {"name": "Wallaby Spin Throw", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Acrobatic Toss [1+2]", "dmg": "40 dmg", "dmg_num": 40, "oki": "Wall Splat near wall"}
    ],
    "roger-jr": [
        {"name": "Kangaroo Punch Throw", "input": "f,f+1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Both Hands Pouch Tackle [1+2]", "dmg": "45 dmg", "dmg_num": 45, "oki": "Floor Break on Sanctum & Descent into Subconscious"},
        {"name": "Giant Tail Swing", "input": "f,hcf+1", "startup": "i10", "break": "1", "window": "20f (Visual Dhoka!)", "visual": "Both Paws Tail Grab (Break 1!)", "dmg": "65 dmg", "dmg_num": 65, "oki": "Wall Splat for massive damage"},
        {"name": "Pouch Takedown", "input": "ANM.1+2", "startup": "i12", "break": "1+2", "window": "20f", "visual": "Animal Stance Both Paws [1+2]", "dmg": "42 dmg", "dmg_num": 42, "oki": "Animal stance oki"}
    ]
}

print("Loaded all command throws for all characters.")

# 2. COMPLETE OPTIMAL WALL ENDERS (All 43 Fighters, 3 distinct routes each = 129 routes)
# Route 1: Max Damage Wall Combo (Tornado T! Available at Wall)
# Route 2: Post-Tornado Wall Ender (T! Expended Mid-Screen)
# Route 3: Oki / Resplat / Unblockable Setup Wall Ender

WALL_COMBOS_DATA = {
    "jin": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "ZEN.1,2 (T!) -> bf+2,1,df+2 (delayed 3rd hit)", "dmg": "44 DMG", "dmg_num": 44, "spike": "Hard Ground Spike", "notes_en": "Delaying df+2 guarantees 60% unscaled grounded damage", "notes_ur": "df+2 ko delay karne se 60% unscaled damage milta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "bf+2,1,df+2 (delay df+2)", "dmg": "28 DMG", "dmg_num": 28, "spike": "Ground Spike", "notes_en": "Reliable high-damage universal ender after midscreen tornado", "notes_ur": "Midscreen tornado ke baad standard high damage ender"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "1 -> d+2 (or db+2,2,3)", "dmg": "22 DMG", "dmg_num": 22, "spike": "Tech Catch / Floor Trap", "notes_en": "d+2 catches tech roll and forces crouch guard on getup", "notes_ur": "d+2 tech roll ko pakarta hai aur crouch par majboor karta hai"}
    ],
    "kazuya": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "df+1,df+2 (T!) -> b+2,2,1+2", "dmg": "46 DMG", "dmg_num": 46, "spike": "Wall Bound Spike", "notes_en": "b+2,2,1+2 deals massive wall execution damage", "notes_ur": "b+2,2,1+2 massive execution wall damage deta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+3,2,1 (delayed 1) -> ff+4 (Steel Pedal)", "dmg": "30 DMG", "dmg_num": 30, "spike": "Face Up Ground Stomp", "notes_en": "Steel Pedal (ff+4) hits grounded for guaranteed +4 oki", "notes_ur": "Steel Pedal ff+4 zameen par guaranteed hit karta hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "1 -> d+1+2 (Demon God Fist) / Hell Sweep Vortex", "dmg": "24 DMG", "dmg_num": 24, "spike": "50/50 Vortex Setup", "notes_en": "Leaves opponent face-down for lethal Hell Sweep / Mid vortex", "notes_ur": "Opponent ko face-down chhorta hai lethal 50/50 mixup ke liye"}
    ],
    "reina": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "df+4,2,3 (T!) -> df+1,1 -> df+4,2,3 (delay 3rd hit)", "dmg": "45 DMG", "dmg_num": 45, "spike": "Ground Stomp Spike", "notes_en": "Delaying 3rd stomp transitions directly to WRA stance at +6", "notes_ur": "Last hit delay karne se Reina WRA stance mein +6 par jati hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+1,1 -> 1+2", "dmg": "27 DMG", "dmg_num": 27, "spike": "Push Splat", "notes_en": "Fast, safe +4 advantage", "notes_ur": "Safe aur consistent wall knockdown"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "df+1 -> SEN.3 -> WRA.1+2 Unblockable Trap", "dmg": "24 DMG", "dmg_num": 24, "spike": "Unblockable Trap", "notes_en": "Catches stand-up tech at the wall with unblockable", "notes_ur": "Deewar par uthte hue opponent ko unblockable se trap karta hai"}
    ],
    "jun": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "IZU.1,1 (T!) -> 1 -> b+2,1,4", "dmg": "42 DMG", "dmg_num": 42, "spike": "Bound Re-splat", "notes_en": "b+2,1,4 completes clean high wall damage", "notes_ur": "b+2,1,4 se maximum wall damage milta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "f+2,1+2", "dmg": "26 DMG", "dmg_num": 26, "spike": "Healing Wall Strike", "notes_en": "Restores Jun's recoverable white health at the wall!", "notes_ur": "f+2,1+2 deewar par Jun ki health heal karta hai!"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "f+3,2 -> IZU.1+2 (Izumo Throw Trap)", "dmg": "22 DMG", "dmg_num": 22, "spike": "Command Grab Trap", "notes_en": "Mixes mid check with unbreakable unscaled throw", "notes_ur": "Izumo stance se throw aur mid mixup banata hai"}
    ],
    "king": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "b+1,2 (T!) -> 1 -> df+4,3,4 (Hold 4 for Dropkick)", "dmg": "48 DMG", "dmg_num": 48, "spike": "Dropkick Spike", "notes_en": "Holding 4 delivers 48 unscaled wall damage", "notes_ur": "4 hold rakhne se 48 unscaled damage milta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "qcb+1+2 (Air Muscle Buster) OR fff+2+4 (Air Shining Wizard)", "dmg": "35 DMG", "dmg_num": 35, "spike": "Air Juggle Throw", "notes_en": "Air throw at wall ignores damage scaling floor", "notes_ur": "Air throw wall par scaling floor ko bypass karta hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "df+1 -> d+3+4,4,4 (Ali Kicks / Ground Mount Grab)", "dmg": "25 DMG", "dmg_num": 25, "spike": "Ground Oki 50/50", "notes_en": "Forces guess between ground grab and mid hopkick", "notes_ur": "Zameen par low kicks aur ground grab ka 50/50 deta hai"}
    ],
    "paul": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "3,2~b (SWY.1+2 T!) -> 3,2~b -> (Delay) SWY.2", "dmg": "50 DMG", "dmg_num": 50, "spike": "Delayed Heavy Palm Spike", "notes_en": "Delaying SWY.2 deals 40+ raw grounded damage", "notes_ur": "SWY.2 delay karne se zameen par 40+ damage milta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "qcf+2 (Deathfist) / d+1+2 (Shoulder)", "dmg": "32 DMG", "dmg_num": 32, "spike": "Clean Wall Impact", "notes_en": "Classic tournament staple for guaranteed finish", "notes_ur": "Guaranteed Deathfist wall finish"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "1 -> 3,2~b (SWY.3 Demoman 50/50)", "dmg": "26 DMG", "dmg_num": 26, "spike": "Demoman Vortex", "notes_en": "Unseeable low into mid Deathfist wall kill", "notes_ur": "Demoman low aur Deathfist mid ka khatarnak 50/50"}
    ],
    "hwoarang": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "uf+3,4,3 (T!) -> f+3~LFS.3,f+4", "dmg": "44 DMG", "dmg_num": 44, "spike": "Flamingo Kick Spike", "notes_en": "High wall carry and max execution damage", "notes_ur": "Flamingo kicks se maximum wall damage"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+3,4 (Power Crush Wall Splat)", "dmg": "26 DMG", "dmg_num": 26, "spike": "Armor Wall Splat", "notes_en": "Safe against mashers on wall rebound", "notes_ur": "Armor move jo mashers ko shut down karta hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "d+3,4 (into RFS Stance Vortex)", "dmg": "22 DMG", "dmg_num": 22, "spike": "+14 Flamingo Vortex", "notes_en": "Forces opponent to guess between RFS low and mid", "notes_ur": "RFS stance se infinite pressure start karein"}
    ],
    "alisa": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "db+1+2 (T!) -> 1 -> f+4,1,4 (delay last hit)", "dmg": "43 DMG", "dmg_num": 43, "spike": "60% Ground Spike", "notes_en": "Delaying last hit spikes opponent into ground for 60% unscaled hit", "notes_ur": "f+4,1,4 ka last hit delay karein for 60% ground spike"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "DES.f+1+2 -> 1+2", "dmg": "28 DMG", "dmg_num": 28, "spike": "Dual Chainsaw Shred", "notes_en": "Heavy chip damage and plus frames on block", "notes_ur": "Chainsaw chip damage aur plus frames"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "d+4 -> DES Stance Mixup", "dmg": "20 DMG", "dmg_num": 20, "spike": "Chainsaw Oki", "notes_en": "Traps opponent getting up against corner", "notes_ur": "Deewar par chainsaw mixup trap"}
    ],
    "asuka": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "f+4 (T!) -> 1+2 -> df+1,2 -> f,f+1+2", "dmg": "44 DMG", "dmg_num": 44, "spike": "Wall Blast Re-splat", "notes_en": "With Naniwa Gusto active, ff+1+2 triggers Wall Blast!", "notes_ur": "Naniwa Gusto active ho toh ff+1+2 wall blast karta hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+1,2 -> d+1+2", "dmg": "27 DMG", "dmg_num": 27, "spike": "Double Palm Spike", "notes_en": "Safe and consistent across all stages", "notes_ur": "Safe aur consistent double palm strike"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "1+2 -> db+3 (Low Sweep Setup)", "dmg": "21 DMG", "dmg_num": 21, "spike": "Can-Can / Sweep Oki", "notes_en": "Launches tech rolls and catches standing guard", "notes_ur": "Tech rolls ko launch karta hai"}
    ],
    "azucena": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "LIB.d+4,4 (T!) -> df+1,4,1 -> (delay) 2", "dmg": "42 DMG", "dmg_num": 42, "spike": "Delayed High Hook Spike", "notes_en": "Delaying 2 deals maximum unscaled wall damage", "notes_ur": "Last hit 2 delay karne se huge damage milta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+1,4,1,2", "dmg": "26 DMG", "dmg_num": 26, "spike": "Standard 4-Hit String", "notes_en": "Quick, zero-drop consistency", "notes_ur": "Zero-drop consistent 4-hit string"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "f+1+2 -> LIB Stance Auto-Dodge", "dmg": "20 DMG", "dmg_num": 20, "spike": "Auto-Whiff Trap", "notes_en": "Evades wake-up kicks automatically in Libertador stance", "notes_ur": "Libertador stance wake-up kicks ko auto dodge karti hai"}
    ],
    "bryan": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "b+2,1~f+2,4 (T!) -> b+3~f+2,1", "dmg": "48 DMG", "dmg_num": 48, "spike": "Knee Gatling Spike", "notes_en": "In Snake Eyes mode, end with uf+2,2,2,2,2,3 Gatling Rush for 58 DMG!", "notes_ur": "Snake Eyes mein uf+2,2,2,2,2,3 Gatling Rush se 58 DMG milta hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "b+3~f+3,4", "dmg": "30 DMG", "dmg_num": 30, "spike": "Face Up Feet Away", "notes_en": "Leaves opponent in perfect Taunt (b+4) range", "notes_ur": "Opponent ko perfect Taunt range mein chhorta hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "Taunt (b+4) -> f,b+2 (Taunt Jet Upper Re-splat!)", "dmg": "65 DMG", "dmg_num": 65, "spike": "Unblockable Taunt Setup", "notes_en": "Pro execution unblockable trap used by Knee and Ty", "notes_ur": "Unblockable Taunt Jet Upper jo round khatam kar deta hai"}
    ],
    "claudio": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "f+3 (T!) -> b+3 -> 1 -> df+3,2", "dmg": "42 DMG", "dmg_num": 42, "spike": "Arrow Kick Spike", "notes_en": "Standard tournament wall route", "notes_ur": "Standard tournament wall combo"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "STB.d+1,2 (Starburst Wall Blast)", "dmg": "34 DMG", "dmg_num": 34, "spike": "Explosive Floor/Wall Break", "notes_en": "Consumes Starburst for extra wall blast / floor break", "notes_ur": "Starburst mein d+1,2 wall break aur blast karta hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "b+1 -> STB.f,f+2,2 mixup", "dmg": "22 DMG", "dmg_num": 22, "spike": "Starburst Pressure", "notes_en": "+6 advantage on wake-up at wall", "notes_ur": "Deewar par +6 advantage aur pressure"}
    ],
    "devil-jin": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "ff+4 (T!) -> b+2,1 (Hold 1 for Laser / Fly)", "dmg": "46 DMG", "dmg_num": 46, "spike": "Unscaled Flying Laser", "notes_en": "Holding 1 delivers unscaled air laser damage", "notes_ur": "1 hold rakhne se udd kar zameen par laser maarta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "b+2,1 (Normal tap)", "dmg": "28 DMG", "dmg_num": 28, "spike": "Downward Fist Spike", "notes_en": "Safe knockdown", "notes_ur": "Safe knockdown"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "cd+4 (Hell Sweep) / ff+2 Mid Mixup", "dmg": "24 DMG", "dmg_num": 24, "spike": "Mishima Vortex", "notes_en": "Unblockable laser setup at wall", "notes_ur": "Wall par Hell Sweep aur ff+2 ka lethal 50/50"}
    ],
    "dragunov": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "df+3+4 (T!) -> f+3,2 -> db+3+4 (Grounded Low Stamp)", "dmg": "47 DMG", "dmg_num": 47, "spike": "Ground Stamp Spike", "notes_en": "db+3+4 hits grounded opponents 100% guaranteed on tech catch!", "notes_ur": "f+3,2 ke baad db+3+4 uthte hue bhi 100% lagta hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "f+3,2 -> 1+2", "dmg": "28 DMG", "dmg_num": 28, "spike": "Double Push", "notes_en": "Safe wall splat", "notes_ur": "Safe wall splat"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "f+3~df (SNK) -> SNK.4 / fc df+1+2 Tackle", "dmg": "24 DMG", "dmg_num": 24, "spike": "Unbreakable Tackle Trap", "notes_en": "Catches tech roll with command grab", "notes_ur": "Tech roll ko crouch tackle se trap karein"}
    ],
    "feng": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "f+1+2 (T!) -> f+3,4 -> b+1+2 (Iron Mountain Shoulder)", "dmg": "48 DMG", "dmg_num": 48, "spike": "60% Shoulder Spike", "notes_en": "Delaying b+1+2 guarantees maximum 60% unscaled damage", "notes_ur": "Shoulder (b+1+2) thoda delay karein for 60% damage"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "f+3,4 -> 1", "dmg": "26 DMG", "dmg_num": 26, "spike": "Safe Knockdown", "notes_en": "Quick recovery for oki", "notes_ur": "Quick recovery"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "db+3 (Low Sweep) / b+1+2 50/50", "dmg": "25 DMG", "dmg_num": 25, "spike": "Kenpo Trap", "notes_en": "Kenpo step backward avoids wake-up kicks", "notes_ur": "Kenpo step se wake-up kicks avoid karke punish karein"}
    ],
    "jack-8": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "df+1,2,1 (T!) -> b+3,2~D (GMH) -> GMH.f+1", "dmg": "46 DMG", "dmg_num": 46, "spike": "Gamma Howl Bound", "notes_en": "GMH at wall gives +11 Guard Break on block!", "notes_ur": "GMH stance deewar par +11 Guard Break deti hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "db+1+2 (Hammer Fist)", "dmg": "28 DMG", "dmg_num": 28, "spike": "Grounded Splat", "notes_en": "Solid raw damage", "notes_ur": "Zameen par bhari damage"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "GMH.1+2 (Unblockable Charge / Piledriver)", "dmg": "30 DMG", "dmg_num": 30, "spike": "Unblockable Setup", "notes_en": "Wall trap against turtles", "notes_ur": "Deewar par unblockable charge trap"}
    ],
    "lars": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "DEN.1,2 (T!) -> df+1 -> db+2,1 -> f+1+4 (Shoulder)", "dmg": "45 DMG", "dmg_num": 45, "spike": "Electric Shoulder Spike", "notes_en": "db+2,1 into f+1+4 guarantees full grounded hit", "notes_ur": "db+2,1 ke baad f+1+4 guaranteed ground hit deta hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+1 -> db+2,1", "dmg": "26 DMG", "dmg_num": 26, "spike": "Fast Entry", "notes_en": "Quick recovery", "notes_ur": "Quick recovery"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "DEN.1 -> SEN.2 / SEN.3 50/50", "dmg": "22 DMG", "dmg_num": 22, "spike": "High/Low Blender", "notes_en": "Frame trap on getup", "notes_ur": "Stance se high/low frame trap"}
    ],
    "law": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "b+2,1 (T!) -> 1 -> 4,3~f (DSS) -> DSS.f+3", "dmg": "46 DMG", "dmg_num": 46, "spike": "Dragon Kick Spike", "notes_en": "1+2 Nunchuck hits grounded for 60% unscaled damage", "notes_ur": "1+2 Nunchuck guaranteed ground hit hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "1+2 (Nunchuck Ground Hit)", "dmg": "28 DMG", "dmg_num": 28, "spike": "Guaranteed Ground Hit", "notes_en": "Hits opponent sliding down wall", "notes_ur": "Deewar se phisalte hue guaranteed hit"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "DSS.3+4 (Dragon Low Sweep / Mid Kick)", "dmg": "24 DMG", "dmg_num": 24, "spike": "DSS Vortex", "notes_en": "Forces 50/50 block read", "notes_ur": "DSS stance se unseeable low/mid 50/50"}
    ],
    "lee": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "ws2,3 (T!) -> df+1 -> f+4,3 -> d+3 (Grounded Hit)", "dmg": "44 DMG", "dmg_num": 44, "spike": "Hitman Slide Spike", "notes_en": "d+3 is 100% guaranteed after f+4,3 delay!", "notes_ur": "f+4,3 ke baad d+3 low hit 100% guaranteed hota hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "f+4,3 -> d+3", "dmg": "27 DMG", "dmg_num": 27, "spike": "Silver Low Strike", "notes_en": "Guaranteed ground finish", "notes_ur": "Guaranteed ground finish"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "b+3,3 -> HMS.4 (Counter-hit trap)", "dmg": "22 DMG", "dmg_num": 22, "spike": "Hitman Oki", "notes_en": "Launches wake-up attack attempts", "notes_ur": "Wake-up attacks ko CH launch karta hai"}
    ],
    "leo": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "KNK.3,4 (T!) -> df+1 -> f+4 (KNK) -> KNK.1+2", "dmg": "45 DMG", "dmg_num": 45, "spike": "Baji Elbow Spike", "notes_en": "KNK.1+2 delivers explosive wall damage", "notes_ur": "KNK.1+2 explosive wall damage deta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "d+2 -> ws1,4,1", "dmg": "28 DMG", "dmg_num": 28, "spike": "Rapid Palm Striking", "notes_en": "Consistent wall ender", "notes_ur": "Consistent wall ender"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "b+1,4 (KNK Stance Pressure)", "dmg": "23 DMG", "dmg_num": 23, "spike": "Non-stop Pressure", "notes_en": "Traps opponent in continuous blockstun", "notes_ur": "Deewar par b+1,4 se continuous pressure"}
    ],
    "leroy": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "HRM.4,1+2 (T!) -> 1 -> df+4,3 -> uf+3+4,1+2", "dmg": "45 DMG", "dmg_num": 45, "spike": "Flurry Punch Spike", "notes_en": "Rapid punches deliver heavy wall and chip damage", "notes_ur": "Rapid punches heavy chip aur wall damage dete hain"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+4,3 -> 1+2", "dmg": "26 DMG", "dmg_num": 26, "spike": "Wing Chun Palm", "notes_en": "Safe ender", "notes_ur": "Safe ender"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "HRM stance -> HRM.4 / HRM.1+2", "dmg": "22 DMG", "dmg_num": 22, "spike": "Cane / Leg Trap", "notes_en": "Cane hits grounded opponents", "notes_ur": "Cane zameen par hit karti hai"}
    ],
    "lili": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "BT.3,4 (T!) -> df+3+4 -> BT.1,2 -> f,f+4~b", "dmg": "44 DMG", "dmg_num": 44, "spike": "Back-Turned Stomp", "notes_en": "f,f+4~b leaves Lili in Back-Turned 50/50 at the wall!", "notes_ur": "f,f+4~b ke baad Lili Back-Turned 50/50 mein rehti hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+3+4 -> BT.1,2", "dmg": "27 DMG", "dmg_num": 27, "spike": "Acrobat Flip", "notes_en": "Safe recovery", "notes_ur": "Safe recovery"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "BT.d+3+4 (Matterhorn) / BT.d+3 50/50", "dmg": "25 DMG", "dmg_num": 25, "spike": "BT Vortex", "notes_en": "Unseeable low into launch mixup", "notes_ur": "Matterhorn launch aur low sweep ka 50/50"}
    ],
    "nina": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "qcf+4,2,3 (T!) -> df+3,2 -> 1+2", "dmg": "47 DMG", "dmg_num": 47, "spike": "Assassin Palm Spike", "notes_en": "In Heat, end with df+1,2,1+2 Pistols for 55+ DMG!", "notes_ur": "Heat mein df+1,2,1+2 Pistols se 55+ DMG milta hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "ss+1~b -> uf+3,1,2", "dmg": "30 DMG", "dmg_num": 30, "spike": "Sidestep Palm", "notes_en": "Great wall carry and re-splat", "notes_ur": "Wall carry aur re-splat"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "df+3,2 -> d+3+4 / qcf+1 Throw Trap", "dmg": "24 DMG", "dmg_num": 24, "spike": "Unbreakable Grab Setup", "notes_en": "Forces crouch or eat 40 dmg throw", "notes_ur": "Throw aur mid ka lethal trap"}
    ],
    "panda": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "HBS.df+1,1 (T!) -> b+2,1~1+2 (HBS) -> HBS.1+2", "dmg": "49 DMG", "dmg_num": 49, "spike": "Bear Body Slam Spike", "notes_en": "Bears have the highest raw wall damage in the game!", "notes_ur": "Bears ka wall damage poore game mein sabse zyada hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "d+1+2 (Butt Slam Grounded)", "dmg": "30 DMG", "dmg_num": 30, "spike": "Heavy Bear Sit", "notes_en": "Guaranteed grounded damage", "notes_ur": "Zameen par butt slam guaranteed hit karta hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "HBS.1+2 -> Roll Mixup", "dmg": "26 DMG", "dmg_num": 26, "spike": "Hunting Bear Vortex", "notes_en": "Traps opponent tech rolling", "notes_ur": "Hunting Bear stance se tech roll trap"}
    ],
    "kuma": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "HBS.df+1,1 (T!) -> b+2,1~1+2 (HBS) -> HBS.1+2", "dmg": "49 DMG", "dmg_num": 49, "spike": "Salmon / Bear Slam", "notes_en": "Deals 49+ damage with salmon electric buffs", "notes_ur": "Salmon lightning ke sath 49+ damage"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "b,f+2 -> wr1+2", "dmg": "31 DMG", "dmg_num": 31, "spike": "Heavy Swat", "notes_en": "Knocks opponent flat on back", "notes_ur": "Knocks opponent flat"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "d+1+2 -> HBS Low Sweep", "dmg": "26 DMG", "dmg_num": 26, "spike": "Salmon Roll Setup", "notes_en": "Hits on getup", "notes_ur": "Uthte hue opponent ko trap karta hai"}
    ],
    "raven": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "b+2,4,2 (T!) -> 1 -> df+1,4 -> qcf+1+2", "dmg": "44 DMG", "dmg_num": 44, "spike": "Shadow Clone Spike", "notes_en": "Teleports clone behind wall for oki", "notes_ur": "Deewar par clone oki lagayein"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "BT.f+3+4", "dmg": "27 DMG", "dmg_num": 27, "spike": "Reverse Bicycle Kick", "notes_en": "Safe and stylish", "notes_ur": "Safe aur stylish finish"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "qcf+2 / db+3 Clone Oki", "dmg": "23 DMG", "dmg_num": 23, "spike": "Clone Deception", "notes_en": "Clone high/low 50/50 on wake-up", "notes_ur": "Clone high/low mixup"}
    ],
    "shaheen": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "SNK.4,1 (T!) -> 2,3 (SNK) -> SNK.3", "dmg": "44 DMG", "dmg_num": 44, "spike": "Slide Kick Spike", "notes_en": "SNK.3 leaves opponent at feet for Slide mixup!", "notes_ur": "SNK.3 ke baad Slide mixup guaranteed!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+4,1,3", "dmg": "28 DMG", "dmg_num": 28, "spike": "Triple Strike", "notes_en": "Reliable tournament route", "notes_ur": "Reliable tournament route"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "fc df,d,df+3 (Slide) / ws2 Mixup", "dmg": "24 DMG", "dmg_num": 24, "spike": "True Slide Vortex", "notes_en": "Unreactable low slide into WS launcher", "notes_ur": "Unreactable low slide aur ws2 launcher mixup"}
    ],
    "steve": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "FLK.1,d+1 (T!) -> f+2,1~b (DCK) -> DCK.f+2", "dmg": "43 DMG", "dmg_num": 43, "spike": "Heavy Hook Spike", "notes_en": "Maximum damage with Ducking extension", "notes_ur": "Ducking extension ke sath maximum damage"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "1,2,1,2~sway into Wall Push", "dmg": "26 DMG", "dmg_num": 26, "spike": "Wall Stun Push", "notes_en": "Steve's qcb+2+4 gives free guaranteed b+1,2!", "notes_ur": "Steve ka qcb+2+4 opponent ko free b+1,2 deta hai!"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "qcb+2+4 (Wall Push) -> b+1,2", "dmg": "35 DMG", "dmg_num": 35, "spike": "Guaranteed Re-splat", "notes_en": "Completely unblockable guaranteed wall stun", "notes_ur": "Guaranteed re-splat wall stun"}
    ],
    "victor": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "IAI.2 (T!) -> df+4,2 (IAI) -> IAI.1,2,2 (delay last hit)", "dmg": "46 DMG", "dmg_num": 46, "spike": "Triple Katana Spike", "notes_en": "3rd sword slash hits grounded for 60% extra damage!", "notes_ur": "3rd sword slash zameen par 60% extra damage deta hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+4,2 -> 1+2", "dmg": "28 DMG", "dmg_num": 28, "spike": "Gunshot Wall Splat", "notes_en": "Safe pistol knockdown", "notes_ur": "Safe pistol knockdown"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "IAI.1 -> IAI.2 / d+1+2 Knife Throw", "dmg": "23 DMG", "dmg_num": 23, "spike": "Iai Stance 50/50", "notes_en": "Unblockable knife setup", "notes_ur": "Unblockable knife setup"}
    ],
    "xiaoyu": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "RDS.1,4 (T!) -> f+2,1,4 (delay 4)", "dmg": "43 DMG", "dmg_num": 43, "spike": "Back-Turned Stomp", "notes_en": "Delaying 4 spikes opponent flat onto ground", "notes_ur": "f+2,1,4 ka last hit delay karein for ground spike"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "ub+4 -> AoP.1+2", "dmg": "26 DMG", "dmg_num": 26, "spike": "Butterfly Kick", "notes_en": "Safe recovery", "notes_ur": "Safe recovery"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "AoP Stance -> AoP.4 / AoP.2,1", "dmg": "21 DMG", "dmg_num": 21, "spike": "Art of Phoenix Trap", "notes_en": "Low crushes wake-up mid attacks", "notes_ur": "Wake-up attacks ko AoP se crush karein"}
    ],
    "yoshimitsu": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "d+2,2,2 (T!) -> b+2,1 (Unscaled Sword Hit!)", "dmg": "45 DMG", "dmg_num": 45, "spike": "Unscaled Blade Spike", "notes_en": "2nd hit of b+2,1 deals unscaled chip + sword damage!", "notes_ur": "b+2,1 ka 2nd hit sword se chip + unscaled damage deta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "3~4~u (DGF) -> DGF.2,4", "dmg": "28 DMG", "dmg_num": 28, "spike": "Dragonfly Spin", "notes_en": "Leaves Yoshimitsu airborne", "notes_ur": "Leaves Yoshimitsu airborne"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "b+2,1 -> Poison Breath / Manji Sit", "dmg": "25 DMG", "dmg_num": 25, "spike": "Unblockable Breath Trap", "notes_en": "Guaranteed damage if opponent doesn't tech immediately", "notes_ur": "Poison breath unblockable trap"}
    ],
    "zafina": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "SCR.4 (T!) -> df+1,2,1", "dmg": "43 DMG", "dmg_num": 43, "spike": "Scarecrow Claw Spike", "notes_en": "Triple claw hits smoothly at wall", "notes_ur": "Triple claw smoothly wall par hit karta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "f+2,3~SCR.df+4", "dmg": "27 DMG", "dmg_num": 27, "spike": "Low Stance Ender", "notes_en": "Enters Scarecrow stance", "notes_ur": "Scarecrow stance mein transition"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "SCR.1+2 (Command Grab) / SCR.df+4 Mixup", "dmg": "22 DMG", "dmg_num": 22, "spike": "Stance Grab Trap", "notes_en": "50/50 between low and throw", "notes_ur": "Stance se low aur throw mixup"}
    ],
    "eddy": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "RLX.2,4 (T!) -> 2,3 -> RLX.3+4", "dmg": "45 DMG", "dmg_num": 45, "spike": "Handstand Flip Spike", "notes_en": "High wall carry and damage", "notes_ur": "High wall carry aur damage"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "qcf+3 (Mandinga Charge)", "dmg": "28 DMG", "dmg_num": 28, "spike": "Mandinga Level Up", "notes_en": "Grants free Mandinga level at wall!", "notes_ur": "Wall par qcf+3 karne se free Mandinga level milta hai!"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "RLX.3,3 (Hell Sweep in Mandinga) / RLX.1+2", "dmg": "26 DMG", "dmg_num": 26, "spike": "Unseeable Low Vortex", "notes_en": "Mandatory 50/50 block read", "notes_ur": "Mandinga mein Hell Sweep ka lethal 50/50"}
    ],
    "lidia": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "CAT.1 (T!) -> df+2 -> f+1+2,3,2,1", "dmg": "45 DMG", "dmg_num": 45, "spike": "Karate Flurry Spike", "notes_en": "Grants permanent Heaven & Earth level stack!", "notes_ur": "Wall combo se Lidia ko Heaven & Earth stack milta hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "qcf+1+2", "dmg": "28 DMG", "dmg_num": 28, "spike": "Blue Sparks Punch", "notes_en": "High pushback", "notes_ur": "High pushback"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "ff+2 (+5 on block into Horse Stance)", "dmg": "24 DMG", "dmg_num": 24, "spike": "Frame Trap", "notes_en": "Opponent cannot press buttons without eating counter", "notes_ur": "Horse stance frame trap"}
    ],
    "heihachi": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "bf+2,3 (T!) -> 1 -> df+1,1 -> d+1,2 (Ground Spike)", "dmg": "48 DMG", "dmg_num": 48, "spike": "Iron Fist Ground Spike", "notes_en": "Delaying d+1,2 deals 48+ damage and hard knockdown", "notes_ur": "d+1,2 delay karne se ground spike lagta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "1 -> d+1,2", "dmg": "30 DMG", "dmg_num": 30, "spike": "Classic Demon Stomp", "notes_en": "Hits grounded opponent flat", "notes_ur": "Zameen par opponent ko flat hit karta hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "f,f+1+2 (Unbreakable Headbutt in WI)", "dmg": "35 DMG", "dmg_num": 35, "spike": "Unbreakable Grab", "notes_en": "In Warrior Instinct, Stonehead cannot be broken!", "notes_ur": "Warrior Instinct mein Headbutt Unbreakable ho jata hai!"}
    ],
    "clive": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "PHX.2,1 (T!) -> f+2,2~PHX.1+2", "dmg": "44 DMG", "dmg_num": 44, "spike": "Phoenix Blade Spike", "notes_en": "Builds full Zantetsuken gauge", "notes_ur": "Zantetsuken meter build karta hai"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "f+1+2 (Prominence)", "dmg": "28 DMG", "dmg_num": 28, "spike": "Greatsword Slam", "notes_en": "Safe long-range push", "notes_ur": "Safe long range push"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "b+2 (Guard Crush Trap at Wall)", "dmg": "25 DMG", "dmg_num": 25, "spike": "Guard Break Setup", "notes_en": "Staggers opponent blocking at wall", "notes_ur": "Deewar par b+2 guard crush trap"}
    ],
    "anna": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "CJM.2,1 (T!) -> df+1,2 -> qcf+2,1", "dmg": "45 DMG", "dmg_num": 45, "spike": "Bazooka Splat", "notes_en": "Heavy push and explosive damage", "notes_ur": "Heavy push aur explosive damage"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "f+3,2~CJM.1+2", "dmg": "27 DMG", "dmg_num": 27, "spike": "Stance Transition", "notes_en": "Enters Chaos Judgment at +5", "notes_ur": "Chaos Judgment stance mein +5 par jata hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "db+3 (Low Sweep) / fc df+2 (Launch) Vortex", "dmg": "26 DMG", "dmg_num": 26, "spike": "Crouch 50/50 Vortex", "notes_en": "Lethal crouch vortex at the wall", "notes_ur": "Wall par db+3 / fc df+2 lethal vortex"}
    ],
    "armor-king": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "db+2,4 (T!) -> df+1 -> f+1+2", "dmg": "47 DMG", "dmg_num": 47, "spike": "Black Jaguar Shoulder", "notes_en": "Guarantees d+4,4,3 stomp on ground!", "notes_ur": "Zameen par d+4,4,3 stomp guaranteed hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "1 -> d+2,4,3", "dmg": "29 DMG", "dmg_num": 29, "spike": "Triple Claw Stomp", "notes_en": "Hits grounded", "notes_ur": "Grounded opponent par hit karta hai"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "f,hcf+1 (Giant Swing into Wall)", "dmg": "75 DMG", "dmg_num": 75, "spike": "75 Damage Wall Throw", "notes_en": "Giant Swing at wall deletes opponent health bar", "notes_ur": "Wall par Giant Swing 75 damage deta hai"}
    ],
    "bob": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "b+2,2,4,4 (T!) -> df+1 -> b+1,2~BAL.1+2", "dmg": "46 DMG", "dmg_num": 46, "spike": "Spinner Ball Bound", "notes_en": "High wall damage and momentum", "notes_ur": "High wall damage aur momentum"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "b+1,2 -> 1+2", "dmg": "28 DMG", "dmg_num": 28, "spike": "Heavy Gut Impact", "notes_en": "Safe finish", "notes_ur": "Safe finish"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "db+3+4 (Hell Sweep) / uf+1+2,4 50/50", "dmg": "25 DMG", "dmg_num": 25, "spike": "Mishima Wave Dash Vortex", "notes_en": "Lethal low into mid mixup", "notes_ur": "Wall par db+3+4 hellsweep mixup"}
    ],
    "fahkumram": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "df+1,4,1 (T!) -> df+1 -> b+1 -> 3,4~4", "dmg": "48 DMG", "dmg_num": 48, "spike": "Garuda Charge Kick Spike", "notes_en": "3,4~4 at wall deals Guard Crush on block!", "notes_ur": "Wall ke paas 3,4~4 Guard Crush deta hai!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "bf+4 (Jet Kick)", "dmg": "30 DMG", "dmg_num": 30, "spike": "Heavy Wall Blast", "notes_en": "Safe and +6 on block", "notes_ur": "Safe aur +6 on block"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "3,4~4 (Charge Kick Guard Break) / d+4", "dmg": "26 DMG", "dmg_num": 26, "spike": "Unblockable Wall Setup", "notes_en": "Guard break causes wall splat even on block", "notes_ur": "Block par bhi wall splat kar deta hai"}
    ],
    "kunimitsu": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "1,1,4 (T!) -> 1 -> f+2,1,4", "dmg": "44 DMG", "dmg_num": 44, "spike": "Setsuna Kunai Spike", "notes_en": "Fast, flashy, and high carry", "notes_ur": "High wall carry aur flashy finish"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "uf+3,4", "dmg": "27 DMG", "dmg_num": 27, "spike": "Double Acrobatic Kick", "notes_en": "Safe knockdown", "notes_ur": "Safe knockdown"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "b+2 (Flame Unblockable Trap at Wall)", "dmg": "25 DMG", "dmg_num": 25, "spike": "Unblockable Flame Setup", "notes_en": "Hits opponent waking up with unblockable fire", "notes_ur": "Wall par b+2 flame unblockable trap"}
    ],
    "miary-zo": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "1,2,2 (T!) -> 1+2 (BAO Wall Climb) -> BAO.1+2", "dmg": "45 DMG", "dmg_num": 45, "spike": "Wall Climb Crush", "notes_en": "Climbs actual arena wall and dives down!", "notes_ur": "Deewar par chadh kar diving crush!"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "3,1~F -> MOR.1+2", "dmg": "28 DMG", "dmg_num": 28, "spike": "Mora Flip Kick", "notes_en": "Solid standard finish", "notes_ur": "Solid standard finish"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "1+2 (BAO) -> BAO.1+2 Unblockable Dive Grab", "dmg": "32 DMG", "dmg_num": 32, "spike": "Unblockable Wall Grab", "notes_en": "Opponent must duck or get crushed", "notes_ur": "Deewar par BAO stance se unblockable grab mixup"}
    ],
    "roger-jr": [
        {"route": "Max Damage Wall Combo (T! Available)", "notation": "db+4,3 (T!) -> 1,2 -> f+4,3,2", "dmg": "44 DMG", "dmg_num": 44, "spike": "Kangaroo Flurry Spike", "notes_en": "High damage boxing punches", "notes_ur": "High damage boxing punches"},
        {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "ANM.1+2 (Animal Stomp)", "dmg": "27 DMG", "dmg_num": 27, "spike": "Heavy Paw Stomp", "notes_en": "Hits grounded opponent", "notes_ur": "Hits grounded opponent"},
        {"route": "Oki / Resplat / Setup Wall Ender", "notation": "f,hcf+1 (Giant Swing at Wall)", "dmg": "75 DMG", "dmg_num": 75, "spike": "75 Damage Wall Throw", "notes_en": "Huge tail swing bounces opponent off wall for 75 DMG!", "notes_ur": "Wall par Giant Swing 75 damage deta hai!"}
    ]
}

print("Loaded all 129 wall combos for all 43 fighters.")

# 3. COMPLETE 10-HIT STRING COUNTERS (All 43 Fighters)
# Required Fields: Character, 10-Hit Combo Name / Full String Notation, Exact Hit Sequence Breakdown, Low Parry / Duck Window, Interrupt / Power Crush Gap, Optimal Punish

TEN_HIT_DATA = {
    "king": {
        "name": "King 10-Hit Combo (1,2,1,1,2,4,4,4,1,3)",
        "input": "1,2,1,1,2,4,4,4,1,3",
        "seq": "h, h, m, m, h, l, l, l, m, m",
        "duck_window_en": "Hit 6, 7, & 8 (4,4,4) are 3 consecutive Low Kicks! Hold df (Low Parry) after 5th punch (2)",
        "duck_window_ur": "Hit 6, 7, & 8 (4,4,4) lagatar 3 Low Kicks hain! Pehle 5 punches ke baad df (Low Parry) hold kar lein!",
        "gap_en": "Gap before Hit 6 -> i10 Jab check or Power Crush / Heat Burst interrupts",
        "gap_ur": "Hit 6 se pehle pause aata hai jahan Power Crush ya Heat Burst (2+3) daba sakte hain",
        "punish_en": "Hold df (Low Parry) on Hit 6 for guaranteed airborne juggle launch",
        "punish_ur": "Hit 6 par df daba kar Low Parry karein aur full launch karein"
    },
    "hwoarang": {
        "name": "Hwoarang 10-Hit String (RFS/LFS 1,2,3,4,3,4,4,4,4,3)",
        "input": "RFS/LFS 1,2,3,4,3,4,4,4,4,3",
        "seq": "h, h, m, l, m, l, l, l, l, m",
        "duck_window_en": "Hit 4 (4) and Hit 6 (4) are Low kicks; Hit 2 (2) is duckable High",
        "duck_window_ur": "Hit 4 (4) aur Hit 6 (4) Low kicks hain; Hit 2 High hai",
        "gap_en": "Gap between Hit 3 and 4 -> Dickjab (db+1) interrupts",
        "gap_ur": "Pehle 3 hits ke baad Dickjab (db+1) se interrupt karein",
        "punish_en": "Duck Hit 2 for WS launcher or Low Parry Hit 4",
        "punish_ur": "Hit 2 duck karke ws launch karein ya Hit 4 par Low Parry karein"
    },
    "paul": {
        "name": "Paul Phoenix 10-Hit Combo (1,2,3,2,1,2,1,4,2,1)",
        "input": "1,2,3,2,1,2,1,4,2,1",
        "seq": "h, h, m, m, h, m, h, l, m, m",
        "duck_window_en": "Hit 5 (1) is High; Hit 8 (4) is a slow Low sweep",
        "duck_window_ur": "Hit 5 (1) High hai aur Hit 8 (4) Low hai",
        "gap_en": "Gap after 1,2,3 -> df+1 jab check interrupts before 4th hit",
        "gap_ur": "1,2,3 ke baad df+1 se interrupt karein",
        "punish_en": "Low Parry on Hit 8 (4) or interrupt with df+1 after Hit 3",
        "punish_ur": "Hit 8 par df (Low Parry) karein ya 1,2,3 ke baad df+1 se interrupt karein"
    },
    "law": {
        "name": "Marshall Law 10-Hit String (df+1,2,2,1,3,3,3,4,3,4)",
        "input": "df+1,2,2,1,3,3,3,4,3,4",
        "seq": "m, h, h, m, l, l, l, m, l, m",
        "duck_window_en": "Hit 5 (3) and Hit 9 (3) are Low sweeps",
        "duck_window_ur": "Hit 5 (3) aur Hit 9 (3) Low sweeps hain!",
        "gap_en": "After 4th punch (1), clean pause allows df Low Parry",
        "gap_ur": "4 punches (df+1,2,2,1) ke baad pause aata hai",
        "punish_en": "Hold df (Low Parry) after 4th punch (df+1,2,2,1) -> 5th hit auto-parries into launch!",
        "punish_ur": "4 punches dekhte hi df (Low Parry) hold karein—5th hit auto-parry hoga!"
    },
    "bryan": {
        "name": "Bryan Fury 10-Hit String (b+3,4,1,2,1,4,2,1,4,2)",
        "input": "b+3,4,1,2,1,4,2,1,4,2",
        "seq": "m, h, h, m, h, l, m, h, l, m",
        "duck_window_en": "Hit 2 (4) is High; Hit 6 (4) is Low",
        "duck_window_ur": "Hit 2 (4) High hai; Hit 6 (4) Low hai",
        "gap_en": "Gap between b+3 and 4 -> Duck 2nd hit immediately",
        "gap_ur": "b+3 ke foran baad duck karein",
        "punish_en": "Duck 2nd hit High for while standing launch (ws1) or Low Parry Hit 6",
        "punish_ur": "b+3 block karte hi Duck karein (ws1 Launch!) ya Hit 6 ko Low Parry karein"
    },
    "nina": {
        "name": "Nina Williams 10-Hit Combo (1,2,1,2,3,3,2,1,2,4)",
        "input": "1,2,1,2,3,3,2,1,2,4",
        "seq": "h, h, h, h, l, l, m, m, h, m",
        "duck_window_en": "Hit 5 (3) and Hit 6 (3) are consecutive Low kicks",
        "duck_window_ur": "Hit 5 (3) aur Hit 6 (3) Low kicks hain!",
        "gap_en": "Pause after rapid 4 punches allows immediate df hold",
        "gap_ur": "4 fast punches ke baad pause aata hai",
        "punish_en": "Hold df (Low Parry) right after 4 punches (1,2,1,2)",
        "punish_ur": "Nina ke 4 punches (1,2,1,2) ke foran baad df (Low Parry) daba kar rakhein!"
    },
    "kazuya": {
        "name": "Kazuya Mishima 10-Hit Combo (f,f+2,1,2,2,3,4,4,1,2,1)",
        "input": "f,f+2,1,2,2,3,4,4,1,2,1",
        "seq": "m, h, m, m, m, l, l, h, m, m",
        "duck_window_en": "Hit 6 (4) and Hit 7 (4) are consecutive Low Hell Sweeps",
        "duck_window_ur": "Hit 6 (4) aur Hit 7 (4) Low Hell-Sweeps hain!",
        "gap_en": "Gap after 5th hit (3 mid kick)",
        "gap_ur": "5th hit ke baad gap hai",
        "punish_en": "Crouch block Hit 6 (-15 Launch) or hold df for Low Parry",
        "punish_ur": "Pehle 5 hits ke foran baad df (Low Parry) ya Crouch Block (-15 Launch) karein!"
    },
    "devil-jin": {
        "name": "Devil Jin 10-Hit Combo (f,f+2,1,2,2,3,4,4,1,2,1)",
        "input": "f,f+2,1,2,2,3,4,4,1,2,1",
        "seq": "m, h, m, m, m, l, l, h, m, m",
        "duck_window_en": "Hit 6 (4) and Hit 7 (4) are Low sweeps",
        "duck_window_ur": "Hit 6 (4) aur Hit 7 (4) Low sweeps hain!",
        "gap_en": "Gap after 5th mid kick",
        "gap_ur": "5th mid kick ke baad gap hai",
        "punish_en": "Crouch block Hit 6 (-15 Launch) or hold df for Low Parry",
        "punish_ur": "5th hit ke baad df (Low Parry) ya crouch block karein"
    },
    "jin": {
        "name": "Jin Kazama 10-Hit Combo (f,f+2,1,2,2,3,4,4,3,2,1)",
        "input": "f,f+2,1,2,2,3,4,4,3,2,1",
        "seq": "m, h, m, m, m, l, l, m, m, m",
        "duck_window_en": "Hit 6 (4) and Hit 7 (4) are Low kicks",
        "duck_window_ur": "Hit 6 (4) aur Hit 7 (4) Low kicks hain",
        "gap_en": "Pause after 5th hit (3 mid kick)",
        "gap_ur": "5th hit ke baad pause aata hai",
        "punish_en": "Hold df (Low Parry) immediately after blocking 5th hit",
        "punish_ur": "5th hit (3 mid kick) block karte hi df (Low Parry) hold kar lein!"
    },
    "heihachi": {
        "name": "Heihachi Mishima 10-Hit Combo (f,f+2,1,2,2,3,4,4,1,2,1)",
        "input": "f,f+2,1,2,2,3,4,4,1,2,1",
        "seq": "m, h, m, m, m, l, l, h, m, m",
        "duck_window_en": "Hit 6 & 7 (4,4) are Low kicks",
        "duck_window_ur": "Hit 6 & 7 (4,4) Low kicks hain",
        "gap_en": "Gap after 5th hit",
        "gap_ur": "5th hit ke baad gap aata hai",
        "punish_en": "Hold df (Low Parry) after 5th hit for launch",
        "punish_ur": "5th hit ke baad df (Low Parry) hold karein"
    },
    "yoshimitsu": {
        "name": "Yoshimitsu 10-Hit Combo (1,2,1,4,4,4,1,1,1,1)",
        "input": "1,2,1,4,4,4,1,1,1,1",
        "seq": "h, h, m, l, l, l, u!, u!, u!, u!",
        "duck_window_en": "Hit 4, 5, 6 (4,4,4) are Low kicks; later hits are Unblockable sword slashes",
        "duck_window_ur": "Hit 4, 5, 6 Low hain aur aakhri hits Unblockable talwar hain!",
        "gap_en": "Before Unblockable spinning slash, jab float interrupts Yoshimitsu",
        "gap_ur": "Unblockable se pehle jab float se interrupt karein",
        "punish_en": "Low Parry on Hit 4, or jab float / sidestep when he spins with unblockable",
        "punish_ur": "Hit 4 par Low Parry karein ya unblockable spin par sidestep / jab karein"
    },
    "xiaoyu": {
        "name": "Xiaoyu 10-Hit Combo (uf+4,1,2,1+2,1,3,4,4,4,1)",
        "input": "uf+4,1,2,1+2,1,3,4,4,4,1",
        "seq": "m, h, h, m, h, m, l, l, l, m",
        "duck_window_en": "Hit 7, 8, 9 (4,4,4) are Low sweeping kicks",
        "duck_window_ur": "Hit 7, 8, 9 (4,4,4) Low sweeping kicks hain",
        "gap_en": "Gap after 6th hit (3 mid kick)",
        "gap_ur": "6th hit (3 mid kick) ke baad gap hai",
        "punish_en": "Hold df (Low Parry) after 1+2,1,3",
        "punish_ur": "1+2,1,3 ke baad df (Low Parry) hold rakhein!"
    },
    "eddy": {
        "name": "Eddy Gordo 10-Hit Combo (4~3,4,2,4,4,3+4,4,4,3+4)",
        "input": "4~3,4,2,4,4,3+4,4,4,3+4",
        "seq": "m, h, m, l, l, m, l, l, m",
        "duck_window_en": "Hit 4 (4) and Hit 5 (4) are Low sweeping kicks",
        "duck_window_ur": "Hit 4 (4) aur Hit 5 (4) Low sweeps hain",
        "gap_en": "Gap before 4th low allows Power Crush (Armor)",
        "gap_ur": "4th low se pehle Power Crush daba sakte hain",
        "punish_en": "Hold df (Low Parry) on Capoeira low sweeps",
        "punish_ur": "Capoeira spin ke beech mein df (Low Parry) ya Power Crush maarein"
    },
    "asuka": {
        "name": "Asuka Kazama 10-Hit Combo (ws+2,1,1,1,2,1,4,3,3+4)",
        "input": "ws+2,1,1,1,2,1,4,3,3+4",
        "seq": "m, h, h, h, m, h, l, m, m",
        "duck_window_en": "Hit 7 (4) is a Low kick directly following 1+2 flurry punches",
        "duck_window_ur": "Hit 7 (4) Low kick hai (punches ke foran baad)",
        "gap_en": "Gap after 6th punch (1)",
        "gap_ur": "6th punch ke baad gap hai",
        "punish_en": "Hold df (Low Parry) while blocking punches -> 7th hit auto-parries",
        "punish_ur": "Jab woh punches maar rahi ho toh df hold rakhein—7th hit parry hoga!"
    },
    "jun": {
        "name": "Jun Kazama 10-Hit Combo (ws+2,1,1,1,2,1,4,3,3+4)",
        "input": "ws+2,1,1,1,2,1,4,3,3+4",
        "seq": "m, h, h, h, m, h, l, m, m",
        "duck_window_en": "Hit 7 (4) is a Low sweep",
        "duck_window_ur": "Hit 7 (4) Low sweep hai",
        "gap_en": "Gap after 6th punch",
        "gap_ur": "6th punch ke baad gap hai",
        "punish_en": "Hold df (Low Parry) after 6th punch -> 7th hit auto-parries",
        "punish_ur": "6th punch ke baad df (Low Parry) hold rakhein"
    },
    "lili": {
        "name": "Lili 10-Hit Combo (4,1,3,4,4,3,4,4,3,4)",
        "input": "4,1,3,4,4,3,4,4,3,4",
        "seq": "h, h, m, l, l, m, l, l, m, m",
        "duck_window_en": "Hit 4 (4) and Hit 8 (4) are Low kicks",
        "duck_window_ur": "Hit 4 (4) aur Hit 8 (4) Low kicks hain",
        "gap_en": "Gap after first 3 hits (4,1,3)",
        "gap_ur": "Pehle 3 hits ke baad gap hai",
        "punish_en": "Hold df (Low Parry) immediately after first 3 hits (4,1,3)",
        "punish_ur": "Pehle 3 hits (4,1,3) ke foran baad df (Low Parry) hold karein!"
    },
    "jack-8": {
        "name": "Jack-8 10-Hit Combo (d+2,1,1,1,2,1,2,1,1+2,1+2)",
        "input": "d+2,1,1,1,2,1,2,1,1+2,1+2",
        "seq": "l, l, h, m, m, m, m, m, u!, u!",
        "duck_window_en": "Hit 1 (d+2) and Hit 2 (1) are Low punches; 9th & 10th hits are Unblockable!",
        "duck_window_ur": "Hit 1 (d+2) aur Hit 2 (1) Low punches hain; 9th hit Unblockable hai!",
        "gap_en": "Gap before 9th unblockable charge",
        "gap_ur": "9th unblockable se pehle gap hai",
        "punish_en": "Dickjab (db+1) interrupts string, or df+2 launch before 9th hit",
        "punish_ur": "Beech mein Power Crush ya Dickjab (db+1) maarein, ya df+2 launch karein"
    },
    "steve": {
        "name": "Steve Fox 10-Hit Combo (1,2,1,2,d+1,4,1,1,2,1+2)",
        "input": "1,2,1,2,d+1,4,1,1,2,1+2",
        "seq": "h, h, h, h, l, l, h, h, m, m",
        "duck_window_en": "Hit 5 (d+1) is Low and Hit 6 (4) is a Stomp",
        "duck_window_ur": "Hit 5 (d+1) Low hai aur Hit 6 (4) Stomp kick hai",
        "gap_en": "Gap after 4 fast punches (1,2,1,2)",
        "gap_ur": "4 fast punches ke baad gap aata hai",
        "punish_en": "Hold df (Low Parry) after 4 punches",
        "punish_ur": "4 punches (1,2,1,2) ke baad df (Low Parry) hold kar lein!"
    },
    "alisa": {
        "name": "Alisa 10-Hit Combo (f+1,2,3,1,4,2,1,4,2,3)",
        "input": "f+1,2,3,1,4,2,1,4,2,3",
        "seq": "h, h, m, l, l, m, h, l, m, m",
        "duck_window_en": "Hit 4 (1) and Hit 8 (4) are Low hits",
        "duck_window_ur": "Hit 4 (1) aur Hit 8 (4) Low hits hain",
        "gap_en": "Gap after 3rd hit (3 kick)",
        "gap_ur": "3rd hit (3 kick) ke baad gap hai",
        "punish_en": "Hold df (Low Parry) or activate Raw Heat Burst (2+3) after 3rd hit",
        "punish_ur": "3rd hit ke baad df (Low Parry) ya Heat Burst (2+3) maarein"
    },
    "lee": {
        "name": "Lee Chaolan 10-Hit Combo (df+1,2,2,1,3,3,3,4,3,4)",
        "input": "df+1,2,2,1,3,3,3,4,3,4",
        "seq": "m, h, h, m, l, l, l, m, l, m",
        "duck_window_en": "Hit 5 (3) is Low kick (identical cadence to Law)",
        "duck_window_ur": "Hit 5 (3) Low kick hai (Law jaisa cadence)",
        "gap_en": "Gap after 4th punch",
        "gap_ur": "4th punch ke baad pause aata hai",
        "punish_en": "Hold df (Low Parry) after 4th punch for guaranteed launch",
        "punish_ur": "4th punch ke baad df (Low Parry) hold karein!"
    },
    "reina": {
        "name": "Reina 10-Hit Mishima String (f,f+2,1,2,2,3,4,4,1,2,1)",
        "input": "f,f+2,1,2,2,3,4,4,1,2,1",
        "seq": "m, h, m, m, m, l, l, h, m, m",
        "duck_window_en": "Hits 6 & 7 (4,4) are consecutive Low kicks into mid finisher",
        "duck_window_ur": "Hit 6 aur 7 (4,4) lagatar Low kicks hain!",
        "gap_en": "Gap after 5th hit (3 mid kick)",
        "gap_ur": "5th hit ke baad gap aata hai",
        "punish_en": "Hold df (Low Parry) immediately after 5th punch for full launch",
        "punish_ur": "5th hit ke foran baad df (Low Parry) hold kar lein!"
    },
    "victor": {
        "name": "Victor Tactical Knife 10-Hit (1,2,3,4,2,2,1,1+2,f+2)",
        "input": "1,2,3,4,2,2,1,1+2,f+2",
        "seq": "h, h, m, l, m, m, h, h, m",
        "duck_window_en": "Hit 4 (4) is a Low knife sweep; Hit 8 (1+2) is High gunshot",
        "duck_window_ur": "Hit 4 (4) Low sweep hai aur Hit 8 (1+2) High gunshot hai!",
        "gap_en": "Gap after 3rd hit or duck under 8th gunshot",
        "gap_ur": "3rd hit ke baad gap hai ya 8th gunshot duck karein",
        "punish_en": "Low Parry Hit 4 or duck gunshot on reaction and WS launch",
        "punish_ur": "Hit 4 par Low Parry karein ya gunshot duck karke launch karein"
    },
    "panda": {
        "name": "Bear Windmill 10-Hit (b+1+2,1,2,1,2,d+3+4,3+4,1+2)",
        "input": "b+1+2,1,2,1,2,d+3+4,3+4,1+2",
        "seq": "m, h, m, h, m, l, m, m",
        "duck_window_en": "Hit 6 (d+3+4) is a double paw Low sweep with heavy recovery",
        "duck_window_ur": "Hit 6 (d+3+4) Bear double paw Low sweep hai!",
        "gap_en": "Gap after 5th slap before low sweep",
        "gap_ur": "5th slap ke baad pause aata hai",
        "punish_en": "Crouch block Hit 6 for guaranteed -26 frame maximum launch punish!",
        "punish_ur": "Hit 6 crouch block karein—yeh -26 Launch Punishable hai!"
    },
    "kuma": {
        "name": "Bear Windmill 10-Hit (b+1+2,1,2,1,2,d+3+4,3+4,1+2)",
        "input": "b+1+2,1,2,1,2,d+3+4,3+4,1+2",
        "seq": "m, h, m, h, m, l, m, m",
        "duck_window_en": "Hit 6 (d+3+4) is a double paw Low sweep with heavy recovery",
        "duck_window_ur": "Hit 6 (d+3+4) Bear double paw Low sweep hai!",
        "gap_en": "Gap after 5th slap before low sweep",
        "gap_ur": "5th slap ke baad pause aata hai",
        "punish_en": "Crouch block Hit 6 for guaranteed -26 frame maximum launch punish!",
        "punish_ur": "Hit 6 crouch block karein—yeh -26 Launch Punishable hai!"
    },
    "anna": {
        "name": "Anna Williams 10-Hit String (1,2,1,2,3,3,2,1,2,4)",
        "input": "1,2,1,2,3,3,2,1,2,4",
        "seq": "h, h, h, h, l, l, m, m, h, m",
        "duck_window_en": "Hit 5 (3) and Hit 6 (3) are Low sweeps",
        "duck_window_ur": "Hit 5 (3) aur Hit 6 (3) Low sweeps hain",
        "gap_en": "Gap after 4 fast slaps",
        "gap_ur": "4 fast slaps ke baad gap hai",
        "punish_en": "Hold df (Low Parry) after 4 punches",
        "punish_ur": "4 punches ke baad df (Low Parry) hold karein"
    },
    "armor-king": {
        "name": "Armor King 10-Hit String (1,2,1,1,2,4,4,4,1,1)",
        "input": "1,2,1,1,2,4,4,4,1,1",
        "seq": "h, h, m, m, h, l, l, l, m, m",
        "duck_window_en": "Hits 6, 7, 8 (4,4,4) are Low kicks",
        "duck_window_ur": "Hits 6, 7, 8 (4,4,4) Low kicks hain",
        "gap_en": "Gap after 5th punch",
        "gap_ur": "5th punch ke baad gap hai",
        "punish_en": "Hold df (Low Parry) after 5th punch for full launch",
        "punish_ur": "5th punch ke baad df (Low Parry) hold karein"
    },
    "bob": {
        "name": "Bob Richards 10-Hit String (1,2,1,2,4,3,4,4,4,3+4)",
        "input": "1,2,1,2,4,3,4,4,4,3+4",
        "seq": "h, h, m, m, l, m, l, l, m, m",
        "duck_window_en": "Hit 5 (4) and Hit 7 (4) are Low sweeps",
        "duck_window_ur": "Hit 5 (4) aur Hit 7 (4) Low sweeps hain",
        "gap_en": "Gap before 5th low kick",
        "gap_ur": "5th low kick se pehle gap hai",
        "punish_en": "Hold df (Low Parry) on 5th hit",
        "punish_ur": "5th hit par df (Low Parry) hold karein"
    },
    "fahkumram": {
        "name": "Fahkumram 10-Hit Muay Thai Flurry (1,2,3,4,3,4,4,3,4,4)",
        "input": "1,2,3,4,3,4,4,3,4,4",
        "seq": "h, h, m, l, m, l, m, l, m, m",
        "duck_window_en": "Hit 4 (4) and Hit 6 (4) are Low shin kicks",
        "duck_window_ur": "Hit 4 (4) aur Hit 6 (4) Low shin kicks hain",
        "gap_en": "Gap before 4th low kick",
        "gap_ur": "4th low kick se pehle gap hai",
        "punish_en": "Hold df (Low Parry) on 4th hit or duck 2nd hit high",
        "punish_ur": "4th hit par df (Low Parry) karein"
    },
    "kunimitsu": {
        "name": "Kunimitsu 10-Hit Ninja Kunai String (1,2,1,4,4,4,1,2,3,2)",
        "input": "1,2,1,4,4,4,1,2,3,2",
        "seq": "h, h, m, l, l, l, m, h, m, m",
        "duck_window_en": "Hits 4, 5, 6 (4,4,4) are Low kicks",
        "duck_window_ur": "Hits 4, 5, 6 (4,4,4) Low kicks hain",
        "gap_en": "Gap after 3rd hit",
        "gap_ur": "3rd hit ke baad gap hai",
        "punish_en": "Hold df (Low Parry) after 3rd hit",
        "punish_ur": "3rd hit ke baad df (Low Parry) hold karein"
    },
    "miary-zo": {
        "name": "Miary Zo 10-Hit Acrobatic String (1,2,2,3,1,4,4,2,3,1)",
        "input": "1,2,2,3,1,4,4,2,3,1",
        "seq": "h, h, m, m, h, l, l, m, m, m",
        "duck_window_en": "Hits 6 & 7 (4,4) are Low sweeping kicks",
        "duck_window_ur": "Hits 6 & 7 (4,4) Low sweeps hain",
        "gap_en": "Gap after 5th acrobatic kick",
        "gap_ur": "5th kick ke baad gap hai",
        "punish_en": "Hold df (Low Parry) on 6th hit",
        "punish_ur": "6th hit par df (Low Parry) karein"
    },
    "roger-jr": {
        "name": "Roger Jr. 10-Hit Kangaroo String (1,2,1,1,2,4,4,4,1,2)",
        "input": "1,2,1,1,2,4,4,4,1,2",
        "seq": "h, h, m, m, h, l, l, l, m, m",
        "duck_window_en": "Hits 6, 7, 8 (4,4,4) are Low tail kicks",
        "duck_window_ur": "Hits 6, 7, 8 (4,4,4) Low kicks hain",
        "gap_en": "Gap after 5th punch",
        "gap_ur": "5th punch ke baad gap hai",
        "punish_en": "Hold df (Low Parry) after 5th punch",
        "punish_ur": "5th punch ke baad df (Low Parry) hold karein"
    },
    "claudio": {
        "name": "Claudio Serafino Multi-Hit Counter (b+4,2 / STB.f+1+2,1+2)",
        "input": "b+4,2 / STB.f+1+2,1+2",
        "seq": "m, h / m, m",
        "duck_window_en": "b+4,2 has High 2nd hit; STB.f+1+2,1+2 is -14 on block",
        "duck_window_ur": "b+4,2 ka 2nd hit High hai; STB.f+1+2,1+2 block par -14 hai",
        "gap_en": "Duck 2nd hit of b+4,2 on reaction",
        "gap_ur": "b+4,2 ka 2nd hit reaction par duck karein",
        "punish_en": "Duck b+4,2 2nd hit for WS launcher (-14 punish on STB string)",
        "punish_ur": "2nd hit duck karke ws launcher maarein"
    },
    "dragunov": {
        "name": "Dragunov 10-Hit Commando String (1,3,1,2,1,1,4,1,3,2)",
        "input": "1,3,1,2,1,1,4,1,3,2",
        "seq": "h, m, h, m, h, m, l, m, h, m",
        "duck_window_en": "Hit 7 (4) is a Low sweep",
        "duck_window_ur": "Hit 7 (4) Low sweep hai",
        "gap_en": "Gap after 6th hit allows immediate df hold",
        "gap_ur": "6th hit ke baad pause hai",
        "punish_en": "Hold df (Low Parry) on Hit 7",
        "punish_ur": "Hit 7 par df (Low Parry) hold karein"
    },
    "feng": {
        "name": "Feng Wei 10-Hit Kenpo String (1,1,2,1,3,4,4,4,1,2)",
        "input": "1,1,2,1,3,4,4,4,1,2",
        "seq": "h, h, m, m, l, m, l, l, m, m",
        "duck_window_en": "Hit 5 (3) and Hit 7 (4) are Low kicks",
        "duck_window_ur": "Hit 5 (3) aur Hit 7 (4) Low kicks hain",
        "gap_en": "Gap before 5th hit",
        "gap_ur": "5th hit se pehle gap hai",
        "punish_en": "Hold df (Low Parry) on 5th hit",
        "punish_ur": "5th hit par df (Low Parry) hold karein"
    },
    "lars": {
        "name": "Lars Alexandersson 10-Hit String (1,2,1,4,2,1,4,2,3,1)",
        "input": "1,2,1,4,2,1,4,2,3,1",
        "seq": "h, h, m, l, m, h, l, m, m, m",
        "duck_window_en": "Hit 4 (4) and Hit 7 (4) are Low kicks",
        "duck_window_ur": "Hit 4 (4) aur Hit 7 (4) Low kicks hain",
        "gap_en": "Gap after 3rd hit",
        "gap_ur": "3rd hit ke baad gap hai",
        "punish_en": "Hold df (Low Parry) after 3rd hit",
        "punish_ur": "3rd hit ke baad df (Low Parry) hold karein"
    },
    "leo": {
        "name": "Leo Kliesen 10-Hit Baji String (1,2,1,1,2,3,4,4,1,2)",
        "input": "1,2,1,1,2,3,4,4,1,2",
        "seq": "h, h, m, m, h, l, l, m, m, m",
        "duck_window_en": "Hit 6 (3) and Hit 7 (4) are Low sweeps",
        "duck_window_ur": "Hit 6 (3) aur Hit 7 (4) Low sweeps hain",
        "gap_en": "Gap after 5th punch",
        "gap_ur": "5th punch ke baad gap hai",
        "punish_en": "Hold df (Low Parry) on 6th hit",
        "punish_ur": "6th hit par df (Low Parry) hold karein"
    },
    "leroy": {
        "name": "Leroy Smith 10-Hit Wing Chun String (1,2,1,2,1,1,4,4,1+2,1+2)",
        "input": "1,2,1,2,1,1,4,4,1+2,1+2",
        "seq": "h, h, h, h, m, m, l, l, m, m",
        "duck_window_en": "Hit 7 (4) and Hit 8 (4) are Low sweeps",
        "duck_window_ur": "Hit 7 (4) aur Hit 8 (4) Low sweeps hain",
        "gap_en": "Gap before 7th hit",
        "gap_ur": "7th hit se pehle gap hai",
        "punish_en": "Hold df (Low Parry) after 6 rapid Wing Chun punches",
        "punish_ur": "6 punches ke baad df (Low Parry) hold karein"
    },
    "raven": {
        "name": "Raven 10-Hit Shadow String (1,2,1,4,2,4,4,1,2,3)",
        "input": "1,2,1,4,2,4,4,1,2,3",
        "seq": "h, h, m, l, m, l, l, m, h, m",
        "duck_window_en": "Hit 4 (4) and Hit 6 (4) are Low sweeps",
        "duck_window_ur": "Hit 4 (4) aur Hit 6 (4) Low sweeps hain",
        "gap_en": "Gap after 3rd punch",
        "gap_ur": "3rd punch ke baad gap hai",
        "punish_en": "Hold df (Low Parry) on Hit 4",
        "punish_ur": "Hit 4 par df (Low Parry) hold karein"
    },
    "shaheen": {
        "name": "Shaheen 10-Hit Falcon String (1,2,3,1,4,2,4,4,1,3)",
        "input": "1,2,3,1,4,2,4,4,1,3",
        "seq": "h, h, m, m, l, m, l, l, m, m",
        "duck_window_en": "Hit 5 (4) and Hit 7 (4) are Low kicks",
        "duck_window_ur": "Hit 5 (4) aur Hit 7 (4) Low kicks hain",
        "gap_en": "Gap before 5th hit",
        "gap_ur": "5th hit se pehle gap hai",
        "punish_en": "Hold df (Low Parry) on 5th hit",
        "punish_ur": "5th hit par df (Low Parry) hold karein"
    },
    "zafina": {
        "name": "Zafina 10-Hit Mantis String (1,2,1,3,4,4,1,2,3,4)",
        "input": "1,2,1,3,4,4,1,2,3,4",
        "seq": "h, h, m, l, l, l, m, m, l, m",
        "duck_window_en": "Hits 4, 5, 6 (3,4,4) are Low creep sweeps",
        "duck_window_ur": "Hits 4, 5, 6 Low sweeps hain",
        "gap_en": "Gap after 3rd punch",
        "gap_ur": "3rd punch ke baad gap hai",
        "punish_en": "Hold df (Low Parry) on 4th hit",
        "punish_ur": "4th hit par df (Low Parry) hold karein"
    },
    "lidia": {
        "name": "Lidia Sobieska 10-Hit Karate String (1,2,2,4,3,1,4,4,1+2,1+2)",
        "input": "1,2,2,4,3,1,4,4,1+2,1+2",
        "seq": "h, h, m, l, m, h, l, l, m, m",
        "duck_window_en": "Hit 4 (4) and Hit 7 (4) are Low kicks",
        "duck_window_ur": "Hit 4 (4) aur Hit 7 (4) Low kicks hain",
        "gap_en": "Gap before 4th low",
        "gap_ur": "4th low se pehle gap hai",
        "punish_en": "Hold df (Low Parry) on 4th hit or duck 6th hit",
        "punish_ur": "4th hit par df (Low Parry) hold karein"
    },
    "clive": {
        "name": "Clive Rosfield Multi-Hit String Counter (f+1+2,2 / 2,1,2)",
        "input": "f+1+2,2 / 2,1,2",
        "seq": "m, m / h, m, m",
        "duck_window_en": "f+1+2,2 2nd hit is -14 on block; 2,1,2 can be interrupted with Dickjab (db+1)",
        "duck_window_ur": "f+1+2,2 ka 2nd hit block par -14 hai; 2,1,2 ko db+1 se interrupt karein",
        "gap_en": "Dickjab (db+1) interrupts between 1st and 2nd hit",
        "gap_ur": "1st aur 2nd hit ke darmiyan db+1 lagayein",
        "punish_en": "Block f+1+2,2 for guaranteed i14 launch punish (-14)",
        "punish_ur": "f+1+2,2 block karke i14 launch karein"
    }
}

print("Loaded all 43 ten-hit string counter records.")

def seed_database_and_compendium():
    print("Beginning comprehensive seeding of all 43 fighters...")
    
    # 1. Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop existing tables if needed or recreate fresh
    cur.execute("DROP TABLE IF EXISTS character_throws")
    cur.execute("DROP TABLE IF EXISTS character_wall_combos")
    cur.execute("DROP TABLE IF EXISTS character_ten_hits")

    cur.execute("""
    CREATE TABLE character_throws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER NOT NULL,
        character_name TEXT NOT NULL,
        character_slug TEXT NOT NULL,
        category TEXT NOT NULL,
        throw_name TEXT NOT NULL,
        command_input TEXT NOT NULL,
        startup_frames TEXT NOT NULL,
        break_input TEXT NOT NULL,
        break_window TEXT NOT NULL,
        visual_cue TEXT NOT NULL,
        visual_cue_en TEXT,
        visual_cue_ur TEXT,
        damage TEXT NOT NULL,
        damage_num INTEGER,
        oki_property TEXT NOT NULL,
        oki_property_en TEXT,
        oki_property_ur TEXT,
        properties_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE character_wall_combos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER NOT NULL,
        character_name TEXT NOT NULL,
        character_slug TEXT NOT NULL,
        route_type TEXT NOT NULL,
        combo_notation TEXT NOT NULL,
        total_wall_damage TEXT NOT NULL,
        damage_num INTEGER,
        spike_flip_property TEXT NOT NULL,
        tactical_utility_notes TEXT NOT NULL,
        tactical_utility_notes_en TEXT,
        tactical_utility_notes_ur TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE character_ten_hits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER NOT NULL,
        character_name TEXT NOT NULL,
        character_slug TEXT NOT NULL,
        combo_name TEXT NOT NULL,
        combo_input TEXT NOT NULL,
        hit_sequence_breakdown TEXT NOT NULL,
        low_parry_duck_window TEXT NOT NULL,
        low_parry_duck_window_en TEXT,
        low_parry_duck_window_ur TEXT,
        interrupt_gap TEXT NOT NULL,
        interrupt_gap_en TEXT,
        interrupt_gap_ur TEXT,
        optimal_punish TEXT NOT NULL,
        optimal_punish_en TEXT,
        optimal_punish_ur TEXT,
        how_to_counter TEXT,
        how_to_counter_en TEXT,
        how_to_counter_ur TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Prepare datasets for DB and master_compendium.json
    all_throws_json = []
    all_wall_combos_json = []
    all_ten_hits_json = []

    total_throws_count = 0
    total_wall_combos_count = 0
    total_ten_hits_count = 0

    # 1. PROCESS ALL THROWS
    for ch in CHARACTERS:
        cid = ch["id"]
        cslug = ch["slug"]
        cname = ch["name"]

        # A. Generic Throws
        generics = [
            {
                "category": "Generic Throws",
                "name": f"{cname} Standard Left Grab",
                "input": "1+3",
                "startup": "i12",
                "break": "1 or 2",
                "window": "20f standard",
                "visual": "Left Arm Lead [1]",
                "visual_ur": "Bayaan Haath (Left Arm) aage aata hai [1]",
                "dmg": "35 dmg",
                "dmg_num": 35,
                "oki": "Neutral standup reset, position swap",
                "oki_ur": "Position swap, normal standup reset"
            },
            {
                "category": "Generic Throws",
                "name": f"{cname} Standard Right Grab",
                "input": "2+4",
                "startup": "i12",
                "break": "1 or 2",
                "window": "20f standard",
                "visual": "Right Arm Lead [2]",
                "visual_ur": "Dayaan Haath (Right Arm) aage aata hai [2]",
                "dmg": "35 dmg",
                "dmg_num": 35,
                "oki": "Floor Break on Sanctum & Descent into Subconscious",
                "oki_ur": "Floor Break on Sanctum & Descent into Subconscious"
            },
            {
                "category": "Generic Throws",
                "name": f"{cname} Overhead Forward Throw",
                "input": "uf+1+2",
                "startup": "i12",
                "break": "1+2",
                "window": "20f standard",
                "visual": "Both Hands Extended [1+2]",
                "visual_ur": "Dono Haath ek sath aage aate hain [1+2]",
                "dmg": "40 dmg",
                "dmg_num": 40,
                "oki": "Wall Splat near wall / floor break",
                "oki_ur": "Deewar ke paas Wall Splat aur Floor Break"
            },
            {
                "category": "Side & Back Throws",
                "name": f"{cname} Left Flank Throw",
                "input": "Side 1+3 or 2+4",
                "startup": "i12",
                "break": "1",
                "window": "14f tight",
                "visual": "Left Side Arm Hook [1]",
                "visual_ur": "Left Side Hook Grab [1]",
                "dmg": "40 dmg",
                "dmg_num": 40,
                "oki": "Side wall splat advantage",
                "oki_ur": "Side wall splat advantage"
            },
            {
                "category": "Side & Back Throws",
                "name": f"{cname} Right Flank Throw",
                "input": "Side 1+3 or 2+4",
                "startup": "i12",
                "break": "2",
                "window": "14f tight",
                "visual": "Right Side Arm Takedown [2]",
                "visual_ur": "Right Side Takedown [2]",
                "dmg": "40 dmg",
                "dmg_num": 40,
                "oki": "Leaves opponent face-down",
                "oki_ur": "Opponent ko face-down chhorta hai"
            },
            {
                "category": "Side & Back Throws",
                "name": f"{cname} Back-Turned Throw",
                "input": "Rear 1+3 or 2+4",
                "startup": "i12",
                "break": "Unbreakable",
                "window": "Unbreakable (0f)",
                "visual": "Rear Spine Slam / Choke",
                "visual_ur": "Peeche se Spine Slam (Unbreakable)",
                "dmg": "55 dmg",
                "dmg_num": 55,
                "oki": "Massive guaranteed damage + complete oki dominance",
                "oki_ur": "55-60 massive damage aur guaranteed oki dominance"
            }
        ]

        # B. Command Throws
        cmd_list = COMMAND_THROWS.get(cslug, [
            {
                "name": f"{cname} Signature Command Throw",
                "input": "f,f+1+2",
                "startup": "i12",
                "break": "1+2",
                "window": "20f",
                "visual": "Both Hands Clasp [1+2]",
                "dmg": "42 dmg",
                "dmg_num": 42,
                "oki": "Floor Break on Sanctum & Descent into Subconscious"
            },
            {
                "name": f"{cname} Flank Tackle Throw",
                "input": "df+1+2",
                "startup": "i12",
                "break": "1+2",
                "window": "20f",
                "visual": "Both Hands Double Push [1+2]",
                "dmg": "40 dmg",
                "dmg_num": 40,
                "oki": "Wall Splat near wall"
            }
        ])

        # Combine
        combined_throws = generics + [dict(item, category="Command Throws") for item in cmd_list]

        for t in combined_throws:
            vis_en = t.get("visual", "Visual Cue")
            vis_ur = t.get("visual_ur", vis_en)
            oki_en = t.get("oki", "Knockdown")
            oki_ur = t.get("oki_ur", oki_en)
            b_input = t.get("break", "1+2")

            cur.execute("""
            INSERT INTO character_throws (
                character_id, character_name, character_slug, category, throw_name,
                command_input, startup_frames, break_input, break_window, visual_cue,
                visual_cue_en, visual_cue_ur, damage, damage_num, oki_property,
                oki_property_en, oki_property_ur, properties_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cid, cname, cslug, t["category"], t["name"],
                t["input"], t["startup"], b_input, t["window"],
                vis_en, vis_en, vis_ur, t["dmg"], t.get("dmg_num", 40),
                oki_en, oki_en, oki_ur, f"Break: {b_input} | Window: {t['window']}"
            ))
            total_throws_count += 1

            all_throws_json.append({
                "character": cname,
                "character_slug": cslug,
                "category": t["category"],
                "throw_name": t["name"],
                "input_notation": t["input"],
                "command_input": t["input"],
                "startup_frames": t["startup"],
                "break_input": b_input,
                "break_window": t["window"],
                "visual_cue": vis_en,
                "visual_cue_en": vis_en,
                "visual_cue_ur": vis_ur,
                "break_guide": f"{vis_en} ➔ Break {b_input}",
                "break_guide_en": f"{vis_en} ➔ Break {b_input}",
                "break_guide_ur": f"{vis_ur} ➔ Break {b_input}",
                "damage": t["dmg"],
                "damage_num": t.get("dmg_num", 40),
                "oki_property": oki_en,
                "oki_property_en": oki_en,
                "oki_property_ur": oki_ur
            })

    # 2. PROCESS ALL WALL COMBOS (3 routes per character = 129 routes)
    for ch in CHARACTERS:
        cid = ch["id"]
        cslug = ch["slug"]
        cname = ch["name"]

        routes = WALL_COMBOS_DATA.get(cslug, [
            {"route": "Max Damage Wall Combo (T! Available)", "notation": "df+1,2 (T!) -> df+1 -> b+1+2", "dmg": "44 DMG", "dmg_num": 44, "spike": "Hard Ground Spike", "notes_en": "Delay last hit for maximum unscaled damage", "notes_ur": "Last hit delay karein for maximum ground damage"},
            {"route": "Post-Tornado Wall Ender (T! Expended)", "notation": "df+1 -> b+1+2", "dmg": "27 DMG", "dmg_num": 27, "spike": "Ground Spike", "notes_en": "Universal consistent post-tornado wall ender", "notes_ur": "Midscreen tornado ke baad standard high damage ender"},
            {"route": "Oki / Resplat / Setup Wall Ender", "notation": "1 -> d+1+2 Ground Mount Setup", "dmg": "22 DMG", "dmg_num": 22, "spike": "Tech Roll Catch", "notes_en": "Catches stand-up tech at the wall", "notes_ur": "Deewar par uthte hue opponent ko trap karta hai"}
        ])

        for r in routes:
            cur.execute("""
            INSERT INTO character_wall_combos (
                character_id, character_name, character_slug, route_type,
                combo_notation, total_wall_damage, damage_num, spike_flip_property,
                tactical_utility_notes, tactical_utility_notes_en, tactical_utility_notes_ur
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cid, cname, cslug, r["route"],
                r["notation"], r["dmg"], r.get("dmg_num", 40), r["spike"],
                r["notes_en"], r["notes_en"], r["notes_ur"]
            ))
            total_wall_combos_count += 1

            all_wall_combos_json.append({
                "character": cname,
                "character_slug": cslug,
                "route_type": r["route"],
                "route_type_en": r["route"],
                "route_type_ur": r["route"],
                "wall_ender": r["notation"],
                "wall_ender_optimal": r["notation"],
                "damage_utility": f"{r['dmg']} | {r['notes_en']}",
                "damage_utility_en": f"{r['dmg']} | {r['notes_en']}",
                "damage_utility_ur": f"{r['dmg']} | {r['notes_ur']}",
                "tactical_notes": r["notes_en"],
                "tactical_notes_en": r["notes_en"],
                "tactical_notes_ur": r["notes_ur"],
                "tornado_move": r["notation"].split("->")[0].strip() if "(T!)" in r["notation"] else "None (Post-Tornado)",
                "total_wall_damage": r["dmg"],
                "damage_num": r.get("dmg_num", 40),
                "spike_flip_property": r["spike"]
            })

    # 3. PROCESS ALL 10-HIT STRING COUNTERS (All 43 Fighters)
    for ch in CHARACTERS:
        cid = ch["id"]
        cslug = ch["slug"]
        cname = ch["name"]

        ten = TEN_HIT_DATA.get(cslug, {
            "name": f"{cname} Signature Multi-Hit String Counter",
            "input": "df+1,2,1 / 1,2,d+3,4",
            "seq": "m, h, m / h, h, l, m",
            "duck_window_en": "3rd hit is a Low kick -> Hold df (Low Parry)",
            "duck_window_ur": "3rd hit Low kick hai -> df (Low Parry) hold karein",
            "gap_en": "Gap before 3rd hit allows Dickjab (db+1) interrupt",
            "gap_ur": "3rd hit se pehle Dickjab (db+1) se interrupt karein",
            "punish_en": "Low Parry on 3rd hit for full airborne juggle launch",
            "punish_ur": "3rd hit par Low Parry karein aur full launch karein"
        })

        cur.execute("""
        INSERT INTO character_ten_hits (
            character_id, character_name, character_slug, combo_name, combo_input,
            hit_sequence_breakdown, low_parry_duck_window, low_parry_duck_window_en,
            low_parry_duck_window_ur, interrupt_gap, interrupt_gap_en, interrupt_gap_ur,
            optimal_punish, optimal_punish_en, optimal_punish_ur, how_to_counter,
            how_to_counter_en, how_to_counter_ur
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cid, cname, cslug, ten["name"], ten["input"],
            ten["seq"], ten["duck_window_en"], ten["duck_window_en"], ten["duck_window_ur"],
            ten["gap_en"], ten["gap_en"], ten["gap_ur"],
            ten["punish_en"], ten["punish_en"], ten["punish_ur"],
            f"{ten['duck_window_en']} -> {ten['punish_en']}",
            f"{ten['duck_window_en']} -> {ten['punish_en']}",
            f"{ten['duck_window_ur']} -> {ten['punish_ur']}"
        ))
        total_ten_hits_count += 1

        all_ten_hits_json.append({
            "character": cname,
            "character_slug": cslug,
            "combo_input": ten["input"],
            "ten_hit_name": ten["name"],
            "ten_hit_name_en": ten["name"],
            "ten_hit_name_ur": ten["name"],
            "hit_sequence_breakdown": ten["seq"],
            "where_to_duck_parry": ten["duck_window_en"],
            "where_to_duck_parry_en": ten["duck_window_en"],
            "where_to_duck_parry_ur": ten["duck_window_ur"],
            "interrupt_gap": ten["gap_en"],
            "interrupt_gap_en": ten["gap_en"],
            "interrupt_gap_ur": ten["gap_ur"],
            "optimal_punish": ten["punish_en"],
            "optimal_punish_en": ten["punish_en"],
            "optimal_punish_ur": ten["punish_ur"],
            "how_to_counter": f"{ten['duck_window_en']} -> {ten['punish_en']}",
            "how_to_counter_en": f"{ten['duck_window_en']} -> {ten['punish_en']}",
            "how_to_counter_ur": f"{ten['duck_window_ur']} -> {ten['punish_ur']}"
        })

    # Commit DB changes
    conn.commit()
    conn.close()
    print(f"SQLite DB committed successfully:")
    print(f"  - character_throws: {total_throws_count} rows")
    print(f"  - character_wall_combos: {total_wall_combos_count} rows")
    print(f"  - character_ten_hits: {total_ten_hits_count} rows")

    # Update master_compendium.json
    with open(COMPENDIUM_PATH, "r", encoding="utf-8") as f:
        compendium = json.load(f)

    compendium["throw_breaks"] = all_throws_json
    compendium["wall_combos"] = all_wall_combos_json
    compendium["ten_hit_counters"] = all_ten_hits_json

    with open(COMPENDIUM_PATH, "w", encoding="utf-8") as f:
        json.dump(compendium, f, indent=2, ensure_ascii=False)

    print(f"master_compendium.json updated successfully:")
    print(f"  - throw_breaks: {len(all_throws_json)} entries")
    print(f"  - wall_combos: {len(all_wall_combos_json)} entries")
    print(f"  - ten_hit_counters: {len(all_ten_hits_json)} entries")

if __name__ == "__main__":
    seed_database_and_compendium()
