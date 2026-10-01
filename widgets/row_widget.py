import flet as ft

from core.base_widget import CROSS_AXIS, MAIN_AXIS, Param, WidgetConfig
from services.code_service import call, code_list, py

COLORS = ["#667EEA", "#48BB78", "#F56565", "#ED8936", "#0EA5E9", "#EC4899", "#14B8A6", "#EAB308"]


def demo_box(i: int, width=None) -> ft.Container:
    return ft.Container(
        content=ft.Text(f"Item {i + 1}", color="#FFFFFF", size=14, weight=ft.FontWeight.W_500),
        bgcolor=COLORS[i % len(COLORS)], padding=14, border_radius=10, width=width,
    )


class RowConfig(WidgetConfig):
    PARAMS = [
        Param("items", "Cantidad de elementos", "slider", 3.0, 1, 8, divisions=7, group="Contenido"),
        Param("spacing", "Spacing", "slider", 10.0, 0, 50, unit="px", group="Distribución"),
        Param("alignment", "alignment (eje principal)", "select", "START", options=MAIN_AXIS, group="Distribución"),
        Param("vertical_alignment", "vertical_alignment", "select", "CENTER", options=CROSS_AXIS[:3],
              group="Distribución"),
        Param("wrap", "wrap (salto de línea)", "switch", False, group="Distribución"),
        Param("scroll", "Scroll horizontal", "switch", False, group="Distribución"),
    ]

    def __init__(self):
        super().__init__(
            name="Row", icon=ft.Icons.VIEW_WEEK, category="Layout",
            description="Organiza controles en horizontal. Controla espaciado, alineación en ambos "
                        "ejes, salto de línea automático (wrap) y scroll.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Container(
            width=440, padding=16, border_radius=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            content=ft.Row(
                [demo_box(i) for i in range(int(p("items")))],
                spacing=p("spacing"),
                alignment=getattr(ft.MainAxisAlignment, p("alignment")),
                vertical_alignment=getattr(ft.CrossAxisAlignment, p("vertical_alignment")),
                wrap=p("wrap"),
                run_spacing=p("spacing"),
                scroll=ft.ScrollMode.AUTO if p("scroll") and not p("wrap") else None,
            ),
        )

    def generate_code(self) -> str:
        p = self.p
        items = [f'ft.Text("Item {i + 1}")' for i in range(int(p("items")))]
        return call(
            "ft.Row",
            ("controls", code_list(items)),
            ("spacing", py(p("spacing"))),
            ("alignment", f"ft.MainAxisAlignment.{p('alignment')}"),
            ("vertical_alignment", f"ft.CrossAxisAlignment.{p('vertical_alignment')}"),
            ("wrap", "True") if p("wrap") else None,
            ("scroll", "ft.ScrollMode.AUTO") if p("scroll") and not p("wrap") else None,
        )
