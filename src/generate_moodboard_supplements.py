from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from style_inspiration_tool.config import IMAGE_ROOT, MANIFEST_JSONL


CANVAS_SIZE = (640, 640)


def existing_count(label: str) -> int:
    return len([path for path in (IMAGE_ROOT / label).glob("*") if path.is_file()])


def load_manifest() -> list[dict]:
    if not MANIFEST_JSONL.exists():
        return []
    return [json.loads(line) for line in MANIFEST_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]


def save_manifest(records: list[dict]) -> None:
    MANIFEST_JSONL.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def draw_minimal(seed: int) -> Image.Image:
    random.seed(seed)
    image = Image.new("RGB", CANVAS_SIZE, random.choice([(245, 244, 240), (250, 250, 248), (236, 232, 226)]))
    draw = ImageDraw.Draw(image)
    palette = [(25, 25, 25), (180, 168, 146), (70, 70, 70), (200, 196, 188)]
    for _ in range(random.randint(3, 5)):
        x1 = random.randint(40, 420)
        y1 = random.randint(40, 420)
        x2 = x1 + random.randint(80, 180)
        y2 = y1 + random.randint(20, 140)
        draw.rectangle((x1, y1, x2, y2), fill=random.choice(palette))
    return image


def draw_industrial(seed: int) -> Image.Image:
    random.seed(seed)
    image = Image.new("RGB", CANVAS_SIZE, (52, 56, 62))
    draw = ImageDraw.Draw(image)
    palette = [(120, 124, 132), (166, 96, 64), (88, 96, 112), (194, 198, 204)]
    for step in range(0, CANVAS_SIZE[0], 48):
        draw.line((step, 0, step, CANVAS_SIZE[1]), fill=(85, 90, 96), width=2)
        draw.line((0, step, CANVAS_SIZE[0], step), fill=(85, 90, 96), width=2)
    for _ in range(8):
        x1 = random.randint(20, 520)
        y1 = random.randint(20, 520)
        x2 = x1 + random.randint(40, 120)
        y2 = y1 + random.randint(40, 120)
        draw.rectangle((x1, y1, x2, y2), outline=random.choice(palette), width=5)
    for _ in range(5):
        x = random.randint(0, CANVAS_SIZE[0])
        draw.line((x, 0, CANVAS_SIZE[0] - x, CANVAS_SIZE[1]), fill=random.choice(palette), width=6)
    return image.filter(ImageFilter.GaussianBlur(radius=0.6))


def draw_organic(seed: int) -> Image.Image:
    random.seed(seed)
    image = Image.new("RGB", CANVAS_SIZE, (232, 240, 228))
    draw = ImageDraw.Draw(image)
    palette = [(84, 114, 71), (153, 103, 67), (102, 136, 88), (191, 174, 118)]
    for _ in range(18):
        cx = random.randint(40, 600)
        cy = random.randint(40, 600)
        rx = random.randint(20, 90)
        ry = random.randint(12, 70)
        angle = random.random() * math.pi
        points = []
        for t in range(18):
            theta = 2 * math.pi * t / 18
            x = cx + math.cos(theta + angle) * rx
            y = cy + math.sin(theta + angle) * ry
            points.append((x, y))
        draw.polygon(points, fill=random.choice(palette))
    return image.filter(ImageFilter.GaussianBlur(radius=1.2))


GENERATORS = {
    "minimal": draw_minimal,
    "industrial": draw_industrial,
    "organic": draw_organic,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate supplemental moodboard images for sparse style categories.")
    parser.add_argument("--target-count", type=int, default=10, help="Minimum image count per generated class.")
    args = parser.parse_args()

    manifest = load_manifest()
    for label, generator in GENERATORS.items():
        label_dir = IMAGE_ROOT / label
        label_dir.mkdir(parents=True, exist_ok=True)
        count = existing_count(label)
        while count < args.target_count:
            image = generator(seed=1000 + count)
            name = f"{label}_generated_{count + 1:02d}.png"
            image.save(label_dir / name)
            manifest.append(
                {
                    "label": label,
                    "query": "generated_moodboard_supplement",
                    "title": name,
                    "image_name": name,
                    "source_url": "",
                    "page_url": "",
                    "license": "project-generated",
                    "creator": "project script",
                }
            )
            count += 1

    save_manifest(manifest)
    for label in GENERATORS:
        print(f"{label}: {existing_count(label)} images")


if __name__ == "__main__":
    main()
