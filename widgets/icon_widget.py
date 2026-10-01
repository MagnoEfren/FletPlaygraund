import flet as ft

from core.base_widget import ICON_OPTIONS, Param, WidgetConfig
from services.code_service import call, py


class IconConfig(WidgetConfig):
    PARAMS = [
        Param("icon", "Icono", "icon", "FAVORITE", options=ICON_OPTIONS, group="Icono"),
        Param("size", "Tamaño", "slider", 64.0, 16, 160, unit="px", group="Icono"),
        Param("color", "Color", "color", "#F56565", allow_none=True, group="Icono"),
        Param("rotate", "Rotación", "slider", 0.0, 0, 6.28, decimals=2, unit=" rad", group="Transformación"),
        Param("opacity", "Opacidad", "slider", 1.0, 0.1, 1.0, decimals=2, group="Transformación"),
    ]

    def __init__(self):
        super().__init__(
            name="Icon", icon=ft.Icons.EMOJI_EMOTIONS, category="Texto y media",
            description="Muestra un icono Material (ft.Icons.*) o Cupertino con tamaño, color, "
                        "rotación y opacidad configurables.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Icon(self.icon_of(p("icon")), size=p("size"), color=p("color"),
                       rotate=p("rotate") or None, opacity=p("opacity"))

    def generate_code(self) -> str:
        p = self.p
        return call(
            "ft.Icon", self.icon_code(p("icon")),
            ("size", py(p("size"))),
            ("color", py(p("color"))) if p("color") else None,
            ("rotate", py(p("rotate"))) if p("rotate") else None,
            ("opacity", py(p("opacity"))) if p("opacity") < 1 else None,
        )
