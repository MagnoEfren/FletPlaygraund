import flet as ft
from core.widget_manager import WidgetManager
from core.base_widget import WidgetConfig
from typing import Callable


class CenterPanel:
    """Panel central: Información y controles del widget"""
    
    def __init__(self, page: ft.Page, widget_manager: WidgetManager, 
                 update_callback: Callable):
        self.page = page
        self.widget_manager = widget_manager
        self.update_callback = update_callback
        
        # Referencias
        self.widget_info_text = ft.Ref[ft.Text]()
        self.controls_container = ft.Ref[ft.Container]()
    
    def update_widget_info(self, widget_config: WidgetConfig):
        """Actualiza la información del widget"""
        self.widget_info_text.current.value = widget_config.description
        self.controls_container.current.content = widget_config.create_controls(
            self.update_callback
        )
        self.page.update()
    
    def build(self) -> ft.Container:
        """Construye el panel central"""
        current_widget = self.widget_manager.current_widget
        
        return ft.Container(
            content=ft.Column([
                # Información del widget
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "ℹ️ Información", 
                            size=18, 
                            weight=ft.FontWeight.BOLD, 
                            color="#2d3748"
                        ),
                        ft.Text(
                            ref=self.widget_info_text,
                            value=current_widget.description,
                            size=13,
                            color="#718096",
                        ),
                    ], spacing=10),
                    padding=20,
                    bgcolor="#ffffff",
                    border_radius=12,
                    border=ft.border.all(1, "#e2e8f0"),
                ),
                
                # Controles de parámetros
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "⚙️ Parámetros", 
                            size=18, 
                            weight=ft.FontWeight.BOLD, 
                            color="#2d3748"
                        ),
                        ft.Container(
                            ref=self.controls_container,
                            content=current_widget.create_controls(self.update_callback),
                            expand=True,
                        ),
                    ], spacing=15),
                    padding=20,
                    bgcolor="#ffffff",
                    border_radius=12,
                    border=ft.border.all(1, "#e2e8f0"),
                    expand=True,
                ),
            ], spacing=20, scroll=ft.ScrollMode.AUTO),
            width=380,
            padding=20,
            border=ft.border.only(right=ft.BorderSide(1, "#e2e8f0")),
        )