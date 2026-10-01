import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py


class DividerConfig(WidgetConfig):
    PARAMS = [
        Param("vertical", "Vertical (VerticalDivider)", "switch", False, group="Tipo"),
        Param("thickness", "Grosor (thickness)", "slider", 2.0, 1, 12, unit="px", group="Estilo"),
        Param("space", "Espacio ocupado (height/width)", "slider", 24.0, 1, 60, unit="px", group="Estilo"),
        Param("leading_indent", "leading_indent", "slider", 0.0, 0, 80, unit="px", group="Estilo"),
        Param("trailing_indent", "trailing_indent", "slider", 0.0, 0, 80, unit="px", group="Estilo"),
        Param("color", "Color", "color", None, allow_none=True, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="Divider", icon=ft.Icons.HORIZONTAL_RULE, category="Layout",
            description="Línea separadora horizontal (Divider) o vertical (VerticalDivider) con "
                        "grosor, sangrías y color configurables.",
        )

    def _kwargs(self):
        p = self.p
        size_key = "width" if p("vertical") else "height"
        return {size_key: p("space"), "thickness": p("thickness"), "color": p("color"),
                "leading_indent": p("leading_indent"), "trailing_indent": p("trailing_indent")}

    def create_preview(self) -> ft.Control:
        p = self.p
        if p("vertical"):
            return ft.Container(
                height=160, content=ft.Row(
                    [ft.Text("Izquierda"), ft.VerticalDivider(**self._kwargs()), ft.Text("Derecha")],
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                ))
        return ft.Container(
            width=320, content=ft.Column(
                [ft.Text("Arriba"), ft.Divider(**self._kwargs()), ft.Text("Abajo")],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ))

    def generate_code(self) -> str:
        p = self.p
        name = "ft.VerticalDivider" if p("vertical") else "ft.Divider"
        args = []
        for k, v in self._kwargs().items():
            if v not in (None, 0.0) or k == "thickness":
                args.append((k, py(v)))
        return call(name, *args)
