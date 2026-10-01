import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py

CAPS = [("ROUND", "Redondeado"), ("BUTT", "Recto"), ("SQUARE", "Cuadrado")]


class ProgressBarConfig(WidgetConfig):
    PARAMS = [
        Param("determinate", "Determinado (con valor)", "switch", True, group="Valor"),
        Param("value", "Progreso", "slider", 0.6, 0, 1, decimals=2, group="Valor"),
        Param("width", "Ancho", "slider", 320.0, 120, 520, unit="px", group="Estilo"),
        Param("bar_height", "Alto de la barra", "slider", 8.0, 2, 30, unit="px", group="Estilo"),
        Param("radius", "Radio de borde", "slider", 8.0, 0, 15, unit="px", group="Estilo"),
        Param("color", "Color", "color", None, allow_none=True, group="Estilo"),
        Param("bgcolor", "Fondo", "color", None, allow_none=True, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="ProgressBar", icon=ft.Icons.HOURGLASS_BOTTOM, category="Feedback",
            description="Barra de progreso lineal: determinada (value 0..1) o indeterminada "
                        "(value=None) para cargas de duración desconocida.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Column([
            ft.Text(f"{p('value') * 100:.0f}%" if p("determinate") else "Cargando…"),
            ft.ProgressBar(value=p("value") if p("determinate") else None, width=p("width"),
                           bar_height=p("bar_height"), border_radius=p("radius"),
                           color=p("color"), bgcolor=p("bgcolor")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def generate_code(self) -> str:
        p = self.p
        return call(
            "ft.ProgressBar",
            ("value", py(p("value")) if p("determinate") else "None"),
            ("width", py(p("width"))),
            ("bar_height", py(p("bar_height"))),
            ("border_radius", py(p("radius"))),
            ("color", py(p("color"))) if p("color") else None,
            ("bgcolor", py(p("bgcolor"))) if p("bgcolor") else None,
        )


class ProgressRingConfig(WidgetConfig):
    PARAMS = [
        Param("determinate", "Determinado (con valor)", "switch", False, group="Valor"),
        Param("value", "Progreso", "slider", 0.7, 0, 1, decimals=2, group="Valor"),
        Param("size", "Tamaño", "slider", 64.0, 16, 160, unit="px", group="Estilo"),
        Param("stroke_width", "Grosor", "slider", 6.0, 1, 20, unit="px", group="Estilo"),
        Param("stroke_cap", "Extremo del trazo", "select", "ROUND", options=CAPS, group="Estilo"),
        Param("color", "Color", "color", None, allow_none=True, group="Estilo"),
        Param("bgcolor", "Pista (fondo)", "color", None, allow_none=True, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="ProgressRing", icon=ft.Icons.DATA_USAGE, category="Feedback",
            description="Indicador de progreso circular. Cambia su tamaño con width/height y el "
                        "grosor con stroke_width.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.ProgressRing(
            value=p("value") if p("determinate") else None,
            width=p("size"), height=p("size"), stroke_width=p("stroke_width"),
            stroke_cap=getattr(ft.StrokeCap, p("stroke_cap")),
            color=p("color"), bgcolor=p("bgcolor"),
        )

    def generate_code(self) -> str:
        p = self.p
        return call(
            "ft.ProgressRing",
            ("value", py(p("value"))) if p("determinate") else None,
            ("width", py(p("size"))),
            ("height", py(p("size"))),
            ("stroke_width", py(p("stroke_width"))),
            ("stroke_cap", f"ft.StrokeCap.{p('stroke_cap')}"),
            ("color", py(p("color"))) if p("color") else None,
            ("bgcolor", py(p("bgcolor"))) if p("bgcolor") else None,
        )
