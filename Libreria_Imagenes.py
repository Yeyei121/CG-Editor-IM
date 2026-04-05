"""
Librería de procesamiento de imágenes usando operaciones de matrices.

Contiene todas las funciones de manipulación de imagen utilizadas
por el Editor de Imágenes. Sin código ejecutable a nivel de módulo.
"""
import numpy as np
from PIL import Image

def estandarizar_imagen(img):
    """
    Estandariza cualquier imagen (PNG o JPG) a formato uint8 (0-255).

    Args:
        img: Array numpy de la imagen.

    Returns:
        Array numpy uint8 con valores entre 0 y 255.
    """
    img = np.copy(img)
    if np.issubdtype(img.dtype, np.floating):
        img = (img * 255).clip(0, 255).astype(np.uint8)
    return img


def invertir_imagen2(img):
    """Invierte los colores de la imagen (negativo). Preserva canal alpha."""
    img = estandarizar_imagen(img)
    resultado = np.copy(img)
    resultado[:, :, :3] = 255 - img[:, :, :3]
    return resultado


def capa_roja(img1):
    """Extrae la capa roja de la imagen, poniendo a cero los demás canales."""
    img1 = estandarizar_imagen(img1)
    capa_r = np.copy(img1)
    capa_r[:, :, 1] = capa_r[:, :, 2] = 0
    return capa_r


def capa_verde(img1):
    """Extrae la capa verde de la imagen, poniendo a cero los demás canales."""
    img1 = estandarizar_imagen(img1)
    capa_v = np.copy(img1)
    capa_v[:, :, 0] = capa_v[:, :, 2] = 0
    return capa_v


def capa_azul(img1):
    """Extrae la capa azul de la imagen, poniendo a cero los demás canales."""
    img1 = estandarizar_imagen(img1)
    capa_a = np.copy(img1)
    capa_a[:, :, 1] = capa_a[:, :, 0] = 0
    return capa_a


def capa_cyan(img1):
    """Extrae la capa cyan de la imagen (verde + azul)."""
    img1 = estandarizar_imagen(img1)
    capa_c = np.copy(img1)
    capa_c[:, :, 0] = 0
    return capa_c


def capa_magenta(img1):
    """Extrae la capa magenta de la imagen (rojo + azul)."""
    img1 = estandarizar_imagen(img1)
    capa_m = np.copy(img1)
    capa_m[:, :, 1] = 0
    return capa_m


def capa_amarilla(img1):
    """Extrae la capa amarilla de la imagen (rojo + verde)."""
    img1 = estandarizar_imagen(img1)
    capa_y = np.copy(img1)
    capa_y[:, :, 2] = 0
    return capa_y


def reconstruir_imagen(capa_r, capa_g, capa_b):
    """
    Reconstruye una imagen a partir de sus tres capas RGB.

    Args:
        capa_r: Array numpy con solo el canal rojo.
        capa_g: Array numpy con solo el canal verde.
        capa_b: Array numpy con solo el canal azul.

    Returns:
        Array numpy de la imagen reconstruida.
    """
    return capa_r[:, :, :] + capa_g[:, :, :] + capa_b[:, :, :]


def fusionar_imagenes(img1, img2, factor=0.5):
    """
    Fusiona dos imágenes con un factor de mezcla.

    Args:
        img1: Primera imagen (numpy array).
        img2: Segunda imagen (numpy array).
        factor: Factor de mezcla (0.0 a 1.0). Default 0.5.

    Returns:
        Imagen fusionada como numpy array uint8.
    """
    img1 = estandarizar_imagen(img1)
    img2 = estandarizar_imagen(img2)
    img1 = np.copy(img1)
    img2 = np.copy(img2)

    # Igualar tamaño si las dimensiones alto/ancho son diferentes
    if img1.shape[:2] != img2.shape[:2]:
        h, w = img1.shape[:2]
        img2 = np.array(
            Image.fromarray(img2).resize((w, h))
        )

    # Extraer solo RGB de ambas
    rgb1 = img1[:, :, :3].astype(np.float32)
    rgb2 = img2[:, :, :3].astype(np.float32)

    # Manejo del canal alpha si existe en alguna de las imágenes
    if img1.shape[2] == 4:
        alpha = img1[:, :, 3].astype(np.float32) / 255.0
        alpha = alpha[:, :, np.newaxis]
        fusion = alpha * (factor * rgb1 + (1 - factor) * rgb2) + (1 - alpha) * rgb2
    elif img2.shape[2] == 4:
        alpha = img2[:, :, 3].astype(np.float32) / 255.0
        alpha = alpha[:, :, np.newaxis]
        fusion = alpha * (factor * rgb1 + (1 - factor) * rgb2) + (1 - alpha) * rgb1
    else:
        fusion = factor * rgb1 + (1 - factor) * rgb2

    fusion = np.clip(fusion, 0, 255).astype(np.uint8)
    return fusion


