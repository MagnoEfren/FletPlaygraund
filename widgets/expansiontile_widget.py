import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, code_list, py

AFFINITY = [("TRAILING", "Flecha a la derecha"), ("LEADING", "Flecha a la izquierda")]


class ExpansionTileConfig(WidgetConfig):
    PARAMS = [
        Param("title", "Título", "text", "Preguntas frecuentes", group="Textos"),
        Param("subtitle", "Subtítulo", "text", "Toca para expandir", group="Textos"),
        Param("children", "Cantidad de hijos", "slider", 3.0, 1, 6, divisions=5, group="Contenido"),
        Param("expanded", "Expandido al inicio", "switch", True, group="Contenido"),
        Param("affinity", "Posición de la flecha", "select", "TRAILING", options=AFFINITY, group="Estilo"),
        Param("bgcolor", "Fondo expandido", "color", None, allow_none=True, group="Estilo"),
        Param("width", "Ancho", "slider", 400.0, 240, 520, unit="px", group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="ExpansionTile", icon=ft.Icons.EXPAND_CIRCLE_DOWN, category="Listas y datos",
            doc_slug="expansiontile",
            description="Fila que se expande para mostrar más controles. Ideal para FAQs, "
                        "acordeones y menús anidados.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Container(
            width=p("width"),
            content=ft.ExpansionTile(
                title=p("title"), subtitle=p("subtitle") or None,
                leading=ft.Icon(ft.Icons.HELP_OUTLINE),
                expanded=p("expanded"),
                affinity=getattr(ft.TileAffinity, p("affinity")),
                bgcolor=p("bgcolor"),
                controls=[ft.ListTile(title=f"Respuesta {i + 1}") for i in range(int(p("children")))],
            ),
        )

    def generate_code(self) -> str:
        p = self.p
        kids = [f'ft.ListTile(title="Respuesta {i + 1}")' for i in range(int(p("children")))]
        return call(
            "ft.ExpansionTile",
            ("title", py(p("title"))),
            ("subtitle", py(p("subtitle"))) if p("subtitle") else None,
            ("leading", "ft.Icon(ft.Icons.HELP_OUTLINE)"),
            ("expanded", "True") if p("expanded") else None,
            ("affinity", f"ft.TileAffinity.{p('affinity')}"),
            ("bgcolor", py(p("bgcolor"))) if p("bgcolor") else None,
            ("controls", code_list(kids)),
        )
