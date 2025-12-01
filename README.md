# Flet Widgets Playground

Una aplicación interactiva para explorar y experimentar con widgets de Flet en tiempo real.

<p align="center"> <img src="https://github.com/MagnoEfren/FletPlaygraund/blob/main/assets/icon.png" alt="Flet Widgets Playground" width="120" /> </p>

## 📁 Estructura del Proyecto

```
flet-widgets-playground/
│
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Este archivo
│
├── core/                        # Módulo core: Clases base y gestores
│   ├── __init__.py
│   ├── base_widget.py          # Clase abstracta base para widgets
│   └── widget_manager.py       # Gestor centralizado de widgets
│
├── widgets/                     # Módulo widgets: Configuraciones específicas
│   ├── __init__.py
│   ├── container_widget.py     # Widget Container
│   ├── text_widget.py          # Widget Text
│   ├── button_widget.py        # Widget ElevatedButton,  etc.
│
└── ui/                          # Módulo UI: Componentes de interfaz
    ├── __init__.py
    ├── layout.py               # Layout principal
    └── panels/                 # Paneles de la interfaz
        ├── __init__.py
        ├── left_panel.py       # Panel izquierdo (lista de widgets)
        ├── center_panel.py     # Panel central (parámetros)
        └── right_panel.py      # Panel derecho (preview y código)
```

## 🚀 Instalación

1. **Clonar el repositorio o crear la estructura de carpetas**

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
python main.py
```

## ✨ Características

- **Exploración Interactiva**: Experimenta con widgets de Flet en tiempo real
- **Vista Previa en Vivo**: Visualiza los cambios inmediatamente
- **Generación de Código**: Obtén el código Flet automáticamente
- **Búsqueda de Widgets**: Encuentra rápidamente el widget que necesitas
- **Interfaz Intuitiva**: Diseño limpio y fácil de usar

## 📚 Widgets Disponibles

1. **Container**: Caja contenedora versátil con control de tamaño, padding, margin, bordes y sombras
2. **Text**: Muestra texto con personalización de tamaño, peso, color y estilo
3. **ElevatedButton**: Botón elevado para acciones principales
4. **TextField**: Campo de entrada de texto con validación
5. **Row**: Organiza widgets horizontalmente
6. **Column**: Organiza widgets verticalmente
7. **Card**: Contenedor con elevación Material Design

## 🔧 Agregar Nuevos Widgets

Para agregar un nuevo widget, sigue estos pasos:

### 1. Crear el archivo del widget

Crea un nuevo archivo en `widgets/` (por ejemplo: `nuevo_widget.py`):

```python
import flet as ft
from core.base_widget import WidgetConfig


class NuevoWidgetConfig(WidgetConfig):
    def __init__(self):
        super().__init__(
            name="NuevoWidget",
            icon=ft.Icons.TU_ICONO,
            description="Descripción de tu widget"
        )
        self.params = {
            'parametro1': valor_inicial,
            'parametro2': valor_inicial,
        }
    
    def create_controls(self, on_change_callback) -> ft.Column:
        # Implementar controles de configuración
        return ft.Column([
            # Tus controles aquí
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_preview(self) -> ft.Control:
        # Implementar vista previa
        return ft.TuWidget(
            # Parámetros configurables
        )
    
    def generate_code(self) -> str:
        # Implementar generación de código
        code_lines = ["ft.TuWidget("]
        # Agregar líneas de código
        code_lines.append(")")
        return "\n".join(code_lines)
```

### 2. Registrar el widget en `widgets/__init__.py`

```python
from .nuevo_widget import NuevoWidgetConfig

__all__ = [
    # ... widgets existentes
    'NuevoWidgetConfig',
]
```

### 3. Agregar al gestor en `core/widget_manager.py`

```python
from widgets.nuevo_widget import NuevoWidgetConfig

class WidgetManager:
    def _register_widgets(self):
        widgets_to_register = [
            # ... widgets existentes
            NuevoWidgetConfig(),
        ]
```

¡Y listo! Tu nuevo widget estará disponible en la aplicación.

## 🎨 Arquitectura

### Patrón de Diseño

El proyecto utiliza varios patrones de diseño:

- **Abstract Factory**: `WidgetConfig` es una clase abstracta que define la interfaz para crear widgets
- **Manager Pattern**: `WidgetManager` gestiona todos los widgets disponibles
- **MVC (Model-View-Controller)**: 
  - Model: Clases de widgets en `widgets/`
  - View: Componentes UI en `ui/`
  - Controller: `WidgetManager` y callbacks

### Flujo de Datos

```
Usuario interactúa con controles
    ↓
on_change_callback se ejecuta
    ↓
Parámetros se actualizan en WidgetConfig
    ↓
update_all() se llama
    ↓
Vista previa y código se regeneran
    ↓
UI se actualiza
```

## 🛠️ Módulos

### Core (`core/`)

Contiene las clases base y lógica central:

- **`base_widget.py`**: Clase abstracta `WidgetConfig` con métodos obligatorios
- **`widget_manager.py`**: Gestiona el registro, búsqueda y acceso a widgets

### Widgets (`widgets/`)

Cada archivo implementa la configuración de un widget específico:

- Extiende `WidgetConfig`
- Define parámetros configurables
- Implementa controles de UI
- Genera vista previa
- Genera código Flet

### UI (`ui/`)

Componentes de interfaz de usuario:

- **`layout.py`**: Coordina todos los paneles
- **`panels/left_panel.py`**: Lista y búsqueda de widgets
- **`panels/center_panel.py`**: Controles de parámetros
- **`panels/right_panel.py`**: Vista previa y código

## 📖 Uso

1. **Seleccionar un widget** desde el panel izquierdo
2. **Ajustar parámetros** en el panel central
3. **Ver cambios en tiempo real** en el panel derecho
4. **Copiar el código generado** con el botón de copiar

## 🤝 Contribuir

Para contribuir al proyecto:

1. Agrega nuevos widgets siguiendo la guía
2. Mejora la documentación
3. Reporta bugs o sugiere mejoras
4. Optimiza el código existente

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🔗 Enlaces Útiles

- [Documentación de Flet](https://flet.dev)
- [Galería de Controles Flet](https://flet.dev/docs/controls)
- [GitHub de Flet](https://github.com/flet-dev/flet)

## 💡 Consejos

- Usa el método `_create_slider()` de la clase base para crear sliders fácilmente
- Mantén la consistencia en los nombres de parámetros
- Documenta bien tu código
- Prueba todos los valores extremos de los parámetros

## 🐛 Resolución de Problemas

### El widget no aparece en la lista
- Verifica que esté registrado en `widget_manager.py`
- Asegúrate de importarlo correctamente en `__init__.py`

### Los cambios no se reflejan en tiempo real
- Verifica que llames a `on_change_callback` en todos los controles
- Asegúrate de usar `_update_param()` correctamente

### Error al generar código
- Verifica que el método `generate_code()` retorne un string válido
- Asegúrate de que todas las comillas estén balanceadas

---

**Desarrollado con ❤️ usando Flet**
