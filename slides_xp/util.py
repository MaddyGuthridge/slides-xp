from pathlib import Path
from typing import Generator


def list_subdirs(path: Path) -> list[Path]:
    return [subdir for subdir in path.iterdir() if subdir.is_dir()]


def dir_contains_md(path: Path) -> bool:
    """
    Returns whether the given directory contains Markdown files.
    """
    return next(slides_list(path), None) is not None


def first_slide(path: Path) -> Path:
    """
    Returns the path of the first slide in the given dir
    """
    return next(slides_list(path))


def slides_list(path: Path) -> Generator[Path]:
    """
    Returns a slides list for the given directory.
    """
    return (
        child for child in path.iterdir() if child.is_file() and child.suffix == ".md"
    )
