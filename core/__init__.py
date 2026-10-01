"""Módulo core: clase base de los widgets y gestor central."""
from .base_widget import CATEGORIES, Param, WidgetConfig
from .widget_manager import WidgetManager

__all__ = ["WidgetConfig", "Param", "CATEGORIES", "WidgetManager"]
