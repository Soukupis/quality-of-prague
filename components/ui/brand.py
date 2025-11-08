from dash import html
from .icon import icon
from .image import image
from ..config import PRIMARY_COLOR, TEXT_COLOR, FONT_SIZE_BRAND, FONT_WEIGHT_BOLD

def brand(
    text: str,
    icon_name: str = None,
    image_src: str = None,
    href: str = "/",
    icon_color: str = PRIMARY_COLOR,
    text_color: str = TEXT_COLOR,
    font_size: str = FONT_SIZE_BRAND,
    image_height: str = "32px"
) -> html.A:
    if image_src:
        brand_icon = image(
            src=image_src,
            alt=f"{text} logo",
            height=image_height,
            class_name="me-2",
            style={
                "objectFit": "contain",
                "verticalAlign": "middle"
            }
        )
    elif icon_name:
        brand_icon = icon(
            name=icon_name,
            color=icon_color,
            class_name="me-2"
        )
    else:
        brand_icon = None

    return html.A([
        brand_icon,
        html.Span(text, style={
            "color": text_color,
            "fontWeight": FONT_WEIGHT_BOLD,
            "fontSize": font_size,
            "textDecoration": "none",
            "lineHeight": "1",
            "verticalAlign": "middle",
            "display": "inline-block"
        })
    ],
    href=href,
    className="navbar-brand d-flex align-items-center",
    style={
        "textDecoration": "none",
        "color": text_color,
        "alignItems": "center",
        "display": "flex",
        "height": "40px"
    })