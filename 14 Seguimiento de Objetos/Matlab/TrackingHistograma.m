clear all
close all
clc

usarHSV = 1;

cam = webcam(3);
cam.Resolution = '640x480';
cam.ExposureMode = 'auto';

% Obtener las coordenadas del bbox a seguir
firstFrame = snapshot(cam);
imshow(firstFrame);
objectRegion=int64(getPosition(imrect));

% Convertir a HSV si se quiere usar ese modelo de color
objectFrame = im2single(firstFrame);
objectHSV = rgb2hsv(objectFrame);

% Crear el objeto tracker
tracker = vision.HistogramBasedTracker;

%Inicializar el objeto
if usarHSV
    initializeObject(tracker, objectHSV(:,:,1) , objectRegion);
else
    initializeObject(tracker, rgb2gray(firstFrame) , objectRegion);
end

while (1)
  frame = im2single(snapshot(cam));
  hsv = rgb2hsv(frame);

  if usarHSV
    [bbox, ~, score] = step(tracker, hsv(:,:,1));
  else
    [bbox, ~, score] = step(tracker, rgb2gray(frame));
  end

  out = insertShape(frame,"rectangle",bbox,Color=[1 0 0],LineWidth=5);
  imshow(out);
end