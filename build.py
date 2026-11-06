import datetime
import hashlib
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "docs"

# Output path -> (template, page title, active tab).
# Folders with index.html give clean URLs like drbefrits.se/behandling/
PAGES = {
    "index.html": ("about.html", "Om mig", "about"),
    "mottagningen/index.html": ("mottagningen.html", "Mottagningen", "mottagningen"),
    "behandling/index.html": ("treatments.html", "Behandling", "treatments"),
    "kontakt/index.html": ("contact.html", "Kontakt", "contact"),
}

# Old URLs that forward to the new ones, so existing links keep working.
REDIRECTS = {
    "treatments.html": "/behandling/",
    "mottagningen.html": "/mottagningen/",
    "contact.html": "/kontakt/",
}

REDIRECT_HTML = """<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<title>Flyttad</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
</head>
<body><a href="{url}">Sidan har flyttat hit</a></body>
</html>
"""


def build():
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    year = datetime.date.today().year
    css_path = STATIC_DIR / "css" / "style.css"
    # Changes only when the CSS changes, so browsers refetch it exactly then
    asset_version = hashlib.md5(css_path.read_bytes()).hexdigest()[:8]

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    for output_name, (template_name, page_title, active) in PAGES.items():
        template = env.get_template(template_name)
        html = template.render(
            page_title=page_title,
            active=active,
            year=year,
            asset_version=asset_version,
        )
        out_path = OUTPUT_DIR / output_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")

    for old_name, new_url in REDIRECTS.items():
        (OUTPUT_DIR / old_name).write_text(
            REDIRECT_HTML.format(url=new_url), encoding="utf-8"
        )

    shutil.copy(css_path, OUTPUT_DIR / "style.css")
    # Custom domain for GitHub Pages; must survive the docs/ wipe above.
    shutil.copy(STATIC_DIR / "CNAME", OUTPUT_DIR / "CNAME")
    shutil.copytree(STATIC_DIR / "images", OUTPUT_DIR / "images")
    shutil.copytree(STATIC_DIR / "fonts", OUTPUT_DIR / "fonts")

    print(f"Built site into {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
