import cv2
import numpy as np
from skimage.feature import local_binary_pattern

# ============================================================
# LBP TEMPLATE MATCHING
# ============================================================

# PARAMETROS LBP
P = 8
R = 1
METHOD = "uniform"  # "uniform"  "default"  "ror" "nri_uniform"

# Escalas a buscar respecto al template
SCALES = [1.0]

# Numero maximo de detecciones mostradas
MAX_DETECTIONS = 30

# ============================================================
# FUNCIONES
# ============================================================

def calculate_lbp(gray):
    return local_binary_pattern(
        gray, P, R, method=METHOD
    )

def calculate_histogram(lbp_image):

    if METHOD == "uniform":
        bins = P + 2
    else:
        bins = 2 ** P

    hist, _ = np.histogram(
        lbp_image.ravel(),
        bins=np.arange(bins + 1) - 0.5
    )

    hist = hist.astype(np.float32)

    # Normalizar histograma
    total = hist.sum()
    if total > 0:
        hist /= total

    return hist.reshape(-1, 1)


def compare_histograms(hist1, hist2):

    distance = cv2.compareHist(
        hist1,
        hist2,
        cv2.HISTCMP_BHATTACHARYYA
    )

    # Convertir distancia a similitud
    similarity = 1.0 - distance

    return similarity


def calculate_iou(box1, box2):

    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    xa = max(x1, x2)
    ya = max(y1, y2)

    xb = min(x1 + w1, x2 + w2)
    yb = min(y1 + h1, y2 + h2)

    intersection = max(0, xb - xa) * max(0, yb - ya)

    area1 = w1 * h1
    area2 = w2 * h2

    union = area1 + area2 - intersection

    if union == 0:
            return 0.0
    
    return intersection / union

# ============================================================
# CARGAR IMAGEN
# ============================================================

path = "./texturas.webp"

image = cv2.imread(path)

if image is None:
    raise ValueError("No se pudo cargar la imagen.")

# Limitar dimensiones de la imagen de entrada
# para agilizar el procesamiento
max_width = 900

if image.shape[1] > max_width:
    scale = max_width / image.shape[1]
    image = cv2.resize(image,None,fx=scale,fy=scale)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# En presencia de cierto tipo de ruido (como el que añade el iso)
# puede convenir hacer un ligero suavizado. 
# la forma más elegante de hacerse robusto al ruido sin perder detalles 
# es aumentar el radio de vecindad a P = 16, R = 2 o P = 24, R = 3

#gray = cv2.GaussianBlur(gray, (3, 3), 0) 

# ============================================================
# SELECCIONAR TEMPLATE
# ============================================================

print("\nSelecciona el objeto que deseas buscar.")
print("Presiona ENTER o SPACE para confirmar.")
print("Presiona ESC para cancelar.")

roi = cv2.selectROI(
    "Selecciona el TEMPLATE",
    image,
    showCrosshair=True,
    fromCenter=False
)

cv2.destroyWindow("Selecciona el TEMPLATE")

x, y, w, h = map(int, roi)

if w == 0 or h == 0:
    raise ValueError("No se selecciono un template valido.")

if w < 12 or h < 12:
    raise ValueError("Selecciona una region mas grande.")

# ============================================================
# CALCULAR MAPA LBP
# ============================================================

print("\nCalculando LBP...")

lbp_image = calculate_lbp(gray)

# Extraer template LBP
template_lbp = lbp_image[y:y+h, x:x+w]

# Histograma del template
template_hist = calculate_histogram(template_lbp)

# Visualizar template y su LBP
template_gray = gray[y:y+h, x:x+w]

template_lbp_display = cv2.normalize(
    template_lbp,
    None,
    0,
    255,
    cv2.NORM_MINMAX
).astype(np.uint8)

#----- Visualizar parches --------------------
escala_zoom = 4
nuevo_tamano = (w * escala_zoom, h * escala_zoom)

template_gray_big = cv2.resize(
    template_gray, nuevo_tamano, interpolation=cv2.INTER_NEAREST
)
template_lbp_display_big = cv2.resize(
    template_lbp_display, nuevo_tamano, interpolation=cv2.INTER_NEAREST
)
cv2.imshow("Template original", template_gray_big)
cv2.imshow("Template LBP", template_lbp_display_big)

# --- Visualizar template_hist ---
hist_h, hist_w = 300, 400
hist_img = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

vals = template_hist.flatten()
num_bins = len(vals)
bin_w = hist_w // num_bins
max_val = vals.max() if vals.max() > 0 else 1.0

