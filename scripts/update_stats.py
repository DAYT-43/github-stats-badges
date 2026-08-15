#!/usr/bin/env python3
"""Сбор статистики профиля GitHub и генерация честных бейджей.

Два бейджа в едином стиле shields.io endpoint badge:
- stars.json      — «stars earned»: сумма звёзд на всех публичных репозиториях (REST API)
- contributions.json — «contributions (last year)»: контрибуции за скользящие 365 дней (GraphQL API)

В отличие от сторонних виджетов (github-readme-stats и др.):
- данные берутся напрямую из официального API GitHub;
- contributions считаются за скользящий год (как на профиле), а не календарный;
- нет зависимости от чужих Vercel-инстансов и их rate-limit.

Используется в GitHub Actions (см. .github/workflows/update-stats.yml).
Требует env: GH_TOKEN (PAT), OWNER (по умолчанию DAYT-43).
"""
import json
import os
import urllib.request
from pathlib import Path

REST_API = "https://api.github.com"
GRAPHQL_API = "https://api.github.com/graphql"
OWNER = os.environ.get("OWNER", "DAYT-43")
TOKEN = os.environ.get("GH_TOKEN", "")

BASE_DIR = Path(__file__).resolve().parent.parent
STARS_FILE = BASE_DIR / "stars.json"
CONTRIB_FILE = BASE_DIR / "contributions.json"


def rest_get(path: str) -> dict:
    req = urllib.request.Request(
        f"{REST_API}/{path}",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-stats-badges",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def graphql(query: str, variables: dict) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_API,
        data=body,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-stats-badges",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def badge(label: str, message: str, color: str = "blue") -> dict:
    return {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color,
        "cacheSeconds": 86400,
    }


def fetch_stars() -> int:
    """Сумма звёзд на всех публичных репозиториях владельца (с пагинацией)."""
    total = 0
    page = 1
    while True:
        repos = rest_get(f"users/{OWNER}/repos?per_page=100&page={page}&sort=updated")
        if not repos:
            break
        total += sum(r.get("stargazers_count", 0) for r in repos)
        if len(repos) < 100:
            break
        page += 1
    return total


def fetch_contributions() -> int:
    """Контрибуции за скользящие 365 дней (как на профиле GitHub)."""
    query = """
    query($u: String!) {
      user(login: $u) {
        contributionsCollection {
          contributionCalendar { totalContributions }
        }
      }
    }
    """
    data = graphql(query, {"u": OWNER})
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]


def main() -> None:
    if not TOKEN:
        raise SystemExit("GH_TOKEN not set")

    stars = fetch_stars()
    contribs = fetch_contributions()

    STARS_FILE.write_text(
        json.dumps(badge("stars earned", str(stars), "brightgreen"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    CONTRIB_FILE.write_text(
        json.dumps(badge("contributions (last year)", str(contribs), "blue"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"stars earned: {stars}")
    print(f"contributions (last year): {contribs}")


if __name__ == "__main__":
    main()