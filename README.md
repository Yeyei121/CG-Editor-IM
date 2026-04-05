# CG-Editor-IM

Editor de imagenes de escritorio hecho en Python con Tkinter. Permite cargar una imagen, aplicar operaciones de color y transformaciones geometricas, visualizar cambios en tiempo real, consultar histograma e informacion tecnica, y guardar el resultado.

## Para que sirve

Este programa sirve para:
- Practicar procesamiento digital de imagenes con operaciones matriciales.
- Editar imagenes de forma local (sin internet) con una interfaz grafica simple.
- Explorar conceptos como brillo, binarizacion, capas RGB/CMY, grises, rotacion, traslacion, recorte, reduccion de resolucion y zoom.
- Entender una arquitectura modular separada por UI, logica de aplicacion, modelo e historial.

## Caracteristicas principales

- Carga y guardado de imagenes (JPG, JPEG, PNG).
- Vista doble: imagen original y resultado.
- Historial con deshacer/rehacer.
- Reset al estado original.
- Preview en vivo para operaciones con sliders.
- Filtro de inversion de color y reconstruccion RGB.
- Capas de color RGB y CMY.
- Escala de grises por tres metodos.
- Transformaciones geometricas.
- Dialogos para fusion y recorte.
- Histograma RGB e informacion de la imagen.

## Arquitectura de la aplicacion

La app sigue un enfoque modular por capas:

1. Punto de entrada
- `main.py`: inicia splash de arranque y ejecuta la aplicacion.

2. Capa de aplicacion (controlador)
- `app/application.py`: coordina eventos de UI, modelo, historial y procesador.
- Maneja atajos, operaciones de archivo, undo/redo, reset y ejecucion de operaciones.

3. Capa de dominio / nucleo
- `core/image_model.py`: estado de imagen original/actual + patron observador.
- `core/history_manager.py`: stacks para deshacer y rehacer con limite configurable.
- `core/image_processor.py`: fachada para aplicar operaciones y utilidades (histograma, info, fusion).
- `core/operations/`: operaciones encapsuladas por tipo (ajuste, color, grises, transformaciones), todas basadas en `BaseOperation`.

4. Capa de interfaz (UI)
- `ui/main_window.py`: layout general de la ventana.
- `ui/toolbar.py`: barra lateral de herramientas.
- `ui/control_panel.py`: sliders y controles por secciones.
- `ui/canvas_panel.py`: render de imagen original y resultado, con zoom.
- `ui/status_bar.py`: estado y metadatos de la imagen.
- `ui/dialogs/`: dialogos de fusion y recorte.

5. Capa de utilidades
- `utils/image_utils.py`: conversion PIL <-> NumPy <-> PhotoImage y guardado/carga.
- `utils/animation_utils.py`: splash, toast y animaciones de UI.

6. Libreria de procesamiento
- `Libreria_Imagenes.py`: implementacion de funciones de procesamiento con NumPy/PIL (y Matplotlib para histograma).

## Flujo general

1. El usuario carga una imagen desde la UI.
2. `Application` actualiza `ImageModel`.
3. `ImageModel` notifica observadores.
4. UI se refresca automaticamente (`CanvasPanel`, `StatusBar`, topbar).
5. Al aplicar una operacion:
- Se guarda estado en `HistoryManager`.
- Se ejecuta la operacion en `ImageProcessor`.
- Se actualiza `ImageModel` con el resultado.

## Transformaciones y operaciones disponibles

### Ajustes
- Brillo global (`ajuste_brillo`).
- Brillo por canal R/G/B (`ajuste_brillo_canal`).
- Binarizacion por umbral (`binarizacion`).

### Color
- Invertir colores.
- Capa Roja, Verde, Azul.
- Capa Cyan, Magenta, Amarilla.
- Reconstruccion de imagen a partir de capas RGB.

### Escala de grises
- Promedio.
- Luminosidad (ponderacion tipo BT.601).
- Midgray (promedio entre maximo y minimo por pixel).

### Geometricas
- Rotacion.
- Traslacion en X/Y.
- Recorte por coordenadas.
- Reduccion de resolucion por factor.
- Zoom central por area + factor.

### Utilidades de analisis
- Histograma RGB.
- Informacion de imagen (shape, dtype, size, min, max).
- Fusion de dos imagenes con factor de mezcla.

## Requerimientos

### Software
- Python 3.10 o superior (recomendado 3.11+).
- pip.
- SO compatible con Tkinter (Windows, Linux, macOS).

### Dependencias de Python
Instala estas librerias:
- `numpy`
- `Pillow`
- `matplotlib`

Tkinter normalmente ya viene con Python en Windows.

## Instalacion

En la raiz del proyecto:

```bash
python -m venv .venv
```

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
pip install numpy Pillow matplotlib
```

### Linux/macOS

```bash
source .venv/bin/activate
pip install numpy Pillow matplotlib
```

## Ejecucion

Con el entorno activo, desde la raiz del proyecto:

```bash
python main.py
```

Opcional: ajustar duracion del splash al arrancar.

### Windows (PowerShell)

```powershell
$env:EDITOR_SPLASH_MS = "1500"
python main.py
```

### Linux/macOS

```bash
EDITOR_SPLASH_MS=1500 python main.py
```

## Atajos de teclado

- `Ctrl+O`: abrir imagen.
- `Ctrl+S`: guardar imagen.
- `Ctrl+Z`: deshacer.
- `Ctrl+Y`: rehacer.
- `Ctrl+R`: restaurar imagen original.

## Estructura del proyecto

```text
CG-Editor-IM/
|-- main.py
|-- Libreria_Imagenes.py
|-- app/
|   |-- application.py
|   `-- config.py
|-- core/
|   |-- history_manager.py
|   |-- image_model.py
|   |-- image_processor.py
|   `-- operations/
|       |-- base_operation.py
|       |-- adjustment_operations.py
|       |-- color_operations.py
|       |-- grayscale_operations.py
|       `-- transform_operations.py
|-- ui/
|   |-- main_window.py
|   |-- toolbar.py
|   |-- control_panel.py
|   |-- canvas_panel.py
|   |-- status_bar.py
|   `-- dialogs/
|       |-- fusion_dialog.py
|       `-- recorte_dialog.py
|-- utils/
|   |-- image_utils.py
|   `-- animation_utils.py
`-- assets/
    `-- icons/
```

## Notas tecnicas

- La app usa arrays NumPy como formato interno de imagen.
- El modelo mantiene dos estados: original y actual.
- Si una operacion produce imagen en 2D (grises), se normaliza a 3 canales para mantener compatibilidad visual en la UI.
- El historial tiene limite de pasos (`HISTORY_MAX_STEPS`, por defecto 20).


