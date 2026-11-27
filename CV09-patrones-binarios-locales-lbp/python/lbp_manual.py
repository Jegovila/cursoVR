import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from skimage import data, color, io


def calcular_lbp_manual(imagen_gris):
    """
    Calcula el Local Binary Pattern (P=8, R=1) de forma manual
    """
    filas, columnas = imagen_gris.shape
    # Creamos una matriz vacía para guardar el resultado (los bordes quedan en 0)
    lbp_imagen = np.zeros((filas, columnas), dtype=np.uint8)
    
    # Definimos los pesos (potencias de 2) en sentido horario empezando arriba-izquierda
    pesos = np.array([
        [1,   2,  4],
        [128, 0,  8],
        [64, 32, 16]
    ], dtype=np.uint8)
    
    # Recorremos cada píxel interior de la imagen (evitando el borde de 1 píxel)
    for i in range(1, filas - 1):
        for j in range(1, columnas - 1):
            # 1. Extraer la vecindad 3x3
            vecindad = imagen_gris[i-1:i+2, j-1:j+2]
            pixel_central = imagen_gris[i, j]
            
            # 2. Umbralización: 1 si el vecino >= central, 0 si es menor
            matriz_binaria = (vecindad >= pixel_central).astype(np.uint8)
            
            # 3. Multiplicar por los pesos y sumar para obtener el valor decimal (0-255)
            valor_lbp = np.sum(matriz_binaria * pesos)
            
            lbp_imagen[i, j] = valor_lbp
            
    return lbp_imagen

def calcular_histograma_manual(lbp_region):
    """Calcula el histograma de 256 bins manualmente sin usar np.histogram."""
    # Ignoramos los bordes de 1 píxel que quedaron en 0 por el padding
    interior = lbp_region[1:-1, 1:-1].flatten()
    histograma = np.zeros(256, dtype=int)
    for valor in interior:
        histograma[valor] += 1
    return histograma

def obtener_detalle_pixel(ventana_3x3):
    """Extrae los pasos intermedios de un solo píxel para mostrarlos en clase."""
    pesos = np.array([[1, 2, 4], [128, 0, 8], [64, 32, 16]])
    centro = ventana_3x3[1, 1]
    binaria = (ventana_3x3 >= centro).astype(int)
    productos = binaria * pesos
    total = np.sum(productos)
    return centro, binaria, pesos, total

# =====================================================================
# 2. CARGA DE IMAGEN Y CONFIGURACIÓN DE LA INTERFAZ INTERACTIVA
# =====================================================================

imagen = data.brick().astype(np.uint8) # brick, grass, gravel
#imagen = (color.rgb2gray(io.imread('./texturas.webp')) * 255).astype(np.uint8)

# Configuración de la figura de Matplotlib
fig = plt.figure(figsize=(14, 8))
fig.canvas.manager.set_window_title('Demostración Interactiva: Local Binary Patterns (LBP)')
plt.suptitle("Arrastra el ratón sobre la imagen original para analizar una textura", fontsize=14, fontweight='bold')

# Definimos la cuadrícula de gráficos
ax_orig = plt.subplot2grid((2, 3), (0, 0), rowspan=2) # Imagen completa a la izquierda
ax_roi  = plt.subplot2grid((2, 3), (0, 1))            # Recorte original
ax_lbp  = plt.subplot2grid((2, 3), (0, 2))            # Recorte LBP
ax_hist = plt.subplot2grid((2, 3), (1, 1))            # Histograma
ax_math = plt.subplot2grid((2, 3), (1, 2))            # Explicación matemática 3x3

# Mostrar imagen original
ax_orig.imshow(imagen, cmap='gray', vmin=0, vmax=255)
ax_orig.set_title("1. Imagen Original\n(Haz clic y arrastra)")
ax_orig.axis('off')

# Textos iniciales en los paneles
ax_roi.set_title("2. Región Seleccionada (ROI)")
ax_roi.axis('off')
ax_lbp.set_title("3. Resultado LBP (Textura)")
ax_lbp.axis('off')
ax_hist.set_title("4. Histograma LBP (0 - 255)")
ax_math.axis('off')

