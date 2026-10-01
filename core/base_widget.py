"""
core/base_widget.py — Clase base de todos los widgets del playground.

Novedad v2: los parámetros se DECLARAN (lista PARAMS de objetos Param) y la
interfaz de controles (sliders, selects, switches, colores, texto, iconos)
se genera sola. Cada widget solo implementa:

    create_preview()  -> el control real de Flet con los parámetros actuales
    generate_code()   -> el código equivalente

Si un widget necesita controles a medida puede sobrescribir create_controls().
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable

import flet as ft

from services import code_service

# Categorías (el orden es el que se muestra en los filtros)
CATEGORIES = ["Layout", "Texto y media", "Botones", "Entrada", "Listas y datos", "Feedback"]


@dataclass
class Param:
    """Describe un parámetro editable."""
    key: str
    label: str
    kind: str                     # slider | select | switch | color | text | icon
    default: Any
    min: float = 0
    max: float = 100
    divisions: int | None = None
    unit: str = ""
    decimals: int = 0
    options: list[tuple[str, str]] = field(default_factory=list)   # (valor, etiqueta)
    group: str = "General"
    allow_none: bool = False      # color: permite "Tema" (None = color del tema)


class WidgetConfig(ABC):
    """Clase base abstracta para la configuración de un widget."""

    #: Lista de Param. Se define en cada subclase.
    PARAMS: list[Param] = []

    def __init__(self, name: str, icon, description: str,
                 category: str = "Layout", doc_slug: str | None = None):
        self.name = name
        self.icon = icon
        self.description = description
        self.category = category
        self.doc_slug = doc_slug or name.lower()
        self.params: dict[str, Any] = {}
        self.reset()

    # ------------------------------------------------------------ estado
    def reset(self) -> None:
        """Restablece todos los parámetros a su valor por defecto."""
        self.params = {p.key: p.default for p in self.PARAMS}

    def p(self, key: str):
        """Atajo: valor actual de un parámetro."""
        return self.params[key]

    def _update_param(self, key: str, value: Any, callback: Callable[[], None]) -> None:
        self.params[key] = value
        callback()

    # ------------------------------------------------------------ UI
    def create_controls(self, on_change_callback: Callable[[], None]) -> ft.Control:
        """Genera automáticamente los controles a partir de PARAMS, agrupados."""
        from ui.components.param_controls import build_param_groups   # evita import circular
        return build_param_groups(self, on_change_callback)

    @abstractmethod
    def create_preview(self) -> ft.Control:
        """Devuelve el control con los parámetros actuales."""

    @abstractmethod
    def generate_code(self) -> str:
        """Devuelve el código Flet equivalente a la vista previa."""

    # ------------------------------------------------------------ código
    def generate_full_app(self) -> str:
        """El snippet envuelto en una app completa y ejecutable (ft.run)."""
        return code_service.wrap_app(self.generate_code(), self.name)

    @property
    def docs_url(self) -> str:
        from theme import DOCS_URL
        return DOCS_URL.format(slug=self.doc_slug)

    # ------------------------------------------------------------ helpers
    @staticmethod
    def icon_of(name: str):
        """'STAR' -> ft.Icons.STAR (con respaldo seguro)."""
        return getattr(ft.Icons, name, ft.Icons.HELP_OUTLINE)

    @staticmethod
    def icon_code(name: str) -> str:
        return f"ft.Icons.{name}"

    def matches(self, query: str) -> bool:
        q = query.strip().lower()
        if not q:
            return True
        return q in self.name.lower() or q in self.description.lower() or q in self.category.lower()


# Opciones reutilizables ------------------------------------------------------
ICON_OPTIONS = [
    ("STAR", "Estrella"), ("FAVORITE", "Corazón"), ("HOME", "Casa"),
    ("SETTINGS", "Ajustes"), ("PERSON", "Persona"), ("SEND", "Enviar"),
    ("DELETE", "Borrar"), ("SHARE", "Compartir"), ("EDIT", "Editar"),
    ("ADD", "Agregar"), ("MAIL", "Correo"), ("NOTIFICATIONS", "Campana"),
]

MAIN_AXIS = [
    ("START", "Start"), ("CENTER", "Center"), ("END", "End"),
    ("SPACE_BETWEEN", "Space between"), ("SPACE_AROUND", "Space around"),
    ("SPACE_EVENLY", "Space evenly"),
]

CROSS_AXIS = [("START", "Start"), ("CENTER", "Center"), ("END", "End"), ("STRETCH", "Stretch")]

FONT_WEIGHTS = [
    ("NORMAL", "Normal"), ("W_300", "Light (300)"), ("W_500", "Medium (500)"),
    ("W_600", "SemiBold (600)"), ("BOLD", "Bold"), ("W_900", "Black (900)"),
]
