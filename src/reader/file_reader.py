from pathlib import Path


def read_markdown_files(directory: Path):
    """
    Liest alle Markdown-Dateien aus dem angegebenen Verzeichnis
    und gibt eine Liste von Path-Objekten zurück.
    """

    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(
            f"Das Verzeichnis '{directory}' existiert nicht."
        )

    markdown_files = [
        file for file in directory.iterdir()
        if file.is_file() and file.suffix.lower() == ".md"
    ]

    return markdown_files
