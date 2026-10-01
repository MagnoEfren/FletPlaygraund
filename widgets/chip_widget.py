import flet as ft

from core.base_widget import ICON_OPTIONS, Param, WidgetConfig
from services.code_service import call, py


class ChipConfig(WidgetConfig):
    PARAMS = [
        Param("label", "Texto", "text", "Python", group="Contenido"),
        Param("show_leading", "Icono inicial", "switch", True, group="Contenido"),
        Param("leading", "Icono", "icon", "STAR", options=ICON_OPTIONS, group="Contenido"),
        Param("selectable", "Seleccionable (filtro)", "switch", True, group="Comportamiento"),
        Param("selected", "Seleccionado", "switch", True, group="Comportamiento"),
        Param("show_checkmark", "Mostrar check", "switch", True, group="Comportamiento"),
        Param("deletable", "Botón de borrar", "switch", False, group="Comportamiento"),
        Param("bgcolor", "Fondo", "color", None, allow_none=True, group="Estilo"),
        Param("selected_color", "Fondo seleccionado", "color", None, allow_none=True, group="Estilo"),
        Param("elevation", "Elevación", "slider", 0.0, 0, 10, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="Chip", icon=ft.Icons.LABEL, category="Listas y datos",
            description="Elemento compacto para etiquetas, filtros o acciones. Puede ser "
                        "seleccionable (on_select) y borrable (on_delete).",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        sel = p("selectable")
        return ft.Chip(
            label=p("label"),
            leading=ft.Icon(self.icon_of(p("leading"))) if p("show_leading") else None,
            selected=p("selected") if sel else False,
            show_checkmark=p("show_checkmark"),
            bgcolor=p("bgcolor"), selected_color=p("selected_color"),
            elevation=p("elevation") or None,
            on_select=(lambda e: None) if sel else None,
            on_delete=(lambda e: print("Borrar")) if p("deletable") else None,
        )

    def generate_code(self) -> str:
        p = self.p
        sel = p("selectable")
        return call(
            "ft.Chip",
            ("label", py(p("label"))),
            ("leading", f"ft.Icon({self.icon_code(p('leading'))})") if p("show_leading") else None,
            ("selected", py(p("selected"))) if sel else None,
            ("show_checkmark", "False") if not p("show_checkmark") else None,
            ("bgcolor", py(p("bgcolor"))) if p("bgcolor") else None,
            ("selected_color", py(p("selected_color"))) if p("selected_color") else None,
            ("elevation", py(p("elevation"))) if p("elevation") else None,
            ("on_select", "lambda e: print(e.control.selected)") if sel else None,
            ("on_delete", 'lambda e: print("Borrar")') if p("deletable") else None,
        )
