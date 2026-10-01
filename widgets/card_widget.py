import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, code_list, py

VARIANTS = [("ELEVATED", "Elevated"), ("FILLED", "Filled"), ("OUTLINED", "Outlined")]


class CardConfig(WidgetConfig):
    PARAMS = [
        Param("variant", "Variante (Material 3)", "select", "ELEVATED", options=VARIANTS, group="Estilo"),
        Param("elevation", "Elevación", "slider", 4.0, 0, 20, group="Estilo"),
        Param("radius", "Radio de borde", "slider", 14.0, 0, 40, unit="px", group="Estilo"),
        Param("bgcolor", "Color de fondo", "color", None, allow_none=True, group="Estilo"),
        Param("width", "Ancho", "slider", 320.0, 200, 460, unit="px", group="Contenido"),
        Param("title", "Título", "text", "Título de la tarjeta", group="Contenido"),
        Param("show_button", "Mostrar botón", "switch", True, group="Contenido"),
    ]

    def __init__(self):
        super().__init__(
            name="Card", icon=ft.Icons.CREDIT_CARD, category="Layout",
            description="Superficie Material 3 con elevación y esquinas redondeadas. Variantes "
                        "elevated, filled y outlined para agrupar información relacionada.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        body = [
            ft.ListTile(leading=ft.Icon(ft.Icons.ALBUM), title=ft.Text(p("title")),
                        subtitle=ft.Text("Subtítulo de ejemplo")),
        ]
        if p("show_button"):
            body.append(ft.Row([ft.TextButton("Cancelar"), ft.Button("Aceptar")],
                               alignment=ft.MainAxisAlignment.END))
        return ft.Card(
            variant=getattr(ft.CardVariant, p("variant")),
            elevation=p("elevation"),
            bgcolor=p("bgcolor"),
            shape=ft.RoundedRectangleBorder(radius=p("radius")),
            content=ft.Container(padding=12, width=p("width"), content=ft.Column(body, spacing=4)),
        )

    def generate_code(self) -> str:
        p = self.p
        body = [call("ft.ListTile", ("leading", "ft.Icon(ft.Icons.ALBUM)"),
                     ("title", f"ft.Text({py(p('title'))})"),
                     ("subtitle", 'ft.Text("Subtítulo de ejemplo")'))]
        if p("show_button"):
            body.append(call("ft.Row", '[ft.TextButton("Cancelar"), ft.Button("Aceptar")]',
                             ("alignment", "ft.MainAxisAlignment.END")))
        return call(
            "ft.Card",
            ("variant", f"ft.CardVariant.{p('variant')}"),
            ("elevation", py(p("elevation"))),
            ("bgcolor", py(p("bgcolor"))) if p("bgcolor") else None,
            ("shape", f"ft.RoundedRectangleBorder(radius={py(p('radius'))})"),
            ("content", call("ft.Container", ("padding", "12"), ("width", py(p("width"))),
                             ("content", call("ft.Column", code_list(body), ("spacing", "4"))))),
        )
