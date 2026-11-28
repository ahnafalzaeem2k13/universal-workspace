#!/usr/bin/env python3
"""Refresh the curated Agent Skills library from selected upstream repositories.

Only copies folders containing SKILL.md. Upstream instructions remain untrusted
reference material; see the repository-root AGENTS.md for safe-use rules.
"""
from __future__ import annotations
import json, shutil, subprocess, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEST = REPO / ".agents" / "skills"
SOURCES = [
    {"id":"gamedev", "url":"https://github.com/gamedev-skills/awesome-gamedev-agent-skills.git", "base":"skills", "mode":"all"},
    {"id":"vercel", "url":"https://github.com/vercel-labs/agent-skills.git", "base":"skills", "mode":"all"},
    {"id":"superpowers", "url":"https://github.com/obra/superpowers.git", "base":"skills", "mode":"all"},
    {"id":"threejs", "url":"https://github.com/uustudy/game-threejs-game-skills.git", "base":"skills", "mode":"all"},
    {"id":"supabase", "url":"https://github.com/supabase/agent-skills.git", "base":"skills", "mode":"all"},
    {"id":"anthropic", "url":"https://github.com/anthropics/skills.git", "base":"skills", "mode":"selected",
     "include":["algorithmic-art","skill-creator","webapp-testing","frontend-design","web-artifacts-builder","mcp-builder"]},
    {"id":"architecture", "url":"https://github.com/edhahn/agent-skills.git", "base":".", "mode":"selected",
     "include":["software-architecture","eval-driven-game-development","game-designer","concept-art"]},
]

def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True)

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    records, seen = [], set()
    with tempfile.TemporaryDirectory(prefix="agent-skills-") as tmp:
        tmp = Path(tmp)
        for src in SOURCES:
            checkout = tmp / src["id"]
            run(["git","clone","--depth","1",src["url"],str(checkout)])
            sha = run(["git","rev-parse","HEAD"], cwd=checkout).stdout.strip()
            base = checkout / src["base"]
            if src["mode"] == "all":
                candidates = sorted(p.parent for p in base.rglob("SKILL.md"))
            else:
                candidates = [base / name for name in src["include"]]
            copied = []
            for folder in candidates:
                skill_file = folder / "SKILL.md"
                if not skill_file.is_file():
                    continue
                skill_name = folder.name
                try:
                    for line in skill_file.read_text(encoding="utf-8").splitlines()[:20]:
                        if line.strip().startswith("name:"):
                            skill_name = line.split(":",1)[1].strip().strip("\"' ")
                            break
                except Exception:
                    pass
                if not skill_name or skill_name in seen:
                    continue
                seen.add(skill_name)
                target = DEST / skill_name
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(folder, target, ignore=shutil.ignore_patterns(".git","node_modules","__pycache__"))
                if not any((target / n).exists() for n in ("LICENSE","LICENSE.md","COPYING")):
                    for license_name in ("LICENSE","LICENSE.md","COPYING"):
                        if (checkout / license_name).is_file():
                            shutil.copy2(checkout / license_name, target / license_name)
                            break
                copied.append(skill_name)
            records.append({"source":src["id"],"url":src["url"],"commit":sha,"skills":copied,"count":len(copied)})
    total = sum(x["count"] for x in records)
    (DEST / "sources.lock.json").write_text(json.dumps(records, indent=2)+"\n", encoding="utf-8")
    lines = [
        "# Curated Agent Skills Index", "",
        f"**Installed skills: {total}.** Skills are stored in this repository, not in temporary Colab storage.", "",
        "## Automatic use", "",
        "Read the root AGENTS.md first. Select only relevant skills for each task; do not load all skills into context.", "",
        "## Collections and provenance", ""
    ]
    for item in records:
        lines += [f"### {item['source']} — {item['count']} skills", f"- Source: {item['url']}", f"- Pinned source commit: {item['commit']}", ""]
        lines += [f"- {name}" for name in item["skills"]]
        lines.append("")
    lines += ["## Updating", "", "Run python tools/refresh_agent_skills.py to refresh from upstream. GitHub Actions also refreshes monthly.", ""]
    (DEST / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Installed {total} unique skills into {DEST}")
    for item in records:
        print(f"{item['source']}: {item['count']} skills @ {item['commit']}")

if __name__ == "__main__":
    main()
