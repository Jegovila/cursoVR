% Crear un objeto de video para la webcam
cam = webcam(3);
cam.Resolution = '640x480';

% Crear un visor de video
videoPlayer = vision.VideoPlayer('Position', [100, 100, 600, 400]);

% Crear un detector de rostros
faceDetector = vision.CascadeObjectDetector();

% Ejecutar el bucle para la detección de rostros en tiempo real
while true
    % Capturar un fotograma de la webcam
    frame = snapshot(cam);

    % Convertir la imagen de RGB a escala de grises
    grayFrame = rgb2gray(frame);

    % Detectar rostros en la imagen en escala de grises
    bbox = step(faceDetector, grayFrame);

    % Dibujar rectángulos alrededor de los rostros detectados
    detectedImg = insertObjectAnnotation(frame, 'rectangle', bbox, 'Face');

    % Mostrar la imagen con los rostros detectados
    step(videoPlayer, detectedImg);

    if ~isOpen(videoPlayer)
        break;
    end

end

% Liberar recursos
release(videoPlayer);
clear cam;
