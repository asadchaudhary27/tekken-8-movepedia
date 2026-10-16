"""
Tekken 8 Battlegrounds Image Downloader & Asset Bundler
Downloads high-resolution 16:9 stage preview images for all 18 official Tekken 8 stages
via the Tekken Fandom MediaWiki API, processes them with Pillow into pristine JPEGs,
saves them to static/images/stages and frontend/assets/img/stages, and bundles them into
tekken8_all_stages.zip in the project root.
"""

import os
import sys
import json
import zipfile
import subprocess
import urllib.request
import urllib.parse
from PIL import Image

STAGE_DEFINITIONS = [
    {
        "filename": "arena.jpg",
        "slug": "the-arena",
        "aliases": ["arena.jpg", "the-arena.jpg"],
        "titles": ["Arena/Tekken_8", "Arena_(Tekken_8)", "The_Arena_(Tekken_8)", "Arena"]
    },
    {
        "filename": "arena_underground.jpg",
        "slug": "arena-underground",
        "aliases": ["arena-underground.jpg"],
        "titles": ["Arena_(Underground)", "Arena/Underground", "The_Arena_(Underground)"]
    },
    {
        "filename": "urban_square.jpg",
        "slug": "urban-square",
        "aliases": ["urban-square.jpg"],
        "titles": ["Urban_Square", "Urban_Square/Tekken_8"]
    },
    {
        "filename": "urban_square_evening.jpg",
        "slug": "urban-square-evening",
        "aliases": ["urban-square-evening.jpg"],
        "titles": ["Urban_Square_(Evening)", "Urban_Square/Evening", "Urban_Square"]
    },
    {
        "filename": "yakushima.jpg",
        "slug": "yakushima",
        "aliases": ["yakushima.jpg"],
        "titles": ["Yakushima", "Yakushima/Tekken_8"]
    },
    {
        "filename": "coliseum_of_fate.jpg",
        "slug": "coliseum",
        "aliases": ["coliseum.jpg", "coliseum-of-fate.jpg"],
        "titles": ["Coliseum_of_Fate", "Coliseum_Of_Fate", "Coliseum"]
    },
    {
        "filename": "rebel_hangar.jpg",
        "slug": "rebel-hangar",
        "aliases": ["rebel-hangar.jpg"],
        "titles": ["Rebel_Hangar"]
    },
    {
        "filename": "fallen_destiny.jpg",
        "slug": "fallen-destiny",
        "aliases": ["fallen-destiny.jpg"],
        "titles": ["Fallen_Destiny"]
    },
    {
        "filename": "descent_into_subconscious.jpg",
        "slug": "descent-into-subconscious",
        "aliases": ["descent-into-subconscious.jpg"],
        "titles": ["Descent_into_Subconscious", "Descent_Into_Subconscious"]
    },
    {
        "filename": "sanctum.jpg",
        "slug": "sanctum",
        "aliases": ["sanctum.jpg"],
        "titles": ["Sanctum", "Sanctum_(Tekken_8)"]
    },
    {
        "filename": "into_the_stratosphere.jpg",
        "slug": "into-the-stratosphere",
        "aliases": ["stratosphere.jpg", "into-the-stratosphere.jpg"],
        "titles": ["Into_the_Stratosphere", "Into_The_Stratosphere"]
    },
    {
        "filename": "ortiz_farm.jpg",
        "slug": "ortiz-farm",
        "aliases": ["ortiz-farm.jpg"],
        "titles": ["Ortiz_Farm", "Ortiz_farm"]
    },
    {
        "filename": "celebration_on_the_seine.jpg",
        "slug": "celebration-on-the-seine",
        "aliases": ["celebration-on-the-seine.jpg"],
        "titles": ["Celebration_on_the_Seine", "Celebration_On_The_Seine"]
    },
    {
        "filename": "secluded_training_ground.jpg",
        "slug": "secluded-training-ground",
        "aliases": ["secluded-training-ground.jpg"],
        "titles": ["Secluded_training_ground", "Secluded_Training_Ground"]
    },
    {
        "filename": "elegant_palace.jpg",
        "slug": "elegant-palace",
        "aliases": ["elegant-palace.jpg"],
        "titles": ["Elegant_Palace", "Château_du_Lion"]
    },
    {
        "filename": "midnight_siege.jpg",
        "slug": "midnight-siege",
        "aliases": ["midnight-siege.jpg"],
        "titles": ["Midnight_Siege"]
    },
    {
        "filename": "seaside_resort.jpg",
        "slug": "seaside-resort",
        "aliases": ["seaside-resort.jpg"],
        "titles": ["Seaside_Resort", "Beach_(Tekken_8)", "Seaside_resort"]
    },
    {
        "filename": "genmaji_temple.jpg",
        "slug": "genmaji-temple",
        "aliases": ["genmaji-temple.jpg"],
        "titles": ["Genmaji_Temple", "Genma-ji_Temple", "Genmaji_temple"]
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def query_fandom_api(titles):
    """Query Fandom API for page thumbnail image."""
    titles_str = "|".join([urllib.parse.quote(t) for t in titles])
    url = f"https://tekken.fandom.com/api.php?action=query&titles={titles_str}&prop=pageimages&pithumbsize=1920&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, pinfo in pages.items():
                if pid != "-1" and "thumbnail" in pinfo:
                    return pinfo["thumbnail"]["source"], pinfo.get("title")
    except Exception as e:
        print(f"  [API Error: {e}]")
    return None, None

def search_fandom_api(query):
    """Fallback search on Fandom if exact titles miss."""
    url = f"https://tekken.fandom.com/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("query", {}).get("search", [])
            for r in results[:3]:
                t = r.get("title")
                src, matched = query_fandom_api([t])
                if src:
                    return src, matched
    except Exception as e:
        print(f"  [Search Error: {e}]")
    return None, None

def download_via_powershell(image_url, page_title, out_path):
    """Use PowerShell Invoke-WebRequest to bypass CDN Cloudflare challenge."""
    referer = f"https://tekken.fandom.com/wiki/{urllib.parse.quote(page_title or 'Tekken_8')}"
    ps_cmd = (
        f'$ProgressPreference = "SilentlyContinue"; '
        f'Invoke-WebRequest -Uri "{image_url}" '
        f'-UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" '
        f'-Headers @{{"Referer"="{referer}"}} '
        f'-OutFile "{out_path}"'
    )
    result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    return os.path.exists(out_path) and os.path.getsize(out_path) > 1000

def process_and_save_image(raw_path, target_dirs, filename, aliases):
    """Process downloaded image with Pillow: convert to RGB 16:9 JPEG."""
    with Image.open(raw_path) as im:
        rgb_im = im.convert("RGB")
        w, h = rgb_im.size
        # Target 16:9 ratio
        target_ratio = 16.0 / 9.0
        current_ratio = w / float(h)
        
        # If substantially different from 16:9, crop to center 16:9
        if abs(current_ratio - target_ratio) > 0.05:
            if current_ratio > target_ratio:
                # Too wide, crop width
                new_w = int(h * target_ratio)
                left = (w - new_w) // 2
                rgb_im = rgb_im.crop((left, 0, left + new_w, h))
            else:
                # Too tall, crop height
                new_h = int(w / target_ratio)
                top = (h - new_h) // 2
                rgb_im = rgb_im.crop((0, top, w, top + new_h))
        
        # If resolution is larger than 1920x1080, we can keep high-res or scale cleanly
        final_w, final_h = rgb_im.size

        # Save to primary targets
        saved_paths = []
        for d in target_dirs:
            out_file = os.path.join(d, filename)
            rgb_im.save(out_file, "JPEG", quality=95, optimize=True)
            saved_paths.append(out_file)

            # Also write alias filenames (e.g. kebab-case or alternate names)
            for alias in aliases:
                alias_file = os.path.join(d, alias)
                if alias_file != out_file:
                    rgb_im.save(alias_file, "JPEG", quality=95, optimize=True)

        return final_w, final_h, saved_paths

def main():
    print("=" * 80)
    print(" TEKKEN 8 OFFICIAL BATTLEGROUNDS - HD STAGE IMAGE PIPELINE")
    print("=" * 80)

    static_dir = os.path.abspath("static/images/stages")
    frontend_dir = os.path.abspath("frontend/assets/img/stages")
    temp_dir = os.path.abspath("temp_stages")

    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(frontend_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    results = []

    for idx, stage in enumerate(STAGE_DEFINITIONS, start=1):
        fn = stage["filename"]
        titles = stage["titles"]
        aliases = stage.get("aliases", [])
        print(f"\n[{idx}/18] Processing '{fn}'...")

        # 1. Query Fandom API
        img_url, resolved_title = query_fandom_api(titles)
        if not img_url:
            clean_name = fn.replace(".jpg", "").replace("_", " ")
            img_url, resolved_title = search_fandom_api(f"{clean_name} Tekken 8")

        if not img_url:
            print(f"  [!] Failed to resolve URL from Fandom for {fn}")
            continue

        print(f"  -> Title: {resolved_title}")
        print(f"  -> URL:   {img_url[:70]}...")

        # 2. Download raw asset
        raw_path = os.path.join(temp_dir, f"raw_{fn}")
        success = download_via_powershell(img_url, resolved_title, raw_path)
        if not success:
            print(f"  [!] Download failed via PowerShell for {fn}")
            continue

        raw_size = os.path.getsize(raw_path) / 1024.0
        print(f"  -> Raw download: {raw_size:.1f} KB")

        # 3. Process with Pillow
        fw, fh, paths = process_and_save_image(raw_path, [static_dir, frontend_dir], fn, aliases)
        jpg_size = os.path.getsize(paths[0]) / 1024.0
        print(f"  -> Processed 16:9 JPEG: {fw}x{fh} ({jpg_size:.1f} KB)")
        print(f"  -> Saved to static & frontend directories (+ aliases: {aliases})")

        results.append({
            "filename": fn,
            "title": resolved_title,
            "resolution": f"{fw}x{fh}",
            "size_kb": f"{jpg_size:.1f} KB",
            "path": paths[0]
        })

    # Clean up temp raw files
    for f in os.listdir(temp_dir):
        try:
            os.remove(os.path.join(temp_dir, f))
        except Exception:
            pass
    try:
        os.rmdir(temp_dir)
    except Exception:
        pass

    # 4. Create tekken8_all_stages.zip
    zip_path = os.path.abspath("tekken8_all_stages.zip")
    print("\n" + "=" * 80)
    print(f" BUNDLING ALL STAGE IMAGES INTO {zip_path}")
    print("=" * 80)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item in results:
            zipf.write(item["path"], arcname=item["filename"])
            print(f"  [ZIP] Added {item['filename']} ({item['size_kb']})")

    zip_size_mb = os.path.getsize(zip_path) / (1024.0 * 1024.0)
    print(f"\n[SUCCESS] Bundled {len(results)}/18 stage images into '{os.path.basename(zip_path)}' ({zip_size_mb:.2f} MB)")

    # Print summary table
    print("\n" + "=" * 80)
    print(f"{'#':<3} {'Filename':<30} {'Resolution':<12} {'Size':<10} {'Fandom Title'}")
    print("-" * 80)
    for idx, r in enumerate(results, start=1):
        print(f"{idx:<3} {r['filename']:<30} {r['resolution']:<12} {r['size_kb']:<10} {r['title']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
