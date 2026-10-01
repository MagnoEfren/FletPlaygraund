import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, code_list, py

DATA = [("Ana", "Diseño", 28, 3200), ("Luis", "Backend", 34, 4100), ("Marta", "Frontend", 25, 3500),
        ("Jorge", "QA", 41, 2900), ("Sofía", "Datos", 30, 4500), ("Pablo", "DevOps", 37, 4300)]
COLS = [("Nombre", False), ("Área", False), ("Edad", True), ("Sueldo", True)]


class DataTableConfig(WidgetConfig):
    PARAMS = [
        Param("rows", "Filas", "slider", 4.0, 1, 6, divisions=5, group="Datos"),
        Param("checkbox", "Columna de selección", "switch", False, group="Datos"),
        Param("sort", "Ordenar por edad", "switch", False, group="Datos"),
        Param("column_spacing", "column_spacing", "slider", 40.0, 10, 80, unit="px", group="Estilo"),
        Param("heading_color", "Fondo del encabezado", "color", None, allow_none=True, group="Estilo"),
        Param("border", "Borde exterior", "switch", True, group="Estilo"),
        Param("lines", "Líneas horizontales", "switch", True, group="Estilo"),
        Param("radius", "Radio de borde", "slider", 10.0, 0, 24, unit="px", group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="DataTable", icon=ft.Icons.TABLE_CHART, category="Listas y datos",
            description="Tabla Material con encabezados, columnas numéricas, selección de filas "
                        "y ordenamiento.",
        )

    def _rows(self):
        rows = DATA[: int(self.p("rows"))]
        if self.p("sort"):
            rows = sorted(rows, key=lambda r: r[2])
        return rows

    def create_preview(self) -> ft.Control:
        p = self.p
        table = ft.DataTable(
            columns=[ft.DataColumn(label=n, numeric=num) for n, num in COLS],
            rows=[ft.DataRow(cells=[ft.DataCell(str(v)) for v in r], selected=i == 0 and p("checkbox"),
                             on_select_change=lambda e: None)
                  for i, r in enumerate(self._rows())],
            show_checkbox_column=p("checkbox"),
            sort_column_index=2 if p("sort") else None, sort_ascending=True,
            column_spacing=p("column_spacing"),
            heading_row_color=p("heading_color"),
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT) if p("border") else None,
            border_radius=p("radius"),
            horizontal_lines=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT) if p("lines") else None,
        )
        return ft.Row([table], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER)

    def generate_code(self) -> str:
        p = self.p
        cols = [f"ft.DataColumn(label={py(n)}{', numeric=True' if num else ''})" for n, num in COLS]
        rows = [call("ft.DataRow", ("cells", code_list([f"ft.DataCell({py(str(v))})" for v in r])))
                for r in self._rows()]
        return call(
            "ft.DataTable",
            ("columns", code_list(cols)),
            ("rows", code_list(rows)),
            ("show_checkbox_column", "True") if p("checkbox") else None,
            ("sort_column_index", "2") if p("sort") else None,
            ("sort_ascending", "True") if p("sort") else None,
            ("column_spacing", py(p("column_spacing"))),
            ("heading_row_color", py(p("heading_color"))) if p("heading_color") else None,
            ("border", "ft.Border.all(1, ft.Colors.OUTLINE_VARIANT)") if p("border") else None,
            ("border_radius", py(p("radius"))),
            ("horizontal_lines", "ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)") if p("lines") else None,
        )
