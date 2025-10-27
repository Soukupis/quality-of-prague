from dataclasses import dataclass

@dataclass
class DistrictMapStyle:
    background_color = "#6BA6F0"
    border_color = "#DDDDDD"
    border_width = 1
    text_color = "black"
    text_size = 12
    highlight_color = "black"
    highlight_width = 3


@dataclass
class DistrictMapLayout:
    style = "white-bg"
    zoom = 10.5
    height = 900
    width = 1000
    margin = None

    def __post_init__(self):
        if self.margin is None:
            self.margin = dict(l=0, r=0, t=0, b=0)