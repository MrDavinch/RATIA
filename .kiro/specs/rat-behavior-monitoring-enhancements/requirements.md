# Especificación de Requisitos - Mejoras del Sistema de Monitoreo de Comportamiento de Ratas

## Introducción

Este documento define los requisitos para mejorar el sistema existente de monitoreo de comportamiento de dolor en ratas. El sistema actual permite conectar una cámara web local, registrar episodios de dolor con cronometraje, y exportar datos estadísticos. Las mejoras propuestas incluyen conectividad con cámaras IP de teléfonos móviles, categorización de comportamientos de dolor, análisis por períodos de estudio personalizables, mejoras en visualización de estadísticas, y empaquetado como ejecutable protegido.

## Requisitos

### Requisito 1: Conectividad con Cámara IP de Teléfono Móvil

**Historia de Usuario:** Como investigador, quiero conectar mi teléfono móvil como cámara remota usando la aplicación IP Webcam, para tener mayor flexibilidad en el posicionamiento de la cámara durante los experimentos.

#### Criterios de Aceptación

1. CUANDO el usuario seleccione "Cámara IP" en el selector de cámaras ENTONCES el sistema deberá mostrar un campo para ingresar la URL de la cámara IP
2. CUANDO el usuario ingrese una URL válida de IP Webcam ENTONCES el sistema deberá conectarse y mostrar el video en tiempo real
3. CUANDO la conexión IP falle ENTONCES el sistema deberá mostrar un mensaje de error específico y mantener la funcionalidad con cámaras locales
4. CUANDO el usuario cambie entre cámara local e IP ENTONCES el sistema deberá mantener todos los cronómetros y datos del experimento activo

### Requisito 2: Categorización de Comportamientos de Dolor

**Historia de Usuario:** Como técnico de laboratorio, quiero poder categorizar los diferentes tipos de comportamientos de dolor observados durante los episodios, para obtener análisis más detallados y específicos del comportamiento animal.

#### Criterios de Aceptación

1. CUANDO el usuario inicie un episodio de dolor ENTONCES el sistema deberá mostrar una lista de comportamientos disponibles para seleccionar
2. CUANDO el usuario seleccione un comportamiento ENTONCES el sistema deberá registrar tanto el tiempo como el tipo de comportamiento en la tabla
3. SI no se selecciona ningún comportamiento ENTONCES el sistema deberá registrar el episodio como "Sin categorizar"
4. CUANDO se exporte la data ENTONCES el archivo deberá incluir la columna de tipo de comportamiento
5. CUANDO se generen estadísticas ENTONCES el sistema deberá mostrar análisis por tipo de comportamiento

Los tipos de comportamiento incluidos serán:
- Grooming facial (Acicalamiento facial)
- Estrechamiento orbital (Orbital tightening)
- Frotamiento contra paredes (Wall rubbing)
- Postura encorvada (Hunched posture)
- Reducción de actividad (Reduced activity)
- Vocalización (Vocalization)

### Requisito 3: Selección de Períodos de Estudio Personalizables

**Historia de Usuario:** Como investigador, quiero poder definir períodos específicos de análisis dentro del experimento total, para evaluar patrones de comportamiento en diferentes fases temporales del estudio.

#### Criterios de Aceptación

1. CUANDO el experimento termine ENTONCES el sistema deberá mostrar una línea de tiempo interactiva del experimento completo
2. CUANDO el usuario haga clic en la línea de tiempo ENTONCES podrá marcar el inicio y fin de períodos de estudio
3. CUANDO se definan múltiples períodos ENTONCES el sistema deberá permitir nombrar cada período (ej: "Período inicial 5min", "Período intermedio 15min")
4. CUANDO se generen estadísticas ENTONCES el sistema deberá mostrar análisis tanto general como por cada período definido
5. CUANDO se exporten datos ENTONCES el archivo deberá incluir una hoja separada para cada período de estudio

### Requisito 4: Mejoras en Visualización de Estadísticas

**Historia de Usuario:** Como investigador, quiero visualizaciones estadísticas más claras y profesionales, para presentar mejor los resultados de mis experimentos en publicaciones científicas.

#### Criterios de Aceptación

1. CUANDO se generen gráficas ENTONCES deberán usar colores profesionales y etiquetas claras en español
2. CUANDO se muestren estadísticas por comportamiento ENTONCES deberá incluir gráficas de barras por tipo de comportamiento
3. CUANDO se analicen períodos de estudio ENTONCES deberá mostrar comparativas entre períodos
4. CUANDO se exporte el análisis ENTONCES deberá incluir las gráficas en formato PNG de alta resolución
5. CUANDO se muestren estadísticas generales ENTONCES deberá incluir medidas de tendencia central y dispersión

### Requisito 5: Preservación de Funcionalidad Existente

**Historia de Usuario:** Como usuario actual del sistema, quiero que todas las funcionalidades existentes se mantengan intactas después de las mejoras, para no perder el trabajo y configuraciones actuales.

#### Criterios de Aceptación

1. CUANDO se implementen las mejoras ENTONCES todas las funciones actuales de cronometraje deberán seguir funcionando igual
2. CUANDO se conecte una cámara local ENTONCES deberá funcionar exactamente como antes
3. CUANDO se registren episodios sin categorizar ENTONCES deberá funcionar como el sistema actual
4. CUANDO se exporten datos básicos ENTONCES deberá mantener el formato Excel actual como opción
5. CUANDO se use la interfaz ENTONCES todos los botones y controles actuales deberán mantener su comportamiento

### Requisito 6: Empaquetado como Ejecutable Protegido

**Historia de Usuario:** Como administrador del laboratorio, quiero distribuir la aplicación como un ejecutable independiente y protegido, para facilitar la instalación y proteger el código fuente de la aplicación.

#### Criterios de Aceptación

1. CUANDO se compile la aplicación ENTONCES deberá generar un archivo ejecutable (.exe) que funcione sin instalación de Python
2. CUANDO se ejecute el .exe ENTONCES deberá incluir todas las dependencias necesarias
3. CUANDO se intente acceder al código fuente ENTONCES deberá estar ofuscado o encriptado
4. CUANDO se distribuya el ejecutable ENTONCES deberá mantener todas las funcionalidades existentes
5. CUANDO se ejecute en diferentes computadoras Windows ENTONCES deberá funcionar sin instalaciones adicionales

