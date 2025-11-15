from dash import html
from typing import Optional, Dict, Any
from ..config import PRIMARY_COLOR, ICON_SIZE_SMALL


def icon(
    name: str,
    size: str = ICON_SIZE_SMALL,
    color: str = PRIMARY_COLOR,
    class_name: str = "",
    style: Optional[Dict[str, Any]] = None
) -> html.I:
    default_style = {
        "fontSize": size,
        "color": color
    }

    if style:
        default_style.update(style)

    return html.I(
        className=f"bi bi-{name} {class_name}",
        style=default_style
    )