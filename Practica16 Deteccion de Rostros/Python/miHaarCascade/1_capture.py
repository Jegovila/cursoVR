
import cv2
from pathlib import Path

# ==========================================
# CONFIGURACIÓN
# ==========================================

CAMERA_ID = 1

BASE_PATH = Path(__file__).resolve().parent

DATASET_PATH = BASE_PATH / "dataset"
POSITIVE_PATH = DATASET_PATH / "positive"
NEGATIVE_PATH = DATASET_PATH / "negative"

IMAGE_FORMAT = ".jpg"

# Crear carpetas automáticamente
POSITIVE_PATH.mkdir(parents=True, exist_ok=True)
NEGATIVE_PATH.mkdir(parents=True, exist_ok=True)


# ==========================================
# FUNCIONES
# ==========================================

def get_next_filename(folder):
    """Obtiene el siguiente nombre consecutivo disponible."""

    existing = list(folder.glob("image_*.jpg"))

    numbers = []

    for file in existing:
        try:
            numbers.append(int(file.stem.split("_")[1]))
        except (IndexError, ValueError):
            pass

    next_number = max(numbers, default=0) + 1

    return folder / f"image_{next_number:05d}{IMAGE_FORMAT}"


def save_image(frame, folder):
    """Guarda una imagen en la carpeta indicada."""

    filename = get_next_filename(folder)

    success = cv2.imwrite(str(filename), frame)

    if success:
        print(f"Imagen guardada: {filename}")
    else:
        print("Error al guardar la imagen.")


def draw_interface(frame, positive_count, negative_count):
    """Dibuja información sobre la imagen de la cámara."""

    display = frame.copy()

    cv2.putText(
        display, "P: Positive",
        (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 255, 0), 2
    )

    cv2.putText(
        display, "N: Negative",
        (20, 65), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 0, 255), 2
    )

    cv2.putText(
        display, "Q: Quit",
        (20, 95), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (255, 255, 255), 2
    )

    cv2.putText(
        display, f"Positive: {positive_count}",
        (20, 140), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 255, 0), 2
    )

    cv2.putText(
        display, f"Negative: {negative_count}",
        (20, 175), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 0, 255), 2
    )

    return display


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

positive_count = len(list(POSITIVE_PATH.glob("image_*.jpg")))
negative_count = len(list(NEGATIVE_PATH.glob("image_*.jpg")))

print("--------------------------------")
print(" HAAR CASCADE IMAGE CAPTURE")
print("--------------------------------")
print("P -> Guardar Positive")
print("N -> Guardar Negative")
print("Q -> Salir")
print("--------------------------------")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error al capturar imagen.")
        break

    display = draw_interface(
        frame,
        positive_count,
        negative_count
    )

    cv2.imshow("Haar Cascade Trainer - Capture", display)

    key = cv2.waitKey(1) & 0xFF

    # Guardar positivo
    if key == ord('p'):

        save_image(frame, POSITIVE_PATH)
        positive_count += 1

    # Guardar negativo
    elif key == ord('n'):

        save_image(frame, NEGATIVE_PATH)
        negative_count += 1

    # Salir
    elif key == ord('q'):

        break


# ==========================================
# FINALIZAR
# ==========================================

cap.release()
cv2.destroyAllWindows()

print("Captura finalizada.")
print(f"Total positivos: {positive_count}")
print(f"Total negativos: {negative_count}")
