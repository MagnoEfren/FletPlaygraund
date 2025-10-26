import flet as ft
from core.widget_manager import WidgetManager
from core.base_widget import WidgetConfig
from typing import Callable


class LeftPanel:
    """Panel izquierdo: Lista de widgets disponibles"""
    
    def __init__(self, page: ft.Page, widget_manager: WidgetManager, 
                 on_widget_change: Callable):
        self.page = page
        self.widget_manager = widget_manager
        self.on_widget_change = on_widget_change
        
        # Referencias
        self.search_field = ft.Ref[ft.TextField]()
        self.widgets_list_view = ft.Ref[ft.Column]()
    
    def search_widgets(self, e):
        """Filtra widgets según la búsqueda"""
        query = self.search_field.current.value
        filtered_widgets = (
            self.widget_manager.search_widgets(query) 
            if query 
            else self.widget_manager.get_all_widgets()
        )
        
        self.widgets_list_view.current.controls = [
            self._create_widget_tile(w) for w in filtered_widgets
        ]
        self.page.update()
    
    def _create_widget_tile(self, widget_config: WidgetConfig) -> ft.Container:
        """Crea un tile para un widget"""
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(widget_config.icon, color="#667eea"),
                title=ft.Text(
                    widget_config.name, 
                    size=14, 
                    weight=ft.FontWeight.W_500
                ),
                on_click=lambda _: self.on_widget_change(widget_config),
            ),
            border_radius=8,
            ink=True,
        )
    
    def build(self) -> ft.Container:
        """Construye el panel izquierdo"""
        return ft.Container(
            content=ft.Column([
                # Header
                ft.Row(
                    controls=[
                        
                        ft.Image(
                                width=48,
                                height=48, 
                                src="https://raw.githubusercontent.com/MagnoEfren/FletPlaygraund/refs/heads/main/assets/icon.png",  
                                fit=ft.ImageFit.COVER,
                            ),
                         
                        ft.ShaderMask(
                            blend_mode=ft.BlendMode.SRC_IN,
                            shader=ft.LinearGradient(
                                colors=["#7edf26", "#0148e2", "#00fbe8"],
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                            ),
                            content=ft.Text(
                                "Flet Widgets\nPlayground",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.LEFT,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                            
                # Buscador
                ft.TextField(
                    ref=self.search_field,
                    hint_text="Buscar widget...",
                    prefix_icon=ft.Icons.SEARCH,
                    border_radius=10,
                    filled=True,
                    on_change=self.search_widgets,
                ),
                
                ft.Divider(height=20),
                
                # Lista de widgets
                ft.Container(
                    content=ft.Column(
                        ref=self.widgets_list_view,
                        controls=[
                            self._create_widget_tile(w) 
                            for w in self.widget_manager.get_all_widgets()
                        ],
                        spacing=5,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    expand=True,
                ),
            ], spacing=10),
            #expand=1,
            padding=20,
            border_radius=12,
            bgcolor="#ffffff",
            border=ft.border.all(1, "#e2e8f0"),
        )
