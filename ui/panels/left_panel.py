"""
Panel izquierdo: buscador, filtros por categoría, favoritos y lista de widgets.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

import theme
from core.widget_manager import ALL, FAVORITES

if TYPE_CHECKING:
    from ui.layout import MainLayout


class LeftPanel(ft.Container):
    def __init__(self, app: "MainLayout", width=theme.SIDEBAR_W, expand=None):
        super().__init__(
            width=width,
            expand=expand,
            padding=theme.PAD,
            bgcolor=theme.PANEL_BG,
            border_radius=theme.RADIUS,
            border=ft.Border.all(1, theme.BORDER),
        )
        self.app = app
        st = app.state

        self.search_tf = ft.TextField(
            value=st.query,
            hint_text="Buscar…  Ctrl+K",
            prefix_icon=ft.Icons.SEARCH,
            dense=True,
            filled=True,
            text_size=14,
            border=ft.OutlineInputBorder(border_radius=theme.RADIUS_SM,
                                         side=ft.BorderSide(0, ft.Colors.TRANSPARENT)),
            on_change=self._on_search,
        )
        self.chips_row = ft.Row(spacing=6, scroll=ft.ScrollMode.AUTO)
        self.count_txt = ft.Text(size=12, color=theme.TEXT_MUTED)
        self.list_view = ft.ListView(expand=True, spacing=4)

        self.content = ft.Column(
            expand=True,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.search_tf,
                self.chips_row,
                self.count_txt,
                self.list_view,
            ],
        )
        self.refrescar()

    # ------------------------------------------------------------ render
    def refrescar(self) -> None:
        self._render_chips()
        self._render_list()

    def _render_chips(self) -> None:
        st = self.app.state
        counts = self.app.manager.count_by_category()
        chips = []
        for cat in self.app.manager.categories():
            if cat == ALL:
                n = len(self.app.manager.widgets)
            elif cat == FAVORITES:
                n = len(st.favorites)
            else:
                n = counts.get(cat, 0)
            chips.append(
                ft.Chip(
                    label=f"{cat} · {n}",
                    leading=ft.Icon(ft.Icons.STAR, size=16) if cat == FAVORITES else None,
                    selected=st.category == cat,
                    show_checkmark=False,
                    data=cat,
                    on_select=self._on_category,
                )
            )
        self.chips_row.controls = chips

    def _render_list(self) -> None:
        st = self.app.state
        items = self.app.manager.filter(st.query, st.category, st.favorites)
        self.count_txt.value = f"{len(items)} de {len(self.app.manager.widgets)} widgets"
        if not items:
            self.list_view.controls = [self._empty_state()]
            return
        self.list_view.controls = [self._tile(w) for w in items]

    def _tile(self, w) -> ft.Container:
        st = self.app.state
        selected = w.name == st.current_widget
        fav = w.name in st.favorites
        return ft.Container(
            data=w.name,
            on_click=self._on_pick,
            ink=True,
            border_radius=theme.RADIUS_SM,
            padding=ft.Padding.only(left=12, right=4, top=6, bottom=6),
            bgcolor=theme.SELECTED_BG if selected else None,
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(w.icon, size=20,
                            color=theme.SELECTED_TEXT if selected else theme.PRIMARY),
                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            ft.Text(w.name, size=14, weight=ft.FontWeight.W_600,
                                    color=theme.SELECTED_TEXT if selected else theme.TEXT,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Text(w.category, size=11, color=theme.TEXT_MUTED),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.STAR if fav else ft.Icons.STAR_BORDER,
                        icon_color=ft.Colors.AMBER if fav else theme.TEXT_MUTED,
                        icon_size=18,
                        tooltip="Quitar de favoritos" if fav else "Agregar a favoritos",
                        data=w.name,
                        on_click=self._on_fav,
                    ),
                ],
            ),
        )

    def _empty_state(self) -> ft.Control:
        st = self.app.state
        msg = ("Aún no tienes favoritos.\nToca la ☆ de un widget para guardarlo aquí."
               if st.category == FAVORITES and not st.query else
               "Ningún widget coincide con tu búsqueda.")
        return ft.Container(
            padding=24,
            content=ft.Column(
                [ft.Icon(ft.Icons.SEARCH_OFF, size=40, color=theme.TEXT_MUTED),
                 ft.Text(msg, text_align=ft.TextAlign.CENTER, color=theme.TEXT_MUTED, size=13)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    # ------------------------------------------------------------ eventos
    def _on_search(self, e: ft.Event) -> None:
        self.app.state.query = e.control.value or ""
        self._render_list()
        self.app.safe_update(self)

    def _on_category(self, e: ft.Event) -> None:
        self.app.state.category = e.control.data
        self.refrescar()
        self.app.safe_update(self)

    async def _on_pick(self, e: ft.Event) -> None:
        await self.app.select_widget(e.control.data)

    async def _on_fav(self, e: ft.Event) -> None:
        await self.app.toggle_favorite(e.control.data)

    async def focus_search(self) -> None:
        try:
            await self.search_tf.focus()
        except Exception:
            pass
