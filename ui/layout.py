import flet as ft
from core.widget_manager import WidgetManager
from core.base_widget import WidgetConfig
from ui.panels.left_panel import LeftPanel
from ui.panels.center_panel import CenterPanel
from ui.panels.right_panel import RightPanel


class MainLayout:
    """Layout principal de la aplicación (responsive)"""
    
    def __init__(self, page: ft.Page, widget_manager: WidgetManager):
        self.page = page
        self.widget_manager = widget_manager
        
        # Crear paneles
        self.left_panel = LeftPanel(page, widget_manager, self.on_widget_change)
        self.center_panel = CenterPanel(page, widget_manager, self.update_all)
        self.right_panel = RightPanel(page, widget_manager)

        # Detectar cambios de tamaño
        self.page.on_resize = self.on_resize

        # Layout actual (se define en build)
        self.layout_container = None

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

    # -----------------------------------------
    # 💡 NUEVO: comportamiento responsive
    # -----------------------------------------
    def on_resize(self, e: ft.ControlEvent):
        """Detecta cambios de tamaño y re-renderiza el layout"""
        self.update_layout(e.page.width)

    def update_layout(self, width: float):
        """Cambia entre diseño horizontal (desktop) y vertical (móvil)"""
        if width < 800:
            # Diseño vertical para pantallas pequeñas
            self.layout_container.controls = [
                self.left_panel.build(),
                self.center_panel.build(),
                self.right_panel.build(),
            ]
            self.layout_container.direction = ft.Column
        else:
            # Diseño horizontal para pantallas grandes
            self.layout_container.controls = [
                self.left_panel.build(),
                self.center_panel.build(),
                self.right_panel.build(),
            ]
            self.layout_container.direction = ft.Row

        self.page.update()

    def build(self):
        """Construye el layout principal"""
        # Por defecto, se asume escritorio
        self.layout_container = ft.ResponsiveRow(
            controls=[
                ft.Container(
                   # expand=True,
                    content=self.left_panel.build(),
                    col={"xs": 12, "sm": 12, "md": 3, "lg": 3},
                    bgcolor=ft.Colors.SURFACE,
                    padding=10,
                ),
                ft.Container(
                  # expand=True,
                    content=self.center_panel.build(),
                    col={"xs": 12, "sm": 12, "md": 4, "lg": 3},
                    bgcolor=ft.Colors.SURFACE,
                    padding=10,
                ),
                ft.Container(
                 #  expand=True,
                    content=self.right_panel.build(),
                    col={"xs": 12, "sm": 12, "md": 5, "lg":6},
                    bgcolor=ft.Colors.SURFACE,
                    padding=10,
                ),
            ],
            expand=True,
            spacing=10,
            run_spacing=10,
        )

        return self.layout_container
