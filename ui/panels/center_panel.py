"""
Panel central: cabecera del widget (info, docs, reset) + parámetros editables.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

import theme

if TYPE_CHECKING:
    from ui.layout import MainLayout


class CenterPanel(ft.Container):
    def __init__(self, app: "MainLayout", width=theme.PARAMS_W, expand=None):
        super().__init__(
            width=width,
            expand=expand,
            padding=theme.PAD,
            bgcolor=theme.PANEL_BG,
            border_radius=theme.RADIUS,
            border=ft.Border.all(1, theme.BORDER),
        )
        self.app = app
        self.header_box = ft.Container()
        self.params_view = ft.ListView(expand=True, spacing=theme.GAP, padding=ft.Padding.only(right=6))
        self.content = ft.Column(
            expand=True,
            spacing=theme.GAP,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[self.header_box, self.params_view],
        )
        self.refrescar()

    def refrescar(self) -> None:
        """Reconstruye cabecera y parámetros del widget actual."""
        w = self.app.manager.current_widget
        self.header_box.content = ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(
                            width=44, height=44, border_radius=12,
                            bgcolor=theme.SELECTED_BG, alignment=ft.Alignment.CENTER,
                            content=ft.Icon(w.icon, color=theme.SELECTED_TEXT),
                        ),
                        ft.Column(
                            expand=True, spacing=0,
                            controls=[
                                ft.Text(w.name, size=20, weight=ft.FontWeight.BOLD, color=theme.TEXT,
                                        max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(w.category, size=12, color=theme.PRIMARY,
                                        weight=ft.FontWeight.W_500),
                            ],
                        ),
                    ],
                ),
                ft.Text(w.description, size=13, color=theme.TEXT_MUTED),
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.OutlinedButton(
                            content="Restablecer", icon=ft.Icons.RESTART_ALT,
                            on_click=self._on_reset,
                        ),
                        ft.TextButton(
                            content="Docs", icon=ft.Icons.MENU_BOOK, tooltip="Abrir la documentación oficial",
                            # Client Action: abre la URL dentro del gesto (funciona en iOS Safari)
                            action=ft.OpenUrl(w.docs_url, target=ft.UrlTarget.BLANK),
                        ),
                    ],
                ),
                ft.Divider(height=1, color=theme.BORDER),
            ],
        )
        self.params_view.controls = [
            ft.Text("Parámetros", size=15, weight=ft.FontWeight.BOLD, color=theme.TEXT),
            w.create_controls(self.app.on_params_changed),
        ]

    def _on_reset(self, e: ft.Event) -> None:
        self.app.reset_current_widget()
