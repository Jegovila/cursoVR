import cv2
import numpy as np
from skimage.feature import local_binary_pattern

# ============================================================
# CONFIGURACION DETECTOR DE DEFECTOS (ANOMALIAS)
# ============================================================
P = 8
R = 1
METHOD = "ror"       # Invariante a rotación (ideal para vetas de madera)
PATCH_SIZE = 48      # Tamaño de la ventana de inspección (en píxeles)
STRIDE = 12          # Qué tanto avanza la ventana en cada paso
MAX_DEFECTS = 100

def calculate_lbp(gray_img):
    # Suavizar ligeramente para ignorar ruido del sensor de la cámara
    blurred = cv2.GaussianBlur(gray_img, (3, 3), 0)
    return local_binary_pattern(blurred, P, R, method=METHOD)

def calculate_histogram(lbp_patch):
    bins = 2 ** P
    hist, _ = np.histogram(lbp_patch.ravel(), bins=np.arange(bins + 1) - 0.5)
    hist = hist.astype(np.float32)
    hist /= (hist.sum() + 1e-10)
    return hist.reshape(-1, 1)

# 1. Cargar imagen de la lámina de madera
image = cv2.imread("./madera.webp")
if image is None:
    raise ValueError("No se pudo cargar la imagen.")

if image.shape[1] > 900:
    scale = 900 / image.shape[1]
    image = cv2.resize(image, None, fx=scale, fy=scale)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. Seleccionar una zona de MADERA SANA (sin rayaduras ni quemaduras)
print("Selecciona un cuadro de textura SANA / SIN DEFECTOS y presiona ENTER.")
roi = cv2.selectROI("Selecciona zona SANA", image, showCrosshair=True, fromCenter=False)
cv2.destroyWindow("Selecciona zona SANA")

x, y, w, h = map(int, roi)
if w < 16 or h < 16:
    raise ValueError("Selecciona una muestra sana más grande.")

# 3. Calcular LBP global y el histograma de referencia (la "norma")
lbp_image = calculate_lbp(gray)
healthy_hist = calculate_histogram(lbp_image[y:y+h, x:x+w])

# 4. Barrer toda la lámina buscando zonas que NO se parezcan a la muestra sana
H, W = gray.shape
anomalies = []

for sy in range(0, H - PATCH_SIZE + 1, STRIDE):
    for sx in range(0, W - PATCH_SIZE + 1, STRIDE):
        window_lbp = lbp_image[sy:sy+PATCH_SIZE, sx:sx+PATCH_SIZE]
        window_hist = calculate_histogram(window_lbp)

        dist = cv2.compareHist(healthy_hist, window_hist, cv2.HISTCMP_BHATTACHARYYA)
        similarity = 1.0 - dist
        
        # Guardamos el puntaje de "anomalía" (1 - similitud): 
        # entre más alto, más defectuoso
        anomaly_score = dist 
        anomalies.append(((sx, sy, PATCH_SIZE, PATCH_SIZE), similarity, anomaly_score))

# Ordenar de MAYOR defecto (menor similitud) a menor defecto
anomalies.sort(key=lambda item: item[2], reverse=True)

all_boxes = np.array([a[0] for a in anomalies], dtype=np.int32)
all_sims = np.array([a[1] for a in anomalies], dtype=np.float32)
all_defects = np.array([a[2] for a in anomalies], dtype=np.float32)

# ============================================================
# VISUALIZACION INTERACTIVA DE DEFECTOS
# ============================================================
WINDOW_NAME = "Inspector de Calidad - Deteccion de Defectos"
cv2.namedWindow(WINDOW_NAME)
cv2.createTrackbar("Similitud Minima (%)", WINDOW_NAME, 70, 100, lambda v: None)

def update_view(min_sim):
    result = image.copy()
    
    # Mostrar en VERDE la muestra sana de referencia
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(result, "Muestra Sana", (x, max(20, y - 7)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Todo lo que tenga similitud MENOR a min_sim se considera defecto
    max_allowed_defect = 1.0 - min_sim
    valid_count = np.searchsorted(-all_defects, -max_allowed_defect, side='right')
    limit = min(valid_count, 1500)

    num_defects = 0
    if limit > 0:
        boxes_list = all_boxes[:limit].tolist()
        scores_list = all_defects[:limit].tolist()

        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes_list,
            scores=scores_list,
            score_threshold=max_allowed_defect,
            nms_threshold=0.25
        )

        if len(indices) > 0:
            indices = indices.flatten()[:MAX_DEFECTS]
            num_defects = len(indices)
            for idx in indices:
                bx, by, bw, bh = boxes_list[idx]
                sim_val = all_sims[idx]
                
                # Dibujar en ROJO las zonas defectuosas
                cv2.rectangle(result, (bx, by), (bx + bw, by + bh), (0, 0, 255), 2)
                cv2.putText(
                    result,
                    f"Sim:{sim_val*100:.0f}%",
                    (bx, max(15, by - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (0, 0, 255),
                    1
                )

    cv2.putText(result, f"Umbral Similitud: < {min_sim*100:.0f}%", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(result, f"Defectos detectados: {num_defects}", (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow(WINDOW_NAME, result)

prev_val = -1
while True:
    val = cv2.getTrackbarPos("Similitud Minima (%)", WINDOW_NAME) / 100.0
    if val != prev_val:
        update_view(val)
        prev_val = val
    if (cv2.waitKey(15) & 0xFF) in [27, ord('q')]:
        break

cv2.destroyAllWindows()