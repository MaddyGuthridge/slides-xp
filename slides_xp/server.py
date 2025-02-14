from flask import Flask, Blueprint, redirect, send_from_directory
from pathlib import Path
import pyhtml as p

from slides_xp.file_picker import file_picker
from slides_xp.slide import slide
from slides_xp.util import dir_contains_md, first_slide, list_subdirs


lib_dir = Path(__file__).parent


def error(code: int, message: str):
    return str(
        p.html(
            p.body(
                p.h1(f"Error {code}"),
                p.p(message),
            )
        )
    ), code


def make_blueprint(name: str, root: Path):
    bp = Blueprint(name, __name__, url_prefix=f"/{name}")

    @bp.get("/", defaults={"path": ""})
    @bp.get("/<path:path>")
    def endpoint(path: str):
        full_path = root / path
        # Root path must be a parent of `full_path` to prevent escaping the
        # specified directories
        if root not in [full_path, *full_path.parents]:
            return error(403, "Illegal path")
        # 404 if file/dir does not exist
        if not full_path.exists():
            return error(404, "File not found")
        # If file, send it
        if full_path.is_file():
            # Render markdown files as HTML
            if full_path.suffix == ".md":
                return str(slide(full_path))
            else:
                return send_from_directory(root, full_path.absolute())
        # If dir with markdown, redirect to first slide
        if dir_contains_md(full_path):
            return redirect(f"/{full_path}/{first_slide(full_path).name}")
        else:
            # Otherwise, dir with no markdown, so render a list of subdirs
            options = file_picker(
                str(root),
                [p.name for p in list_subdirs(full_path)],
                parent=str(root.parent),
            )
            return str(
                p.html(
                    p.head(
                        p.title("Slides XP"),
                    ),
                    p.body(
                        options,
                    ),
                )
            )

    return bp


def make_app(paths: list[Path], theme: str | None = None):
    if theme is None:
        theme_dir = lib_dir / "themes" / "default"
    elif Path(theme).is_dir():
        theme_dir = Path(theme)
    elif (lib_dir / "themes" / theme).is_dir():
        theme_dir = lib_dir / "themes" / theme
    else:
        # Invalid theme
        theme_dir = lib_dir / "themes" / "default"

    app = Flask(__name__)

    for path in paths:
        app.register_blueprint(make_blueprint(path.name, path))

    @app.get("/")
    def root():
        """
        Root path.

        If using one path, redirect to it. Otherwise give a choice.
        """
        if len(paths) == 1:
            return redirect(f"/{paths[0].name}/")
        else:
            options = file_picker("", [p.name for p in paths])
            return str(
                p.html(
                    p.head(
                        p.title("Slides XP"),
                    ),
                    p.body(
                        options,
                    ),
                )
            )

    @app.get("/javascript/<path>")
    def scripts(path):
        return send_from_directory(lib_dir / "javascript", path)

    @app.get("/css/<path>")
    def css(path):
        return send_from_directory(lib_dir / "css", path)

    @app.get("/theme/<path>")
    def theme_css(path):
        return send_from_directory(theme_dir, path)

    return app


if __name__ == "__main__":
    app = make_app([Path("temp")])
    app.run(port=3000)
