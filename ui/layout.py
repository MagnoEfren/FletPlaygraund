"""
ui/layout.py — Orquestador de la app.

Layout responsivo con tres modos (se reconstruye SOLO al cruzar un punto de quiebre):

  desktop (>= 1100 px)  │ Widgets │ Parámetros │ [Vista previa | Código] (pestañas) │
  tablet  (700–1099 px) │ barra inferior: Widgets · Editor (parámetros + vista previa) · Código
  mobile  (< 700 px)    │ barra inferior: Widgets · Editor (vista previa arriba, parámetros abajo) · Código
"""
from __future__ import annotations

import flet as ft

import theme
from core.widget_manager import WidgetManager
from models.app_state import AppState
from services import prefs_service
from ui.components.feedback import show_snack
from ui.panels.center_panel import CenterPanel
from ui.panels.left_panel import LeftPanel
from ui.panels.right_panel import CodePanel, PreviewPanel

TAB_WIDGETS, TAB_EDITOR, TAB_CODE = 0, 1, 2


class MainLayout:
    def __init__(self, page: ft.Page, widget_manager: WidgetManager):
        self.page = page
        self.manager = widget_manager
        self.state = AppState()

        # Paneles vivos (se recrean al cambiar de layout; pueden ser None)
        self.left_panel: LeftPanel | None = None
        self.center_panel: CenterPanel | None = None
        self.preview_panel: PreviewPanel | None = None
        self.code_panel: CodePanel | None = None

        # Pestaña activa del panel derecho en escritorio: "preview" | "code"
        self.desktop_tab: str = "preview"
        self.desktop_tabs: ft.SegmentedButton | None = None

        self.theme_btn = ft.IconButton(on_click=self._on_toggle_theme)
        self.count_badge = ft.Container(
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            border_radius=20,
            bgcolor=theme.SELECTED_BG,
            content=ft.Text(f"{len(self.manager.widgets)} widgets", size=12,
                            color=theme.SELECTED_TEXT, weight=ft.FontWeight.W_600),
        )
        self.title_txt = ft.Text(theme.APP_NAME, size=17, weight=ft.FontWeight.BOLD)
        self.version_txt = ft.Text(f"v{theme.APP_VERSION} · Flet 1.0", size=11, color=theme.TEXT_MUTED)
        self.header = self._build_header()
        self.body = ft.Container(expand=True, padding=theme.GAP)
        self.root = ft.Column(expand=True, spacing=0, controls=[self.header, self.body])

        page.on_resize = self._on_resize
        page.on_keyboard_event = self._on_key
        page.on_platform_brightness_change = self._on_brightness

    # ================================================================ build
    def build(self) -> ft.Control:
        self._apply_layout(self._mode_for(self.page.width))
        return self.root

    def _build_header(self) -> ft.Container:
        self._sync_theme_icon()
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=theme.PAD, vertical=10),
            bgcolor=theme.PANEL_BG,
            border=ft.Border.only(bottom=ft.BorderSide(1, theme.BORDER)),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Image(src="icon.png", width=36, height=36, fit=ft.BoxFit.CONTAIN),
                    ft.ShaderMask(
                        blend_mode=ft.BlendMode.SRC_IN,
                        shader=ft.LinearGradient(colors=theme.BRAND_GRADIENT,
                                                 begin=ft.Alignment.TOP_LEFT,
                                                 end=ft.Alignment.BOTTOM_RIGHT),
                        content=self.title_txt,
                    ),
                    self.version_txt,
                    ft.Container(expand=True),
                    self.count_badge,
                    ft.IconButton(icon=ft.Icons.CODE, tooltip="Ver el proyecto en GitHub",
                                  action=ft.OpenUrl(theme.REPO_URL, target=ft.UrlTarget.BLANK)),
                    self.theme_btn,
                ],
            ),
        )

    # ================================================================ responsive
    @staticmethod
    def _mode_for(width) -> str:
        width = width or theme.BP_DESKTOP
        if width < theme.BP_MOBILE:
            return "mobile"
        if width < theme.BP_DESKTOP:
            return "tablet"
        return "desktop"

    def _on_resize(self, e) -> None:
        mode = self._mode_for(getattr(e, "width", None) or self.page.width)
        if mode != self.state.layout_mode:          # solo al cruzar un punto de quiebre
            self._apply_layout(mode)
            self.page.update()

    def _apply_layout(self, mode: str) -> None:
        self.state.layout_mode = mode
        self.left_panel = self.center_panel = self.preview_panel = self.code_panel = None
        self.desktop_tabs = None
        compact = mode == "mobile"

        # Cabecera compacta en móvil
        self.title_txt.value = "Flet Playground" if compact else theme.APP_NAME
        self.title_txt.size = 16 if compact else 17
        self.count_badge.visible = mode == "desktop"
        self.version_txt.visible = not compact
        self.body.padding = 8 if compact else theme.GAP

        if mode == "desktop":
            self.page.navigation_bar = None
            self.left_panel = LeftPanel(self)
            self.center_panel = CenterPanel(self)
            # Vista previa y código ocupan TODO el alto; se alternan con pestañas
            self.preview_panel = PreviewPanel(self, expand=True)
            self.code_panel = CodePanel(self, expand=True)
            self.desktop_tabs = ft.SegmentedButton(
                segments=[
                    ft.Segment(value="preview", label="Vista previa", icon=ft.Icons.VISIBILITY),
                    ft.Segment(value="code", label="Código", icon=ft.Icons.CODE),
                ],
                selected=[self.desktop_tab],
                show_selected_icon=False,
                on_change=self._on_desktop_tab,
            )
            self._sync_desktop_tab()
            self.body.content = ft.Row(
                expand=True,
                spacing=theme.GAP,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.left_panel,
                    self.center_panel,
                    ft.Column(
                        expand=True,
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            ft.Row([self.desktop_tabs], alignment=ft.MainAxisAlignment.CENTER),
                            self.preview_panel,
                            self.code_panel,
                        ],
                    ),
                ],
            )
            return

        # tablet / móvil -> navegación inferior
        self.page.navigation_bar = ft.NavigationBar(
            selected_index=self.state.mobile_tab,
            on_change=self._on_tab,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.WIDGETS_OUTLINED,
                                            selected_icon=ft.Icons.WIDGETS, label="Widgets"),
                ft.NavigationBarDestination(icon=ft.Icons.TUNE, label="Editor"),
                ft.NavigationBarDestination(icon=ft.Icons.CODE, label="Código"),
            ],
        )
        tab = self.state.mobile_tab
        if tab == TAB_WIDGETS:
            self.left_panel = LeftPanel(self, width=None, expand=True)
            self.body.content = self.left_panel
        elif tab == TAB_CODE:
            self.code_panel = CodePanel(self)
            self.body.content = self.code_panel
        elif mode == "tablet":
            self.center_panel = CenterPanel(self, width=320)
            self.preview_panel = PreviewPanel(self)
            self.body.content = ft.Row(
                expand=True, spacing=theme.GAP,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[self.center_panel, self.preview_panel],
            )
        else:  # móvil: vista previa fija arriba, parámetros con scroll abajo
            self.preview_panel = PreviewPanel(self, expand=False, height=theme.MOBILE_PREVIEW_H,
                                              compact=True)
            self.center_panel = CenterPanel(self, width=None, expand=True)
            self.body.content = ft.Column(
                expand=True, spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[self.preview_panel, self.center_panel],
            )

    # ---------------------------------------------------------------- pestañas escritorio
    def _sync_desktop_tab(self) -> None:
        """Muestra solo el panel de la pestaña activa (el otro sigue actualizado, pero oculto)."""
        if self.preview_panel is not None:
            self.preview_panel.visible = self.desktop_tab == "preview"
        if self.code_panel is not None:
            self.code_panel.visible = self.desktop_tab == "code"
        if self.desktop_tabs is not None:
            self.desktop_tabs.selected = [self.desktop_tab]

    def _on_desktop_tab(self, e: ft.Event) -> None:
        selected = e.control.selected or ["preview"]
        self.desktop_tab = selected[0]
        self._sync_desktop_tab()
        self.page.update()

    def _go_tab(self, index: int) -> None:
        self.state.mobile_tab = index
        if self.state.layout_mode != "desktop":
            self._apply_layout(self.state.layout_mode)

    def _on_tab(self, e: ft.Event) -> None:
        self._go_tab(int(e.control.selected_index))
        self.page.update()

    # ================================================================ acciones
    async def select_widget(self, name: str) -> None:
        self.state.current_widget = name
        self.manager.set_current_widget(name)
        if self.state.layout_mode != "desktop" and self.state.mobile_tab == TAB_WIDGETS:
            self._go_tab(TAB_EDITOR)            # en móvil/tablet saltamos directo al editor
        else:
            for panel in (self.left_panel, self.center_panel, self.preview_panel, self.code_panel):
                if panel is not None:
                    panel.refrescar()
        self.page.update()
        await prefs_service.save(prefs_service.KEY_LAST, name)

    async def toggle_favorite(self, name: str) -> None:
        favs = self.state.favorites
        if name in favs:
            favs.discard(name)
            msg, icon = f"{name} quitado de favoritos", ft.Icons.STAR_BORDER
        else:
            favs.add(name)
            msg, icon = f"{name} agregado a favoritos", ft.Icons.STAR
        if self.left_panel is not None:
            self.left_panel.refrescar()
        show_snack(self.page, msg, icon)
        self.page.update()
        await prefs_service.save(prefs_service.KEY_FAVS, sorted(favs))

    def on_params_changed(self) -> None:
        """Callback de cada control de parámetros: regenera vista previa y código."""
        if self.preview_panel is not None:
            self.preview_panel.refrescar()
        if self.code_panel is not None:
            self.code_panel.refrescar()
        self.page.update()

    def reset_current_widget(self) -> None:
        self.manager.current_widget.reset()
        if self.center_panel is not None:
            self.center_panel.refrescar()
        self.on_params_changed()
        show_snack(self.page, "Parámetros restablecidos", ft.Icons.RESTART_ALT)

    async def set_preview_mode(self, mode: str) -> None:
        self.state.preview_mode = mode
        if self.preview_panel is not None:
            self.preview_panel.refrescar()
        self.page.update()
        await prefs_service.save(prefs_service.KEY_PREVIEW_MODE, mode)

    async def set_code_mode(self, mode: str) -> None:
        self.state.code_mode = mode
        if self.code_panel is not None:
            self.code_panel.refrescar()
        self.page.update()
        await prefs_service.save(prefs_service.KEY_CODE_MODE, mode)

    # ================================================================ tema
    def is_dark(self) -> bool:
        mode = self.state.theme_mode
        if mode == "system":
            return self.page.platform_brightness == ft.Brightness.DARK
        return mode == "dark"

    def _sync_theme_icon(self) -> None:
        dark = self.is_dark()
        self.theme_btn.icon = ft.Icons.LIGHT_MODE if dark else ft.Icons.DARK_MODE
        self.theme_btn.tooltip = "Cambiar a modo claro" if dark else "Cambiar a modo oscuro"

    async def _on_toggle_theme(self, e: ft.Event) -> None:
        self.state.theme_mode = "light" if self.is_dark() else "dark"
        theme.apply_theme(self.page, self.state.theme_mode)
        self._after_theme_change()
        await prefs_service.save(prefs_service.KEY_THEME, self.state.theme_mode)

    def _on_brightness(self, e) -> None:
        if self.state.theme_mode == "system":
            self._after_theme_change()

    def _after_theme_change(self) -> None:
        self._sync_theme_icon()
        if self.code_panel is not None:
            self.code_panel.refrescar()      # el resaltado de código sigue al tema
        self.page.update()

    # ================================================================ teclado
    async def _on_key(self, e: ft.KeyboardEvent) -> None:
        if (e.key or "").lower() == "k" and (e.ctrl or e.meta):
            if self.state.layout_mode != "desktop" and self.state.mobile_tab != TAB_WIDGETS:
                self._go_tab(TAB_WIDGETS)
                self.page.update()
            if self.left_panel is not None:
                await self.left_panel.focus_search()

    # ================================================================ util
    @staticmethod
    def safe_update(control: ft.Control) -> None:
        try:
            control.update()
        except Exception:
            pass  # el control puede no estar montado
