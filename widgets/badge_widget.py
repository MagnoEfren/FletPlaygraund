import flet as ft

from core.base_widget import ICON_OPTIONS, Param, WidgetConfig
from services.code_service import call, py


class BadgeConfig(WidgetConfig):
    PARAMS = [
        Param("label", "Etiqueta", "text", "3", group="Badge"),
        Param("label_visible", "Mostrar etiqueta (si no: punto)", "switch", True, group="Badge"),
        Param("bgcolor", "Fondo", "color", "#F56565", group="Badge"),
        Param("text_color", "Color del texto", "color", "#FFFFFF", group="Badge"),
        Param("large_size", "large_size", "slider", 20.0, 12, 40, unit="px", group="Badge"),
        Param("icon", "Icono base", "icon", "NOTIFICATIONS", options=ICON_OPTIONS, group="Control"),
        Param("icon_size", "Tamaño del icono", "slider", 48.0, 20, 120, unit="px", group="Control"),
    ]

    def __init__(self):
        super().__init__(
            name="Badge", icon=ft.Icons.NOTIFICATIONS_ACTIVE, category="Texto y media",
            description="Marca de notificación que se adjunta a cualquier control mediante su "
                        "propiedad badge=. Puede mostrar un número o un simple punto.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Icon(
            self.icon_of(p("icon")), size=p("icon_size"),
            badge=ft.Badge(label=p("label"), label_visible=p("label_visible"),
                           bgcolor=p("bgcolor"), text_color=p("text_color"),
                           large_size=p("large_size")),
        )

    def generate_code(self) -> str:
        p = self.p
        return call(
            "ft.Icon", self.icon_code(p("icon")),
            ("size", py(p("icon_size"))),
            ("badge", call("ft.Badge",
                           ("label", py(p("label"))),
                           ("label_visible", "False") if not p("label_visible") else None,
                           ("bgcolor", py(p("bgcolor"))),
                           ("text_color", py(p("text_color"))),
                           ("large_size", py(p("large_size"))))),
        )
