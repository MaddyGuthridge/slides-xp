import pyhtml as p
from pathlib import Path

from slides_xp.markdown import render_markdown
from slides_xp.util import slides_list


def slide(file: Path) -> p.html:
    slides = list(slides_list(file.parent))

    curr_index = slides.index(file)

    first = f"'{slides[0]}'" if len(slides) else "null"
    prev = f"'{slides[curr_index - 1]}'" if curr_index > 0 else "null"
    next = f"'{slides[curr_index + 1]}'" if curr_index < len(slides) - 1 else "null"

    return p.html(
        p.head(
            p.title("Slides XP"),
            p.script(src="/javascript/navigator.js", defer=True),
            p.link(href="/css/root.css", rel="stylesheet"),
            p.link(href="/theme/main.css", rel="stylesheet"),
            p.link(href="/theme/slide.css", rel="stylesheet"),
        ),
        p.body(
            p.script(f"""
                window.sxp = {{
                    first: {first},
                    prev: {prev},
                    next: {next},
                }};
            """),
            p.div(class_="slide-content")(
                p.DangerousRawHtml(render_markdown(file.read_text())),
            ),
        ),
    )