def promedio(img1):
    """Convierte a escala de grises usando técnica de promedio."""
    img1 = estandarizar_imagen(img1)
    img1 = np.copy(img1)
    return img1[:, :, 0] + img1[:, :, 1] + img1[:, :, 2] / 3


def luminosidad(img1):
    """Convierte a escala de grises con ponderación de luminosidad (BT.601)."""
    img1 = estandarizar_imagen(img1)
    img1 = np.copy(img1)
    return 0.299 * img1[:, :, 0] + 0.587 * img1[:, :, 1] + 0.114 * img1[:, :, 2]


def midgray(img1):
    """Convierte a escala de grises usando promedio de máximo y mínimo por píxel."""
    img1 = estandarizar_imagen(img1)
    img1 = np.copy(img1)
    matriz_max = np.maximum(np.maximum(img1[:, :, 0], img1[:, :, 1]), img1[:, :, 2])
    matriz_min = np.minimum(np.minimum(img1[:, :, 0], img1[:, :, 1]), img1[:, :, 2])
    return (matriz_max + matriz_min) / 2


def ajuste_brillo(img1, brillo=0):
    """
    Ajusta el brillo global de la imagen.

    Args:
        img1: Imagen numpy array.
        brillo: Valor de brillo a sumar (-255 a 255).

    Returns:
        Imagen con brillo ajustado como uint8.
    """
    img1 = estandarizar_imagen(img1)
    img1 = np.copy(img1)
    img1 = img1.astype(np.float32) + brillo
    img1 = np.clip(img1, 0, 255).astype(np.uint8)
    return img1


def ajuste_brillo_canal(img1, canal, brillo):
    """
    Ajusta el brillo de un canal específico.

    Args:
        img1: Imagen numpy array.
        canal: "Red", "Green" o "Blue".
        brillo: Valor de brillo a sumar (-255 a 255).

    Returns:
        Imagen con brillo de canal ajustado como uint8.
    """
    img1 = estandarizar_imagen(img1)
    img_copy = img1.astype(np.float32).copy()
    if canal == "Red":
        img_copy[:, :, 0] = np.clip(img_copy[:, :, 0] + brillo, 0, 255)
    elif canal == "Green":
        img_copy[:, :, 1] = np.clip(img_copy[:, :, 1] + brillo, 0, 255)
    elif canal == "Blue":
        img_copy[:, :, 2] = np.clip(img_copy[:, :, 2] + brillo, 0, 255)
    return img_copy.astype(np.uint8)


def binarizacion(img1, umbral):
    """
    Binariza la imagen según un umbral.

    Args:
        img1: Imagen numpy array.
        umbral: Valor de umbral (0-255).

    Returns:
        Imagen binarizada (0 o 255) como uint8.
    """
    img_gray = luminosidad(img1)
    umbral = np.clip(umbral, 0, 255)
    img_bin = np.where(img_gray >= umbral, 255, 0).astype(np.uint8)
    return img_bin


def traslacion(img1, dx, dy):
    """
    Traslada la imagen en dx y dy píxeles.

    Args:
        img1: Imagen numpy array.
        dx: Desplazamiento horizontal (+ derecha, - izquierda).
        dy: Desplazamiento vertical (+ abajo, - arriba).

    Returns:
        Imagen trasladada.
    """
    h, w = img1.shape[:2]
    traslada = np.zeros_like(img1)

    #Coordenadas en la imagen destino
    x1d = max(0, dx)
    y1d = max(0, dy)
    x2d = min(w, w + dx)
    y2d = min(h, h + dy)

    #Coordenadas correspondientes en la imagen origen 
    x1s = max(0, -dx)
    y1s = max(0, -dy)
    x2s = x1s + (x2d - x1d)
    y2s = y1s + (y2d - y1d)

    #Copia solo si hay intersección válida
    if x2d > x1d and y2d > y1d:
        traslada[y1d:y2d, x1d:x2d] = img1[y1s:y2s, x1s:x2s]

    return traslada


