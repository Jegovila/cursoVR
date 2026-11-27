clear all
close all
clc
imScene = imageDatastore('./');
montage(imScene.Files);

%Leer la primera imagen
I = readimage(imScene, 1);

%extraer puntos de interés de la primera imagen
grayImage = rgb2gray(I);
points = detectKAZEFeatures(grayImage);
[features, points] = extractFeatures(grayImage, points);

%inicializar Transformaciones
numImages = numel(imScene.Files);
tforms(numImages) = projective2d(eye(3));

%Variable para guardar tamaño de las imágenes
imageSize = zeros(numImages,2);

for n=2:numImages
    
    %guardar puntos de I(n-1)
    pointsPrevious = points;
    featuresPrevious = features;
    
    %Leer I(n)
    I = readimage(imScene,n);
    grayImage = rgb2gray(I);
    
    %guardar tamaño
    imageSize(n,:) = size(grayImage);
    
    %extraer puntos para I(n)
    points = detectKAZEFeatures(grayImage);
    [features, points] = extractFeatures(grayImage,points);
    
    %matches entre I(n) e I(n-1)
    indexPairs = matchFeatures(features, featuresPrevious);
    
    matchedPoints = points(indexPairs(:,1),:);
    matchedPointsPrev = pointsPrevious(indexPairs(:,2),:);
    
    %estimar T entre I(n) e I(n-1)
    tforms(n) = estimateGeometricTransform(matchedPoints,matchedPointsPrev, 'projective', 'Confidence', 99.9, 'MaxNumTrials', 2000);
    
    %Calcular T(n) = T(n-1) * ... * T(1)
    tforms(n).T = tforms(n).T * tforms(n-1).T;
end

%calcular límites de cada transformación
for i = 1:numel(tforms)
    
    [xlim(i,:),ylim(i,:)] = outputLimits(tforms(i),[1 imageSize(i,2)], [1 imageSize(i,1)]);
    
end

%%
%Tomar imagen del medio como referencia
centerImageIdx = 2;
Tinv = invert(tforms(centerImageIdx));

for i = 1:numel(tforms)
    tforms(i).T = tforms(i).T * Tinv.T; 
end

for i = 1:numel(tforms)
   [xlim(i,:), ylim(i,:)] = outputLimits(tforms(i),[1 imageSize(i,2)], [1 imageSize(i,1)]); 
end

%%

%crear lienzo
maxImageSize = max(imageSize);

%min-max X
xMin = min([1;xlim(:)]);
xMax = max([maxImageSize(2); xlim(:)]);

%min-max Y
yMin = min([1;ylim(:)]);
yMax = max([maxImageSize(1); ylim(:)]);

%ancho y alto
width = round(xMax-xMin);
height = round(yMax-yMin);

%panorama vacío
panorama = zeros([height, width, 3],'like', I);

blender = vision.AlphaBlender('Operation', 'Binary Mask', 'MaskSource', 'Input port');

%crear la imagen de referencia
xLimits = [xMin xMax];
yLimits = [yMin yMax];
panoramaView = imref2d([height width], xLimits, yLimits);

%crear panorama
for i = 1:numImages
   %leer primera imagen
    I = readimage(imScene, i);
    
    %Transformar
    wrapedImage = imwarp(I, tforms(i), 'OutputView', panoramaView);
    
    %Máscara binaria
    mask = imwarp(true(size(I,1),size(I,2)), tforms(i), 'OutputView', panoramaView);
    
    panorama = step(blender, panorama, wrapedImage, mask);
end

figure
imshow(panorama)