"""Gestor centralizado: registro, búsqueda, filtros y widget actual."""
from __future__ import annotations

from core.base_widget import CATEGORIES, WidgetConfig

FAVORITES = "Favoritos"
ALL = "Todos"


class WidgetManager:
    def __init__(self):
        self.widgets: dict[str, WidgetConfig] = {}
        self._register_widgets()
        self.current_widget: WidgetConfig = self.widgets["Container"]

    def _register_widgets(self) -> None:
        from widgets import ALL_WIDGETS
        for cls in ALL_WIDGETS:
            widget = cls()
            if widget.name in self.widgets:
                raise ValueError(f"Widget duplicado: {widget.name}")
            self.widgets[widget.name] = widget

    # -------- consultas
    def names(self) -> set[str]:
        return set(self.widgets)

    def get_widget(self, name: str) -> WidgetConfig:
        return self.widgets.get(name, self.widgets["Container"])

    def get_all_widgets(self) -> list[WidgetConfig]:
        return list(self.widgets.values())

    def search_widgets(self, query: str) -> list[WidgetConfig]:
        return [w for w in self.widgets.values() if w.matches(query)]

    def filter(self, query: str = "", category: str = ALL,
               favorites: set[str] | None = None) -> list[WidgetConfig]:
        """Búsqueda por texto + filtro por categoría o favoritos."""
        favorites = favorites or set()
        result = []
        for w in self.widgets.values():
            if category == FAVORITES and w.name not in favorites:
                continue
            if category not in (ALL, FAVORITES) and w.category != category:
                continue
            if w.matches(query):
                result.append(w)
        return result

    def categories(self) -> list[str]:
        used = {w.category for w in self.widgets.values()}
        return [ALL, FAVORITES] + [c for c in CATEGORIES if c in used]

    def count_by_category(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for w in self.widgets.values():
            counts[w.category] = counts.get(w.category, 0) + 1
        return counts

    def set_current_widget(self, widget: WidgetConfig | str) -> None:
        self.current_widget = self.get_widget(widget) if isinstance(widget, str) else widget
