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
    """Create a Bootstrap icon component.

    Generates an HTML icon element using Bootstrap Icons. Provides convenient
    defaults for size and color while allowing customization through style
    overrides.

    Args:
        name: Bootstrap icon name without the 'bi-' prefix (e.g., 'map',
            'gear', 'house').
        size: Font size for the icon. Defaults to ICON_SIZE_SMALL from config.
        color: Icon color as CSS color value. Defaults to PRIMARY_COLOR from config.
        class_name: Additional CSS classes to apply to the icon. Defaults to "".
        style: Optional dictionary of CSS properties to override or add to
            default styles. Defaults to None.

    Returns:
        html.I: Dash HTML.I component configured as a Bootstrap icon.

    Examples:
        >>> # Simple icon with defaults
        >>> home_icon = icon("house")
        >>>
        >>> # Large colored icon
        >>> settings_icon = icon(
        ...     "gear",
        ...     size="2rem",
        ...     color="#ff6b6b"
        ... )
        >>>
        >>> # Icon with custom styles
        >>> map_icon = icon(
        ...     "map",
        ...     class_name="me-2",
        ...     style={"marginTop": "5px"}
        ... )
    """
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