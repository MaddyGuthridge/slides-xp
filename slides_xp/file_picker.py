import pyhtml as p


def file_picker(root: str, choices: list[str], parent: str | None = None):
    choices_html = [
        p.div(class_="picker-choice")(
            p.a(href=f"{root}/{choice}")(choice),
        )
        for choice in choices
    ]

    if parent is not None:
        choices_html.insert(0, p.div(class_="picker-choice")(p.a(href=parent)("..")))

    return p.div(choices_html)
