from typing import Dict, List
from core.base_widget import WidgetConfig
from widgets.container_widget import ContainerConfig
from widgets.text_widget import TextConfig
from widgets.button_widget import ElevatedButtonConfig
from widgets.textfield_widget import TextFieldConfig
from widgets.row_widget import RowConfig
from widgets.column_widget import ColumnConfig
from widgets.card_widget import CardConfig


class WidgetManager:
    """Gestor centralizado de todos los widgets disponibles"""
    
    def __init__(self):
        """Inicializa el gestor con todos los widgets registrados"""
        self.widgets: Dict[str, WidgetConfig] = {}
        self._register_widgets()
        self.current_widget: WidgetConfig = self.widgets['Container']
    
    def _register_widgets(self):
        """Registra todos los widgets disponibles en la aplicación"""
        widgets_to_register = [
            ContainerConfig(),
            TextConfig(),
            ElevatedButtonConfig(),
            TextFieldConfig(),
            RowConfig(),
            ColumnConfig(),
            CardConfig(),
        ]
        
        for widget in widgets_to_register:
            self.widgets[widget.name] = widget
    
    def get_widget(self, name: str) -> WidgetConfig:
        """
        Obtiene un widget por su nombre
        
        Args:
            name: Nombre del widget
            
        Returns:
            WidgetConfig correspondiente o Container por defecto
        """
        return self.widgets.get(name, self.widgets['Container'])
    
    def search_widgets(self, query: str) -> List[WidgetConfig]:
        """
        Busca widgets que coincidan con la consulta
        
        Args:
            query: Texto de búsqueda
            
        Returns:
            Lista de widgets que coinciden
        """
        query = query.lower()
        return [
            widget for widget in self.widgets.values() 
            if query in widget.name.lower()
        ]
    
    def get_all_widgets(self) -> List[WidgetConfig]:
        """
        Obtiene todos los widgets disponibles
        
        Returns:
            Lista con todos los widgets
        """
        return list(self.widgets.values())
    
    def set_current_widget(self, widget: WidgetConfig):
        """
        Establece el widget actual
        
        Args:
            widget: Widget a establecer como actual
        """
        self.current_widget = widget