import flet as ft
from core.widget_manager import WidgetManager
from core.base_widget import WidgetConfig
from ui.panels.left_panel import LeftPanel
from ui.panels.center_panel import CenterPanel
from ui.panels.right_panel import RightPanel


class MainLayout:
    """Layout principal de la aplicación"""
    
    def __init__(self, page: ft.Page, widget_manager: WidgetManager):
        self.page = page
        self.widget_manager = widget_manager
        
        # Crear paneles
        self.left_panel = LeftPanel(page, widget_manager, self.on_widget_change)
        self.center_panel = CenterPanel(page, widget_manager, self.update_all)
        self.right_panel = RightPanel(page, widget_manager)
    
    def on_widget_change(self, widget_config: WidgetConfig):
        """Callback cuando se cambia de widget"""
        self.widget_manager.set_current_widget(widget_config)
        self.center_panel.update_widget_info(widget_config)
        self.update_all()
    
    def update_all(self):
        """Actualiza todos los paneles"""
        self.right_panel.update_preview()
        self.right_panel.update_code()
        self.page.update()
    
    def build(self) -> ft.Row:
        """Construye el layout principal"""
        return ft.Row(
            [
                self.left_panel.build(),
                self.center_panel.build(),
                self.right_panel.build(),
            ],
            spacing=0,
            expand=True,
        )