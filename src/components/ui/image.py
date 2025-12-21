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
    """Create an HTML image component with optional sizing and styling.

    Generates a Dash HTML.Img element with convenient width and height
    parameters that automatically apply to the style dictionary.

    Args:
        src: Image source URL or path (e.g., "/assets/logo.png",
            "https://example.com/image.jpg").
        alt: Alternative text for accessibility. Defaults to "".
        width: Optional CSS width value (e.g., "100px", "50%"). Defaults to None.
        height: Optional CSS height value (e.g., "100px", "auto"). Defaults to None.
        class_name: Additional CSS classes to apply. Defaults to "".
        style: Optional dictionary of CSS properties to override or add to
            default styles. Defaults to None.

    Returns:
        html.Img: Dash HTML.Img component with configured properties.

    Examples:
        >>> # Simple image
        >>> logo = image(src="/assets/logo.png", alt="Company Logo")
        >>>
        >>> # Image with specific dimensions
        >>> banner = image(
        ...     src="/assets/banner.jpg",
        ...     alt="Prague Banner",
        ...     width="100%",
        ...     height="300px"
        ... )
        >>>
        >>> # Image with custom styling
        >>> thumbnail = image(
        ...     src="/assets/thumb.png",
        ...     alt="Thumbnail",
        ...     height="80px",
        ...     class_name="rounded",
        ...     style={"objectFit": "cover", "border": "2px solid #ddd"}
        ... )
    """
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