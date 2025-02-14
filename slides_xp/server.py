from flask import Flask, Blueprint, redirect, send_file
from pathlib import Path
import pyhtml as p

from slides_xp.file_picker import file_picker
from slides_xp.util import dir_contains_md, first_slide, list_subdirs


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
            return send_file(full_path.absolute())
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


def make_app(paths: list[Path]):
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
            options = file_picker("/", [p.name for p in paths])
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

    return app


if __name__ == "__main__":
    app = make_app([Path("temp")])
    app.run(port=3000)
