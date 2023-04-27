% 1. Match entre puntos dispersos de dos imágenes
% 2. Estimar matriz Esencial/Fundamental
% 3. Calcular movimiento de la cámara con relativeCameraPose
% 4. Match entre puntos densos de dos imágenes
% 5. Determinar puntos 3D de los puntos con triangulación

%% Leer imágenes
imageDir = './img/';
images = imageDatastore(imageDir);
I1 = readimage(images, 1);
I2 = readimage(images, 2);
figure
imshowpair(I1, I2, 'montage'); 
title('Original Images');


%% Intrinsics
focalLength = [3422.9 3421.53];
principalPoint = [3111.07 2055.06];
imageSize = size(rgb2gray(I1));
intrinsics = cameraIntrinsics(focalLength,principalPoint,imageSize);

I1 = undistortImage(I1, intrinsics);
I2 = undistortImage(I2, intrinsics);
figure 
imshowpair(I1, I2, 'montage');
title('Undistorted Images');

%% Encontrar correspondencias entre imágenes
% Detectar puntos
imagePoints1 = detectMinEigenFeatures(im2gray(I1), MinQuality = 0.1);

% Visualizar puntos
figure
imshow(I1, InitialMagnification = 50);
title('150 Strongest Corners from the First Image');
hold on
plot(selectStrongest(imagePoints1, 150));


% Crear el tracker
tracker = vision.PointTracker(MaxBidirectionalError=1, NumPyramidLevels=5);

% Inicializar el tracker
imagePoints1 = imagePoints1.Location;
initialize(tracker, imagePoints1, I1);

% Track de los puntos
[imagePoints2, validIdx] = step(tracker, I2);
matchedPoints1 = imagePoints1(validIdx, :);
matchedPoints2 = imagePoints2(validIdx, :);

% Visualizar correspondencias
figure
showMatchedFeatures(I1, I2, matchedPoints1, matchedPoints2);
title('Tracked Features');

%% Estimar matriz fundamental
% Estimar matriz fundamental
[E, epipolarInliers] = estimateEssentialMatrix(...
    matchedPoints1, matchedPoints2, intrinsics, Confidence = 99.99);

% Encontrar líneas epipolares
inlierPoints1 = matchedPoints1(epipolarInliers, :);
inlierPoints2 = matchedPoints2(epipolarInliers, :);

% Visualizar matches
figure
showMatchedFeatures(I1, I2, inlierPoints1, inlierPoints2);
title('Epipolar Inliers');

%% Calcular la pose de la cámara
[relPoseR, relPoseT] = relativeCameraPose(E, intrinsics, inlierPoints1, inlierPoints2);


%% Reconstrucción de puntos 3D (matches)
% Detectar puntos densos. Se usa una ROI para excluir puntos cerca de los
% bordes
border = 30;
roi = [border, border, size(I1, 2)- 2*border, size(I1, 1)- 2*border];
imagePoints1 = detectMinEigenFeatures(im2gray(I1), ROI = roi, ...
    MinQuality = 0.001);

% Crear tracker
tracker = vision.PointTracker(MaxBidirectionalError=1, NumPyramidLevels=5);

% Inicializar tracker
imagePoints1 = imagePoints1.Location;
initialize(tracker, imagePoints1, I1);

% Track de los puntos
[imagePoints2, validIdx] = step(tracker, I2);
matchedPoints1 = imagePoints1(validIdx, :);
matchedPoints2 = imagePoints2(validIdx, :);

% Calcular las matrices para cada posición de la cámara
% La primera cámara está en el origen y por lo tanto su transformación es la
% identidad
camMatrix1 = cameraMatrix(intrinsics, rigid3d);
camMatrix2 = cameraMatrix(intrinsics, cameraPoseToExtrinsics(rigid3d(relPoseR,relPoseT)));

% Calcular los puntos 3D
points3D = triangulate(matchedPoints1, matchedPoints2, camMatrix1, camMatrix2);

% Obtener el color de los puntos
numPixels = size(I1, 1) * size(I1, 2);
allColors = reshape(I1, [numPixels, 3]);
colorIdx = sub2ind([size(I1, 1), size(I1, 2)], round(matchedPoints1(:,2)), ...
    round(matchedPoints1(:, 1)));
color = allColors(colorIdx, :);

% Crear la nube de puntos
ptCloud = pointCloud(points3D, 'Color', color);

%% Desplegar nube de puntos 3D
% Visualizar la pose de las cámaras
cameraSize = 0.3;
figure
plotCamera(Size=cameraSize, Color='r', Label='1', Opacity=0);
hold on
grid on
plotCamera(AbsolutePose=rigid3d(relPoseR,relPoseT), Size=cameraSize, ...
    Color='b', Label='2', Opacity=0);

% Visualizar la nube de puntos
pcshow(ptCloud, VerticalAxis='y', VerticalAxisDir='down', MarkerSize=45);

% Rotación y zoom de la gráfica
camorbit(0, -30);
camzoom(1.5);

% Etiquetar ejes
xlabel('x-axis');
ylabel('y-axis');
zlabel('z-axis')

title('Escena a escala');