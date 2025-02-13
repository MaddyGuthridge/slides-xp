from flask import Flask, Blueprint, redirect
from pathlib import Path
import pyhtml as p

from slides_xp.components import file_picker


def make_blueprint(name: str, path: Path):
    bp = Blueprint(name, __name__, url_prefix=f"/{name}")

    @bp.get("/", defaults={"path": ""})
    @bp.get("/<path:path>")
    def endpoint(path: str):
        return "Hi"

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
