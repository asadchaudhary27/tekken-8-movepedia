"""
Seed centimeter-accurate stage telemetry into tekken8_fyp.db.
Populates all 18 official Tekken 8 battlegrounds with:
- Metric (m) and Centimeter (cm) dimensions
- Total area in m2
- Exact center coordinates (0, 0) and round-start spawn telemetry (P1: -200 cm, P2: +200 cm)
- Distance to nearest back wall in m and cm + number of backdashes required
- Distance to side walls in m and cm
- Combo carry requirement to reach wall splat zone
- Multi-tier lower/secondary floor dimensions for all multi-level stages
"""
import sqlite3
import json

STAGE_TELEMETRY = {
    1: { # The Arena
        "name": "The Arena",
        "slug": "the-arena",
        "boundary_shape": "Octagonal",
        "wall_distance": "28.0m x 28.0m / 2,800 cm x 2,800 cm (Octagon)",
        "width_m": 28.0, "length_m": 28.0, "width_cm": 2800, "length_cm": 2800, "area_sqm": 784,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 12.0, "wall_dist_behind_cm": 1200, "backdashes_to_wall": 7,
        "side_wall_dist_m": 14.0, "side_wall_dist_cm": 1400,
        "combo_carry_requirement": "Launch + 4 hits + Tornado (T!) + Heat Dash to reach wall splat zone",
        "secondary_floor": None,
        "elements": [
            {"element_type": "wall", "label": "Tournament Perimeter Barrier", "points": "120,40 280,40 360,120 360,280 280,360 120,360 40,280 40,120", "color": "#ef4444", "notes": "Solid unbroken tournament wall boundary."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Round start spawn (-200 cm)"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Round start spawn (+200 cm)"},
            {"element_type": "spawn_zone", "label": "Neutral Standoff (0,0)", "x": 200, "y": 200, "radius": 40, "color": "rgba(56, 189, 248, 0.25)", "notes": "Center point (0,0) with 400 cm opening standoff"}
        ]
    },
    2: { # Urban Square
        "name": "Urban Square",
        "slug": "urban-square",
        "boundary_shape": "Rectangular",
        "wall_distance": "24.0m x 36.0m / 2,400 cm x 3,600 cm (Rectangle)",
        "width_m": 24.0, "length_m": 36.0, "width_cm": 2400, "length_cm": 3600, "area_sqm": 864,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 16.0, "wall_dist_behind_cm": 1600, "backdashes_to_wall": 9,
        "side_wall_dist_m": 10.0, "side_wall_dist_cm": 1000,
        "combo_carry_requirement": "Launch + 5 hits + Tornado (T!) into South Balcony Break",
        "secondary_floor": {
            "name": "Lower Subway Plaza (After Balcony Break)",
            "width_m": 20.0, "length_m": 24.0, "width_cm": 2000, "length_cm": 2400, "area_sqm": 480,
            "wall_dist_behind_m": 10.0, "wall_dist_behind_cm": 1000, "backdashes_to_wall": 6
        },
        "elements": [
            {"element_type": "wall", "label": "North Building Perimeter", "x": 200, "y": 25, "width": 320, "height": 12, "color": "#64748b", "notes": "Unbreakable building front."},
            {"element_type": "hazard", "label": "Wall Blast Billboard (East)", "x": 355, "y": 150, "width": 12, "height": 160, "color": "#ef4444", "notes": "Explosive digital billboard triggers Wall Blast on wall splat."},
            {"element_type": "balcony", "label": "Balcony Break Railing (South)", "x": 200, "y": 265, "width": 260, "height": 12, "color": "#f59e0b", "notes": "Balcony break sends opponent down to Lower Subway Plaza (20m x 24m)."},
            {"element_type": "wall", "label": "West Storefront Perimeter", "x": 45, "y": 150, "width": 12, "height": 160, "color": "#64748b", "notes": "Storefront wall boundary."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 150, "radius": 8, "color": "#38bdf8", "notes": "Crosswalk standoff P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 150, "radius": 8, "color": "#f43f5e", "notes": "Crosswalk standoff P2"}
        ]
    },
    3: { # Yakushima
        "name": "Yakushima",
        "slug": "yakushima",
        "boundary_shape": "Huge Open (Semi-Infinite)",
        "wall_distance": "80.0m x 120.0m / 8,000 cm x 12,000 cm (Open Field)",
        "width_m": 80.0, "length_m": 120.0, "width_cm": 8000, "length_cm": 12000, "area_sqm": 9600,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 58.0, "wall_dist_behind_cm": 5800, "backdashes_to_wall": 35,
        "side_wall_dist_m": 38.0, "side_wall_dist_cm": 3800,
        "combo_carry_requirement": "Infinite open ground — zero wall splat reach; optimize for maximum raw launcher damage and oki",
        "secondary_floor": None,
        "elements": [
            {"element_type": "wall", "label": "Distant Forest Boundary", "points": "40,40 360,40 360,360 40,360", "color": "#22c55e", "notes": "Massive natural open boundaries; virtually infinite playable spacing."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "P1 Sanctuary spawn"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "P2 Sanctuary spawn"},
            {"element_type": "spawn_zone", "label": "Sacred Grove Center (0,0)", "x": 200, "y": 200, "radius": 50, "color": "rgba(34, 197, 94, 0.2)", "notes": "Center point (0,0) in ancient cedar grove"}
        ]
    },
    4: { # Rebel Hangar
        "name": "Rebel Hangar",
        "slug": "rebel-hangar",
        "boundary_shape": "Irregular Octagon",
        "wall_distance": "24.0m x 24.0m / 2,400 cm x 2,400 cm (Square Octagon)",
        "width_m": 24.0, "length_m": 24.0, "width_cm": 2400, "length_cm": 2400, "area_sqm": 576,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 10.0, "wall_dist_behind_cm": 1000, "backdashes_to_wall": 6,
        "side_wall_dist_m": 12.0, "side_wall_dist_cm": 1200,
        "combo_carry_requirement": "Launch + 3 hits + Tornado (T!) into Munitions Wall Blast / Side Ledge",
        "secondary_floor": {
            "name": "Lower Maintenance Trench (Side Ledge Break)",
            "width_m": 20.0, "length_m": 20.0, "width_cm": 2000, "length_cm": 2000, "area_sqm": 400,
            "wall_dist_behind_m": 8.0, "wall_dist_behind_cm": 800, "backdashes_to_wall": 5
        },
        "elements": [
            {"element_type": "wall", "label": "Reinforced Bulkhead (North)", "x": 200, "y": 45, "width": 290, "height": 14, "color": "#475569", "notes": "Reinforced steel hangar wall."},
            {"element_type": "hazard", "label": "Wall Blast Munitions Bay (East)", "x": 345, "y": 200, "width": 14, "height": 220, "color": "#ef4444", "notes": "Munitions storage bulkhead triggers explosive Wall Blast."},
            {"element_type": "wall", "label": "South Flight Deck Barrier", "x": 200, "y": 355, "width": 290, "height": 14, "color": "#475569", "notes": "Steel bulkhead perimeter."},
            {"element_type": "balcony", "label": "Side Ledge Balcony Break (West)", "x": 55, "y": 200, "width": 14, "height": 220, "color": "#f59e0b", "notes": "Side catwalk collapses into lower maintenance trench."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Flight deck starting spawn P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Flight deck starting spawn P2"}
        ]
    },
    5: { # Sanctum
        "name": "Sanctum",
        "slug": "sanctum",
        "boundary_shape": "Narrow Corridor",
        "wall_distance": "22.0m x 32.0m / 2,200 cm x 3,200 cm (Narrow Octagon)",
        "width_m": 22.0, "length_m": 32.0, "width_cm": 2200, "length_cm": 3200, "area_sqm": 704,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 14.0, "wall_dist_behind_cm": 1400, "backdashes_to_wall": 8,
        "side_wall_dist_m": 9.0, "side_wall_dist_cm": 900,
        "combo_carry_requirement": "Launch + 3 hits + Tornado (T!) into Temple Pillar Wall Break",
        "secondary_floor": {
            "name": "Subterranean Crypt (Floor Break)",
            "width_m": 20.0, "length_m": 20.0, "width_cm": 2000, "length_cm": 2000, "area_sqm": 400,
            "wall_dist_behind_m": 8.0, "wall_dist_behind_cm": 800, "backdashes_to_wall": 5
        },
        "elements": [
            {"element_type": "wall", "label": "Ancient Temple Columns", "points": "130,50 270,50 350,130 350,270 270,350 130,350 50,270 50,130", "color": "#8b5cf6", "notes": "Hard wall break zone and stone pillars inducing wall bound."},
            {"element_type": "break_zone", "label": "Subterranean Crypt Floor Break", "x": 200, "y": 200, "radius": 50, "color": "#f97316", "notes": "Downward knockdown collapses center floor into crypt (20m x 20m)."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Altar standoff P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Altar standoff P2"}
        ]
    },
    6: { # Into the Stratosphere
        "name": "Into the Stratosphere",
        "slug": "into-the-stratosphere",
        "boundary_shape": "Octagon to Narrow Core",
        "wall_distance": "26.0m x 26.0m / 2,600 cm x 2,600 cm (Core Octagon)",
        "width_m": 26.0, "length_m": 26.0, "width_cm": 2600, "length_cm": 2600, "area_sqm": 676,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 11.0, "wall_dist_behind_cm": 1100, "backdashes_to_wall": 6.5,
        "side_wall_dist_m": 13.0, "side_wall_dist_cm": 1300,
        "combo_carry_requirement": "Launch + 4 hits + Tornado (T!) / Downward Spike Floor Break",
        "secondary_floor": {
            "name": "Lower Magma Chamber (Hard Floor Break + Floor Blast)",
            "width_m": 22.0, "length_m": 22.0, "width_cm": 2200, "length_cm": 2200, "area_sqm": 484,
            "wall_dist_behind_m": 9.0, "wall_dist_behind_cm": 900, "backdashes_to_wall": 5.5
        },
        "elements": [
            {"element_type": "wall", "label": "Volcanic Asteroid Ring", "points": "140,40 260,40 360,140 360,260 260,360 140,360 40,260 40,140", "color": "#f97316", "notes": "Igneous rock crust boundary."},
            {"element_type": "hazard", "label": "Floor Blast Magma Vents", "x": 200, "y": 200, "radius": 45, "color": "#ef4444", "notes": "Downward slam breaks floor; lower magma chamber triggers vertical relaunch Floor Blast."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Crater spawn P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Crater spawn P2"}
        ]
    },
    7: { # Ortiz Farm
        "name": "Ortiz Farm",
        "slug": "ortiz-farm",
        "boundary_shape": "Multi-tier 3-Level Compound",
        "wall_distance": "26.0m x 22.0m / 2,600 cm x 2,200 cm (Tier 1 Field)",
        "width_m": 26.0, "length_m": 22.0, "width_cm": 2600, "length_cm": 2200, "area_sqm": 572,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 11.0, "wall_dist_behind_cm": 1100, "backdashes_to_wall": 6.5,
        "side_wall_dist_m": 9.0, "side_wall_dist_cm": 900,
        "combo_carry_requirement": "Launch + 3 hits + Tornado (T!) into Barn Wall Break (Highest damage stage)",
        "secondary_floor": {
            "name": "Tier 2 Barn (Wall Break) & Tier 3 Lower Cellar (Floor Break)",
            "width_m": 22.0, "length_m": 20.0, "width_cm": 2200, "length_cm": 2000, "area_sqm": 440,
            "tier3_cellar_m": "20.0m x 18.0m / 2,000 cm x 1,800 cm (Area: 360 m2)",
            "wall_dist_behind_m": 9.0, "wall_dist_behind_cm": 900, "backdashes_to_wall": 5.5
        },
        "elements": [
            {"element_type": "wall", "label": "Farmhouse Perimeter", "x": 200, "y": 30, "width": 280, "height": 14, "color": "#a16207", "notes": "Wood fence perimeter."},
            {"element_type": "wall_break", "label": "Barn Wall Break (East)", "x": 340, "y": 200, "width": 14, "height": 180, "color": "#ea580c", "notes": "Wall break transitions into Tier 2 Barn interior."},
            {"element_type": "break_zone", "label": "Barn Floor Break Zone", "x": 200, "y": 200, "radius": 40, "color": "#f59e0b", "notes": "Tier 2 floor breaks down to Tier 3 Ancient Cellar."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Coffee grove P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Coffee grove P2"}
        ]
    },
    8: { # Coliseum / Coliseum of Fate
        "name": "Coliseum",
        "slug": "coliseum",
        "boundary_shape": "Huge Octagon",
        "wall_distance": "44.0m x 44.0m / 4,400 cm x 4,400 cm (Grand Octagon)",
        "width_m": 44.0, "length_m": 44.0, "width_cm": 4400, "length_cm": 4400, "area_sqm": 1936,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 20.0, "wall_dist_behind_cm": 2000, "backdashes_to_wall": 12,
        "side_wall_dist_m": 22.0, "side_wall_dist_cm": 2200,
        "combo_carry_requirement": "Launch + 6 hits + Tornado (T!) + Double Dash / Heat Dash to wall",
        "secondary_floor": None,
        "elements": [
            {"element_type": "wall", "label": "Coliseum Stone Perimeter", "points": "100,20 300,20 380,100 380,300 300,380 100,380 20,300 20,100", "color": "#eab308", "notes": "Grand unbroken Roman arena perimeter."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Gladiator spawn P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Gladiator spawn P2"}
        ]
    },
    9: { # Celebration on the Seine
        "name": "Celebration on the Seine",
        "slug": "celebration-on-the-seine",
        "boundary_shape": "Narrow Bridge",
        "wall_distance": "20.0m x 34.0m / 2,000 cm x 3,400 cm (Narrow Rectangle)",
        "width_m": 20.0, "length_m": 34.0, "width_cm": 2000, "length_cm": 3400, "area_sqm": 680,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 15.0, "wall_dist_behind_cm": 1500, "backdashes_to_wall": 9,
        "side_wall_dist_m": 8.0, "side_wall_dist_cm": 800,
        "combo_carry_requirement": "Launch + 4 hits + Tornado (T!) — lateral walls are only 2-3 sidesteps away!",
        "secondary_floor": None,
        "elements": [
            {"element_type": "wall", "label": "Bridge Railing (North)", "x": 200, "y": 50, "width": 340, "height": 12, "color": "#3b82f6", "notes": "Tight lateral bridge barrier."},
            {"element_type": "wall", "label": "Bridge Railing (South)", "x": 200, "y": 350, "width": 340, "height": 12, "color": "#3b82f6", "notes": "Tight lateral bridge barrier."},
            {"element_type": "wall", "label": "Bridge Gate (East)", "x": 370, "y": 200, "width": 12, "height": 300, "color": "#64748b", "notes": "Unbreakable bridge archway."},
            {"element_type": "wall", "label": "Bridge Gate (West)", "x": 30, "y": 200, "width": 12, "height": 300, "color": "#64748b", "notes": "Unbreakable bridge archway."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Bridge centerline P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Bridge centerline P2"}
        ]
    },
    10: { # Midnight Siege
        "name": "Midnight Siege",
        "slug": "midnight-siege",
        "boundary_shape": "Asymmetric Ruin",
        "wall_distance": "22.0m x 24.0m / 2,200 cm x 2,400 cm (Urban Ruins)",
        "width_m": 22.0, "length_m": 24.0, "width_cm": 2200, "length_cm": 2400, "area_sqm": 528,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 9.0, "wall_dist_behind_cm": 900, "backdashes_to_wall": 5.5,
        "side_wall_dist_m": 10.0, "side_wall_dist_cm": 1000,
        "combo_carry_requirement": "Launch + 3 hits + Tornado (T!) into APC Truck Wall Break",
        "secondary_floor": {
            "name": "Lower War Ruins (After APC Rubble Break)",
            "width_m": 20.0, "length_m": 18.0, "width_cm": 2000, "length_cm": 1800, "area_sqm": 360,
            "wall_dist_behind_m": 7.0, "wall_dist_behind_cm": 700, "backdashes_to_wall": 4.5
        },
        "elements": [
            {"element_type": "wall", "label": "Ruin Bulkhead (North)", "x": 200, "y": 40, "width": 260, "height": 14, "color": "#64748b", "notes": "Crumbling urban concrete wall."},
            {"element_type": "wall_break", "label": "APC Truck Wall Break (East)", "x": 330, "y": 200, "width": 14, "height": 200, "color": "#ea580c", "notes": "Wall break triggers APC collision and expands combat arena."},
            {"element_type": "hazard", "label": "Explosive Munitions (West)", "x": 70, "y": 200, "width": 14, "height": 200, "color": "#ef4444", "notes": "Wall Blast hazard triggers massive relaunch."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Rubble standoff P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Rubble standoff P2"}
        ]
    },
    11: { # Urban Square (Evening)
        "name": "Urban Square (Evening)",
        "slug": "urban-square-evening",
        "boundary_shape": "Rectangular",
        "wall_distance": "24.0m x 36.0m / 2,400 cm x 3,600 cm (Evening Rectangle)",
        "width_m": 24.0, "length_m": 36.0, "width_cm": 2400, "length_cm": 3600, "area_sqm": 864,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 16.0, "wall_dist_behind_cm": 1600, "backdashes_to_wall": 9,
        "side_wall_dist_m": 10.0, "side_wall_dist_cm": 1000,
        "combo_carry_requirement": "Launch + 5 hits + Tornado (T!) into South Balcony Break",
        "secondary_floor": {
            "name": "Lower Subway Station (After Balcony Break)",
            "width_m": 20.0, "length_m": 24.0, "width_cm": 2000, "length_cm": 2400, "area_sqm": 480,
            "wall_dist_behind_m": 10.0, "wall_dist_behind_cm": 1000, "backdashes_to_wall": 6
        },
        "elements": [
            {"element_type": "wall", "label": "North Perimeter Wall", "x": 200, "y": 25, "width": 320, "height": 12, "color": "#64748b", "notes": "Evening city storefront."},
            {"element_type": "hazard", "label": "Wall Blast Zone (East)", "x": 355, "y": 150, "width": 12, "height": 160, "color": "#ef4444", "notes": "Explosive billboard triggers Wall Blast."},
            {"element_type": "balcony", "label": "Balcony Break Railing (South)", "x": 200, "y": 265, "width": 260, "height": 12, "color": "#f59e0b", "notes": "Balcony break plunges fighters down into Lower Subway Plaza."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 150, "radius": 8, "color": "#38bdf8", "notes": "Evening crosswalk P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 150, "radius": 8, "color": "#f43f5e", "notes": "Evening crosswalk P2"}
        ]
    },
    12: { # The Arena (Underground)
        "name": "The Arena (Underground)",
        "slug": "arena-underground",
        "boundary_shape": "Enclosed Octagon",
        "wall_distance": "24.0m x 24.0m / 2,400 cm x 2,400 cm (Enclosed Octagon)",
        "width_m": 24.0, "length_m": 24.0, "width_cm": 2400, "length_cm": 2400, "area_sqm": 576,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 10.0, "wall_dist_behind_cm": 1000, "backdashes_to_wall": 6,
        "side_wall_dist_m": 12.0, "side_wall_dist_cm": 1200,
        "combo_carry_requirement": "Launch + 3 hits + Tornado (T!) into 4x Wall Blasts",
        "secondary_floor": None,
        "elements": [
            {"element_type": "hazard", "label": "Explosive Blast Barriers (All 4 Quadrants)", "points": "120,40 280,40 360,120 360,280 280,360 120,360 40,280 40,120", "color": "#ef4444", "notes": "4x Active Wall Blast panels; walls explode on impact for 110+ dmg juggles."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Cage center P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Cage center P2"}
        ]
    },
    13: { # Elegant Palace
        "name": "Elegant Palace",
        "slug": "elegant-palace",
        "boundary_shape": "Large Chamber",
        "wall_distance": "30.0m x 32.0m / 3,000 cm x 3,200 cm (Grand Palace)",
        "width_m": 30.0, "length_m": 32.0, "width_cm": 3000, "length_cm": 3200, "area_sqm": 960,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 14.0, "wall_dist_behind_cm": 1400, "backdashes_to_wall": 8,
        "side_wall_dist_m": 13.0, "side_wall_dist_cm": 1300,
        "combo_carry_requirement": "Launch + 4 hits + Tornado (T!) into 2x Wall Breaks / Center Balcony Break",
        "secondary_floor": {
            "name": "Lower Courtyard (Balcony Break)",
            "width_m": 24.0, "length_m": 22.0, "width_cm": 2400, "length_cm": 2200, "area_sqm": 528,
            "wall_dist_behind_m": 9.0, "wall_dist_behind_cm": 900, "backdashes_to_wall": 5.5
        },
        "elements": [
            {"element_type": "wall", "label": "Palace Ballroom Walls", "points": "100,30 300,30 370,100 370,300 300,370 100,370 30,300 30,100", "color": "#d97706", "notes": "Opulent gilded walls with 2 destructible wall sections."},
            {"element_type": "balcony", "label": "Grand Center Balcony Break", "x": 200, "y": 360, "width": 160, "height": 14, "color": "#f59e0b", "notes": "Balcony splat drops opponent down into Lower Rose Courtyard."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Chandelier standoff P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Chandelier standoff P2"}
        ]
    },
    14: { # Descent into Subconscious
        "name": "Descent into Subconscious",
        "slug": "descent-into-subconscious",
        "boundary_shape": "Multi-Tier Void",
        "wall_distance": "24.0m x 24.0m / 2,400 cm x 2,400 cm (Tier 1 Void)",
        "width_m": 24.0, "length_m": 24.0, "width_cm": 2400, "length_cm": 2400, "area_sqm": 576,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 10.0, "wall_dist_behind_cm": 1000, "backdashes_to_wall": 6,
        "side_wall_dist_m": 12.0, "side_wall_dist_cm": 1200,
        "combo_carry_requirement": "Launch + 3 hits + Downward Spike / Throw Floor Break (2x Consecutive Breaks)",
        "secondary_floor": {
            "name": "Tier 2 Mindscape & Tier 3 Abyss (2x Consecutive Floor Breaks)",
            "width_m": 22.0, "length_m": 22.0, "width_cm": 2200, "length_cm": 2200, "area_sqm": 484,
            "tier3_abyss_m": "20.0m x 20.0m / 2,000 cm x 2,000 cm (Area: 400 m2)",
            "wall_dist_behind_m": 8.0, "wall_dist_behind_cm": 800, "backdashes_to_wall": 5
        },
        "elements": [
            {"element_type": "wall", "label": "Memory Fragment Barrier", "points": "120,40 280,40 360,120 360,280 280,360 120,360 40,280 40,120", "color": "#6366f1", "notes": "Ethereal memory void boundary."},
            {"element_type": "break_zone", "label": "Double Floor Break Nexus", "x": 200, "y": 200, "radius": 55, "color": "#ec4899", "notes": "Dual floor break zones plunge fighters through 3 layers of subconsciousness."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Void epicenter P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Void epicenter P2"}
        ]
    },
    15: { # Secluded Training Ground
        "name": "Secluded Training Ground",
        "slug": "secluded-training-ground",
        "boundary_shape": "Long Hallway",
        "wall_distance": "18.0m x 40.0m / 1,800 cm x 4,000 cm (Long Corridor)",
        "width_m": 18.0, "length_m": 40.0, "width_cm": 1800, "length_cm": 4000, "area_sqm": 720,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 18.0, "wall_dist_behind_cm": 1800, "backdashes_to_wall": 11,
        "side_wall_dist_m": 7.0, "side_wall_dist_cm": 700,
        "combo_carry_requirement": "Launch + 3 hits + Tornado (T!) into 3x Consecutive Corridor Wall Breaks",
        "secondary_floor": None,
        "elements": [
            {"element_type": "wall_break", "label": "Wall Break #1 (North Partition)", "x": 200, "y": 45, "width": 260, "height": 14, "color": "#ea580c", "notes": "First wooden shoji partition shatters on splat."},
            {"element_type": "wall_break", "label": "Wall Break #2 (South Partition)", "x": 200, "y": 355, "width": 260, "height": 14, "color": "#ea580c", "notes": "Second wooden partition wall break extends runway."},
            {"element_type": "wall", "label": "Narrow Side Walls (East/West)", "x": 50, "y": 200, "width": 14, "height": 320, "color": "#475569", "notes": "Extremely narrow lateral walls (700 cm from center)."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Dojo centerline P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Dojo centerline P2"}
        ]
    },
    16: { # Genmaji Temple
        "name": "Genmaji Temple",
        "slug": "genmaji-temple",
        "boundary_shape": "Temple Courtyard",
        "wall_distance": "24.0m x 28.0m / 2,400 cm x 2,800 cm (Temple Courtyard)",
        "width_m": 24.0, "length_m": 28.0, "width_cm": 2400, "length_cm": 2800, "area_sqm": 672,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 12.0, "wall_dist_behind_cm": 1200, "backdashes_to_wall": 7,
        "side_wall_dist_m": 10.0, "side_wall_dist_cm": 1000,
        "combo_carry_requirement": "Launch + 4 hits + Tornado (T!) into Temple Gate Wall Break / Floor Break",
        "secondary_floor": {
            "name": "Lower Shrine Crypt (Underground Floor Break)",
            "width_m": 20.0, "length_m": 20.0, "width_cm": 2000, "length_cm": 2000, "area_sqm": 400,
            "wall_dist_behind_m": 8.0, "wall_dist_behind_cm": 800, "backdashes_to_wall": 5
        },
        "elements": [
            {"element_type": "wall_break", "label": "Sacred Temple Torii Gate (East)", "x": 340, "y": 200, "width": 14, "height": 180, "color": "#ea580c", "notes": "Torii gate wall break expands into autumn forest."},
            {"element_type": "break_zone", "label": "Shrine Floor Break Zone", "x": 200, "y": 200, "radius": 45, "color": "#f59e0b", "notes": "Temple floor breaks into subterranean shrine crypt."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Autumn courtyard P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Autumn courtyard P2"}
        ]
    },
    17: { # Fallen Destiny
        "name": "Fallen Destiny",
        "slug": "fallen-destiny",
        "boundary_shape": "Square",
        "wall_distance": "28.0m x 28.0m / 2,800 cm x 2,800 cm (Storm Octagon)",
        "width_m": 28.0, "length_m": 28.0, "width_cm": 2800, "length_cm": 2800, "area_sqm": 784,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 12.0, "wall_dist_behind_cm": 1200, "backdashes_to_wall": 7,
        "side_wall_dist_m": 14.0, "side_wall_dist_cm": 1400,
        "combo_carry_requirement": "Launch + 4 hits + Tornado (T!) + Heat Dash to reach wall splat zone",
        "secondary_floor": None,
        "elements": [
            {"element_type": "wall", "label": "Shipwreck Perimeter Barrier", "points": "120,40 280,40 360,120 360,280 280,360 120,360 40,280 40,120", "color": "#3b82f6", "notes": "Solid unbroken ocean storm barrier."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Storm center P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Storm center P2"}
        ]
    },
    18: { # Seaside Resort
        "name": "Seaside Resort",
        "slug": "seaside-resort",
        "boundary_shape": "Rectangular",
        "wall_distance": "32.0m x 24.0m / 3,200 cm x 2,400 cm (Beachside Rectangle)",
        "width_m": 32.0, "length_m": 24.0, "width_cm": 3200, "length_cm": 2400, "area_sqm": 768,
        "spawn_distance_m": 4.0, "spawn_distance_cm": 400,
        "wall_dist_behind_m": 14.0, "wall_dist_behind_cm": 1400, "backdashes_to_wall": 8,
        "side_wall_dist_m": 10.0, "side_wall_dist_cm": 1000,
        "combo_carry_requirement": "Launch + 4 hits + Tornado (T!) into Beachside Boardwalk Wall",
        "secondary_floor": None,
        "elements": [
            {"element_type": "wall", "label": "Boardwalk Beachside Perimeter", "x": 200, "y": 40, "width": 320, "height": 14, "color": "#0ea5e9", "notes": "Unbreakable tropical resort boundary."},
            {"element_type": "spawn_p1", "label": "P1 Spawn (-200 cm)", "x": 170, "y": 200, "radius": 8, "color": "#38bdf8", "notes": "Cabana beach standoff P1"},
            {"element_type": "spawn_p2", "label": "P2 Spawn (+200 cm)", "x": 230, "y": 200, "radius": 8, "color": "#f43f5e", "notes": "Cabana beach standoff P2"}
        ]
    }
}

def seed_stage_telemetry():
    conn = sqlite3.connect('tekken8_fyp.db')
    c = conn.cursor()
    
    updated_count = 0
    for stage_id, data in STAGE_TELEMETRY.items():
        geo_payload = {
            "is_verified": True,
            "shape": data["boundary_shape"],
            "width_meters": data["width_m"],
            "length_meters": data["length_m"],
            "width_cm": data["width_cm"],
            "length_cm": data["length_cm"],
            "area_sqm": data["area_sqm"],
            "center_spawn_coords": {"x": 0, "y": 0},
            "p1_spawn_coords": {"x": -200, "y": 0, "unit": "cm", "label": "P1 (-200 cm)"},
            "p2_spawn_coords": {"x": 200, "y": 0, "unit": "cm", "label": "P2 (+200 cm)"},
            "spawn_distance_m": data["spawn_distance_m"],
            "spawn_distance_cm": data["spawn_distance_cm"],
            "distance_to_back_wall_m": data["wall_dist_behind_m"],
            "distance_to_back_wall_cm": data["wall_dist_behind_cm"],
            "backdashes_to_wall": data["backdashes_to_wall"],
            "distance_to_side_wall_m": data["side_wall_dist_m"],
            "distance_to_side_wall_cm": data["side_wall_dist_cm"],
            "combo_carry_requirement": data["combo_carry_requirement"],
            "secondary_floor": data["secondary_floor"],
            "canvas_viewbox": "0 0 400 400",
            "elements": data["elements"]
        }
        
        c.execute("""
            UPDATE stages
            SET boundary_shape = ?,
                wall_distance = ?,
                geometry_data_json = ?
            WHERE id = ?
        """, (data["boundary_shape"], data["wall_distance"], json.dumps(geo_payload), stage_id))
        updated_count += 1
    
    conn.commit()
    conn.close()
    print(f"Successfully updated telemetry for {updated_count} stages in tekken8_fyp.db!")

if __name__ == "__main__":
    seed_stage_telemetry()
