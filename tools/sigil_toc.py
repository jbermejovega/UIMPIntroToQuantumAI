from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NAV = ROOT / "ccms" / "sigil_course_navigation_v1.json"


@dataclass(frozen=True)
class Target:
    path: Path
    anchor: str | None


def load_navigation() -> dict[str, Any]:
    return json.loads(NAV.read_text(encoding="utf-8"))


def github_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def markdown_headings(path: Path) -> set[str]:
    headings: set[str] = set()
    seen: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = github_slug(match.group(1))
        n = seen.get(base, 0)
        slug = base if n == 0 else f"{base}-{n}"
        seen[base] = n + 1
        headings.add(slug)
    return headings


def split_target(raw: str) -> Target:
    if "#" in raw:
        path_part, anchor = raw.split("#", 1)
        return Target(ROOT / path_part, anchor or None)
    return Target(ROOT / raw, None)


def validate_target(raw: str) -> list[str]:
    target = split_target(raw)
    errors: list[str] = []
    if not target.path.exists():
        errors.append(f"missing file: {target.path.relative_to(ROOT)}")
        return errors
    if target.anchor:
        if target.path.suffix.lower() != ".md":
            errors.append(
                f"anchor declared for non-Markdown target: "
                f"{target.path.relative_to(ROOT)}#{target.anchor}"
            )
        else:
            headings = markdown_headings(target.path)
            if target.anchor not in headings:
                errors.append(
                    f"missing anchor: {target.path.relative_to(ROOT)}#{target.anchor}"
                )
    return errors


def validate_root_compatibility(data: dict[str, Any]) -> list[str]:
    root = ROOT / data["compatibility"]["root_readme"]
    if not root.exists():
        return [f"missing root README: {root.relative_to(ROOT)}"]
    headings = markdown_headings(root)
    errors: list[str] = []
    for route in data["routes"]:
        anchor = route.get("root_anchor")
        if anchor and anchor not in headings:
            errors.append(f"root compatibility anchor missing: README.md#{anchor}")
    return errors


def iter_markdown_local_targets(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    out: list[str] = []
    pattern = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
    for match in pattern.finditer(text):
        raw = match.group(1).strip()
        if not raw or raw.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if " " in raw and not raw.startswith("<"):
            raw = raw.split(" ", 1)[0]
        out.append(raw.strip("<>"))
    return out


def validate_markdown_local_assets(path: Path) -> list[str]:
    errors: list[str] = []
    for raw in iter_markdown_local_targets(path):
        path_part = raw.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (path.parent / path_part).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"local link escapes repository: {path}:{raw}")
            continue
        if not resolved.exists():
            errors.append(
                f"broken local link: {path.relative_to(ROOT)} -> {raw}"
            )
    return errors


def validate_navigation(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    route_ids = [route["id"] for route in data["routes"]]
    if len(route_ids) != len(set(route_ids)):
        errors.append("duplicate navigation route ids")

    localizers = set(data["localizers"])
    for route in data["routes"]:
        if route["localizer"] not in localizers:
            errors.append(
                f"route {route['id']} uses unknown localizer {route['localizer']}"
            )
        errors.extend(
            f"route {route['id']}: {error}"
            for error in validate_target(route["target"])
        )

    errors.extend(validate_root_compatibility(data))

    legacy = ROOT / data["compatibility"]["legacy_guide"]
    if legacy.exists():
        errors.extend(validate_markdown_local_assets(legacy))
    else:
        errors.append(f"missing legacy guide: {legacy.relative_to(ROOT)}")

    return errors


def route(data: dict[str, Any], route_id: str) -> dict[str, Any]:
    by_id = {item["id"]: item for item in data["routes"]}
    if route_id not in by_id:
        raise KeyError(f"unknown route: {route_id}")
    item = dict(by_id[route_id])
    item["localizer_contract"] = data["localizers"][item["localizer"]]
    return item


def print_atlas(data: dict[str, Any]) -> None:
    for item in data["routes"]:
        loc = data["localizers"][item["localizer"]]
        print(
            f"{item['id']}\t{loc['facet']}\t{item['localizer']}\t"
            f"{item['target']}\t{item['label']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SIGIL/KRONE/WML typed navigation checker and localizer"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    sub.add_parser("atlas")
    p = sub.add_parser("route")
    p.add_argument("route_id")

    args = parser.parse_args()
    data = load_navigation()

    if args.command == "check":
        errors = validate_navigation(data)
        if errors:
            for error in errors:
                print(f"[fail] {error}", file=sys.stderr)
            return 1
        print("[pass] typed TOC/navigation")
        print(f"[pass] {len(data['routes'])} routes")
        return 0

    if args.command == "atlas":
        print_atlas(data)
        return 0

    if args.command == "route":
        print(json.dumps(route(data, args.route_id), indent=2, sort_keys=True))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
