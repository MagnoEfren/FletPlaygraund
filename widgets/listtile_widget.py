import flet as ft

from core.base_widget import ICON_OPTIONS, Param, WidgetConfig
from services.code_service import call, py

TRAILING = [("none", "Nada"), ("chevron", "Flecha"), ("switch", "Switch"), ("checkbox", "Checkbox"),
            ("menu", "Menú (PopupMenuButton)")]


class ListTileConfig(WidgetConfig):
    PARAMS = [
        Param("title", "Título", "text", "Ana García", group="Textos"),
        Param("subtitle", "Subtítulo", "text", "ana@ejemplo.com", group="Textos"),
        Param("leading", "Icono inicial", "icon", "PERSON", options=ICON_OPTIONS, group="Elementos"),
        Param("trailing", "Elemento final", "select", "chevron", options=TRAILING, group="Elementos"),
        Param("width", "Ancho", "slider", 380.0, 220, 520, unit="px", group="Estilo"),
        Param("bgcolor", "Fondo", "color", None, allow_none=True, group="Estilo"),
        Param("dense", "Denso", "switch", False, group="Estilo"),
        Param("selected", "Seleccionado", "switch", False, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="ListTile", icon=ft.Icons.LIST, category="Listas y datos",
            description="Fila de lista con elemento inicial, título, subtítulo y elemento final. "
                        "La pieza base de menús, contactos y ajustes.",
        )

    def _trailing(self):
        t = self.p("trailing")
        return {
            "none": (None, None),
            "chevron": (ft.Icon(ft.Icons.CHEVRON_RIGHT), "ft.Icon(ft.Icons.CHEVRON_RIGHT)"),
            "switch": (ft.Switch(value=True), "ft.Switch(value=True)"),
            "checkbox": (ft.Checkbox(value=True), "ft.Checkbox(value=True)"),
            "menu": (ft.PopupMenuButton(items=[ft.PopupMenuItem(content="Editar"),
                                               ft.PopupMenuItem(content="Eliminar")]),
                     'ft.PopupMenuButton(items=[\n    ft.PopupMenuItem(content="Editar"),\n'
                     '    ft.PopupMenuItem(content="Eliminar"),\n])'),
        }[t]

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Container(
            width=p("width"), border_radius=12, border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            content=ft.ListTile(
                leading=ft.Icon(self.icon_of(p("leading"))),
                title=p("title"), subtitle=p("subtitle") or None,
                trailing=self._trailing()[0],
                bgcolor=p("bgcolor"), dense=p("dense"), selected=p("selected"),
                on_click=lambda e: print("Tile pulsado"),
            ),
        )

    def generate_code(self) -> str:
        p = self.p
        trailing = self._trailing()[1]
        return call(
            "ft.ListTile",
            ("leading", f"ft.Icon({self.icon_code(p('leading'))})"),
            ("title", py(p("title"))),
            ("subtitle", py(p("subtitle"))) if p("subtitle") else None,
            ("trailing", trailing) if trailing else None,
            ("bgcolor", py(p("bgcolor"))) if p("bgcolor") else None,
            ("dense", "True") if p("dense") else None,
            ("selected", "True") if p("selected") else None,
            ("on_click", 'lambda e: print("Tile pulsado")'),
        )
