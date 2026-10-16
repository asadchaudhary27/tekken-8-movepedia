"""
Update frontend/assets/js/stages.js with centimeter-accurate telemetry
for all 18 official battlegrounds.
"""
import re
import json

STAGE_CONFIGS = {
    'the-arena': {
        'width_m': 28.0, 'length_m': 28.0, 'width_cm': 2800, 'length_cm': 2800, 'area_sqm': 784,
        'distance_to_wall': 'Medium (28m)', 'distance_rating_code': 'MED_28M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 12.0, 'wall_dist_behind_cm': 1200, 'backdashes_to_wall': 7,
        'side_wall_dist_m': 14.0, 'side_wall_dist_cm': 1400,
        'combo_carry_requirement': 'Launch + 4 hits + Tornado (T!) + Heat Dash to wall',
        'secondary_floor': None, 'boundary_shape': 'Octagonal'
    },
    'urban-square': {
        'width_m': 24.0, 'length_m': 36.0, 'width_cm': 2400, 'length_cm': 3600, 'area_sqm': 864,
        'distance_to_wall': 'Medium-Short', 'distance_rating_code': 'RECT_36M_X_24M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 16.0, 'wall_dist_behind_cm': 1600, 'backdashes_to_wall': 9,
        'side_wall_dist_m': 10.0, 'side_wall_dist_cm': 1000,
        'combo_carry_requirement': 'Launch + 5 hits + Tornado (T!) into South Balcony Break',
        'secondary_floor': {
            'name': 'Lower Subway Plaza (After Balcony Break)',
            'width_m': 20.0, 'length_m': 24.0, 'width_cm': 2000, 'length_cm': 2400, 'area_sqm': 480,
            'wall_dist_behind_m': 10.0, 'wall_dist_behind_cm': 1000, 'backdashes_to_wall': 6
        },
        'boundary_shape': 'Rectangular'
    },
    'yakushima': {
        'width_m': 80.0, 'length_m': 120.0, 'width_cm': 8000, 'length_cm': 12000, 'area_sqm': 9600,
        'distance_to_wall': 'Boundless / Infinite', 'distance_rating_code': 'INFINITE_BOUNDLESS',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 58.0, 'wall_dist_behind_cm': 5800, 'backdashes_to_wall': 35,
        'side_wall_dist_m': 38.0, 'side_wall_dist_cm': 3800,
        'combo_carry_requirement': 'Infinite open ground — zero wall splat reach; optimize for maximum raw launcher damage and oki',
        'secondary_floor': None, 'boundary_shape': 'Huge Open (Semi-Infinite)'
    },
    'rebel-hangar': {
        'width_m': 24.0, 'length_m': 24.0, 'width_cm': 2400, 'length_cm': 2400, 'area_sqm': 576,
        'distance_to_wall': 'Short (High Threat)', 'distance_rating_code': 'SHORT_24M_OCT',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 10.0, 'wall_dist_behind_cm': 1000, 'backdashes_to_wall': 6,
        'side_wall_dist_m': 12.0, 'side_wall_dist_cm': 1200,
        'combo_carry_requirement': 'Launch + 3 hits + Tornado (T!) into Munitions Wall Blast / Side Ledge',
        'secondary_floor': {
            'name': 'Lower Maintenance Trench (Side Ledge Break)',
            'width_m': 20.0, 'length_m': 20.0, 'width_cm': 2000, 'length_cm': 2000, 'area_sqm': 400,
            'wall_dist_behind_m': 8.0, 'wall_dist_behind_cm': 800, 'backdashes_to_wall': 5
        },
        'boundary_shape': 'Irregular Octagon'
    },
    'sanctum': {
        'width_m': 22.0, 'length_m': 32.0, 'width_cm': 2200, 'length_cm': 3200, 'area_sqm': 704,
        'distance_to_wall': 'Narrow Lateral', 'distance_rating_code': 'NARROW_22M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 14.0, 'wall_dist_behind_cm': 1400, 'backdashes_to_wall': 8,
        'side_wall_dist_m': 9.0, 'side_wall_dist_cm': 900,
        'combo_carry_requirement': 'Launch + 3 hits + Tornado (T!) into Temple Pillar Wall Break',
        'secondary_floor': {
            'name': 'Subterranean Crypt (Floor Break)',
            'width_m': 20.0, 'length_m': 20.0, 'width_cm': 2000, 'length_cm': 2000, 'area_sqm': 400,
            'wall_dist_behind_m': 8.0, 'wall_dist_behind_cm': 800, 'backdashes_to_wall': 5
        },
        'boundary_shape': 'Narrow Corridor'
    },
    'into-the-stratosphere': {
        'width_m': 26.0, 'length_m': 26.0, 'width_cm': 2600, 'length_cm': 2600, 'area_sqm': 676,
        'distance_to_wall': 'Medium-Short', 'distance_rating_code': 'MED_26M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 11.0, 'wall_dist_behind_cm': 1100, 'backdashes_to_wall': 6.5,
        'side_wall_dist_m': 13.0, 'side_wall_dist_cm': 1300,
        'combo_carry_requirement': 'Launch + 4 hits + Tornado (T!) / Downward Spike Floor Break',
        'secondary_floor': {
            'name': 'Lower Magma Chamber (Hard Floor Break + Floor Blast)',
            'width_m': 22.0, 'length_m': 22.0, 'width_cm': 2200, 'length_cm': 2200, 'area_sqm': 484,
            'wall_dist_behind_m': 9.0, 'wall_dist_behind_cm': 900, 'backdashes_to_wall': 5.5
        },
        'boundary_shape': 'Octagon to Narrow Core'
    },
    'ortiz-farm': {
        'width_m': 26.0, 'length_m': 22.0, 'width_cm': 2600, 'length_cm': 2200, 'area_sqm': 572,
        'distance_to_wall': 'Short (Multi-Tier)', 'distance_rating_code': 'TIER1_26M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 11.0, 'wall_dist_behind_cm': 1100, 'backdashes_to_wall': 6.5,
        'side_wall_dist_m': 9.0, 'side_wall_dist_cm': 900,
        'combo_carry_requirement': 'Launch + 3 hits + Tornado (T!) into Barn Wall Break (Highest damage stage)',
        'secondary_floor': {
            'name': 'Tier 2 Barn (Wall Break) & Tier 3 Ancient Cellar (Floor Break)',
            'width_m': 22.0, 'length_m': 20.0, 'width_cm': 2200, 'length_cm': 2000, 'area_sqm': 440,
            'tier3_cellar_m': '20.0m x 18.0m / 2,000 cm x 1,800 cm (Area: 360 m2)',
            'wall_dist_behind_m': 9.0, 'wall_dist_behind_cm': 900, 'backdashes_to_wall': 5.5
        },
        'boundary_shape': 'Multi-tier 3-Level Compound'
    },
    'coliseum': {
        'width_m': 44.0, 'length_m': 44.0, 'width_cm': 4400, 'length_cm': 4400, 'area_sqm': 1936,
        'distance_to_wall': 'Very Wide', 'distance_rating_code': 'WIDE_44M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 20.0, 'wall_dist_behind_cm': 2000, 'backdashes_to_wall': 12,
        'side_wall_dist_m': 22.0, 'side_wall_dist_cm': 2200,
        'combo_carry_requirement': 'Launch + 6 hits + Tornado (T!) + Double Dash / Heat Dash to wall',
        'secondary_floor': None, 'boundary_shape': 'Huge Octagon'
    },
    'celebration-on-the-seine': {
        'width_m': 20.0, 'length_m': 34.0, 'width_cm': 2000, 'length_cm': 3400, 'area_sqm': 680,
        'distance_to_wall': 'Extremely Narrow Lateral', 'distance_rating_code': 'NARROW_20M_LATERAL',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 15.0, 'wall_dist_behind_cm': 1500, 'backdashes_to_wall': 9,
        'side_wall_dist_m': 8.0, 'side_wall_dist_cm': 800,
        'combo_carry_requirement': 'Launch + 4 hits + Tornado (T!) — lateral walls are only 2-3 sidesteps away!',
        'secondary_floor': None, 'boundary_shape': 'Narrow Bridge'
    },
    'midnight-siege': {
        'width_m': 22.0, 'length_m': 24.0, 'width_cm': 2200, 'length_cm': 2400, 'area_sqm': 528,
        'distance_to_wall': 'Short Asymmetric', 'distance_rating_code': 'SHORT_22M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 9.0, 'wall_dist_behind_cm': 900, 'backdashes_to_wall': 5.5,
        'side_wall_dist_m': 10.0, 'side_wall_dist_cm': 1000,
        'combo_carry_requirement': 'Launch + 3 hits + Tornado (T!) into APC Truck Wall Break',
        'secondary_floor': {
            'name': 'Lower War Ruins (After APC Rubble Break)',
            'width_m': 20.0, 'length_m': 18.0, 'width_cm': 2000, 'length_cm': 1800, 'area_sqm': 360,
            'wall_dist_behind_m': 7.0, 'wall_dist_behind_cm': 700, 'backdashes_to_wall': 4.5
        },
        'boundary_shape': 'Asymmetric Ruin'
    },
    'urban-square-evening': {
        'width_m': 24.0, 'length_m': 36.0, 'width_cm': 2400, 'length_cm': 3600, 'area_sqm': 864,
        'distance_to_wall': 'Medium-Short', 'distance_rating_code': 'RECT_36M_X_24M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 16.0, 'wall_dist_behind_cm': 1600, 'backdashes_to_wall': 9,
        'side_wall_dist_m': 10.0, 'side_wall_dist_cm': 1000,
        'combo_carry_requirement': 'Launch + 5 hits + Tornado (T!) into South Balcony Break',
        'secondary_floor': {
            'name': 'Lower Subway Station (After Balcony Break)',
            'width_m': 20.0, 'length_m': 24.0, 'width_cm': 2000, 'length_cm': 2400, 'area_sqm': 480,
            'wall_dist_behind_m': 10.0, 'wall_dist_behind_cm': 1000, 'backdashes_to_wall': 6
        },
        'boundary_shape': 'Rectangular'
    },
    'arena-underground': {
        'width_m': 24.0, 'length_m': 24.0, 'width_cm': 2400, 'length_cm': 2400, 'area_sqm': 576,
        'distance_to_wall': 'Short Enclosed', 'distance_rating_code': 'SHORT_24M_OCT',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 10.0, 'wall_dist_behind_cm': 1000, 'backdashes_to_wall': 6,
        'side_wall_dist_m': 12.0, 'side_wall_dist_cm': 1200,
        'combo_carry_requirement': 'Launch + 3 hits + Tornado (T!) into 4x Wall Blasts',
        'secondary_floor': None, 'boundary_shape': 'Enclosed Octagon'
    },
    'elegant-palace': {
        'width_m': 30.0, 'length_m': 32.0, 'width_cm': 3000, 'length_cm': 3200, 'area_sqm': 960,
        'distance_to_wall': 'Medium-Wide', 'distance_rating_code': 'MED_32M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 14.0, 'wall_dist_behind_cm': 1400, 'backdashes_to_wall': 8,
        'side_wall_dist_m': 13.0, 'side_wall_dist_cm': 1300,
        'combo_carry_requirement': 'Launch + 4 hits + Tornado (T!) into 2x Wall Breaks / Center Balcony Break',
        'secondary_floor': {
            'name': 'Lower Courtyard (Balcony Break)',
            'width_m': 24.0, 'length_m': 22.0, 'width_cm': 2400, 'length_cm': 2200, 'area_sqm': 528,
            'wall_dist_behind_m': 9.0, 'wall_dist_behind_cm': 900, 'backdashes_to_wall': 5.5
        },
        'boundary_shape': 'Large Chamber'
    },
    'descent-into-subconscious': {
        'width_m': 24.0, 'length_m': 24.0, 'width_cm': 2400, 'length_cm': 2400, 'area_sqm': 576,
        'distance_to_wall': 'Short (Multi-Tier Void)', 'distance_rating_code': 'SHORT_24M_OCT',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 10.0, 'wall_dist_behind_cm': 1000, 'backdashes_to_wall': 6,
        'side_wall_dist_m': 12.0, 'side_wall_dist_cm': 1200,
        'combo_carry_requirement': 'Launch + 3 hits + Downward Spike / Throw Floor Break (2x Consecutive Breaks)',
        'secondary_floor': {
            'name': 'Tier 2 Mindscape & Tier 3 Abyss (2x Consecutive Floor Breaks)',
            'width_m': 22.0, 'length_m': 22.0, 'width_cm': 2200, 'length_cm': 2200, 'area_sqm': 484,
            'tier3_abyss_m': '20.0m x 20.0m / 2,000 cm x 2,000 cm (Area: 400 m2)',
            'wall_dist_behind_m': 8.0, 'wall_dist_behind_cm': 800, 'backdashes_to_wall': 5
        },
        'boundary_shape': 'Multi-Tier Void'
    },
    'secluded-training-ground': {
        'width_m': 18.0, 'length_m': 40.0, 'width_cm': 1800, 'length_cm': 4000, 'area_sqm': 720,
        'distance_to_wall': 'Extremely Long / Tight Lateral', 'distance_rating_code': 'CORRIDOR_18MX40M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 18.0, 'wall_dist_behind_cm': 1800, 'backdashes_to_wall': 11,
        'side_wall_dist_m': 7.0, 'side_wall_dist_cm': 700,
        'combo_carry_requirement': 'Launch + 3 hits + Tornado (T!) into 3x Consecutive Corridor Wall Breaks',
        'secondary_floor': None, 'boundary_shape': 'Long Hallway'
    },
    'genmaji-temple': {
        'width_m': 24.0, 'length_m': 28.0, 'width_cm': 2400, 'length_cm': 2800, 'area_sqm': 672,
        'distance_to_wall': 'Medium Courtyard', 'distance_rating_code': 'MED_28M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 12.0, 'wall_dist_behind_cm': 1200, 'backdashes_to_wall': 7,
        'side_wall_dist_m': 10.0, 'side_wall_dist_cm': 1000,
        'combo_carry_requirement': 'Launch + 4 hits + Tornado (T!) into Temple Gate Wall Break / Floor Break',
        'secondary_floor': {
            'name': 'Lower Shrine Crypt (Underground Floor Break)',
            'width_m': 20.0, 'length_m': 20.0, 'width_cm': 2000, 'length_cm': 2000, 'area_sqm': 400,
            'wall_dist_behind_m': 8.0, 'wall_dist_behind_cm': 800, 'backdashes_to_wall': 5
        },
        'boundary_shape': 'Temple Courtyard'
    },
    'fallen-destiny': {
        'width_m': 28.0, 'length_m': 28.0, 'width_cm': 2800, 'length_cm': 2800, 'area_sqm': 784,
        'distance_to_wall': 'Medium (28m)', 'distance_rating_code': 'MED_28M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 12.0, 'wall_dist_behind_cm': 1200, 'backdashes_to_wall': 7,
        'side_wall_dist_m': 14.0, 'side_wall_dist_cm': 1400,
        'combo_carry_requirement': 'Launch + 4 hits + Tornado (T!) + Heat Dash to reach wall splat zone',
        'secondary_floor': None, 'boundary_shape': 'Square'
    },
    'seaside-resort': {
        'width_m': 32.0, 'length_m': 24.0, 'width_cm': 3200, 'length_cm': 2400, 'area_sqm': 768,
        'distance_to_wall': 'Medium-Long', 'distance_rating_code': 'MED_32M',
        'spawn_distance_m': 4.0, 'spawn_distance_cm': 400,
        'center_coords': '0, 0', 'p1_spawn': '-200 cm (P1)', 'p2_spawn': '+200 cm (P2)',
        'wall_dist_behind_m': 14.0, 'wall_dist_behind_cm': 1400, 'backdashes_to_wall': 8,
        'side_wall_dist_m': 10.0, 'side_wall_dist_cm': 1000,
        'combo_carry_requirement': 'Launch + 4 hits + Tornado (T!) into Beachside Boardwalk Wall',
        'secondary_floor': None, 'boundary_shape': 'Rectangular'
    }
}

