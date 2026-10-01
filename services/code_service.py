"""
Lógica PURA de generación de código (sin flet).
Se puede probar por consola:  python3 -c "from services.code_service import *; print(py(3.0))"
"""
from textwrap import indent as _indent


def py(value) -> str:
    """Convierte un valor de Python a su literal en código."""
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return "None"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.2f}".rstrip("0").rstrip(".")
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def indent(code: str, spaces: int = 4) -> str:
    return _indent(code, " " * spaces)


def call(fn: str, *args) -> str:
    """
    Arma una llamada multilínea.
    args: cadenas (argumento posicional ya en código) o tuplas (nombre, código).
    Los None se ignoran, así es fácil poner argumentos condicionales.
    """
    items = [a for a in args if a is not None]
    if not items:
        return f"{fn}()"
    parts = [a if isinstance(a, str) else f"{a[0]}={a[1]}" for a in items]
    inline = f"{fn}({', '.join(parts)})"
    if len(inline) <= 72 and "\n" not in inline:
        return inline                      # llamadas cortas en una sola línea
    lines = [f"{fn}("]
    for text in parts:
        lines.append(indent(text) + ",")
    lines.append(")")
    return "\n".join(lines)


def code_list(items: list[str]) -> str:
    """Lista multilínea de expresiones ya en código."""
    if not items:
        return "[]"
    return "[\n" + ",\n".join(indent(i) for i in items) + ",\n]"


def opt(name: str, value, default=None):
    """Argumento opcional: solo aparece si difiere del valor por defecto."""
    if value == default:
        return None
    return (name, py(value))


def wrap_app(snippet: str, title: str) -> str:
    """Envuelve un snippet en una app completa y ejecutable con Flet 1.0."""
    body = indent(snippet, 8)
    return (
        "import flet as ft\n\n\n"
        "def main(page: ft.Page):\n"
        f"    page.title = {py(title + ' — demo')}\n"
        "    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER\n"
        "    page.vertical_alignment = ft.MainAxisAlignment.CENTER\n"
        "    page.add(\n"
        f"{body}\n"
        "    )\n\n\n"
        "ft.run(main)\n"
    )


def file_name_for(widget_name: str) -> str:
    return f"{widget_name.lower()}_demo.py"
