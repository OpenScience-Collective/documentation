"""Render the OSCAR doctrine and worked examples into the docs site at build time.

The OSCAR content lives in the OSCAR repo (added here as the ``oscar/`` submodule),
a single source of truth. This mkdocs-gen-files script copies the doctrine
(``oscar/docs``) and the worked-example write-ups (``oscar/examples/*/README.md``)
into the virtual site tree under ``oscar/`` on every build, rewriting links so they
resolve either to the rendered doctrine pages or to the OSCAR repo on GitHub.

Nothing is duplicated in git: edit the docs in the OSCAR repo, bump the submodule
here, and docs.osc.earth reflects the change on the next build.
"""

from __future__ import annotations

import re
from pathlib import Path

import mkdocs_gen_files

REPO = "https://github.com/OpenScience-Collective/oscar"
DOCS_SRC = Path("oscar/docs")
EXAMPLES_SRC = Path("oscar/examples")

# Doctrine: repo-relative "up and out" links (templates, and the like) -> GitHub blob.
_UP_AND_OUT = re.compile(r"\]\((?:\.\./)+([^)]+)\)")
# Example: after/ links (files or directories) -> GitHub.
_AFTER = re.compile(r"\]\((after/[^)]*)\)")
# Examples index: sibling directory links like ](nemar/) -> the rendered page.
_EX_DIR = re.compile(r"\]\(([a-z][a-z0-9-]*)/\)")


def rewrite_doctrine(text: str) -> str:
    return _UP_AND_OUT.sub(lambda m: f"]({REPO}/blob/main/{m.group(1)})", text)


def rewrite_example(text: str, name: str) -> str:
    # Doctrine cross-links (../../docs/X) stay on the site as ../../X.
    text = text.replace("](../../docs/", "](../../")

    # after/ links point at files that are not rendered here; send them to GitHub.
    def _after(m: re.Match) -> str:
        target = m.group(1)
        kind = "tree" if target.endswith("/") else "blob"
        return f"]({REPO}/{kind}/main/examples/{name}/{target})"

    return _AFTER.sub(_after, text)


if not DOCS_SRC.is_dir():
    raise SystemExit(
        f"OSCAR docs not found at {DOCS_SRC}. Initialise the submodule with: "
        "git submodule update --init oscar"
    )

# Doctrine pages.
for src in sorted(DOCS_SRC.rglob("*.md")):
    rel = src.relative_to(DOCS_SRC)
    dest = rel.with_name("index.md") if rel.name == "README.md" else rel
    out = (Path("oscar") / dest).as_posix()
    with mkdocs_gen_files.open(out, "w") as fh:
        fh.write(rewrite_doctrine(src.read_text(encoding="utf-8")))
    mkdocs_gen_files.set_edit_path(out, f"{REPO}/edit/main/docs/{rel.as_posix()}")

# Worked-example write-ups: the examples index, then one page per example.
if EXAMPLES_SRC.is_dir():
    index = EXAMPLES_SRC / "README.md"
    if index.is_file():
        out = "oscar/examples/index.md"
        text = _EX_DIR.sub(lambda m: f"]({m.group(1)}/index.md)", index.read_text(encoding="utf-8"))
        with mkdocs_gen_files.open(out, "w") as fh:
            fh.write(text)
        mkdocs_gen_files.set_edit_path(out, f"{REPO}/edit/main/examples/README.md")

    for readme in sorted(EXAMPLES_SRC.glob("*/README.md")):
        name = readme.parent.name
        out = f"oscar/examples/{name}/index.md"
        with mkdocs_gen_files.open(out, "w") as fh:
            fh.write(rewrite_example(readme.read_text(encoding="utf-8"), name))
        mkdocs_gen_files.set_edit_path(out, f"{REPO}/edit/main/examples/{name}/README.md")
