import flet as ft

from core.base_widget import ICON_OPTIONS, Param, WidgetConfig
from services.code_service import call, py

STYLES = [("standard", "Estándar"), ("filled", "Relleno"), ("outlined", "Con borde")]


class IconButtonConfig(WidgetConfig):
    PARAMS = [
        Param("icon", "Icono", "icon", "FAVORITE", options=ICON_OPTIONS, group="Icono"),
        Param("icon_size", "Tamaño", "slider", 32.0, 16, 72, unit="px", group="Icono"),
        Param("icon_color", "Color del icono", "color", None, allow_none=True, group="Icono"),
        Param("look", "Estilo", "select", "filled", options=STYLES, group="Estilo"),
        Param("bgcolor", "Fondo (estilo relleno)", "color", "#667EEA", group="Estilo"),
        Param("tooltip", "Tooltip", "text", "Me gusta", group="Estilo"),
        Param("toggle", "Modo alternable (selected)", "switch", False, group="Estado"),
        Param("selected", "Seleccionado", "switch", False, group="Estado"),
    ]

    def __init__(self):
        super().__init__(
            name="IconButton", icon=ft.Icons.TOUCH_APP, category="Botones",
            description="Botón que solo muestra un icono. Admite tooltip, estilos relleno/borde "
                        "y modo alternable con selected + selected_icon.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        look = p("look")
        style = None
        if look == "outlined":
            style = ft.ButtonStyle(side=ft.BorderSide(1, ft.Colors.OUTLINE))
        return ft.IconButton(
            icon=self.icon_of(p("icon")),
            selected_icon=ft.Icons.CHECK_CIRCLE if p("toggle") else None,
            selected=p("selected") if p("toggle") else None,
            icon_size=p("icon_size"),
            icon_color=p("icon_color"),
            bgcolor=p("bgcolor") if look == "filled" else None,
            tooltip=p("tooltip") or None,
            style=style,
        )

    def generate_code(self) -> str:
        p = self.p
        look = p("look")
        return call(
            "ft.IconButton",
            ("icon", self.icon_code(p("icon"))),
            ("selected_icon", "ft.Icons.CHECK_CIRCLE") if p("toggle") else None,
            ("selected", py(p("selected"))) if p("toggle") else None,
            ("icon_size", py(p("icon_size"))),
            ("icon_color", py(p("icon_color"))) if p("icon_color") else None,
            ("bgcolor", py(p("bgcolor"))) if look == "filled" else None,
            ("tooltip", py(p("tooltip"))) if p("tooltip") else None,
            ("style", "ft.ButtonStyle(side=ft.BorderSide(1, ft.Colors.OUTLINE))") if look == "outlined" else None,
        )
