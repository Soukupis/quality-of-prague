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
    """Create a clickable brand component with text and optional icon or logo.

    Builds a navbar brand element combining text with either a Bootstrap icon
    or a custom image/logo. Commonly used in navigation headers.

    Args:
        text: Brand name or application title to display.
        icon_name: Bootstrap icon name (without 'bi-' prefix). Optional.
        image_src: URL or path to brand logo image. Optional. Takes precedence
            over icon_name if both provided.
        href: Link destination when brand is clicked. Defaults to "/" (home).
        icon_color: Color for the icon if icon_name is used. Defaults to
            PRIMARY_COLOR from config.
        text_color: Color for the brand text. Defaults to TEXT_COLOR from config.
        font_size: Font size for the brand text. Defaults to FONT_SIZE_BRAND
            from config.
        image_height: Height of the logo image if image_src is used. Defaults
            to "32px".

    Returns:
        html.A: Dash HTML.A component configured as a clickable navbar brand
            with proper styling and alignment.

    Examples:
        >>> # Text-only brand
        >>> brand_component = brand("Quality of Prague")
        >>>
        >>> # Brand with icon
        >>> brand_with_icon = brand(
        ...     text="Prague Analytics",
        ...     icon_name="bar-chart",
        ...     href="/dashboard"
        ... )
        >>>
        >>> # Brand with custom logo
        >>> brand_with_logo = brand(
        ...     text="Quality of Prague",
        ...     image_src="/assets/prague_icon.png",
        ...     image_height="40px"
        ... )
    """
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