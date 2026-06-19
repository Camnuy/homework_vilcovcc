from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

import requests

from style_inspiration_tool.config import DATA_ROOT, IMAGE_ROOT, MANIFEST_JSONL, WIKIMEDIA_QUERIES


COMMONS_API = "https://commons.wikimedia.org/w/api.php"
SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "EMI-Style-Inspiration-Tool/1.0 (educational project; contact: local-codex-session)"
    }
)

SKIP_TITLE_KEYWORDS = {
    "svg",
    "diagram",
    "pangram",
    "ambigram",
    "alphabet",
    "typography",
    "font",
    "logo",
    "icon",
    "map",
    "cell",
}

LABEL_SKIP_KEYWORDS = {
    "industrial": {"school", "educativa"},
    "minimal": {"tanga", "ogg", "clock tower", "straw", "hartriegel", "park"},
}


def should_skip_page(label: str, title: str) -> bool:
    title_lower = title.lower()
    if any(keyword in title_lower for keyword in SKIP_TITLE_KEYWORDS):
        return True
    return any(keyword in title_lower for keyword in LABEL_SKIP_KEYWORDS.get(label, set()))


def extension_from_url(url: str) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp"} else ".jpg"


def commons_search(query: str, limit: int) -> list[dict]:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": 6,
        "gsrsearch": query,
        "gsrlimit": limit,
        "prop": "imageinfo|info",
        "iiprop": "url|mime|extmetadata",
        "iiurlwidth": 640,
        "inprop": "url",
    }
    response = SESSION.get(COMMONS_API, params=params, timeout=60)
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {})
    return list(pages.values())


def download_image(url: str, destination: Path) -> None:
    response = SESSION.get(url, timeout=60)
    response.raise_for_status()
    destination.write_bytes(response.content)


def load_existing_manifest(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a small public-domain / open-license starter dataset from Wikimedia Commons.")
    parser.add_argument("--per-query", type=int, default=10, help="How many search results to request per query.")
    parser.add_argument("--per-label", type=int, default=12, help="Maximum number of images to keep per label.")
    parser.add_argument("--max-per-query", type=int, default=2, help="Maximum number of accepted images per query, to improve diversity.")
    args = parser.parse_args()

    IMAGE_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_records = load_existing_manifest(MANIFEST_JSONL)
    seen_urls = {record["source_url"] for record in manifest_records if "source_url" in record}

    for label, queries in WIKIMEDIA_QUERIES.items():
        label_dir = IMAGE_ROOT / label
        label_dir.mkdir(parents=True, exist_ok=True)
        downloaded = len([path for path in label_dir.glob("*") if path.is_file()])
        for query in queries:
            if downloaded >= args.per_label:
                break
            downloaded_for_query = 0
            for page in commons_search(query, limit=args.per_query):
                if downloaded >= args.per_label:
                    break
                if downloaded_for_query >= args.max_per_query:
                    break
                imageinfo = (page.get("imageinfo") or [{}])[0]
                source_url = imageinfo.get("thumburl") or imageinfo.get("url")
                if not source_url or source_url in seen_urls:
                    continue
                title = page.get("title", "").replace("File:", "")
                if should_skip_page(label, title):
                    continue
                extmetadata = imageinfo.get("extmetadata") or {}
                license_short = extmetadata.get("LicenseShortName", {}).get("value", "")
                creator = extmetadata.get("Artist", {}).get("value", "")
                digest = hashlib.sha1(source_url.encode("utf-8")).hexdigest()[:10]
                filename = f"{label}_{downloaded + 1:02d}_{digest}{extension_from_url(source_url)}"
                destination = label_dir / filename
                try:
                    download_image(source_url, destination)
                except Exception:
                    continue
                manifest_records.append(
                    {
                        "label": label,
                        "query": query,
                        "title": title,
                        "image_name": filename,
                        "source_url": source_url,
                        "page_url": page.get("fullurl", ""),
                        "license": license_short,
                        "creator": creator,
                    }
                )
                seen_urls.add(source_url)
                downloaded += 1
                downloaded_for_query += 1

    MANIFEST_JSONL.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in manifest_records) + "\n",
        encoding="utf-8",
    )
    print(f"Saved dataset manifest: {MANIFEST_JSONL}")
    for label_dir in sorted(IMAGE_ROOT.iterdir()):
        if label_dir.is_dir():
            print(f"{label_dir.name}: {len(list(label_dir.glob('*')))} images")


if __name__ == "__main__":
    main()
