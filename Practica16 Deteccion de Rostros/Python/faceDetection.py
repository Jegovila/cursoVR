import cv2

# Cargar el clasificador de detección de rostros preentrenado
# Para ver más modelos preentrenados:
# https://github.com/opencv/opencv/tree/master/data/haarcascades

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Iniciar la webcam
cap = cv2.VideoCapture(2)

while True:
    # Capturar fotograma por fotograma
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el fotograma
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Mostrar el fotograma con los rostros detectados
    cv2.imshow('Face Detection', frame)

    # Salir del bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la webcam y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
