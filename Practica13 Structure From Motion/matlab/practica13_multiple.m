% 1. Encontrar correspondencias entre imágenes consecutivas
% 2. Estimar la pose relativa de la vista actual con respecto a la anterior
% 3. Transformar la pose de la vista actual al sistema coordenado de la
%    primera vista
% 4. Almacenar pose de cámara y puntos de imágenes actuales
% 5. Almacenar matches entre vista previa y actual
% 6. Encontrar la pista de los puntos en todas las vistas procesadas
% 7. Triangulación para calcular las coordenadas 3D iniciales 
% 8. Bundle Adjustment

%% Obtener imágenes
imageDir = './img/';
imds = imageDatastore(imageDir);

% Desplegar imágenes.
figure
montage(imds.Files, 'Size', [1, 2]);

% Convertir a escala de grises.
images = cell(1, numel(imds.Files));
for i = 1:numel(imds.Files)
    I = readimage(imds, i);
    images{i} = im2gray(I);
end

title('Imágenes de entrada');

%% Prámetros de la imagen
focalLength = [3422.9 3421.53];
principalPoint = [3111.07 2055.06];
imageSize = size(images{1});
intrinsics = cameraIntrinsics(focalLength,principalPoint,imageSize);

% Rectificar imágenes.
I = undistortImage(images{1}, intrinsics); 

% Detectar puntos de interés. Incrementar 'NumOctaves' ayuda a detectar
% puntos de interés en imágenes a alta resolución. Usar ROI para eliminar
% falsos puntos de interés cerca de los bordes.
border = 50;
roi = [border, border, size(I, 2)- 2*border, size(I, 1)- 2*border];
prevPoints   = detectSURFFeatures(I, NumOctaves=8, ROI=roi);

% Extraer puntos de interes. 'Upright' mejora la correspondencia mientras
% el movimiento de la cámara implica poca o ninguna rotación en el plano.
prevFeatures = extractFeatures(I, prevPoints, Upright=true);

% Crear imageviewset en blanco para trabajar cada vista
vSet = imageviewset;

% Añadir la primer vista. Colocar la cámara asociada con la primera vista
% en el origen y orientada en el eje Z
viewId = 1;
vSet = addView(vSet, viewId, rigid3d, Points=prevPoints);

%% Añadir el resto de vistas

