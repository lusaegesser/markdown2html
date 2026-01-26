import logging
from pathlib import Path

import markdown

from src.template_renderer import render_template

logging.getLogger(__name__)


def cleanup_output_dir(output_dir: Path):
    output_dir = Path(output_dir)
    if not output_dir.exists():
        return

    for file in output_dir.glob("*.html"):
        logging.info(f"Lösche alte Datei: {file.name}")
        file.unlink()


def convert_markdown_to_html(md_content: str) -> str:
    return markdown.markdown(
        md_content,
        extensions=["fenced_code", "tables"]
    )


def convert_file(md_file_path: Path, output_dir: str = "dist", navigation=None) -> Path:
    md_file_path = Path(md_file_path)
    output_dir = Path(output_dir)

    if not md_file_path.exists():
        raise FileNotFoundError(f"Markdown-Datei nicht gefunden: {md_file_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    md_content = md_file_path.read_text(encoding="utf-8")
    html_raw = convert_markdown_to_html(md_content)

    html_final = render_template(
        content_html=html_raw,
        title=md_file_path.stem,
        navigation=navigation or [],
        current_page=md_file_path.stem,
        version="3.1"
    )

    output_file = output_dir / f"{md_file_path.stem}.html"
    output_file.write_text(html_final, encoding="utf-8")

    logging.info(f"HTML gespeichert: {output_file}")
    return output_file
