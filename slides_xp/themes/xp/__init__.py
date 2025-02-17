"""
slides_xp / Windows XP theme.
"""

from textwrap import dedent
import pyhtml as p


def make_intro_slide(
    author: str,
    title: str,
    copyright: str,
) -> p.div:
    return p.div(class_="bootloader")(
        p.span(class_="bootloader-title")(
            p.h2(author),
            p.sup("®"),
            p.img(class_="windows-logo")(
                alt="Windows XP logo", src="/theme/xp.png"
            ),
            p.sub("TM"),
        ),
        p.span(class_="bootloader-subtitle")(
            p.h1(f"{title}", p.sup(p.small("®"))),
            p.h1(class_="xp")("xp"),
        ),
        p.div(class_="boot-animation")(
            [p.div()] * 3,
        ),
        p.div(class_="gap"),
        p.div(class_="copyright")(f"Copyright © {copyright}"),
    )


def make_bsod_slide(
    slide_type: str,
    instructions: str,
) -> p.div:
    return p.div(class_="bsod")(
        p.div(class_="bsod-title")("Windows"),
        p.pre(
            dedent(f"""
            A fatal exception has occurred at 00:C562F1B7 in VXD ctpci9x(05) +
            00001853, The {slide_type} will be terminated.
            """),
            instructions,
        ),
        p.div("Press any key to continue _"),
    )
