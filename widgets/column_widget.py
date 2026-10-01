import flet as ft

from core.base_widget import CROSS_AXIS, MAIN_AXIS, Param, WidgetConfig
from services.code_service import call, code_list, py
from widgets.row_widget import demo_box


class ColumnConfig(WidgetConfig):
    PARAMS = [
        Param("items", "Cantidad de elementos", "slider", 3.0, 1, 8, divisions=7, group="Contenido"),
        Param("height", "Alto del contenedor", "slider", 280.0, 150, 420, unit="px", group="Contenido"),
        Param("spacing", "Spacing", "slider", 10.0, 0, 50, unit="px", group="Distribución"),
        Param("alignment", "alignment (vertical)", "select", "START", options=MAIN_AXIS, group="Distribución"),
        Param("horizontal_alignment", "horizontal_alignment", "select", "CENTER", options=CROSS_AXIS,
              group="Distribución"),
        Param("scroll", "Scroll", "switch", False, group="Distribución"),
    ]

    def __init__(self):
        super().__init__(
            name="Column", icon=ft.Icons.VIEW_AGENDA, category="Layout",
            description="Organiza controles en vertical. Es el complemento de Row: espaciado, "
                        "alineación en ambos ejes y scroll cuando el contenido no cabe.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Container(
            width=260, height=p("height"), padding=16, border_radius=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            content=ft.Column(
                [demo_box(i, width=None if p("horizontal_alignment") == "STRETCH" else 160)
                 for i in range(int(p("items")))],
                spacing=p("spacing"),
                alignment=getattr(ft.MainAxisAlignment, p("alignment")),
                horizontal_alignment=getattr(ft.CrossAxisAlignment, p("horizontal_alignment")),
                scroll=ft.ScrollMode.AUTO if p("scroll") else None,
            ),
        )

    def generate_code(self) -> str:
        p = self.p
        items = [f'ft.Text("Item {i + 1}")' for i in range(int(p("items")))]
        return call(
            "ft.Column",
            ("controls", code_list(items)),
            ("spacing", py(p("spacing"))),
            ("alignment", f"ft.MainAxisAlignment.{p('alignment')}"),
            ("horizontal_alignment", f"ft.CrossAxisAlignment.{p('horizontal_alignment')}"),
            ("scroll", "ft.ScrollMode.AUTO") if p("scroll") else None,
        )
