"""Generate API reference pages for mkdocs.

This script auto-generates API reference documentation from Python source code
using mkdocstrings. It creates markdown files that reference the actual Python
modules, which are then rendered by mkdocstrings during the build.
"""

from pathlib import Path

import mkdocs_gen_files

# Project configurations for auto-documentation
PROJECTS = {
    "osa": {
        "src_path": Path("osa/src"),
        "doc_path": "osa/reference",
        "modules": [
            "api.main",
            "api.config",
            "cli.main",
            "cli.config",
            "cli.client",
            "agents.base",
            "agents.state",
            "tools.base",
            "tools.hed",
            "tools.hed_validation",
            "tools.fetcher",
            "tools.markdown_cleaner",
            "core.services.llm",
        ],
    },
}


def generate_reference_docs():
    """Generate reference documentation for all configured projects."""
    nav = mkdocs_gen_files.Nav()

    for project_name, config in PROJECTS.items():
        src_path = config["src_path"]
        doc_path = Path(config["doc_path"])

        # Check if source path exists
        if not src_path.exists():
            print(f"Warning: Source path {src_path} does not exist, skipping {project_name}")
            continue

        for module in config["modules"]:
            # Create the markdown file path
            module_path = module.replace(".", "/")
            doc_file = doc_path / f"{module_path}.md"

            # Generate the documentation content
            full_module = f"src.{module}"

            content = f"""# `{module}`

::: {full_module}
    options:
      show_root_heading: true
      show_source: true
      members_order: source
"""

            # Write the file
            with mkdocs_gen_files.open(doc_file, "w") as f:
                f.write(content)

            # Add to navigation
            nav[tuple(module.split("."))] = str(doc_file)

            mkdocs_gen_files.set_edit_path(
                doc_file, f"../{src_path / module.replace('.', '/')}.py"
            )

    # Generate SUMMARY.md for literate-nav
    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


# Only run during mkdocs build
if __name__ != "__main__":
    generate_reference_docs()
