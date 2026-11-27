
from pathlib import Path
import cv2
import time

ruta_script = Path(__file__).resolve().parent

# Cargar nuestro clasificador Haar Cascade entrenado
cascade = cv2.CascadeClassifier(
    str(ruta_script / "cascade" / "cascade.xml")
)

# Verificar que el clasificador se cargó correctamente
if cascade.empty():
    print("ERROR: No se pudo cargar cascade.xml")
    exit()

# Iniciar la webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:

    # Capturar fotograma por fotograma
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar objetos
    objects = cascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(100, 100)
    )


    # Dibujar rectángulos alrededor de los objetos detectados
    for (x, y, w, h) in objects:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

    # Mostrar el fotograma
    cv2.imshow("Haar Cascade Detection", frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la webcam y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