for i = 2:numel(images)
    % Rectificar imagen actual.
    I = undistortImage(images{i}, intrinsics);
    
    % Detectar y establecer corresondencias.
    currPoints   = detectSURFFeatures(I, NumOctaves=8, ROI=roi);
    currFeatures = extractFeatures(I, currPoints, Upright=true);    
    indexPairs   = matchFeatures(prevFeatures, currFeatures, ...
        MaxRatio=0.7, Unique=true);
    
    % Seleccionar correspondencias.
    matchedPoints1 = prevPoints(indexPairs(:, 1));
    matchedPoints2 = currPoints(indexPairs(:, 2));
    
    % Estimar la pose de la vista actual relativa a la anterior. La pose es
    % calculada a escala, lo que significa que la distancia entre vista
    % actual y vista previa se establece en 1 y se corrige con
    % bundleAdjustment.
    [relPoseR, relPoseT, inlierIdx] = helperEstimateRelativePose(...
        matchedPoints1, matchedPoints2, intrinsics);
    
    % Obtener la tabla que contiene la pose de la vista anterior.
    prevPose = poses(vSet, i-1).AbsolutePose;
        
    % Calcular la pose de la vista actual en el sistema de coordenadas
    % global relativa a la primera vista.
    A = [prevPose.Rotation(1,:) prevPose.Translation(1);
        prevPose.Rotation(2,:) prevPose.Translation(2);
        prevPose.Rotation(3,:) prevPose.Translation(3);
        0 0 0 1];
    B = [relPoseR(1,:) relPoseT(1);
        relPoseR(2,:) relPoseT(2);
        relPoseR(3,:) relPoseT(3);
        0 0 0 1];
    C  = A*B;
    currPose = rigid3d(C(1:3,1:3), C(1:3,4)');
    
    % Añadir la vista actual al viewset.
    vSet = addView(vSet, i, currPose, Points=currPoints);

    % Almacenar las correspondencias entre vistas previa y actual.
    relPose = rigid3d(relPoseR, relPoseT);
    vSet = addConnection(vSet, i-1, i, relPose, Matches=indexPairs(inlierIdx,:));
    
    % Encontrar tracks en todas las vistas.
    tracks = findTracks(vSet);

    % Obtener tabla que contiene las poses de las cámaras para todas las vistas.
    camPoses = poses(vSet);

    % Triangular ubicaciones iniciales para los puntos 3D.
    xyzPoints = triangulateMultiview(tracks, camPoses, intrinsics);
    
    % Ajustar los puntos 3D y las poses de las cámaras.
    [xyzPoints, camPoses, reprojectionErrors] = bundleAdjustment(xyzPoints, ...
        tracks, camPoses, intrinsics, FixedViewId=1, ...
        PointsUndistorted=true);

    % Almacenar las poses de las cámaras ajustadas.
    vSet = updateView(vSet, camPoses);

    prevFeatures = currFeatures;
    prevPoints   = currPoints;  
end

%% Desplegar poses de las cámaras.
camPoses = poses(vSet);
figure;
plotCamera(camPoses, Size=0.2);
hold on

% Excluir puntos 3D ruidosos.
goodIdx = (reprojectionErrors < 5);
xyzPoints = xyzPoints(goodIdx, :);

% Desplegar puntos 3D y cámaras.
pcshow(xyzPoints, VerticalAxis='y', VerticalAxisDir='down', MarkerSize= 45);
grid on
hold off

loc1 = camPoses.AbsolutePose(1).Translation;
xlim([loc1(1)-5, loc1(1)+4]);
ylim([loc1(2)-5, loc1(2)+4]);
zlim([loc1(3)-1, loc1(3)+20]);
camorbit(0, -30);

title('Refined Camera Poses');

%% Calcular reconstruicción densa
% Leer y rectificar la primer imagen
I = undistortImage(images{1}, intrinsics); 

% Detectar esquinas en la primer imagen.
prevPoints = detectMinEigenFeatures(I, MinQuality=0.001);

% Crear tracker para seguir los puntos a través de las vistas.
tracker = vision.PointTracker(MaxBidirectionalError=1, NumPyramidLevels=6);

% Inicializar el tracker.
prevPoints = prevPoints.Location;
initialize(tracker, prevPoints, I);

% Almacenar puntos densos en el viewsetStore.
vSet = updateConnection(vSet, 1, 2, Matches=zeros(0, 2));
vSet = updateView(vSet, 1, Points=prevPoints);

% Track de los puntos en todas las vistas.
for i = 2:numel(images)
    % Leer y rectificar imagen actual.
    I = undistortImage(images{i}, intrinsics); 
    
    % Track de los puntos.
    [currPoints, validIdx] = step(tracker, I);
    
    % Limpiar correspondencias viejas entre puntos.
    if i < numel(images)
        vSet = updateConnection(vSet, i, i+1, Matches=zeros(0, 2));
    end
    vSet = updateView(vSet, i, Points=currPoints);
    
    % Almacenar matches en el viewset.
    matches = repmat((1:size(prevPoints, 1))', [1, 2]);
    matches = matches(validIdx, :);        
    vSet = updateConnection(vSet, i-1, i, Matches=matches);
end

% Encontrar los tracks de los puntos en todas las vistas.
tracks = findTracks(vSet);
camPoses = poses(vSet);

% Triangular ubicaciones iniciales de los puntos 3D.
xyzPoints = triangulateMultiview(tracks, camPoses,...
    intrinsics);

% Ajustar poses de las cámaras 3D.
[xyzPoints, camPoses, reprojectionErrors] = bundleAdjustment(...
    xyzPoints, tracks, camPoses, intrinsics, FixedViewId=1, ...
    PointsUndistorted=true);

%% Desplegar cámaras ajustadas
figure;
plotCamera(camPoses, Size=0.2);
hold on

% Excluir puntos ruidosos.
goodIdx = (reprojectionErrors < 5);

% Desplegar puntos 3D densos.
pcshow(xyzPoints(goodIdx, :), VerticalAxis='y', VerticalAxisDir='down', MarkerSize=45);
grid on
hold off

loc1 = camPoses.AbsolutePose(1).Translation;
xlim([loc1(1)-5, loc1(1)+4]);
ylim([loc1(2)-5, loc1(2)+4]);
zlim([loc1(3)-1, loc1(3)+20]);
camorbit(0, -30);

title('Reconstrucción densa');