for i, val in enumerate(vals):
    bar_h = int((val / max_val) * (hist_h - 45))
    x1 = i * bin_w + 4
    x2 = (i + 1) * bin_w - 4
    y1 = hist_h - 25 - bar_h
    y2 = hist_h - 25
    
    # Dibujar barra y etiqueta del bin
    cv2.rectangle(hist_img, (x1, y1), (x2, y2), (0, 220, 255), -1)
    cv2.putText(hist_img, str(i), (x1 + 5, hist_h - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    # Mostrar porcentaje encima de la barra
    cv2.putText(hist_img, f"{val*100:.0f}%", (x1 + 2, max(15, y1 - 5)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

cv2.imshow("Histograma LBP del Template", hist_img)

# ============================================================
# BUSQUEDA MEDIANTE VENTANA DESLIZANTE
# ============================================================

H, W = gray.shape

detections = []

for scale in SCALES:

    window_w = int(w * scale)
    window_h = int(h * scale)

    if window_w < 8 or window_h < 8:
        continue

    if window_w > W or window_h > H:
        continue

    # Paso de desplazamiento
    stride = max(
        6,
        min(window_w, window_h) // 8
    )

    for sy in range(0, H - window_h + 1, stride):

        for sx in range(0, W - window_w + 1, stride):

            # Evitar que el template se encuentre a si mismo
            candidate_box = (sx, sy, window_w, window_h)
            template_box = (x, y, w, h)

            if calculate_iou(
                candidate_box,
                template_box
            ) > 0.5:
                continue

            # Extraer ventana del mapa LBP
            window_lbp = lbp_image[
                sy:sy+window_h,
                sx:sx+window_w
            ]

            # Histograma de la ventana
            window_hist = calculate_histogram(
                window_lbp
            )

            # Comparar histogramas
            similarity = compare_histograms(
                template_hist,
                window_hist
            )

            detections.append(
                (candidate_box, similarity)
            )

# ============================================================
# VISUALIZACION 
# ============================================================

# 1. Ordenar TODAS las detecciones una sola vez por similitud descendente
detections.sort(key=lambda item: item[1], reverse=True)

# Pre-extraer arreglos 
all_boxes = np.array([d[0] for d in detections], dtype=np.int32)
all_scores = np.array([d[1] for d in detections], dtype=np.float32)

WINDOW_NAME = "LBP - Busqueda de objetos"
cv2.namedWindow(WINDOW_NAME)

def nothing(value):
    pass

cv2.createTrackbar("Similitud (%)", WINDOW_NAME, 75, 100, nothing)

def show_results(threshold):
    result = image.copy()

    # Dibujar template original en azul
    cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 2. Filtrar rápido usando NumPy (como ya está ordenado, encontramos el índice de corte)
    valid_count = np.searchsorted(-all_scores, -threshold, side='right')
    
    # Limitar a las mejores 1500 cajas antes de NMS para evitar congelamientos en umbrales bajos
    limit = min(valid_count, 1500)
    
    if limit > 0:
        boxes_to_nms = all_boxes[:limit].tolist()
        scores_to_nms = all_scores[:limit].tolist()

        # 3. NMS nativo de OpenCV en C++
        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes_to_nms,
            scores=scores_to_nms,
            score_threshold=threshold,
            nms_threshold=0.30
        )

        # Limitar al máximo de detecciones a dibujar
        if len(indices) > 0:
            indices = indices.flatten()[:MAX_DETECTIONS]

            for idx in indices:
                bx, by, bw, bh = boxes_to_nms[idx]
                score = scores_to_nms[idx]

                cv2.rectangle(result, (bx, by), (bx + bw, by + bh), (0, 255, 0), 2)
                cv2.putText(
                    result,
                    f"{score*100:.1f}%",
                    (bx, max(20, by - 7)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 0),
                    2
                )
        num_matches = len(indices)
    else:
        num_matches = 0

    # Información en pantalla
    cv2.putText(result, f"Umbral: {threshold*100:.0f}%", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(result, f"Coincidencias: {num_matches}", (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow(WINDOW_NAME, result)


previous_threshold = -1

while True:
    threshold = cv2.getTrackbarPos("Similitud (%)", WINDOW_NAME) / 100.0

    if threshold != previous_threshold:
        show_results(threshold)
        previous_threshold = threshold

    key = cv2.waitKey(15) & 0xFF
    if key == 27 or key == ord('q'):
        break

cv2.destroyAllWindows()