def format_secondary_floor(sf):
    if not sf:
        return 'null'
    inner_lines = []
    for k, v in sf.items():
        if isinstance(v, (int, float)):
            inner_lines.append(f"          {k}: {v}")
        else:
            inner_lines.append(f"          {k}: '{v}'")
    return "{\n" + ",\n".join(inner_lines) + "\n        }"

def update_stages_js():
    with open('frontend/assets/js/stages.js', 'r', encoding='utf-8') as f:
        content = f.read()

    updated = content
    for slug, cfg in STAGE_CONFIGS.items():
        # Match the stage block
        pattern = re.compile(rf"('{slug}':\s*\{{.*?dimensions:\s*\{{)(.*?)(\}},\s*hazards:)", re.DOTALL)
        match = pattern.search(updated)
        if not match:
            print(f"Warning: Could not match slug '{slug}'")
            continue
        
        prefix = match.group(1)
        suffix = match.group(3)
        
        sf_repr = format_secondary_floor(cfg['secondary_floor'])
        
        dim_replacement = f"""
        width_m: {cfg['width_m']},
        length_m: {cfg['length_m']},
        width_cm: {cfg['width_cm']},
        length_cm: {cfg['length_cm']},
        area_sqm: {cfg['area_sqm']},
        distance_to_wall: '{cfg['distance_to_wall']}',
        distance_rating_code: '{cfg['distance_rating_code']}',
        spawn_distance_m: {cfg['spawn_distance_m']},
        spawn_distance_cm: {cfg['spawn_distance_cm']},
        center_coords: '{cfg['center_coords']}',
        p1_spawn: '{cfg['p1_spawn']}',
        p2_spawn: '{cfg['p2_spawn']}',
        wall_dist_behind_m: {cfg['wall_dist_behind_m']},
        wall_dist_behind_cm: {cfg['wall_dist_behind_cm']},
        backdashes_to_wall: {cfg['backdashes_to_wall']},
        side_wall_dist_m: {cfg['side_wall_dist_m']},
        side_wall_dist_cm: {cfg['side_wall_dist_cm']},
        combo_carry_requirement: '{cfg['combo_carry_requirement']}',
        secondary_floor: {sf_repr},
        boundary_shape: '{cfg['boundary_shape']}'
      """
        
        updated = updated[:match.start()] + prefix + dim_replacement + suffix + updated[match.end():]

    with open('frontend/assets/js/stages.js', 'w', encoding='utf-8') as f:
        f.write(updated)
    
    print("Successfully updated frontend/assets/js/stages.js with complete centimeter telemetry!")

if __name__ == '__main__':
    update_stages_js()
