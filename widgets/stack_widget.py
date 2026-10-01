import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, code_list, py

CORNERS = [("top_left", "Arriba izquierda"), ("top_right", "Arriba derecha"),
           ("bottom_left", "Abajo izquierda"), ("bottom_right", "Abajo derecha")]


def _pos(corner: str, m: float) -> dict:
    vert, horiz = corner.split("_")
    return {vert: m, horiz: m}


class StackConfig(WidgetConfig):
    PARAMS = [
        Param("size", "Tamaño del Stack", "slider", 260.0, 160, 400, unit="px", group="Stack"),
        Param("corner", "Posición del elemento superior", "select", "top_right", options=CORNERS,
              group="Posicionamiento"),
        Param("margin", "Distancia al borde", "slider", 12.0, 0, 60, unit="px", group="Posicionamiento"),
        Param("bubble", "Tamaño del círculo", "slider", 56.0, 24, 120, unit="px", group="Posicionamiento"),
        Param("bubble_color", "Color del círculo", "color", "#F56565", group="Posicionamiento"),
        Param("show_label", "Texto centrado", "switch", True, group="Capas"),
    ]

    def __init__(self):
        super().__init__(
            name="Stack", icon=ft.Icons.LAYERS, category="Layout",
            description="Superpone controles uno encima de otro. Con left/top/right/bottom se "
                        "posiciona cada hijo de forma absoluta: ideal para badges, banners y overlays.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        size = p("size")
        layers = [
            ft.Container(
                left=0, top=0, right=0, bottom=0, border_radius=16,
                gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                                           colors=["#667EEA", "#764BA2"]),
            ),
            ft.Container(
                width=p("bubble"), height=p("bubble"), border_radius=p("bubble") / 2,
                bgcolor=p("bubble_color"), alignment=ft.Alignment.CENTER,
                content=ft.Icon(ft.Icons.STAR, color="#FFFFFF"),
                **_pos(p("corner"), p("margin")),
            ),
        ]
        if p("show_label"):
            layers.insert(1, ft.Container(
                left=0, top=0, right=0, bottom=0, alignment=ft.Alignment.CENTER,
                content=ft.Text("Capa base", size=20, color="#FFFFFF", weight=ft.FontWeight.BOLD),
            ))
        return ft.Stack(layers, width=size, height=size)

    def generate_code(self) -> str:
        p = self.p
        vert, horiz = p("corner").split("_")
        layers = [
            call("ft.Container", ("left", "0"), ("top", "0"), ("right", "0"), ("bottom", "0"),
                 ("border_radius", "16"),
                 ("gradient", call("ft.LinearGradient", ("begin", "ft.Alignment.TOP_LEFT"),
                                   ("end", "ft.Alignment.BOTTOM_RIGHT"),
                                   ("colors", '["#667EEA", "#764BA2"]')))),
        ]
        if p("show_label"):
            layers.append(call("ft.Container", ("left", "0"), ("top", "0"), ("right", "0"),
                               ("bottom", "0"), ("alignment", "ft.Alignment.CENTER"),
                               ("content", 'ft.Text("Capa base", size=20, color="#FFFFFF")')))
        layers.append(call(
            "ft.Container",
            ("width", py(p("bubble"))), ("height", py(p("bubble"))),
            ("border_radius", py(p("bubble") / 2)), ("bgcolor", py(p("bubble_color"))),
            ("alignment", "ft.Alignment.CENTER"),
            ("content", 'ft.Icon(ft.Icons.STAR, color="#FFFFFF")'),
            (vert, py(p("margin"))), (horiz, py(p("margin"))),
        ))
        return call("ft.Stack", code_list(layers), ("width", py(p("size"))), ("height", py(p("size"))))
