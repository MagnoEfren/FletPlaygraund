import flet as ft

from core.base_widget import ICON_OPTIONS, Param, WidgetConfig
from services.code_service import call, py

VARIANTS = [
    ("Button", "Button (antes ElevatedButton)"),
    ("FilledButton", "FilledButton"),
    ("FilledTonalButton", "FilledTonalButton"),
    ("OutlinedButton", "OutlinedButton"),
    ("TextButton", "TextButton"),
]


class ButtonConfig(WidgetConfig):
    PARAMS = [
        Param("variant", "Variante", "select", "Button", options=VARIANTS, group="Tipo"),
        Param("text", "Texto", "text", "Click me!", group="Contenido"),
        Param("show_icon", "Mostrar icono", "switch", True, group="Contenido"),
        Param("icon", "Icono", "icon", "SEND", options=ICON_OPTIONS, group="Contenido"),
        Param("bgcolor", "Fondo", "color", None, allow_none=True, group="Estilo"),
        Param("color", "Color del texto", "color", None, allow_none=True, group="Estilo"),
        Param("radius", "Radio de borde", "slider", 20.0, 0, 30, unit="px", group="Estilo"),
        Param("elevation", "Elevación", "slider", 2.0, 0, 16, group="Estilo"),
        Param("pad_h", "Padding horizontal", "slider", 24.0, 8, 60, unit="px", group="Estilo"),
        Param("pad_v", "Padding vertical", "slider", 16.0, 4, 40, unit="px", group="Estilo"),
        Param("disabled", "Deshabilitado", "switch", False, group="Estado"),
    ]

    def __init__(self):
        super().__init__(
            name="Button", icon=ft.Icons.SMART_BUTTON, category="Botones",
            description="Botones Material 3. En Flet 1.0 ElevatedButton se eliminó: usa ft.Button "
                        "(o Filled, FilledTonal, Outlined, Text) y siempre content= en vez de text=.",
        )

    def _style_args(self):
        p = self.p
        return dict(
            bgcolor=p("bgcolor"), color=p("color"), elevation=p("elevation"),
            shape=ft.RoundedRectangleBorder(radius=p("radius")),
            padding=ft.Padding.symmetric(horizontal=p("pad_h"), vertical=p("pad_v")),
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        cls = getattr(ft, p("variant"))
        return cls(
            content=p("text"),
            icon=self.icon_of(p("icon")) if p("show_icon") else None,
            disabled=p("disabled"),
            style=ft.ButtonStyle(**self._style_args()),
            on_click=lambda e: print("¡Click!"),
        )

    def generate_code(self) -> str:
        p = self.p
        style = call(
            "ft.ButtonStyle",
            ("bgcolor", py(p("bgcolor"))) if p("bgcolor") else None,
            ("color", py(p("color"))) if p("color") else None,
            ("elevation", py(p("elevation"))),
            ("shape", f"ft.RoundedRectangleBorder(radius={py(p('radius'))})"),
            ("padding", f"ft.Padding.symmetric(horizontal={py(p('pad_h'))}, vertical={py(p('pad_v'))})"),
        )
        return call(
            f"ft.{p('variant')}",
            ("content", py(p("text"))),
            ("icon", self.icon_code(p("icon"))) if p("show_icon") else None,
            ("disabled", "True") if p("disabled") else None,
            ("style", style),
            ("on_click", 'lambda e: print("¡Click!")'),
        )
