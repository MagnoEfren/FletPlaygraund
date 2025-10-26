import flet as ft
from core.widget_manager import WidgetManager


class RightPanel:
    """Panel derecho: Vista previa y código generado"""
    
    def __init__(self, page: ft.Page, widget_manager: WidgetManager):
        self.page = page
        self.widget_manager = widget_manager
        
        # Referencias
        self.preview_container = ft.Ref[ft.Container]()
        self.code_container = ft.Ref[ft.Container]()
    
    def update_preview(self):
        """Actualiza la vista previa del widget"""
        self.preview_container.current.content = (
            self.widget_manager.current_widget.create_preview()
        )
    
    def update_code(self):
        """Actualiza el código generado"""
        code_text = self.widget_manager.current_widget.generate_code()
        
        self.code_container.current.content = ft.Column([
            ft.Row([
                ft.Text(
                    "📋 Código Generado", 
                    size=16, 
                    weight=ft.FontWeight.BOLD, 
                    color="#2d3748"
                ),
                ft.IconButton(
                    icon=ft.Icons.COPY,
                    tooltip="Copiar código",
                    on_click=lambda _: self.page.set_clipboard(code_text)
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Text(
                    code_text,
                    size=12,
                    font_family="Courier New",
                    selectable=True,
                    color="#2d3748",
                ),
                bgcolor="#f8f9fa",
                padding=15,
                border_radius=10,
                border=ft.border.all(1, "#e2e8f0"),
            ),
        ], spacing=10)
    
    def build(self) -> ft.Container:
        """Construye el panel derecho"""
        current_widget = self.widget_manager.current_widget
        code_text = current_widget.generate_code()
        
        return ft.Container(
            content=ft.Column([
                # Vista previa
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "👁️ Vista Previa", 
                            size=18, 
                            weight=ft.FontWeight.BOLD, 
                            color="#2d3748"
                        ),
                        ft.Container(
                            ref=self.preview_container,
                            content=current_widget.create_preview(),
                            alignment=ft.alignment.center,
                            padding=30,
                            bgcolor="#f7fafc",
                            border_radius=12,
                            border=ft.border.all(1, "#e2e8f0"),
                            height=300,
                        ),
                    ], spacing=15),
                    padding=20,
                    bgcolor="#ffffff",
                    border_radius=12,
                    border=ft.border.all(1, "#e2e8f0"),
                ),
                
                # Código generado
                ft.Container(
                    ref=self.code_container,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(
                                "📋 Código Generado", 
                                size=16, 
                                weight=ft.FontWeight.BOLD, 
                                color="#2d3748"
                            ),
                            ft.IconButton(
                                icon=ft.Icons.COPY,
                                tooltip="Copiar código",
                                on_click=lambda _: self.page.set_clipboard(code_text)
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(
                            content=ft.Text(
                                code_text,
                                size=12,
                                font_family="Courier New",
                                selectable=True,
                                color="#2d3748",
                            ),
                            bgcolor="#f8f9fa",
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, "#e2e8f0"),
                        ),
                    ], spacing=10),
                    padding=20,
                    bgcolor="#ffffff",
                    border_radius=12,
                    border=ft.border.all(1, "#e2e8f0"),
                    expand=True,
                ),
            ], spacing=20, scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True,
        )