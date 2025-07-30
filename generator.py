#!/usr/bin/env python3
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

def generate_stories_json(article_files_by_tier, output_file):
    def infer_tags(slug):
        tags = []
        if "creek" in slug or "stream" in slug:
            tags.append("nature")
        if "estate" in slug or "real" in slug or "fsbo" in slug:
            tags.append("real estate")
        if "school" in slug or "bus" in slug:
            tags.append("community")
        if "legacy" in slug or "history" in slug:
            tags.append("heritage")
        if "walk" in slug or "trail" in slug or "still-waters" in slug:
            tags.append("walks")
        return tags

    stories = []
    for tier, files in article_files_by_tier.items():
        for fname in files:
            slug = fname.replace(".html", "")
            title = fname.replace("-", " ").replace(".html", "").title()
            stories.append({
                "title": title,
                "slug": slug,
                "tier": tier,
                "summary": f"Curated story in the {tier} membership tier.",
                "date": datetime.today().strftime('%Y-%m-%d'),
                "tags": infer_tags(slug),
                "featured": False,
                "filename": fname,
                "image": f"https://via.placeholder.com/600x300.png?text={tier.capitalize()}+Story"
            })
    with open(output_file, "w") as f:
        json.dump(stories, f, indent=2)
    print(f"✅ stories.json written to {output_file}")

def generate_thumbnail_script(asset_dir, output_script):
    images = list(Path(asset_dir).rglob("*.[pjg][pnif][gf]"))
    script_lines = ["#!/bin/bash", "mkdir -p thumbnails"]
    for img in images:
        base = img.stem
        ext = img.suffix
        thumb = f"{base}-thmbn{ext}"
        rel_path = img.relative_to(Path.cwd())
        script_lines.append(f'cp "{rel_path}" "thumbnails/{thumb}"')
    with open(output_script, "w") as f:
        f.write("\n".join(script_lines))
    print(f"🛠️ generate_thumbnails.sh created at {output_script}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Charlotte Everley DevOps Generator")
    parser.add_argument("--mode", choices=["stories", "thumbnails"], required=True, help="Mode to run: stories or thumbnails")
    parser.add_argument("--output", help="Output file (for stories.json or .sh script)")
    parser.add_argument("--assets", help="Assets directory for thumbnail script")
    args = parser.parse_args()

    if args.mode == "stories":
        sample_data = {
            "free": ["te-bus-routes-2.html", "te-bus-routes-3.html"],
            "trial": ["The-Hidden-Stream-of-Devon.html"],
            "silver": ["estates-alongside-the-creek.html"],
            "gold": ["Legacy-of-947Contention-Lane.html"]
        }
        output_file = args.output or "stories/stories.json"
        generate_stories_json(sample_data, output_file)

    elif args.mode == "thumbnails":
        asset_dir = args.assets or "assets"
        output_script = args.output or "generate_thumbnails.sh"
        generate_thumbnail_script(asset_dir, output_script)
