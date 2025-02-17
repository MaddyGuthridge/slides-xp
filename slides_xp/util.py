from pathlib import Path


def list_subdirs(path: Path) -> list[Path]:
    return [subdir for subdir in path.iterdir() if subdir.is_dir()]


def dir_contains_slides(path: Path) -> bool:
    """
    Returns whether the given directory contains Markdown files.
    """
    return next(iter(slides_list(path)), None) is not None


def first_slide(path: Path) -> Path:
    """
    Returns the path of the first slide in the given dir
    """
    return next(iter(slides_list(path)))


def slides_list(path: Path) -> list[Path]:
    """
    Returns a slides list for the given directory.
    """
    return sorted(
        [
            child
            for child in path.iterdir()
            if child.is_file()
            and child.suffixes in [[".md"], [".slide", ".py"]]
        ],
        key=lambda i: i.name,
    )
