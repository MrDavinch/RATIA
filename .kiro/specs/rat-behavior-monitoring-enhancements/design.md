# Documento de Diseño - Mejoras del Sistema de Monitoreo de Comportamiento de Ratas

## Visión General

El diseño se basa en la arquitectura existente del sistema, manteniendo la separación de responsabilidades entre GUI, manejo de cámara, y lógica de negocio. Las mejoras se implementarán como extensiones modulares que preserven toda la funcionalidad actual mientras agregan las nuevas capacidades requeridas.

## Arquitectura

### Arquitectura Actual
```
main.py
├── src/gui/
│   ├── main_window.py (MonitorGrimaceApp)
│   ├── splash_screen.py
│   └── style.py
├── src/camera/
│   └── camera_handler.py (CameraHandler)
└── resources/
    └── logo.jpeg
```

### Arquitectura Propuesta
```
main.py
├── src/gui/
│   ├── main_window.py (MonitorGrimaceApp - extendido)
│   ├── splash_screen.py
│   ├── style.py (mejorado)
│   ├── timeline_widget.py (nuevo)
│   ├── behavior_selector.py (nuevo)
│   └── statistics_window.py (nuevo)
├── src/camera/
│   ├── camera_handler.py (extendido)
│   └── ip_camera_handler.py (nuevo)
├── src/models/
│   ├── behavior_types.py (nuevo)
│   ├── study_period.py (nuevo)
│   └── experiment_data.py (nuevo)
├── src/analytics/
│   ├── statistics_generator.py (nuevo)
│   └── chart_generator.py (nuevo)
├── src/utils/
│   ├── data_exporter.py (nuevo)
│   └── config_manager.py (nuevo)
└── resources/
    └── logo.jpeg
```

## Componentes y Interfaces

### 1. Manejo de Cámara IP (src/camera/ip_camera_handler.py)

**Responsabilidad:** Manejar conexiones a cámaras IP de teléfonos móviles usando IP Webcam.

**Interfaz:**
```python
class IPCameraHandler:
    def __init__(self, ip_url: str)
    def connect(self) -> bool
    def read_frame(self) -> Optional[np.ndarray]
    def release(self) -> None
    def is_connected(self) -> bool
```

**Implementación:** 
- Usar OpenCV con URLs HTTP para conectar a streams IP Webcam
- Formato típico: `http://192.168.1.100:8080/video`
- Manejo de timeouts y reconexión automática
- Validación de URL y formato de stream

### 2. Selector de Comportamientos (src/gui/behavior_selector.py)

**Responsabilidad:** Widget para seleccionar tipos de comportamiento durante episodios de dolor.

**Interfaz:**
```python
class BehaviorSelector(QWidget):
    behavior_selected = pyqtSignal(str)
    
    def __init__(self, parent=None)
    def get_selected_behavior(self) -> str
    def reset_selection(self) -> None
```

**Implementación:**
- QComboBox con comportamientos predefinidos
- Integración con el botón de episodio de dolor existente
- Señales PyQt5 para comunicación con ventana principal

### 3. Línea de Tiempo Interactiva (src/gui/timeline_widget.py)

**Responsabilidad:** Widget para seleccionar períodos de estudio en la línea de tiempo del experimento.

**Interfaz:**
```python
class TimelineWidget(QWidget):
    period_selected = pyqtSignal(int, int, str)  # start_sec, end_sec, name
    
    def __init__(self, total_duration: int, parent=None)
    def add_period(self, start: int, end: int, name: str) -> None
    def get_periods(self) -> List[StudyPeriod]
    def clear_periods(self) -> None
```

**Implementación:**
- Widget personalizado con QPainter para dibujar línea de tiempo
- Manejo de eventos de mouse para selección de rangos
- Diálogo para nombrar períodos seleccionados

### 4. Modelos de Datos (src/models/)

**BehaviorTypes (behavior_types.py):**
```python
class BehaviorType(Enum):
    FACIAL_GROOMING = "Grooming facial"
    ORBITAL_TIGHTENING = "Estrechamiento orbital"
    WALL_RUBBING = "Frotamiento contra paredes"
    HUNCHED_POSTURE = "Postura encorvada"
    REDUCED_ACTIVITY = "Reducción de actividad"
    VOCALIZATION = "Vocalización"
    UNCATEGORIZED = "Sin categorizar"
```

**StudyPeriod (study_period.py):**
```python
@dataclass
class StudyPeriod:
    name: str
    start_time: int  # segundos desde inicio
    end_time: int    # segundos desde inicio
    episodes: List[PainEpisode]
```

