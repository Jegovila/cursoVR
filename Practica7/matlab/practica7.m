clear all
close all

cam = webcam(1);
cam.Resolution = '640x480';
cam.ExposureMode = 'manual';
cam.Exposure = -3;

%Tomar imagen de referencia (Práctica)
fig = figure(1);
while(1)
    I = snapshot(cam);
    Ig_ref = rgb2gray(I);
    imshow(Ig_ref);
    if ~isempty(get(fig,'CurrentCharacter'))
        break
    end
    pause(.001)
end
Hblob = vision.BlobAnalysis;

fig2 = figure(2);
while(1)
    I = snapshot(cam);
    Ig = rgb2gray(I);
    Ibinaria = Ig > 90;

    se = strel('disk',2,4);

%% Erosion y dilatación
%     Ierosionada = imerode(Ibinaria,se);
%     Idilatada = imdilate(Ibinaria,se);
% 
%     Ierosionada = imerode(Ierosionada,se);
%     Ierosionada = imerode(Ierosionada,se);
%     Ierosionada = imerode(Ierosionada,se);
%     
%     Idilatada = imdilate(Ierosionada,se);
%     Idilatada = imdilate(Idilatada,se);
%     Idilatada = imdilate(Idilatada,se);
% 
%     subplot(1,3,1)
%     imshow(Ibinaria)
%     subplot(1,3,2)
%     imshow(Ierosionada)
%     subplot(1,3,3)
%     imshow(Idilatada)

%% Apertura y cierre
%     Iapertura = imopen(Ibinaria,se);
%     Icierre = imclose(Ibinaria,se);
%     
%     subplot(1,3,1)
%     imshow(Ibinaria)
%     subplot(1,3,2)
%     imshow(Iapertura)
%     subplot(1,3,3)
%     imshow(Icierre)

%% Múltiples aperturas o cierres
%     Iapertura = imopen(Ibinaria,se);   
%     subplot(1,3,1)
%     imshow(Ibinaria)
%     subplot(1,3,2)
%     imshow(Iapertura)
% 
%     Iapertura = imopen(Iapertura,se);
%     Iapertura = imopen(Iapertura,se);
%     Iapertura = imopen(Iapertura,se);
%     Iapertura = imopen(Iapertura,se);
%     Iapertura = imopen(Iapertura,se);
%     Iapertura = imopen(Iapertura,se);
%     subplot(1,3,3)
%     imshow(Iapertura)

%% Detección de bordes
%     Ierosionada = imerode(Ibinaria,se);
%     Ie_inv = 1 - Ierosionada;
% 
%     If = logical(and(Ie_inv,Ibinaria));
%     imshow(If)

%% Detección de movimiento
    Idif = abs(double(Ig) -double(Ig_ref));
    Idif = Idif > 30;

    % Aplicar erosion / dilatacion
    Idif = imerode(Idif,se);
    Idif = imdilate(Idif,se);
    % ---------------------------

    [area,centroid,bbox] = Hblob(Idif);
    [value, index] = (max(area(:)));
    imshow(I);
    
    [n,~] = size(area)
    X = sprintf('Número de objetos: %d \n',n);
    disp(X)

%     Y = sprintf('Ubicacion X: %d \n',centroid(index,1));
%     disp(Y)
%     Z = sprintf('Ubicacion Y: %d \n',centroid(index,2));
%     disp(Z)

    if value > 20
        hold on
        rectangle('Position',bbox(index,:),...
             'EdgeColor','r','LineWidth',2,'LineStyle','-')
        hold off
    end



    if ~isempty(get(fig2,'CurrentCharacter'))
        break
    end
    pause(.001)
end

clear cam
close all