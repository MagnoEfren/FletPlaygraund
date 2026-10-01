import flet as ft

from core.base_widget import FONT_WEIGHTS, Param, WidgetConfig
from services.code_service import call, py

ALIGNS = [("LEFT", "Izquierda"), ("CENTER", "Centro"), ("RIGHT", "Derecha"), ("JUSTIFY", "Justificado")]
DECORATIONS = [("NONE", "Ninguna"), ("UNDERLINE", "Subrayado"), ("LINE_THROUGH", "Tachado"),
               ("OVERLINE", "Línea superior")]
OVERFLOWS = [("VISIBLE", "Visible"), ("ELLIPSIS", "Elipsis (…)"), ("FADE", "Fade"), ("CLIP", "Clip")]


class TextConfig(WidgetConfig):
    PARAMS = [
        Param("value", "Texto", "text", "Flet hace que crear apps en Python sea rápido y divertido.",
              group="Contenido"),
        Param("width", "Ancho máximo", "slider", 320.0, 100, 520, unit="px", group="Contenido"),
        Param("size", "Tamaño", "slider", 24.0, 10, 64, unit="px", group="Tipografía"),
        Param("weight", "Peso", "select", "W_500", options=FONT_WEIGHTS, group="Tipografía"),
        Param("letter_spacing", "Espaciado entre letras", "slider", 0.0, -2, 10, decimals=1,
              unit="px", group="Tipografía"),
        Param("color", "Color", "color", None, allow_none=True, group="Tipografía"),
        Param("text_align", "Alineación", "select", "CENTER", options=ALIGNS, group="Párrafo"),
        Param("decoration", "Decoración", "select", "NONE", options=DECORATIONS, group="Párrafo"),
        Param("max_lines", "Máx. líneas (0 = sin límite)", "slider", 0.0, 0, 6, divisions=6, group="Párrafo"),
        Param("overflow", "Overflow", "select", "ELLIPSIS", options=OVERFLOWS, group="Párrafo"),
        Param("italic", "Cursiva", "switch", False, group="Párrafo"),
        Param("selectable", "Seleccionable", "switch", False, group="Párrafo"),
    ]

    def __init__(self):
        super().__init__(
            name="Text", icon=ft.Icons.TEXT_FIELDS, category="Texto y media",
            description="Muestra texto con control total de tipografía: tamaño, peso, color, "
                        "espaciado, decoración, alineación y límite de líneas.",
        )

    def _style(self):
        p = self.p
        deco = None if p("decoration") == "NONE" else getattr(ft.TextDecoration, p("decoration"))
        if deco is None and not p("letter_spacing"):
            return None
        return ft.TextStyle(letter_spacing=p("letter_spacing") or None, decoration=deco)

    def create_preview(self) -> ft.Control:
        p = self.p
        lines = int(p("max_lines"))
        return ft.Text(
            p("value"),
            width=p("width"),
            size=p("size"),
            weight=getattr(ft.FontWeight, p("weight")),
            color=p("color"),
            italic=p("italic"),
            selectable=p("selectable"),
            text_align=getattr(ft.TextAlign, p("text_align")),
            max_lines=lines or None,
            overflow=getattr(ft.TextOverflow, p("overflow")) if lines else None,
            style=self._style(),
        )

    def generate_code(self) -> str:
        p = self.p
        lines = int(p("max_lines"))
        style = None
        if self._style() is not None:
            style = ("style", call(
                "ft.TextStyle",
                ("letter_spacing", py(p("letter_spacing"))) if p("letter_spacing") else None,
                ("decoration", f"ft.TextDecoration.{p('decoration')}") if p("decoration") != "NONE" else None,
            ))
        return call(
            "ft.Text",
            py(p("value")),
            ("width", py(p("width"))),
            ("size", py(p("size"))),
            ("weight", f"ft.FontWeight.{p('weight')}"),
            ("color", py(p("color"))) if p("color") else None,
            ("text_align", f"ft.TextAlign.{p('text_align')}"),
            ("max_lines", py(lines)) if lines else None,
            ("overflow", f"ft.TextOverflow.{p('overflow')}") if lines else None,
            ("italic", "True") if p("italic") else None,
            ("selectable", "True") if p("selectable") else None,
            style,
        )