# =====================================================================
# 3. FUNCIÓN DE ACTUALIZACIÓN AL SELECCIONAR REGIÓN (ROI)
# =====================================================================
def al_seleccionar_region(eclick, erelease):
    # Obtener coordenadas del rectángulo seleccionado
    x1, y1 = int(min(eclick.xdata, erelease.xdata)), int(min(eclick.ydata, erelease.ydata))
    x2, y2 = int(max(eclick.xdata, erelease.xdata)), int(max(eclick.ydata, erelease.ydata))
    
    # Evitar selecciones demasiado pequeñas (mínimo 5x5 píxeles)
    if (x2 - x1) < 5 or (y2 - y1) < 5:
        return
        
    # Recortar la región original y la región LBP
    roi_gris = imagen[y1:y2, x1:x2]
    # Recalculamos sobre el ROI para demostrar que es local
    roi_lbp = calcular_lbp_manual(roi_gris)
    hist = calcular_histograma_manual(roi_lbp)
    
    # --- Actualizar Panel 2: ROI Original ---
    ax_roi.clear()
    ax_roi.imshow(roi_gris, cmap='gray', vmin=0, vmax=255)
    ax_roi.set_title(f"2. ROI Gris ({x2-x1}x{y2-y1} px)")
    # Marcar el píxel central del ROI con un punto rojo
    cy, cx = roi_gris.shape[0] // 2, roi_gris.shape[1] // 2
    ax_roi.plot(cx, cy, 'ro', markersize=5, label='Píxel analizado')
    ax_roi.legend(loc='upper right', fontsize=8)
    ax_roi.axis('off')
    
    # --- Actualizar Panel 3: ROI LBP ---
    ax_lbp.clear()
    ax_lbp.imshow(roi_lbp[1:-1, 1:-1], cmap='gray', vmin=0, vmax=255)
    ax_lbp.set_title("3. Mapa LBP Calculado")
    ax_lbp.axis('off')
    
    # --- Actualizar Panel 4: Histograma ---
    ax_hist.clear()
    ax_hist.bar(range(256), hist, width=1.0, color='#2b5c8f', edgecolor='none')
    ax_hist.set_title("4. Histograma de Códigos LBP")
    ax_hist.set_xlim([0, 255])
    ax_hist.set_xlabel("Código Decimal LBP (0 - 255)")
    ax_hist.set_ylabel("Frecuencia (Píxeles)")
    ax_hist.grid(axis='y', linestyle='--', alpha=0.5)
    
    # --- Actualizar Panel 5: Matemática paso a paso del píxel central ---
    ax_math.clear()
    ax_math.axis('off')
    ventana_3x3 = roi_gris[cy-1:cy+2, cx-1:cx+2]
    centro, binaria, pesos, total = obtener_detalle_pixel(ventana_3x3)
    
    texto_math = (
        f"5. CÁLCULO EN EL PÍXEL ROJO (3x3)\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Intensidades (Centro = {centro}):\n"
        f"  {ventana_3x3[0,0]:3d}  {ventana_3x3[0,1]:3d}  {ventana_3x3[0,2]:3d}\n"
        f"  {ventana_3x3[1,0]:3d} [{ventana_3x3[1,1]:3d}] {ventana_3x3[1,2]:3d}\n"
        f"  {ventana_3x3[2,0]:3d}  {ventana_3x3[2,1]:3d}  {ventana_3x3[2,2]:3d}\n\n"
        f"Umbral (Vecino >= {centro} -> 1):\n"
        f"   {binaria[0,0]}    {binaria[0,1]}    {binaria[0,2]}\n"
        f"   {binaria[1,0]}   [C]   {binaria[1,2]}\n"
        f"   {binaria[2,0]}    {binaria[2,1]}    {binaria[2,2]}\n\n"
        f"Pesos (Potencias de 2):\n"
        f"   1    2    4   |  Suma ponderada:\n"
        f"  128  [0]   8   |  LBP = {total}\n"
        f"  64   32   16   |"
    )
    ax_math.text(0.05, 0.95, texto_math, transform=ax_math.transAxes,
                 fontsize=9.5, verticalalignment='top', family='monospace',
                 bbox=dict(boxstyle='round', facecolor='#f4f4f4', edgecolor='#cccccc'))
    
    fig.canvas.draw_idle()

# Conectar el selector rectangular de Matplotlib
selector = RectangleSelector(
    ax_orig, al_seleccionar_region,
    useblit=True,
    button=[1], # Solo clic izquierdo
    minspanx=5, minspany=5,
    spancoords='pixels',
    interactive=True
)

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.show()