**ExperimentData (experiment_data.py):**
```python
@dataclass
class PainEpisode:
    episode_number: int
    start_time: str
    duration: str
    behavior_type: BehaviorType
    status: str

@dataclass
class ExperimentData:
    total_duration: int
    episodes: List[PainEpisode]
    study_periods: List[StudyPeriod]
```

### 5. Generador de Estadísticas (src/analytics/statistics_generator.py)

**Responsabilidad:** Calcular estadísticas generales y por períodos de estudio.

**Interfaz:**
```python
class StatisticsGenerator:
    def __init__(self, experiment_data: ExperimentData)
    def generate_general_stats(self) -> Dict[str, Any]
    def generate_period_stats(self, period: StudyPeriod) -> Dict[str, Any]
    def generate_behavior_stats(self) -> Dict[str, Any]
    def compare_periods(self) -> Dict[str, Any]
```

### 6. Generador de Gráficas (src/analytics/chart_generator.py)

**Responsabilidad:** Crear visualizaciones mejoradas usando matplotlib.

**Interfaz:**
```python
class ChartGenerator:
    def __init__(self, experiment_data: ExperimentData)
    def create_timeline_chart(self) -> Figure
    def create_behavior_distribution_chart(self) -> Figure
    def create_period_comparison_chart(self) -> Figure
    def create_duration_evolution_chart(self) -> Figure
    def save_charts(self, output_dir: str) -> None
```

## Modelos de Datos

### Estructura de Datos Extendida

**Tabla de Episodios (extendida):**
- Episodio #
- Tiempo de Inicio
- Duración
- Tipo de Comportamiento (nuevo)
- Estado
- Período de Estudio (calculado)

**Configuración de Cámara:**
```python
@dataclass
class CameraConfig:
    camera_type: str  # "local" | "ip"
    camera_index: int  # para cámaras locales
    ip_url: str       # para cámaras IP
    resolution: Tuple[int, int]
```

## Manejo de Errores

### Estrategias de Error por Componente

**Cámara IP:**
- Timeout de conexión: 10 segundos
- Reintentos automáticos: 3 intentos
- Fallback a cámara local si está disponible
- Mensajes de error específicos para problemas de red

**Selección de Períodos:**
- Validación de rangos superpuestos
- Prevención de períodos fuera del tiempo total
- Confirmación antes de eliminar períodos

**Exportación de Datos:**
- Validación de permisos de escritura
- Backup automático antes de sobrescribir
- Manejo de errores de formato Excel

## Estrategia de Testing

### Pruebas Unitarias

**Componentes a Testear:**
1. `IPCameraHandler` - Conexión y lectura de frames
2. `StatisticsGenerator` - Cálculos estadísticos
3. `BehaviorTypes` - Validación de tipos
4. `ExperimentData` - Serialización/deserialización

**Herramientas:**
- pytest para pruebas unitarias
- unittest.mock para simular conexiones de cámara
- Datos de prueba sintéticos para validar estadísticas

### Pruebas de Integración

**Escenarios:**
1. Flujo completo: Conectar cámara IP → Registrar episodios → Seleccionar períodos → Exportar
2. Cambio entre cámaras durante experimento activo
3. Exportación con diferentes configuraciones de períodos
4. Manejo de desconexiones de red durante grabación

### Pruebas de Interfaz

**Validaciones:**
1. Responsividad de widgets personalizados
2. Integración de nuevos controles con tema existente
3. Comportamiento de línea de tiempo con diferentes duraciones
4. Visualización correcta de gráficas en diferentes resoluciones

## Consideraciones de Rendimiento

### Optimizaciones de Video

**Cámara IP:**
- Buffer de frames para evitar lag
- Compresión automática si el ancho de banda es limitado
- Detección de calidad de conexión

**Interfaz:**
- Actualización de UI en thread separado
- Lazy loading de gráficas estadísticas
- Caché de cálculos estadísticos

### Gestión de Memoria

**Estrategias:**
- Liberación automática de recursos de cámara
- Límite de frames en memoria para experimentos largos
- Garbage collection explícito después de exportar datos

## Plan de Migración

### Compatibilidad con Datos Existentes

**Estrategia:**
1. Mantener formato de tabla actual como base
2. Agregar columnas opcionales para nuevas funcionalidades
3. Migración automática de datos existentes
4. Exportación en formato legacy como opción

### Preservación de Funcionalidad

**Garantías:**
1. Todos los botones y controles actuales mantienen comportamiento exacto
2. Cronómetros funcionan idénticamente
3. Exportación básica a Excel sin cambios
4. Tema visual y estilos preservados

### Configuración por Defecto

**Valores Iniciales:**
- Comportamiento por defecto: "Sin categorizar"
- Cámara por defecto: Cámara local (índice 0)
- Períodos de estudio: Opcional, no requerido
- Estadísticas: Mostrar tanto básicas como avanzadas