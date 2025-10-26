import flet as ft
from abc import ABC, abstractmethod
from typing import Any


class WidgetConfig(ABC):
    """Clase base abstracta para configuración de widgets"""
    
    def __init__(self, name: str, icon: str, description: str):
        self.name = name
        self.icon = icon
        self.description = description
        self.params = {}
    
    @abstractmethod
    def create_controls(self, on_change_callback) -> ft.Column:
        """
        Crea los controles de configuración del widget
        
        Args:
            on_change_callback: Función a llamar cuando cambia un parámetro
            
        Returns:
            ft.Column con los controles de configuración
        """
        pass
    
    @abstractmethod
    def create_preview(self) -> ft.Control:
        """
        Crea la vista previa del widget con los parámetros actuales
        
        Returns:
            ft.Control con la vista previa
        """
        pass
    
    @abstractmethod
    def generate_code(self) -> str:
        """
        Genera el código Flet del widget con los parámetros actuales
        
        Returns:
            String con el código generado
        """
        pass
    
    def _update_param(self, key: str, value: Any, callback):
        """
        Actualiza un parámetro y ejecuta el callback
        
        Args:
            key: Nombre del parámetro
            value: Nuevo valor
            callback: Función a ejecutar después de actualizar
        """
        self.params[key] = value
        callback()
    
    def _create_slider(self, label: str, param_key: str, min_val: float, 
                   max_val: float, on_change_callback) -> ft.Column:
        
        """
        Crea un slider con etiqueta para ajustar un parámetro
        
        Args:
            label: Etiqueta del slider
            param_key: Clave del parámetro en self.params
            min_val: Valor mínimo
            max_val: Valor máximo
            on_change_callback: Callback al cambiar
            
        Returns:
            ft.Column con el slider y su etiqueta
        """
        value_text = ft.Text(
            f"{label}: {self.params[param_key]:.0f}px", 
            size=13, 
            weight=ft.FontWeight.W_500, 
            color="#2d3748"
        )

        def on_slider_change(e):
            new_value = e.control.value
            self._update_param(param_key, new_value, on_change_callback)
            value_text.value = f"{label}: {new_value:.0f}px"
            value_text.update()   

        return ft.Column([
            value_text,
            ft.Slider(
                min=min_val,
                max=max_val,
                value=self.params[param_key],
                on_change=on_slider_change
            ),
        ], spacing=5)
