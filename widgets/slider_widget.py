import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py


class SliderConfig(WidgetConfig):
    PARAMS = [
        Param("value", "Valor inicial", "slider", 40.0, 0, 100, group="Rango"),
        Param("divisions", "Divisiones (0 = continuo)", "slider", 10.0, 0, 20, divisions=20, group="Rango"),
        Param("width", "Ancho", "slider", 320.0, 150, 520, unit="px", group="Estilo"),
        Param("active_color", "Color activo", "color", None, allow_none=True, group="Estilo"),
        Param("inactive_color", "Color inactivo", "color", None, allow_none=True, group="Estilo"),
        Param("show_label", "Mostrar valor al arrastrar", "switch", True, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="Slider", icon=ft.Icons.LINEAR_SCALE, category="Entrada",
            description="Selecciona un valor dentro de un rango arrastrando. Con divisions se "
                        "vuelve discreto y label='{value}' muestra el valor actual.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        div = int(p("divisions"))
        return ft.Slider(
            min=0, max=100, value=p("value"), divisions=div or None,
            width=p("width"), label="{value}" if p("show_label") else None,
            active_color=p("active_color"), inactive_color=p("inactive_color"),
        )

    def generate_code(self) -> str:
        p = self.p
        div = int(p("divisions"))
        return call(
            "ft.Slider",
            ("min", "0"), ("max", "100"),
            ("value", py(p("value"))),
            ("divisions", py(div)) if div else None,
            ("width", py(p("width"))),
            ("label", '"{value}"') if p("show_label") else None,
            ("active_color", py(p("active_color"))) if p("active_color") else None,
            ("inactive_color", py(p("inactive_color"))) if p("inactive_color") else None,
            ("on_change", "lambda e: print(e.control.value)"),
        )
