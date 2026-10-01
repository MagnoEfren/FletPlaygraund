import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py

ALIGNMENTS = [("CENTER", "Centro"), ("TOP_LEFT", "Arriba izq."), ("TOP_RIGHT", "Arriba der."),
              ("BOTTOM_LEFT", "Abajo izq."), ("BOTTOM_RIGHT", "Abajo der.")]


class ContainerConfig(WidgetConfig):
    PARAMS = [
        Param("width", "Ancho", "slider", 260.0, 50, 500, unit="px", group="Tamaño"),
        Param("height", "Alto", "slider", 180.0, 50, 400, unit="px", group="Tamaño"),
        Param("padding", "Padding", "slider", 20.0, 0, 60, unit="px", group="Tamaño"),
        Param("border_radius", "Radio de borde", "slider", 16.0, 0, 120, unit="px", group="Forma"),
        Param("alignment", "Alineación del contenido", "select", "CENTER", options=ALIGNMENTS, group="Forma"),
        Param("bgcolor", "Color de fondo", "color", "#667EEA", group="Color"),
        Param("gradient", "Degradado", "switch", False, group="Color"),
        Param("shadow", "Sombra", "switch", True, group="Efectos"),
        Param("border", "Borde", "switch", False, group="Efectos"),
        Param("border_width", "Grosor del borde", "slider", 3.0, 1, 12, unit="px", group="Efectos"),
        Param("border_color", "Color del borde", "color", "#2D3748", group="Efectos"),
        Param("rotate", "Rotación", "slider", 0.0, -0.8, 0.8, decimals=2, unit=" rad", group="Efectos"),
    ]

    def __init__(self):
        super().__init__(
            name="Container",
            icon=ft.Icons.CROP_SQUARE,
            category="Layout",
            description="Caja contenedora versátil: controla tamaño, padding, color, degradados, "
                        "bordes, sombras, alineación y transformaciones de su contenido.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Container(
            content=ft.Text("¡Hola Flet!", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
            width=p("width"),
            height=p("height"),
            padding=p("padding"),
            border_radius=p("border_radius"),
            alignment=getattr(ft.Alignment, p("alignment")),
            bgcolor=None if p("gradient") else p("bgcolor"),
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                colors=[p("bgcolor"), "#764BA2"],
            ) if p("gradient") else None,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=18,
                                color=ft.Colors.with_opacity(0.3, "#000000"),
                                offset=ft.Offset(0, 6)) if p("shadow") else None,
            border=ft.Border.all(p("border_width"), p("border_color")) if p("border") else None,
            rotate=p("rotate") or None,
        )

    def generate_code(self) -> str:
        p = self.p
        fill = (("gradient", call("ft.LinearGradient",
                                  ("begin", "ft.Alignment.TOP_LEFT"),
                                  ("end", "ft.Alignment.BOTTOM_RIGHT"),
                                  ("colors", f"[{py(p('bgcolor'))}, \"#764BA2\"]")))
                if p("gradient") else ("bgcolor", py(p("bgcolor"))))
        return call(
            "ft.Container",
            ("content", 'ft.Text("¡Hola Flet!", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD)'),
            ("width", py(p("width"))),
            ("height", py(p("height"))),
            ("padding", py(p("padding"))),
            ("border_radius", py(p("border_radius"))),
            ("alignment", f"ft.Alignment.{p('alignment')}"),
            fill,
            ("shadow", call("ft.BoxShadow", ("spread_radius", "1"), ("blur_radius", "18"),
                            ("color", 'ft.Colors.with_opacity(0.3, "#000000")'),
                            ("offset", "ft.Offset(0, 6)"))) if p("shadow") else None,
            ("border", f"ft.Border.all({py(p('border_width'))}, {py(p('border_color'))})") if p("border") else None,
            ("rotate", py(p("rotate"))) if p("rotate") else None,
        )
