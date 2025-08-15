# Plan de Implementación - Mejoras del Sistema de Monitoreo de Comportamiento de Ratas

- [ ] 1. Crear modelos de datos y tipos de comportamiento
  - Implementar enum BehaviorType con todos los tipos de comportamiento definidos
  - Crear dataclass PainEpisode extendida con campo behavior_type
  - Crear dataclass StudyPeriod para períodos de estudio
  - Crear dataclass ExperimentData para manejar datos completos del experimento
  - Escribir tests unitarios para validación de modelos de datos
  - _Requisitos: 2.1, 2.2, 3.3_

- [ ] 2. Implementar manejo de cámara IP
  - Crear clase IPCameraHandler que extienda funcionalidad de CameraHandler
  - Implementar conexión HTTP a streams de IP Webcam usando OpenCV
  - Agregar validación de URL y manejo de timeouts de conexión
  - Implementar reconexión automática en caso de pérdida de señal
  - Escribir tests unitarios para conexión IP y manejo de errores
  - _Requisitos: 1.1, 1.2, 1.3_

- [ ] 3. Extender selector de cámara en interfaz principal
  - Modificar QComboBox para incluir opción "Cámara IP"
  - Agregar QLineEdit para ingresar URL de cámara IP cuando se seleccione
  - Actualizar método connect_camera() para manejar ambos tipos de cámara
  - Implementar validación de URL antes de intentar conexión
  - Mantener funcionalidad existente de cámaras locales intacta
  - _Requisitos: 1.1, 1.4, 6.2_

- [ ] 4. Crear widget selector de comportamientos
  - Implementar clase BehaviorSelector como QWidget con QComboBox
  - Integrar selector en diálogo modal que aparezca al iniciar episodio de dolor
  - Configurar señales PyQt5 para comunicar comportamiento seleccionado
  - Implementar opción por defecto "Sin categorizar" para compatibilidad
  - Escribir tests para interacción del widget
  - _Requisitos: 2.1, 2.3, 6.3_

- [ ] 5. Integrar selector de comportamientos con registro de episodios
  - Modificar método toggle_pain_episode() para mostrar selector de comportamiento
  - Actualizar método start_episode() para recibir y almacenar tipo de comportamiento
  - Extender tabla de episodios para mostrar columna de comportamiento
  - Actualizar método complete_episode() para mantener información de comportamiento
  - Asegurar que episodios sin categorizar funcionen como antes
  - _Requisitos: 2.1, 2.2, 6.3_

- [ ] 6. Crear widget de línea de tiempo interactiva
  - Implementar clase TimelineWidget usando QPainter para dibujar línea de tiempo
  - Agregar manejo de eventos de mouse para seleccionar rangos de tiempo
  - Implementar diálogo para nombrar períodos seleccionados
  - Crear métodos para agregar, editar y eliminar períodos de estudio
  - Escribir tests para interacciones de mouse y validación de rangos
  - _Requisitos: 3.1, 3.2, 3.3_

- [ ] 7. Integrar línea de tiempo con finalización de experimento
  - Modificar método finalize_experiment() para mostrar TimelineWidget
  - Crear ventana modal con línea de tiempo del experimento completo
  - Implementar validación de períodos superpuestos o inválidos
  - Almacenar períodos definidos en estructura ExperimentData
  - Mantener opción de exportar sin definir períodos (comportamiento actual)
  - _Requisitos: 3.1, 3.4, 6.4_

- [ ] 8. Implementar generador de estadísticas avanzadas
  - Crear clase StatisticsGenerator para cálculos estadísticos
  - Implementar análisis general de episodios (actual + por comportamiento)
  - Implementar análisis por períodos de estudio definidos
  - Agregar cálculos de comparación entre períodos
  - Escribir tests unitarios para todos los cálculos estadísticos
  - _Requisitos: 2.5, 3.4, 4.2, 4.5_

- [ ] 9. Crear generador de gráficas mejoradas
  - Implementar clase ChartGenerator usando matplotlib
  - Crear gráfica de distribución por tipos de comportamiento
  - Crear gráficas comparativas entre períodos de estudio
  - Mejorar gráficas existentes con colores profesionales y etiquetas en español
  - Implementar exportación de gráficas en PNG de alta resolución
  - _Requisitos: 4.1, 4.2, 4.3, 4.4_

- [ ] 10. Actualizar exportador de datos
  - Extender método export_table_to_excel() para incluir columna de comportamiento
  - Implementar exportación de hojas separadas por período de estudio
  - Agregar exportación de estadísticas detalladas en hoja adicional
  - Mantener formato de exportación actual como opción por defecto
  - Escribir tests para validar formato Excel generado
  - _Requisitos: 2.4, 3.5, 6.4_

- [ ] 11. Integrar estadísticas y gráficas en ventana de análisis
  - Modificar método show_analysis() para usar nuevos generadores
  - Crear pestañas separadas para análisis general, por comportamiento y por períodos
  - Integrar gráficas mejoradas en interfaz de análisis
  - Implementar navegación entre diferentes vistas de análisis
  - Mantener análisis básico actual como vista por defecto
  - _Requisitos: 4.1, 4.2, 4.3, 6.5_

- [ ] 12. Actualizar estilos y tema visual
  - Extender archivo style.py con estilos para nuevos widgets
  - Asegurar consistencia visual con tema oscuro existente
  - Agregar estilos específicos para TimelineWidget y BehaviorSelector
  - Mejorar colores de gráficas para mejor legibilidad
  - Mantener todos los estilos actuales sin cambios
  - _Requisitos: 4.1, 6.5_

- [ ] 13. Implementar configuración y persistencia
  - Crear clase ConfigManager para guardar configuraciones de usuario
  - Implementar persistencia de URL de cámara IP favoritas
  - Guardar configuraciones de períodos de estudio como plantillas
  - Implementar carga automática de última configuración usada
  - Escribir tests para serialización y deserialización de configuración
  - _Requisitos: 1.4, 3.3_

- [ ] 14. Crear tests de integración completos
  - Escribir test de flujo completo: conectar cámara IP → registrar episodios → definir períodos → exportar
  - Implementar test de cambio entre tipos de cámara durante experimento
  - Crear test de exportación con diferentes configuraciones de períodos
  - Validar que funcionalidad existente no se vea afectada
  - Implementar tests de manejo de errores de red y cámara
  - _Requisitos: 1.3, 1.4, 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 15. Preparar empaquetado como ejecutable
  - Configurar PyInstaller para crear ejecutable Windows
  - Incluir todas las dependencias (OpenCV, PyQt5, matplotlib, pandas)
  - Implementar ofuscación de código usando herramientas como pyarmor
  - Crear script de build automatizado
  - Probar ejecutable en diferentes versiones de Windows
  - _Requisitos: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 16. Validación final y documentación
  - Ejecutar suite completa de tests unitarios e integración
  - Validar que todas las funcionalidades existentes funcionan idénticamente
  - Crear documentación de usuario para nuevas funcionalidades
  - Realizar pruebas de rendimiento con experimentos largos
  - Crear guía de instalación y configuración del ejecutable
  - _Requisitos: 6.1, 6.2, 6.3, 6.4, 6.5_