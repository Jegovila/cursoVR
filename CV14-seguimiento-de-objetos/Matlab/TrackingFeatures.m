clear all
close all
clc

cam = webcam(3);
cam.Resolution = '640x480';
cam.ExposureMode = 'auto';

% Seleccionar ROI
firstFrame = snapshot(cam);
imshow(firstFrame);
objectRegion=int64(getPosition(imrect));
objectFrame = im2single(firstFrame);

% Detectar puntos
points = detectMinEigenFeatures(rgb2gray(objectFrame),'ROI',objectRegion);
pointImage = insertMarker(objectFrame,points.Location,'+','Color','white');

% Crear e inicializar tracker
tracker = vision.PointTracker('MaxBidirectionalError',1);
initialize(tracker,points.Location,objectFrame);

while (1)
  frame = im2single(snapshot(cam));
  [points,validity] = tracker(frame);
  validPoints = points(validity, :);

  if isempty(validPoints)
      break
  end

  out = insertShape(frame,"FilledCircle",[mean(validPoints(:,1)),mean(validPoints(:,2)),35],LineWidth=5);
  %out = insertMarker(frame,points(validity, :),'+');
  imshow(out);

end

disp("Se perdió el objeto")
clear cam
close all