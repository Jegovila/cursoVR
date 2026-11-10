from pathlib import Path
import cv2

ruta_script = Path(__file__).resolve().parent

# Cargar el clasificador de detección de rostros preentrenado
# Para ver más modelos preentrenados:
# https://github.com/opencv/opencv/tree/master/data/haarcascades
# Descargar el xml en la carpeta donde esté el este script

face_cascade_rostro = cv2.CascadeClassifier(str(ruta_script) + '/haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier(str(ruta_script) + 'haarcascade_profileface.xml')
#face_cascade_ojo = cv2.CascadeClassifier(str(ruta_script) + 'haarcascade_eye.xml')

# Iniciar la webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    # Capturar fotograma por fotograma
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el fotograma
    faces = face_cascade_rostro.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    #eyes = face_cascade_ojo.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    #for (x, y, w, h) in eyes:
    #    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Mostrar el fotograma con los rostros detectados
    cv2.imshow('Face Detection', frame)

    # Salir del bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la webcam y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
