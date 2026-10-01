import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py
from widgets.row_widget import COLORS


class GridViewConfig(WidgetConfig):
    PARAMS = [
        Param("items", "Cantidad de elementos", "slider", 12.0, 1, 40, divisions=39, group="Contenido"),
        Param("runs_count", "Columnas (runs_count)", "slider", 3.0, 1, 6, divisions=5, group="Rejilla"),
        Param("spacing", "spacing", "slider", 8.0, 0, 30, unit="px", group="Rejilla"),
        Param("run_spacing", "run_spacing", "slider", 8.0, 0, 30, unit="px", group="Rejilla"),
        Param("ratio", "child_aspect_ratio", "slider", 1.0, 0.5, 2.0, decimals=2, group="Rejilla"),
    ]

    def __init__(self):
        super().__init__(
            name="GridView", icon=ft.Icons.GRID_VIEW, category="Layout",
            description="Rejilla con scroll y construcción bajo demanda. Ideal para galerías y "
                        "catálogos con muchos elementos.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Container(
            width=380, height=320, padding=8, border_radius=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            content=ft.GridView(
                runs_count=int(p("runs_count")), spacing=p("spacing"), run_spacing=p("run_spacing"),
                child_aspect_ratio=p("ratio"),
                controls=[
                    ft.Container(bgcolor=COLORS[i % len(COLORS)], border_radius=10,
                                 alignment=ft.Alignment.CENTER,
                                 content=ft.Text(str(i + 1), color="#FFFFFF", weight=ft.FontWeight.BOLD))
                    for i in range(int(p("items")))
                ],
            ),
        )

    def generate_code(self) -> str:
        p = self.p
        item = call("ft.Container", ("bgcolor", '"#667EEA"'), ("border_radius", "10"),
                    ("alignment", "ft.Alignment.CENTER"), ("content", "ft.Text(str(i + 1))"))
        return call(
            "ft.GridView",
            ("runs_count", py(int(p("runs_count")))),
            ("spacing", py(p("spacing"))),
            ("run_spacing", py(p("run_spacing"))),
            ("child_aspect_ratio", py(p("ratio"))),
            ("height", "320"),
            ("controls", f"[\n    {item.replace(chr(10), chr(10) + '    ')}\n    for i in range({int(p('items'))})\n]"),
        )
