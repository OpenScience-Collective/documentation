"""Render the OSCAR doctrine into the docs site at build time.

The OSCAR doctrine lives in the OSCAR repo (added here as the ``oscar/``
submodule), so it has a single source of truth. This mkdocs-gen-files script
copies the markdown from ``oscar/docs/`` into the virtual site tree under
``oscar/`` on every build, rewriting repo-relative links (to templates,
examples, and the like) so they resolve to the OSCAR repo on GitHub.

Nothing is duplicated in git: edit the docs in the OSCAR repo, bump the
submodule here, and docs.osc.earth reflects the change on the next build.
"""

from __future__ import annotations

import re
from pathlib import Path

import mkdocs_gen_files

SRC = Path("oscar/docs")
REPO = "https://github.com/OpenScience-Collective/oscar"

# Links like ](../../templates/llms.txt) point at files that live in the OSCAR
# repo, not the docs site. Rewrite any "up and out" link to a GitHub blob URL.
_UP_AND_OUT = re.compile(r"\]\((?:\.\./)+([^)]+)\)")


def rewrite_links(text: str) -> str:
    return _UP_AND_OUT.sub(lambda m: f"]({REPO}/blob/main/{m.group(1)})", text)


if not SRC.is_dir():
    raise SystemExit(
        f"OSCAR docs not found at {SRC}. Initialise the submodule with: "
        "git submodule update --init oscar"
    )

for src in sorted(SRC.rglob("*.md")):
    rel = src.relative_to(SRC)
    dest = rel.with_name("index.md") if rel.name == "README.md" else rel
    out = (Path("oscar") / dest).as_posix()
    with mkdocs_gen_files.open(out, "w") as fh:
        fh.write(rewrite_links(src.read_text(encoding="utf-8")))
    mkdocs_gen_files.set_edit_path(out, f"{REPO}/edit/main/docs/{rel.as_posix()}")
