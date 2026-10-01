"""
Panel derecho, dividido en dos piezas reutilizables:

- PreviewPanel: el control real, con su PROPIO tema (Auto / Claro / Oscuro)
  independiente del tema de la app, para comprobar cómo se ve en ambos modos.
- CodePanel: código con resaltado de sintaxis, modo Snippet / App completa,
  copiar (Client Action, compatible con iOS Safari) y descargar como .py.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

import theme
from services import code_service
from ui.components.feedback import show_snack

if TYPE_CHECKING:
    from ui.layout import MainLayout


def _section_title(text: str, icon) -> ft.Row:
    return ft.Row(
        spacing=8,
        controls=[ft.Icon(icon, size=18, color=theme.PRIMARY),
                  ft.Text(text, size=15, weight=ft.FontWeight.BOLD, color=theme.TEXT)],
    )


class PreviewPanel(ft.Container):
    MODES = [("auto", "Auto", ft.Icons.BRIGHTNESS_AUTO),
             ("light", "Claro", ft.Icons.LIGHT_MODE),
             ("dark", "Oscuro", ft.Icons.DARK_MODE)]

    def __init__(self, app: "MainLayout", expand=True, height=None, compact=False):
        super().__init__(
            expand=expand,
            height=height,
            padding=theme.PAD if not compact else 10,
            bgcolor=theme.PANEL_BG,
            border_radius=theme.RADIUS,
            border=ft.Border.all(1, theme.BORDER),
        )
        self.app = app
        self.compact = compact

        self.mode_selector = ft.SegmentedButton(
            segments=[ft.Segment(value=v, label=None if compact else lbl, icon=ic,
                                 tooltip=f"Vista previa en modo {lbl.lower()}")
                      for v, lbl, ic in self.MODES],
            selected=[app.state.preview_mode],
            show_selected_icon=False,
            on_change=self._on_mode,
        )
        # Contenedor donde se monta el control real
        self.preview_slot = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.content = ft.Column(
            expand=True,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,   # el escenario ocupa todo el ancho
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[_section_title("Vista previa", ft.Icons.VISIBILITY), self.mode_selector],
                    wrap=False,
                ),
                ft.Container(expand=True),          # lugar del escenario (se crea en refrescar)
            ],
        )
        self.refrescar()

    def _build_stage(self, mode: str) -> ft.Container:
        """
        "Escenario" con su PROPIO tema. Se crea de nuevo en cada cambio de modo
        (theme_mode se fija al construir, verificado renderizando la app).
        Dentro va un Card: es un Material, así el texto por defecto también
        toma el color del tema forzado (un Container no lo hace).
        """
        forced = {"light": ft.ThemeMode.LIGHT, "dark": ft.ThemeMode.DARK}.get(mode)
        return ft.Container(
            expand=True,
            # "auto": sin tema propio -> hereda el de la app
            theme=theme.build_theme() if forced else None,
            dark_theme=theme.build_theme() if forced else None,
            theme_mode=forced,
            content=ft.Card(
                variant=ft.CardVariant.OUTLINED,
                elevation=0,
                margin=0,
                bgcolor=theme.STAGE_BG,
                shape=ft.RoundedRectangleBorder(radius=theme.RADIUS_SM),
                content=ft.Container(padding=20, content=self.preview_slot),
            ),
        )

    def refrescar(self) -> None:
        mode = self.app.state.preview_mode
        self.mode_selector.selected = [mode]
        if mode != getattr(self, "_stage_mode", None):
            self._stage_mode = mode
            self.content.controls[1] = self._build_stage(mode)
        w = self.app.manager.current_widget
        try:
            control = w.create_preview()
        except Exception as ex:                     # un parámetro inválido no tumba la app
            control = ft.Column(
                [ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.ERROR, size=36),
                 ft.Text(f"No se pudo crear la vista previa:\n{ex}", color=ft.Colors.ERROR,
                         text_align=ft.TextAlign.CENTER)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        self.preview_slot.controls = [control]

    async def _on_mode(self, e: ft.Event) -> None:
        selected = e.control.selected or ["auto"]
        await self.app.set_preview_mode(selected[0])


class CodePanel(ft.Container):
    def __init__(self, app: "MainLayout", expand=True):
        super().__init__(
            expand=expand,
            padding=theme.PAD,
            bgcolor=theme.PANEL_BG,
            border_radius=theme.RADIUS,
            border=ft.Border.all(1, theme.BORDER),
        )
        self.app = app
        self.current_code = ""

        self.mode_selector = ft.SegmentedButton(
            segments=[ft.Segment(value="snippet", label="Snippet", icon=ft.Icons.DATA_OBJECT),
                      ft.Segment(value="app", label="App completa", icon=ft.Icons.ROCKET_LAUNCH)],
            selected=[app.state.code_mode],
            show_selected_icon=False,
            on_change=self._on_mode,
        )
        # action= se ejecuta en el cliente DENTRO del click: necesario en web/iOS
        self.copy_btn = ft.IconButton(icon=ft.Icons.CONTENT_COPY, tooltip="Copiar código",
                                      on_click=self._on_copied)
        self.download_btn = ft.IconButton(icon=ft.Icons.DOWNLOAD, tooltip="Descargar como .py",
                                          on_click=self._on_download)
        self.lines_txt = ft.Text(size=12, color=theme.TEXT_MUTED)
        self.code_md = ft.Markdown(
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        )
        self.content = ft.Column(
            expand=True,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    wrap=False,
                    controls=[
                        _section_title("Código", ft.Icons.CODE),
                        ft.Container(expand=True),
                        self.lines_txt,
                        self.copy_btn,
                        self.download_btn,
                    ],
                ),
                self.mode_selector,
                ft.Container(
                    expand=True,
                    bgcolor=theme.STAGE_BG,
                    border=ft.Border.all(1, theme.BORDER),
                    border_radius=theme.RADIUS_SM,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    # Row con scroll: las líneas largas se desplazan en horizontal
                    # en vez de partirse (importante en móvil)
                    content=ft.ListView(
                        expand=True,
                        controls=[ft.Row([self.code_md], scroll=ft.ScrollMode.AUTO,
                                         vertical_alignment=ft.CrossAxisAlignment.START)],
                    ),
                ),
            ],
        )
        self.refrescar()

    def refrescar(self) -> None:
        w = self.app.manager.current_widget
        self.mode_selector.selected = [self.app.state.code_mode]
        code = w.generate_full_app() if self.app.state.code_mode == "app" else w.generate_code()
        self.current_code = code
        self.code_md.value = f"```python\n{code}\n```"
        self.code_md.code_theme = (ft.MarkdownCodeTheme.ATOM_ONE_DARK if self.app.is_dark()
                                   else ft.MarkdownCodeTheme.ATOM_ONE_LIGHT)
        self.copy_btn.action = ft.CopyToClipboard(code)
        self.lines_txt.value = f"{code.count(chr(10)) + 1} líneas"

    # ------------------------------------------------------------ eventos
    async def _on_mode(self, e: ft.Event) -> None:
        selected = e.control.selected or ["snippet"]
        await self.app.set_code_mode(selected[0])

    def _on_copied(self, e: ft.Event) -> None:
        # La copia ya la hizo la Client Action; aquí solo avisamos.
        show_snack(self.app.page, "Código copiado al portapapeles")

    async def _on_download(self, e: ft.Event) -> None:
        w = self.app.manager.current_widget
        name = code_service.file_name_for(w.name)
        data = self.current_code.encode("utf-8")
        try:
            path = await ft.FilePicker().save_file(
                dialog_title="Guardar código",
                file_name=name,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["py"],
                src_bytes=data,
            )
        except Exception as ex:
            show_snack(self.app.page, f"No se pudo guardar: {ex}", ft.Icons.ERROR_OUTLINE)
            return
        if self.app.page.web:
            show_snack(self.app.page, f"Descargando {name}", ft.Icons.DOWNLOAD_DONE)
            return
        if not path:
            return  # canceló
        try:
            # En escritorio nos aseguramos de que el archivo quede escrito.
            with open(path, "wb") as fh:
                fh.write(data)
            show_snack(self.app.page, f"Guardado en {path}", ft.Icons.DOWNLOAD_DONE)
        except OSError as ex:
            show_snack(self.app.page, f"No se pudo escribir el archivo: {ex}", ft.Icons.ERROR_OUTLINE)
