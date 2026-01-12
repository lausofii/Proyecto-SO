# Manual de Usuario
## Simulador de Algoritmos de Planificación de CPU

**Universidad Católica Andrés Bello**  
**Facultad de Ingeniería - Escuela de Informática**  
**Sistemas Operativos - Equipo 7**

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Inicio del Programa](#inicio-del-programa)
5. [Descripción de la Interfaz](#descripción-de-la-interfaz)
6. [Navegación y Atajos de Teclado](#navegación-y-atajos-de-teclado)
7. [Funcionalidades Principales](#funcionalidades-principales)
8. [Guía de Uso Paso a Paso](#guía-de-uso-paso-a-paso)
9. [Formato de Archivos](#formato-de-archivos)
10. [Interpretación de Resultados](#interpretación-de-resultados)
11. [Solución de Problemas](#solución-de-problemas)

---

## 1. Introducción

El **Simulador de Algoritmos de Planificación de CPU** es una herramienta educativa diseñada para visualizar y comparar el comportamiento de diferentes algoritmos de planificación de procesos en un sistema operativo. Permite analizar métricas de rendimiento como tiempos de espera, tiempo de retorno, utilización de CPU y throughput.

### Características Principales

- ✅ Simulación de 5 algoritmos de planificación:
  - FCFS (First Come First Served)
  - SJF (Shortest Job First - No apropiativo)
  - Round Robin (con quantum configurable)
  - Prioridades (sin desalojo)
  - Prioridades (con desalojo)
- ✅ Interfaz gráfica de terminal moderna (TUI) usando Textual
- ✅ Carga de procesos desde archivos (JSON, CSV, TXT)
- ✅ Visualización de diagramas de Gantt
- ✅ Cálculo y comparación de métricas de rendimiento
- ✅ Historial de simulaciones

---

## 2. Requisitos del Sistema

### Requisitos Mínimos

- **Sistema Operativo**: Windows 10/11, Linux, o macOS
- **Python**: Versión 3.8 o superior
- **Memoria RAM**: 4 GB mínimo
- **Espacio en disco**: 100 MB libres
- **Terminal**: Terminal moderna compatible con Textual (Windows Terminal, Terminal.app, o terminales modernas de Linux)

### Dependencias

El simulador requiere las siguientes librerías de Python:
- `textual` (versión 0.40 o superior)
- `rich` (versión 13.0 o superior)

---

## 3. Instalación

### Paso 1: Verificar Python

Asegúrese de tener Python 3.8 o superior instalado:

```bash
python --version
```

### Paso 2: Instalar Dependencias

Navegue al directorio del proyecto y ejecute:

```bash
pip install -r requirements.txt
```

Esto instalará automáticamente:
- `textual` (framework para TUI)
- `rich` (formato de texto enriquecido)

### Paso 3: Verificar Instalación

Ejecute el programa para verificar que todo esté correcto:

```bash
python main.py
```

Si aparece la interfaz gráfica del simulador con el menú principal, la instalación fue exitosa.

---

## 4. Inicio del Programa

### Método 1: Ejecución Directa (Recomendado)

```bash
python main.py
```

Este método inicia la aplicación con la interfaz Textual completa.

### Método 2: Usando el Script Alternativo

```bash
python run.py
```

**Nota**: Este método usa la interfaz de consola tradicional. Para la interfaz Textual, use `main.py`.

---

## 5. Descripción de la Interfaz

La interfaz del simulador utiliza **Textual**, un framework moderno para crear aplicaciones de terminal interactivas. La aplicación funciona con **pantallas (screens)** que se navegan mediante botones y atajos de teclado.

### Pantalla Principal

Al iniciar el programa, verá la **Pantalla Principal** que contiene:

1. **Encabezado**: Muestra el título del simulador y la información del equipo
2. **Menú de Opciones**: Botones numerados del 1 al 7 para acceder a las diferentes funcionalidades:
   - **1. Cargar procesos desde archivo**
   - **2. Crear procesos manualmente**
   - **3. Usar casos de prueba predefinidos**
   - **4. Ejecutar simulación**
   - **5. Comparar todos los algoritmos**
   - **6. Ver historial de resultados**
   - **7. Configurar parámetros**
3. **Tabla de Procesos**: Muestra los procesos actualmente cargados (si hay alguno)
4. **Pie de Página**: Muestra los atajos de teclado disponibles

### Navegación entre Pantallas

- Cada opción del menú abre una **nueva pantalla** con su propia interfaz
- Use el botón **"Volver"** o la tecla **Escape** para regresar a la pantalla anterior
- Las pantallas se apilan, permitiendo navegar hacia atrás en el historial

### Elementos de la Interfaz

- **Botones**: Use las flechas del teclado o Tab para navegar, Enter para activar
- **Tablas**: Use las flechas para navegar, Enter para seleccionar
- **Campos de entrada**: Escriba directamente, Tab para moverse entre campos
- **Notificaciones**: Aparecen en la parte superior para informar sobre acciones exitosas o errores

---

## 6. Navegación y Atajos de Teclado

### Atajos Globales

- **`q`**: Salir de la aplicación (desde cualquier pantalla)
- **`Escape`**: Volver a la pantalla anterior
- **`Tab`**: Navegar al siguiente elemento
- **`Shift+Tab`**: Navegar al elemento anterior
- **`Enter`**: Activar botón o confirmar entrada
- **Flechas**: Navegar en tablas y listas

### Navegación con Mouse

Si su terminal lo soporta, también puede:
- Hacer clic en los botones
- Hacer clic en las filas de las tablas para seleccionarlas
- Hacer scroll en las áreas desplazables

---

## 7. Funcionalidades Principales

### 7.1. Cargar Procesos desde Archivo

Permite cargar procesos desde archivos en formato JSON, CSV o TXT ubicados en la carpeta `data/`.

**Pasos:**
1. Desde el menú principal, seleccione **"1. Cargar procesos desde archivo"**
2. Se abrirá una pantalla que muestra:
   - Una tabla con los archivos disponibles en `data/`
   - Un campo de entrada para escribir el nombre del archivo
3. Puede:
   - **Seleccionar un archivo de la tabla**: Use las flechas para navegar y Enter para seleccionar (el nombre se copiará al campo de entrada)
   - **Escribir el nombre manualmente**: Escriba el nombre del archivo en el campo de entrada
4. Haga clic en **"Cargar"** o presione Enter
5. Si la carga es exitosa, verá una notificación verde y regresará al menú principal
6. La tabla de procesos en el menú principal se actualizará automáticamente

**Nota**: Si el archivo no tiene extensión, se asumirá `.json` por defecto.

### 7.2. Crear Procesos Manualmente

Permite ingresar procesos uno por uno especificando sus características.

**Pasos:**
1. Desde el menú principal, seleccione **"2. Crear procesos manualmente"**
2. Complete el formulario:
   - **PID**: Identificador del proceso (ej: P1, P2, Proceso1)
   - **Tiempo de llegada**: Momento en que el proceso llega al sistema (número entero ≥ 0)
   - **Tiempo de ráfaga**: Tiempo de CPU requerido (número entero > 0)
   - **Prioridad**: Nivel de prioridad (número entero, menor = mayor prioridad)
3. Haga clic en **"Agregar"** para agregar el proceso a la lista
4. El proceso aparecerá en la tabla inferior
5. Para eliminar un proceso: Selecciónelo en la tabla y presione Enter
6. Use **"Limpiar"** para vaciar el formulario
7. Cuando termine, haga clic en **"Guardar y volver"** o **"Volver sin guardar"**

**Nota**: Los procesos se guardan en memoria. Para guardarlos en un archivo, use la opción de guardar antes de volver.

### 7.3. Casos de Prueba Predefinidos

Incluye tres conjuntos de prueba predefinidos y la opción de generar procesos aleatorios.

**Pasos:**
1. Desde el menú principal, seleccione **"3. Usar casos de prueba predefinidos"**
2. Se mostrarán 4 opciones:
   - **Conjunto 1**: Procesos Básicos (4 procesos)
     - P1(0,8,3), P2(1,4,1), P3(2,9,4), P4(3,5,2)
   - **Conjunto 2**: Procesos Variados (5 procesos)
     - P1(0,10,2), P2(2,3,1), P3(4,6,3), P4(6,1,1), P5(8,4,2)
   - **Conjunto 3**: Caso Personal (6 procesos)
     - P1(0,7,1), P2(2,4,3), P3(3,9,2), P4(5,5,1), P5(6,3,4), P6(8,6,2)
   - **Generar procesos aleatorios**: Abre un diálogo para especificar la cantidad (4-10)
3. Seleccione la opción deseada
4. Si selecciona "Generar procesos aleatorios":
   - Se abrirá un diálogo modal
   - Ingrese el número de procesos (entre 4 y 10)
   - Haga clic en **"Generar"**
5. Verá una notificación de confirmación y regresará al menú principal

### 7.4. Ejecutar Simulación

Ejecuta una simulación con un algoritmo específico y muestra los resultados detallados.

**Pasos:**
1. **Asegúrese de tener procesos cargados** (si no hay, verá una advertencia)
2. Desde el menú principal, seleccione **"4. Ejecutar simulación"**
3. Se mostrará una pantalla con los 5 algoritmos disponibles:
   - **1. FCFS (First Come First Served)**
   - **2. SJF (Shortest Job First - No apropiativo)**
   - **3. Round Robin (Quantum configurable)**
   - **4. Prioridades (sin desalojo)**
   - **5. Prioridades (con desalojo)**
4. Seleccione el algoritmo deseado
5. **Si selecciona Round Robin (opción 3)**:
   - Se abrirá un diálogo modal para configurar el quantum
   - Ingrese el valor del quantum (número entero > 0)
   - Haga clic en **"Aceptar"** o **"Cancelar"**
6. La simulación se ejecutará automáticamente
7. Se mostrará la **Pantalla de Resultados** con:
   - Información general (algoritmo, tiempo total, procesos completados)
   - **Diagrama de Gantt**: Visualización del orden de ejecución
   - **Tabla de Métricas por Proceso**: Detalles de cada proceso
   - **Métricas del Sistema**: Promedios y estadísticas generales
8. Use **"Volver"** para regresar al menú principal

**Nota**: Los resultados se guardan automáticamente en el historial.

### 7.5. Comparar Algoritmos

Ejecuta todos los algoritmos con los mismos procesos y muestra una tabla comparativa.

**Pasos:**
1. **Asegúrese de tener procesos cargados**
2. Desde el menú principal, seleccione **"5. Comparar todos los algoritmos"**
3. Se mostrará una pantalla con:
   - Campo para configurar el quantum de Round Robin (opcional, por defecto 4)
   - Botón **"Ejecutar comparativa"**
4. Ingrese el quantum deseado (o deje el valor por defecto)
5. Haga clic en **"Ejecutar comparativa"**
6. El sistema ejecutará todos los algoritmos automáticamente
7. Se mostrará la **Pantalla de Comparación** con:
   - **Tabla Comparativa**: Muestra todas las métricas de cada algoritmo
   - **Indicadores**: Estrellas (⭐) marcan los mejores valores en cada categoría
   - **Recomendación**: Sugerencia del mejor algoritmo para este caso específico
   - **Ranking**: Puntuación de cada algoritmo
8. Use **"Volver"** para regresar

**Interpretación de la Comparativa:**
- **Menores valores** en tiempos (retorno, espera, respuesta) = mejor rendimiento
- **Mayores valores** en CPU utilización y throughput = mejor rendimiento
- Los algoritmos con ⭐ tienen el mejor valor en esa métrica

### 7.6. Ver Historial de Resultados

Muestra las últimas 10 simulaciones realizadas.

**Pasos:**
1. Desde el menú principal, seleccione **"6. Ver historial de resultados"**
2. Se mostrará una tabla con las últimas 10 simulaciones, incluyendo:
   - **#**: Número de simulación
   - **Fecha/Hora**: Cuándo se ejecutó
   - **Algoritmo**: Algoritmo utilizado
   - **Procesos**: Cantidad de procesos simulados
   - **Tiempo Total**: Tiempo total de simulación
   - **T.Retorno Prom.**: Tiempo promedio de retorno
   - **CPU Util.**: Utilización de CPU
3. Use **"Volver"** para regresar

**Nota**: El historial se guarda en `data/simulation_history.json` y se mantiene entre sesiones.

### 7.7. Configurar Parámetros

Permite configurar parámetros por defecto del sistema.

**Pasos:**
1. Desde el menú principal, seleccione **"7. Configurar parámetros"**
2. Se mostrarán opciones para:
   - **Quantum por defecto para Round Robin**:
     - Ingrese el valor deseado en el campo
     - Haga clic en **"Guardar"**
   - **Modo de prioridad por defecto**:
     - **"Sin desalojo"**: Los procesos no pueden ser interrumpidos
     - **"Con desalojo"**: Los procesos pueden ser interrumpidos por otros de mayor prioridad
3. Verá notificaciones de confirmación cuando guarde cambios
4. Use **"Volver"** para regresar

---

## 8. Guía de Uso Paso a Paso

### Ejemplo 1: Simulación Básica con FCFS

1. **Iniciar el programa**:
   ```bash
   python main.py
   ```

2. **Cargar procesos**:
   - Haga clic en **"3. Usar casos de prueba predefinidos"**
   - Seleccione **"1. Conjunto 1: Procesos Básicos"**
   - Verá una notificación de confirmación

3. **Ejecutar simulación**:
   - Haga clic en **"4. Ejecutar simulación"**
   - Seleccione **"1. FCFS (First Come First Served)"**
   - La simulación se ejecutará automáticamente

4. **Ver resultados**:
   - Revise el **Diagrama de Gantt** para ver el orden de ejecución
   - Examine la **Tabla de Métricas por Proceso**
   - Revise las **Métricas del Sistema**

5. **Regresar**:
   - Haga clic en **"Volver"** o presione Escape

### Ejemplo 2: Comparación de Algoritmos

1. **Cargar procesos**:
   - Use **"3. Usar casos de prueba predefinidos"** → **"Conjunto 2"**

2. **Comparar algoritmos**:
   - Haga clic en **"5. Comparar todos los algoritmos"**
   - Ingrese el quantum para Round Robin (ej: 4) o deje el valor por defecto
   - Haga clic en **"Ejecutar comparativa"**

3. **Analizar resultados**:
   - Revise la tabla comparativa
   - Identifique qué algoritmo tiene más estrellas (⭐)
   - Lea la recomendación al final
   - Compare los valores de las métricas

4. **Interpretar**:
   - Busque el algoritmo con menores tiempos de espera y retorno
   - Verifique la utilización de CPU y throughput
   - Considere la recomendación del sistema

### Ejemplo 3: Cargar desde Archivo Personalizado

1. **Preparar archivo**:
   - Cree un archivo JSON en la carpeta `data/` con el formato:
   ```json
   [
     {"pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 1},
     {"pid": "P2", "arrival_time": 2, "burst_time": 3, "priority": 2}
   ]
   ```
   - Guarde el archivo como `mi_conjunto.json` en la carpeta `data/`

2. **Cargar archivo**:
   - Haga clic en **"1. Cargar procesos desde archivo"**
   - Seleccione el archivo de la tabla o escriba `mi_conjunto.json`
   - Haga clic en **"Cargar"**

3. **Verificar carga**:
   - Verá una notificación de confirmación
   - La tabla de procesos en el menú principal mostrará los procesos cargados

4. **Simular**:
   - Ejecute la simulación con el algoritmo deseado

### Ejemplo 4: Crear Procesos Personalizados

1. **Abrir editor de procesos**:
   - Haga clic en **"2. Crear procesos manualmente"**

2. **Agregar procesos**:
   - Complete el formulario para cada proceso:
     - PID: `MiProceso1`
     - Tiempo de llegada: `0`
     - Tiempo de ráfaga: `10`
     - Prioridad: `1`
   - Haga clic en **"Agregar"**
   - Repita para más procesos

3. **Gestionar procesos**:
   - Para eliminar: Seleccione el proceso en la tabla y presione Enter
   - Para limpiar el formulario: Haga clic en **"Limpiar"**

4. **Finalizar**:
   - Haga clic en **"Guardar y volver"** para mantener los procesos en memoria

---

## 9. Formato de Archivos

### Formato JSON (Recomendado)

```json
[
  {
    "pid": "P1",
    "arrival_time": 0,
    "burst_time": 8,
    "priority": 3
  },
  {
    "pid": "P2",
    "arrival_time": 1,
    "burst_time": 4,
    "priority": 1
  }
]
```

### Formato CSV

```csv
PID,Arrival_Time,Burst_Time,Priority
P1,0,8,3
P2,1,4,1
P3,2,9,4
P4,3,5,2
```

### Formato TXT (con espacios o tabs)

```
P1 0 8 3
P2 1 4 1
P3 2 9 4
P4 3 5 2
```

O con tabs:

```
P1	0	8	3
P2	1	4	1
```

### Campos Requeridos

- **pid**: Identificador único del proceso (texto, ej: "P1", "Proceso1")
- **arrival_time**: Tiempo de llegada (entero ≥ 0)
- **burst_time**: Tiempo de ráfaga de CPU (entero > 0)
- **priority**: Prioridad del proceso (entero, menor número = mayor prioridad)

**Nota**: En CSV y TXT, si falta la prioridad, se asume 1 por defecto.

---

## 10. Interpretación de Resultados

### Pantalla de Resultados Individual

Cuando ejecuta una simulación individual, verá:

#### Información General
- **Algoritmo**: Nombre del algoritmo utilizado
- **Tiempo total**: Tiempo total de simulación
- **Procesos completados**: Cantidad de procesos que terminaron

#### Diagrama de Gantt

Muestra visualmente el orden de ejecución:
- Cada bloque representa un proceso ejecutándose
- Los números debajo indican los tiempos acumulados
- Permite ver el orden de ejecución y los cambios de contexto
- Útil para entender la secuencia temporal

#### Métricas por Proceso

Tabla que muestra para cada proceso:
- **PID**: Identificador del proceso
- **Llegada**: Tiempo en que el proceso llegó al sistema
- **Ráfaga**: Tiempo de CPU requerido
- **Prioridad**: Nivel de prioridad
- **Fin**: Tiempo en que el proceso terminó
- **Retorno (Turnaround Time)**: Tiempo total desde llegada hasta finalización
- **Espera (Waiting Time)**: Tiempo que el proceso estuvo en cola de listos
- **Respuesta (Response Time)**: Tiempo hasta la primera ejecución

#### Métricas del Sistema

- **Tiempo Promedio de Retorno**: Promedio de turnaround time de todos los procesos (menor es mejor)
- **Tiempo Promedio de Espera**: Promedio de waiting time (menor es mejor)
- **Tiempo Promedio de Respuesta**: Promedio de response time (menor es mejor)
- **Utilización de CPU**: Porcentaje de tiempo que la CPU estuvo ocupada (mayor es mejor, idealmente cerca de 100%)
- **Throughput**: Número de procesos completados por unidad de tiempo (mayor es mejor)

### Pantalla de Comparación

En la comparativa de algoritmos:

- **Tabla Comparativa**: Muestra todas las métricas lado a lado
- **Indicadores ⭐**: Marcan el mejor valor en cada categoría
- **Recomendación**: El sistema sugiere el mejor algoritmo basado en un ranking
- **Ranking**: Puntuación de cada algoritmo (mayor es mejor)

**Cómo interpretar**:
1. Busque los algoritmos con más estrellas (⭐)
2. Compare los valores numéricos
3. Considere el contexto: ¿Qué métrica es más importante para su caso?
4. Revise la recomendación del sistema

---

## 11. Solución de Problemas

### Problema: "Error de importación" al iniciar

**Síntomas**: El programa no inicia y muestra un error de importación.

**Solución**:
1. Verifique que las dependencias estén instaladas:
   ```bash
   pip install -r requirements.txt
   ```
2. Verifique la versión de Python:
   ```bash
   python --version
   ```
   Debe ser 3.8 o superior.

### Problema: "No hay procesos cargados"

**Síntomas**: Al intentar ejecutar una simulación, aparece una advertencia.

**Solución**:
- Use **"3. Usar casos de prueba predefinidos"** para cargar procesos de prueba
- O cargue un archivo desde **"1. Cargar procesos desde archivo"**
- O cree procesos manualmente con **"2. Crear procesos manualmente"**

### Problema: "Archivo no encontrado"

**Síntomas**: Al intentar cargar un archivo, aparece un error.

**Solución**:
1. Verifique que el archivo esté en la carpeta `data/`
2. Verifique que el nombre del archivo sea correcto (incluyendo extensión: `.json`, `.csv`, o `.txt`)
3. Verifique el formato del archivo según la sección [Formato de Archivos](#9-formato-de-archivos)
4. Asegúrese de que el archivo no esté abierto en otro programa

### Problema: "Valores inválidos" al crear procesos

**Síntomas**: Al intentar agregar un proceso, aparece un error.

**Solución**:
- Asegúrese de que los tiempos sean números enteros positivos
- El PID no puede estar vacío
- Verifique que todos los campos estén completos
- Los valores deben ser números (no texto) excepto el PID

### Problema: La interfaz no se muestra correctamente

**Síntomas**: La interfaz se ve distorsionada o no se renderiza bien.

**Solución**:
1. Use una terminal moderna compatible:
   - **Windows**: Windows Terminal (recomendado) o PowerShell
   - **Linux**: Terminal moderno (gnome-terminal, konsole, etc.)
   - **macOS**: Terminal.app o iTerm2
2. Verifique que la terminal tenga soporte para colores y caracteres especiales
3. Redimensione la ventana de la terminal si es necesario (mínimo 80x24 caracteres)
4. Asegúrese de que la fuente de la terminal soporte caracteres Unicode

### Problema: Los resultados no se guardan en el historial

**Síntomas**: El historial está vacío o no se actualiza.

**Solución**:
1. Verifique que exista la carpeta `data/`
2. Verifique permisos de escritura en el directorio
3. Asegúrese de que el archivo `data/simulation_history.json` no esté bloqueado
4. Las simulaciones se guardan automáticamente al ejecutarlas

### Problema: No puedo navegar con el teclado

**Síntomas**: Las teclas no responden o la navegación no funciona.

**Solución**:
1. Use **Tab** para navegar entre elementos
2. Use **Flechas** para navegar en tablas y listas
3. Use **Enter** para activar botones o seleccionar elementos
4. Use **Escape** para volver atrás
5. Si su terminal lo soporta, también puede usar el mouse

### Problema: El diagrama de Gantt se ve mal

**Síntomas**: El diagrama de Gantt no se muestra correctamente.

**Solución**:
1. Asegúrese de que su terminal soporte caracteres Unicode (┌, ─, ┐, │, └, ┘)
2. Use una fuente que soporte estos caracteres (como Consolas, Courier New, o fuentes monospace modernas)
3. Si el problema persiste, los datos numéricos en la tabla de resultados son igualmente válidos

### Problema: La simulación tarda mucho

**Síntomas**: La simulación parece congelarse.

**Solución**:
- Esto es normal para conjuntos grandes de procesos
- El sistema está ejecutando la simulación en segundo plano
- Espere a que aparezca la pantalla de resultados
- Si realmente se congela, presione `Ctrl+C` y reinicie

---

## Apéndice A: Algoritmos Implementados

### FCFS (First Come First Served)
- **Tipo**: No apropiativo
- **Criterio**: Orden de llegada (primero en llegar, primero en ser servido)
- **Ventajas**: Simple, sin inanición, fácil de implementar
- **Desventajas**: Puede tener alto tiempo de espera promedio, no es óptimo para tiempos de ráfaga variables
- **Mejor para**: Sistemas simples, procesos con tiempos similares

### SJF (Shortest Job First)
- **Tipo**: No apropiativo
- **Criterio**: Menor tiempo de ráfaga primero
- **Ventajas**: Minimiza tiempo de espera promedio, óptimo para minimizar tiempo de retorno promedio
- **Desventajas**: Puede causar inanición de procesos largos, requiere conocer el tiempo de ráfaga
- **Mejor para**: Sistemas batch, cuando se conocen los tiempos de ejecución

### Round Robin
- **Tipo**: Apropiativo
- **Criterio**: Quantum fijo, rotación circular
- **Ventajas**: Justo, buen tiempo de respuesta, no causa inanición
- **Desventajas**: Overhead por cambios de contexto, el quantum debe elegirse cuidadosamente
- **Mejor para**: Sistemas interactivos, time-sharing
- **Parámetro**: Quantum (tiempo que cada proceso ejecuta antes de ser desalojado)

### Prioridades (sin desalojo)
- **Tipo**: No apropiativo
- **Criterio**: Mayor prioridad primero (menor número = mayor prioridad)
- **Ventajas**: Permite priorizar procesos importantes, simple
- **Desventajas**: Puede causar inanición de procesos de baja prioridad
- **Mejor para**: Sistemas donde algunos procesos son más críticos

### Prioridades (con desalojo)
- **Tipo**: Apropiativo
- **Criterio**: Mayor prioridad, con interrupción cuando llega un proceso de mayor prioridad
- **Ventajas**: Respuesta rápida a procesos de alta prioridad, más justo que sin desalojo
- **Desventajas**: Mayor overhead por cambios de contexto, posible inanición
- **Mejor para**: Sistemas en tiempo real, donde la prioridad es crítica

---

## Apéndice B: Ejemplos de Archivos

### ejemplo1.json
```json
[
  {"pid": "P1", "arrival_time": 0, "burst_time": 8, "priority": 3},
  {"pid": "P2", "arrival_time": 1, "burst_time": 4, "priority": 1},
  {"pid": "P3", "arrival_time": 2, "burst_time": 9, "priority": 4},
  {"pid": "P4", "arrival_time": 3, "burst_time": 5, "priority": 2}
]
```

### ejemplo2.csv
```csv
PID,Arrival_Time,Burst_Time,Priority
P1,0,10,2
P2,2,3,1
P3,4,6,3
P4,6,1,1
P5,8,4,2
```

### ejemplo3.txt
```
P1 0 7 1
P2 2 4 3
P3 3 9 2
P4 5 5 1
P5 6 3 4
P6 8 6 2
```

---

## Contacto y Soporte

**Equipo 7:**
- Maria Marin (30.709.208)
- Laura Martínez (30.346.546)
- Andrea Gamarra (28.492.138)

**Universidad Católica Andrés Bello**  
**Facultad de Ingeniería - Escuela de Informática**  
**Sistemas Operativos**

---

## Versión del Manual

**Versión**: 2.0  
**Fecha**: Diciembre 2024  
**Última actualización**: Diciembre 2024  
**Interfaz**: Textual (TUI)

---

*Este manual fue generado para el proyecto de Sistemas Operativos de la Universidad Católica Andrés Bello. La interfaz utiliza Textual, un framework moderno para aplicaciones de terminal interactivas.*
