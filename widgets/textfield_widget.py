import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py

BORDERS = [("outline", "OutlineInputBorder"), ("underline", "UnderlineInputBorder"),
           ("none", "Sin borde (NoInputBorder)")]


class TextFieldConfig(WidgetConfig):
    PARAMS = [
        Param("label", "Label", "text", "Correo electrónico", group="Textos"),
        Param("hint_text", "Hint", "text", "tucorreo@ejemplo.com", group="Textos"),
        Param("helper", "Texto de ayuda (helper)", "text", "No compartiremos tu correo", group="Textos"),
        Param("width", "Ancho", "slider", 320.0, 150, 520, unit="px", group="Estilo"),
        Param("border", "Tipo de borde", "select", "outline", options=BORDERS, group="Estilo"),
        Param("radius", "Radio de borde", "slider", 12.0, 0, 30, unit="px", group="Estilo"),
        Param("border_color", "Color del borde enfocado", "color", "#667EEA", group="Estilo"),
        Param("filled", "Relleno (filled)", "switch", False, group="Estilo"),
        Param("prefix_icon", "Icono prefijo", "switch", True, group="Comportamiento"),
        Param("password", "Contraseña", "switch", False, group="Comportamiento"),
        Param("multiline", "Multilínea", "switch", False, group="Comportamiento"),
        Param("counter", "Contador (max_length=40)", "switch", False, group="Comportamiento"),
        Param("error", "Mostrar error", "switch", False, group="Comportamiento"),
    ]

    def __init__(self):
        super().__init__(
            name="TextField", icon=ft.Icons.INPUT, category="Entrada",
            description="Campo de texto con label, hint, ayuda, error, contraseña, multilínea y "
                        "contador. En Flet 1.0 el borde se define con border=ft.OutlineInputBorder(...).",
        )

    def _border(self, color, width=1.0):
        p = self.p
        kind = p("border")
        side = ft.BorderSide(width, color)
        if kind == "underline":
            return ft.UnderlineInputBorder(side=side)
        if kind == "none":
            return ft.NoInputBorder()
        return ft.OutlineInputBorder(border_radius=p("radius"), side=side)

    def _border_code(self, color_code, width="1"):
        p = self.p
        kind = p("border")
        side = f"ft.BorderSide({width}, {color_code})"
        if kind == "underline":
            return f"ft.UnderlineInputBorder(side={side})"
        if kind == "none":
            return "ft.NoInputBorder()"
        return f"ft.OutlineInputBorder(border_radius={py(p('radius'))}, side={side})"

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.TextField(
            label=p("label"), hint_text=p("hint_text"), helper=p("helper") or None,
            width=p("width"), filled=p("filled"),
            prefix_icon=ft.Icons.MAIL_OUTLINE if p("prefix_icon") else None,
            password=p("password"), can_reveal_password=p("password"),
            multiline=p("multiline") and not p("password"),
            min_lines=3 if p("multiline") and not p("password") else None,
            max_length=40 if p("counter") else None,
            error="Este campo es obligatorio" if p("error") else None,
            border={
                ft.ControlState.DEFAULT: self._border(ft.Colors.OUTLINE),
                ft.ControlState.FOCUSED: self._border(p("border_color"), 2),
                ft.ControlState.ERROR: self._border(ft.Colors.ERROR),
            },
        )

    def generate_code(self) -> str:
        p = self.p
        multi = p("multiline") and not p("password")
        borders = (
            "{\n"
            f"    ft.ControlState.DEFAULT: {self._border_code('ft.Colors.OUTLINE')},\n"
            f"    ft.ControlState.FOCUSED: {self._border_code(py(p('border_color')), '2')},\n"
            f"    ft.ControlState.ERROR: {self._border_code('ft.Colors.ERROR')},\n"
            "}"
        )
        return call(
            "ft.TextField",
            ("label", py(p("label"))),
            ("hint_text", py(p("hint_text"))),
            ("helper", py(p("helper"))) if p("helper") else None,
            ("width", py(p("width"))),
            ("filled", "True") if p("filled") else None,
            ("prefix_icon", "ft.Icons.MAIL_OUTLINE") if p("prefix_icon") else None,
            ("password", "True") if p("password") else None,
            ("can_reveal_password", "True") if p("password") else None,
            ("multiline", "True") if multi else None,
            ("min_lines", "3") if multi else None,
            ("max_length", "40") if p("counter") else None,
            ("error", '"Este campo es obligatorio"') if p("error") else None,
            ("border", borders),
        )
