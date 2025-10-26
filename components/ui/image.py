from dash import html
from typing import Optional, Dict, Any


def image(
    src: str,
    alt: str = "",
    width: Optional[str] = None,
    height: Optional[str] = None,
    class_name: str = "",
    style: Optional[Dict[str, Any]] = None
) -> html.Img:
    default_style = {}

    if width:
        default_style["width"] = width
    if height:
        default_style["height"] = height

    if style:
        default_style.update(style)

    return html.Img(
        src=src,
        alt=alt,
        className=class_name,
        style=default_style if default_style else None
    )
