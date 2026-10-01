"""
Construye los controles de edición a partir de la lista declarativa PARAMS.

Tipos soportados: slider, select, switch, color, text, icon.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import flet as ft

import theme

if TYPE_CHECKING:
    from core.base_widget import Param, WidgetConfig


def _label(text: str) -> ft.Text:
    return ft.Text(text, size=13, weight=ft.FontWeight.W_500, color=theme.TEXT)


def _fmt(param: "Param", value) -> str:
    if value is None:
        return "—"
    if param.decimals:
        return f"{value:.{param.decimals}f}{param.unit}"
    return f"{value:.0f}{param.unit}"


def _slider(cfg: "WidgetConfig", param: "Param", on_change: Callable) -> ft.Control:
    value_txt = ft.Text(_fmt(param, cfg.p(param.key)), size=12, color=theme.TEXT_MUTED,
                        font_family="monospace")

    def changed(e: ft.Event):
        v = round(float(e.control.value), param.decimals)
        value_txt.value = _fmt(param, v)
        cfg._update_param(param.key, v, on_change)

    return ft.Column(
        spacing=0,
        controls=[
            ft.Row([_label(param.label), value_txt],
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Slider(
                min=param.min, max=param.max, value=cfg.p(param.key),
                divisions=param.divisions, round=param.decimals,
                label="{value}", on_change=changed,
            ),
        ],
    )


def _dropdown(cfg: "WidgetConfig", param: "Param", on_change: Callable, with_icons=False) -> ft.Control:
    def changed(e: ft.Event):
        cfg._update_param(param.key, e.control.value, on_change)

    options = [
        ft.DropdownOption(
            key=value, text=text,
            leading_icon=getattr(ft.Icons, value, None) if with_icons else None,
        )
        for value, text in param.options
    ]
    return ft.Column(
        spacing=6,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            _label(param.label),
            # Dentro de un Row, expand estira en HORIZONTAL (verificado: expanded_insets no bastó)
            ft.Row([ft.Dropdown(
                expand=True,
                value=cfg.p(param.key),
                options=options,
                on_select=changed,                       # Flet 1.0: on_select (no on_change)
                dense=True,
                text_size=13,
                leading_icon=getattr(ft.Icons, cfg.p(param.key), None) if with_icons else None,
                border=ft.OutlineInputBorder(border_radius=theme.RADIUS_SM,
                                             side=ft.BorderSide(1, theme.BORDER)),
            )]),
        ],
    )


def _switch(cfg: "WidgetConfig", param: "Param", on_change: Callable) -> ft.Control:
    def changed(e: ft.Event):
        cfg._update_param(param.key, bool(e.control.value), on_change)

    return ft.Switch(label=param.label, value=bool(cfg.p(param.key)), on_change=changed,
                     label_text_style=ft.TextStyle(size=13))


def _text(cfg: "WidgetConfig", param: "Param", on_change: Callable) -> ft.Control:
    def changed(e: ft.Event):
        cfg._update_param(param.key, e.control.value, on_change)

    return ft.Column(
        spacing=6,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            _label(param.label),
            ft.TextField(
                value=cfg.p(param.key), on_change=changed, dense=True, text_size=13,
                border=ft.OutlineInputBorder(border_radius=theme.RADIUS_SM,
                                             side=ft.BorderSide(1, theme.BORDER)),
            ),
        ],
    )


def _color(cfg: "WidgetConfig", param: "Param", on_change: Callable) -> ft.Control:
    """Muestras de color clicables (+ 'Tema' si allow_none)."""
    swatches = ft.Row(wrap=True, spacing=8, run_spacing=8)
    choices: list[tuple[str | None, str]] = list(theme.PALETTE)
    if param.allow_none:
        choices.insert(0, (None, "Color del tema"))

    def paint():
        current = cfg.p(param.key)
        swatches.controls = [_swatch(value, label, value == current) for value, label in choices]

    def _swatch(value, label, selected):
        is_none = value is None
        return ft.Container(
            width=30, height=30,
            border_radius=15,
            bgcolor=theme.CARD_BG if is_none else value,
            border=ft.Border.all(3 if selected else 1,
                                 theme.PRIMARY if selected else theme.BORDER),
            tooltip=label if is_none else f"{label}  {value}",
            data=value,
            on_click=picked,
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(ft.Icons.FORMAT_COLOR_RESET, size=16, color=theme.TEXT_MUTED)
            if is_none else None,
        )

    def picked(e: ft.Event):
        cfg.params[param.key] = e.control.data
        paint()
        on_change()

    paint()
    return ft.Column([_label(param.label), swatches], spacing=8)


_BUILDERS = {
    "slider": _slider,
    "select": _dropdown,
    "switch": _switch,
    "text": _text,
    "color": _color,
}


def build_param_control(cfg: "WidgetConfig", param: "Param", on_change: Callable) -> ft.Control:
    if param.kind == "icon":
        return _dropdown(cfg, param, on_change, with_icons=True)
    builder = _BUILDERS.get(param.kind)
    if builder is None:
        return ft.Text(f"Tipo de parámetro desconocido: {param.kind}", color=ft.Colors.ERROR)
    return builder(cfg, param, on_change)


def build_param_groups(cfg: "WidgetConfig", on_change: Callable) -> ft.Control:
    """Agrupa los parámetros por 'group' en tarjetas con título."""
    groups: dict[str, list] = {}
    for param in cfg.PARAMS:
        groups.setdefault(param.group, []).append(param)

    if not groups:
        return ft.Text("Este widget no tiene parámetros editables.", color=theme.TEXT_MUTED)

    sections = []
    for title, params in groups.items():
        switches = [build_param_control(cfg, p, on_change) for p in params if p.kind == "switch"]
        others = [build_param_control(cfg, p, on_change) for p in params if p.kind != "switch"]
        body = list(others)
        if switches:
            body.append(ft.Row(switches, wrap=True, spacing=4, run_spacing=0))
        sections.append(
            ft.Container(
                padding=ft.Padding.all(14),
                bgcolor=theme.CARD_BG,
                border_radius=theme.RADIUS_SM,
                content=ft.Column(
                    spacing=12,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,   # Dropdowns a todo el ancho
                    controls=[
                        ft.Text(title.upper(), size=11, weight=ft.FontWeight.BOLD,
                                color=theme.PRIMARY),
                        *body,
                    ],
                ),
            )
        )
    return ft.Column(sections, spacing=theme.GAP,
                     horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
