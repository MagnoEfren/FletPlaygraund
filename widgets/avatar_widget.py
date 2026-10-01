import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py

KINDS = [("initials", "Iniciales"), ("icon", "Icono"), ("image", "Foto")]
PHOTO = "https://i.pravatar.cc/300?img=12"


class CircleAvatarConfig(WidgetConfig):
    PARAMS = [
        Param("kind", "Contenido", "select", "initials", options=KINDS, group="Contenido"),
        Param("initials", "Iniciales", "text", "ME", group="Contenido"),
        Param("radius", "Radio", "slider", 48.0, 16, 120, unit="px", group="Estilo"),
        Param("bgcolor", "Fondo", "color", "#667EEA", group="Estilo"),
        Param("color", "Color del contenido", "color", "#FFFFFF", group="Estilo"),
        Param("online", "Indicador 'en línea' (Badge)", "switch", True, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="CircleAvatar", icon=ft.Icons.ACCOUNT_CIRCLE, category="Texto y media",
            description="Avatar circular para usuarios: iniciales, icono o foto, con indicador "
                        "de estado usando ft.Badge.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        kind = p("kind")
        content = (ft.Text(p("initials"), size=p("radius") * 0.6, weight=ft.FontWeight.BOLD)
                   if kind == "initials" else
                   ft.Icon(ft.Icons.PERSON, size=p("radius")) if kind == "icon" else None)
        return ft.CircleAvatar(
            content=content,
            foreground_image_src=PHOTO if kind == "image" else None,
            radius=p("radius"), bgcolor=p("bgcolor"), color=p("color"),
            badge=ft.Badge(small_size=p("radius") * 0.4, bgcolor="#48BB78",
                           alignment=ft.Alignment.BOTTOM_RIGHT) if p("online") else None,
        )

    def generate_code(self) -> str:
        p = self.p
        kind = p("kind")
        content = (f'ft.Text({py(p("initials"))}, size={py(p("radius") * 0.6)}, weight=ft.FontWeight.BOLD)'
                   if kind == "initials" else
                   f"ft.Icon(ft.Icons.PERSON, size={py(p('radius'))})" if kind == "icon" else None)
        return call(
            "ft.CircleAvatar",
            ("content", content) if content else None,
            ("foreground_image_src", py(PHOTO)) if kind == "image" else None,
            ("radius", py(p("radius"))),
            ("bgcolor", py(p("bgcolor"))),
            ("color", py(p("color"))),
            ("badge", f'ft.Badge(small_size={py(p("radius") * 0.4)}, bgcolor="#48BB78", '
                      f"alignment=ft.Alignment.BOTTOM_RIGHT)") if p("online") else None,
        )