def recorte(img1, xIni, xFin, yIni, yFin):
    """
    Recorta la imagen en las coordenadas especificadas.

    Args:
        img1: Imagen numpy array.
        xIni, xFin: Rango horizontal.
        yIni, yFin: Rango vertical.

    Returns:
        Imagen recortada, o la original si las coordenadas son inválidas.
    """
    h, w = img1.shape[:2]
    if xIni < xFin and yIni < yFin and xIni <= w and yIni <= h and xIni >= 0 and yIni >= 0:
        return img1[yIni:yFin, xIni:xFin]
    else:
        return img1


def rotacion(img1, angulo):
    """
    Rota la imagen por un ángulo dado en grados.

    Args:
        img1: Imagen numpy array.
        angulo: Ángulo de rotación en grados.

    Returns:
        Imagen rotada.
    """
    img1 = estandarizar_imagen(img1)
    img1_pil = Image.fromarray(img1)
    rotada = img1_pil.rotate(angulo, resample=Image.BICUBIC, expand=True)
    rotada = np.array(rotada)
    return rotada


def reducir_resolucion(img1, factor):
    """
    Reduce la resolución de la imagen por un factor.

    Args:
        img1: Imagen numpy array.
        factor: Factor de reducción (entero > 0).

    Returns:
        Imagen con resolución reducida.
    """
    try:
        factor = int(factor)
        if factor > 0:
            return img1[::factor, ::factor]
        else:
            return img1
    except ValueError:
        return img1


def zoom_central(img1, zoom_area, zoom_factor):
    """
    Aplica zoom a la región central de la imagen.

    Args:
        img1: Imagen numpy array.
        zoom_area: Tamaño del área central a recortar.
        zoom_factor: Factor de zoom (repetición de píxeles).

    Returns:
        Imagen con zoom aplicado.
    """
    h, w = img1.shape[:2]

    start_row = h // 2 - zoom_area // 2
    end_row = h // 2 + zoom_area // 2
    start_col = w // 2 - zoom_area // 2
    end_col = w // 2 + zoom_area // 2

    #Recortar región central
    recorte_central = recorte(img1, start_col, end_col, start_row, end_row)
    
    #Zoom repitiendo pixeles
    zoomed_area = np.kron(recorte_central, np.ones((zoom_factor, zoom_factor, 1)))
    
    #Convertir a mismo tipo de dato que la imagen original
    zoomed_area = zoomed_area.astype(img1.dtype)

    return zoomed_area


def histograma_de_imagen(img1):
    """
    Muestra el histograma RGB de la imagen.

    Args:
        img1: Imagen numpy array.
    """
    import matplotlib.pyplot as plt

    img1 = estandarizar_imagen(img1)

    # Separar canales RGB
    R = img1[:, :, 0]
    G = img1[:, :, 1]
    B = img1[:, :, 2]

    # Crear figura
    plt.figure(figsize=(10, 6))

    # Histograma canal rojo
    plt.subplot(3, 1, 1)
    plt.hist(R.ravel(), bins=256, color='red')
    plt.title('Histograma Canal Rojo')
    plt.xlim(0, 255)

    # Histograma canal verde
    plt.subplot(3, 1, 2)
    plt.hist(G.ravel(), bins=256, color='green')
    plt.title('Histograma Canal Verde')
    plt.xlim(0, 255)

    # Histograma canal azul
    plt.subplot(3, 1, 3)
    plt.hist(B.ravel(), bins=256, color='blue')
    plt.title('Histograma Canal Azul')
    plt.xlim(0, 255)

    plt.tight_layout()
    plt.show()


def mostrar_imagen(img1, img2, titulo="", grises=None):
    """
    Muestra la imagen original y la modificada lado a lado.

    Args:
        img1: Imagen original.
        img2: Imagen modificada.
        titulo: Título de la imagen modificada.
        grises: Si no es None, muestra img2 en escala de grises.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img1)
    plt.title("Imagen Original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    if grises is not None:
        plt.imshow(img2, cmap="gray")
    else:
        plt.imshow(img2)
    plt.title(f"Imagen: {titulo}")
    plt.axis("off")

    plt.show()


def info_imagen(img):
    """
    Retorna información de la imagen como diccionario.

    Args:
        img: Array numpy de la imagen.

    Returns:
        dict con shape, dtype, size, max y min de la imagen.
    """
    return {
        "shape": img.shape,
        "dtype": str(img.dtype),
        "size": img.size,
        "max": int(np.max(img)),
        "min": int(np.min(img)),
    }
