from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_template(
    content_html: str,
    title: str,
    navigation: Optional[List[Dict]] = None,
    current_page: Optional[str] = None,
    date: Optional[str] = None,
    version: Optional[str] = None
) -> str:
    project_root = Path(__file__).resolve().parent.parent
    template_dir = project_root / "templates"

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("base.html")

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    if navigation is None:
        navigation = []

    # active-Flag setzen
    if current_page:
        for item in navigation:
            item["active"] = (item.get("label") == current_page)

    return template.render(
        title=title,
        content=content_html,
        navigation=navigation,
        date=date,
        version=version
    )
