import pyhtml as p


def file_picker(root: str, choices: list[str]):
    choices_html = [
        p.div(class_="picker-choice")(
            p.a(href=f"{root}/{choice}")(choice),
        )
        for choice in choices
    ]

    return p.div(choices_html)
