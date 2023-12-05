"""Generate the code reference pages."""

from pathlib import Path

import mkdocs_gen_files

src = Path(__file__).parent.parent.parent

for path in sorted(src.rglob("*.py")):
    if path.name != 'script.py':
        continue # Skip the assets folder
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("", doc_path)

    parts = list(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
    elif parts[-1] == "__main__":
        continue

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        fd.write("```python\n\n")
        fd.write(open(path).read())
        fd.write("\n```\n")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)