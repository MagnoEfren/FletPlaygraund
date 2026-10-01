import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, code_list, py

SEGMENTS = [("dia", "Día", "CALENDAR_VIEW_DAY"), ("semana", "Semana", "CALENDAR_VIEW_WEEK"),
            ("mes", "Mes", "CALENDAR_VIEW_MONTH"), ("anio", "Año", "CALENDAR_TODAY")]


class SegmentedButtonConfig(WidgetConfig):
    PARAMS = [
        Param("count", "Cantidad de segmentos", "slider", 3.0, 2, 4, divisions=2, group="Segmentos"),
        Param("show_icons", "Iconos en los segmentos", "switch", True, group="Segmentos"),
        Param("multiple", "Selección múltiple", "switch", False, group="Selección"),
        Param("allow_empty", "Permitir vacío", "switch", False, group="Selección"),
        Param("show_selected_icon", "Check en seleccionado", "switch", True, group="Selección"),
        Param("vertical", "Dirección vertical", "switch", False, group="Selección"),
    ]

    def __init__(self):
        super().__init__(
            name="SegmentedButton", icon=ft.Icons.VIEW_COLUMN, category="Botones",
            description="Grupo de opciones relacionadas (selección única o múltiple). Perfecto "
                        "para filtros y cambiar vistas. ¡Pruébalo en la vista previa!",
        )

    def _segments(self):
        return SEGMENTS[: int(self.p("count"))]

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.SegmentedButton(
            segments=[ft.Segment(value=v, label=lbl,
                                 icon=getattr(ft.Icons, ic) if p("show_icons") else None)
                      for v, lbl, ic in self._segments()],
            selected=[self._segments()[0][0]],
            allow_multiple_selection=p("multiple"),
            allow_empty_selection=p("allow_empty"),
            show_selected_icon=p("show_selected_icon"),
            direction=ft.Axis.VERTICAL if p("vertical") else None,
        )

    def generate_code(self) -> str:
        p = self.p
        segs = [call("ft.Segment", ("value", py(v)), ("label", py(lbl)),
                     ("icon", f"ft.Icons.{ic}") if p("show_icons") else None)
                for v, lbl, ic in self._segments()]
        return call(
            "ft.SegmentedButton",
            ("segments", code_list(segs)),
            ("selected", f"[{py(self._segments()[0][0])}]"),
            ("allow_multiple_selection", "True") if p("multiple") else None,
            ("allow_empty_selection", "True") if p("allow_empty") else None,
            ("show_selected_icon", "False") if not p("show_selected_icon") else None,
            ("direction", "ft.Axis.VERTICAL") if p("vertical") else None,
            ("on_change", "lambda e: print(e.control.selected)"),
        )
