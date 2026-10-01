import flet as ft

from core.base_widget import ICON_OPTIONS, Param, WidgetConfig
from services.code_service import call, py

SHAPES = [("rounded", "Redondeado"), ("circle", "Círculo"), ("stadium", "Píldora")]


class FloatingActionButtonConfig(WidgetConfig):
    PARAMS = [
        Param("extended", "Extendido (icono + texto)", "switch", False, group="Contenido"),
        Param("text", "Texto", "text", "Nuevo", group="Contenido"),
        Param("icon", "Icono", "icon", "ADD", options=ICON_OPTIONS, group="Contenido"),
        Param("bgcolor", "Fondo", "color", None, allow_none=True, group="Estilo"),
        Param("foreground_color", "Color del contenido", "color", None, allow_none=True, group="Estilo"),
        Param("shape", "Forma", "select", "rounded", options=SHAPES, group="Estilo"),
        Param("radius", "Radio (si es redondeado)", "slider", 16.0, 0, 32, unit="px", group="Estilo"),
        Param("elevation", "Elevación", "slider", 6.0, 0, 20, group="Estilo"),
        Param("mini", "Mini", "switch", False, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="FloatingActionButton", icon=ft.Icons.ADD_CIRCLE, category="Botones",
            doc_slug="floatingactionbutton",
            description="Botón de acción flotante para la acción principal de una pantalla. "
                        "Asígnalo a page.floating_action_button para que flote sobre el contenido.",
        )

    def _shape(self):
        s = self.p("shape")
        if s == "circle":
            return ft.CircleBorder(), "ft.CircleBorder()"
        if s == "stadium":
            return ft.StadiumBorder(), "ft.StadiumBorder()"
        r = self.p("radius")
        return ft.RoundedRectangleBorder(radius=r), f"ft.RoundedRectangleBorder(radius={py(r)})"

    def create_preview(self) -> ft.Control:
        p = self.p
        extended = p("extended")
        return ft.FloatingActionButton(
            content=p("text") if extended else None,
            icon=self.icon_of(p("icon")),
            bgcolor=p("bgcolor"), foreground_color=p("foreground_color"),
            shape=self._shape()[0], elevation=p("elevation"),
            mini=p("mini") and not extended,
        )

    def generate_code(self) -> str:
        p = self.p
        extended = p("extended")
        return call(
            "ft.FloatingActionButton",
            ("content", py(p("text"))) if extended else None,
            ("icon", self.icon_code(p("icon"))),
            ("bgcolor", py(p("bgcolor"))) if p("bgcolor") else None,
            ("foreground_color", py(p("foreground_color"))) if p("foreground_color") else None,
            ("shape", self._shape()[1]),
            ("elevation", py(p("elevation"))),
            ("mini", "True") if p("mini") and not extended else None,
        )
