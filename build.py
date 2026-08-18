import datetime
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "docs"

PAGES = {
    "index.html": ("about.html", "Om mig", "about"),
    "treatments.html": ("treatments.html", "Behandlingar", "treatments"),
    "contact.html": ("contact.html", "Kontakt", "contact"),
}


def build():
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    year = datetime.date.today().year

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    for output_name, (template_name, page_title, active) in PAGES.items():
        template = env.get_template(template_name)
        html = template.render(page_title=page_title, active=active, year=year)
        (OUTPUT_DIR / output_name).write_text(html, encoding="utf-8")

    shutil.copy(STATIC_DIR / "css" / "style.css", OUTPUT_DIR / "style.css")

    images_src = STATIC_DIR / "images"
    if images_src.exists() and any(images_src.iterdir()):
        images_dst = OUTPUT_DIR / "images"
        shutil.copytree(images_src, images_dst)

    print(f"Built site into {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
