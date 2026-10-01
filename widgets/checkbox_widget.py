import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py

VALUES = [("true", "Marcado"), ("false", "Desmarcado"), ("none", "Indeterminado (tristate)")]
POSITIONS = [("RIGHT", "Derecha"), ("LEFT", "Izquierda")]


class CheckboxConfig(WidgetConfig):
    PARAMS = [
        Param("label", "Label", "text", "Acepto los términos", group="Contenido"),
        Param("value", "Valor", "select", "true", options=VALUES, group="Estado"),
        Param("label_position", "Posición del label", "select", "RIGHT", options=POSITIONS, group="Estilo"),
        Param("fill_color", "Color de relleno", "color", None, allow_none=True, group="Estilo"),
        Param("check_color", "Color del check", "color", None, allow_none=True, group="Estilo"),
        Param("radius", "Radio de las esquinas", "slider", 4.0, 0, 12, unit="px", group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="Checkbox", icon=ft.Icons.CHECK_BOX, category="Entrada",
            description="Casilla de verificación con estados marcado, desmarcado e indeterminado "
                        "(tristate=True).",
        )

    def _value(self):
        return {"true": True, "false": False, "none": None}[self.p("value")]

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Checkbox(
            label=p("label"), value=self._value(), tristate=p("value") == "none",
            label_position=getattr(ft.LabelPosition, p("label_position")),
            fill_color=p("fill_color"), check_color=p("check_color"),
            shape=ft.RoundedRectangleBorder(radius=p("radius")),
        )

    def generate_code(self) -> str:
        p = self.p
        return call(
            "ft.Checkbox",
            ("label", py(p("label"))),
            ("value", py(self._value())),
            ("tristate", "True") if p("value") == "none" else None,
            ("label_position", "ft.LabelPosition.LEFT") if p("label_position") == "LEFT" else None,
            ("fill_color", py(p("fill_color"))) if p("fill_color") else None,
            ("check_color", py(p("check_color"))) if p("check_color") else None,
            ("shape", f"ft.RoundedRectangleBorder(radius={py(p('radius'))})"),
            ("on_change", "lambda e: print(e.control.value)"),
        )
