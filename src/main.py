import argparse
import logging
import shutil
from pathlib import Path

from src.reader.file_reader import read_markdown_files
from src.markdown_converter import convert_file, cleanup_output_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    force=True
)


def copy_assets(project_root: Path, output_dir: Path):
    source_css = project_root / "assets" / "style.css"
    target_css_dir = output_dir / "assets" / "css"
    target_css = target_css_dir / "style.css"

    if not source_css.exists():
        logging.error(f"CSS-Datei fehlt: {source_css}")
        return False

    target_css_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_css, target_css)
    logging.info(f"CSS kopiert nach: {target_css}")
    return True


def build_navigation(md_files):
    """
    Erstellt Navigationseinträge aus Markdown-Dateien.
    """
    navigation = []
    for md in md_files:
        navigation.append({
            "label": md.stem,
            "href": f"{md.stem}.html",
            "active": False
        })
    return navigation


def run_build(input_dir: Path, output_dir: Path):
    logging.info("Starte Markdown → HTML Build-Prozess")
    logging.info(f"Eingabeordner: {input_dir}")
    logging.info(f"Ausgabeordner: {output_dir}")

    if not input_dir.exists() or not input_dir.is_dir():
        logging.error(f"Eingabeverzeichnis existiert nicht oder ist kein Ordner: {input_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        md_files = read_markdown_files(input_dir)
    except FileNotFoundError as e:
        logging.error(str(e))
        return

    logging.info(f"{len(md_files)} Markdown-Dateien gefunden")
    if not md_files:
        logging.warning("Keine Markdown-Dateien zur Verarbeitung vorhanden")
        return

    cleanup_output_dir(output_dir)
    logging.info("Alte HTML-Dateien bereinigt")

    project_root = Path(__file__).resolve().parent.parent
    if not copy_assets(project_root, output_dir):
        logging.error("Build abgebrochen, da CSS-Assets fehlen")
        return

    navigation = build_navigation(md_files)

    for md in md_files:
        logging.info(f"Konvertiere Datei: {md.name}")
        convert_file(md, output_dir=str(output_dir), navigation=navigation)

    logging.info("Build-Prozess erfolgreich abgeschlossen")


def main():
    project_root = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(description="Markdown → HTML Dokumentationsgenerator")

    parser.add_argument(
        "command",
        nargs="?",
        default="build",
        choices=["build"],
        help="Auszuführender Befehl (Standard: build)"
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=project_root / "docs",
        help="Eingabeverzeichnis für Markdown-Dateien"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "dist",
        help="Ausgabeverzeichnis für HTML-Dateien"
    )

    args = parser.parse_args()

    if args.command == "build":
        run_build(args.input, args.output)


if __name__ == "__main__":
    main()
