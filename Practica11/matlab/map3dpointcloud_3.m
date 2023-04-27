cam1 = webcam(1);
cam2 = webcam(3);


frameLeft =  snapshot(cam1);
frameRight = snapshot(cam2);

[frameLeftRect, frameRightRect] = rectifyStereoImages(frameLeft, frameRight, stereoParams);

frameLeftGray  = rgb2gray(frameLeftRect);
frameRightGray = rgb2gray(frameRightRect);
    
disparityMap = disparitySGM(frameLeftGray, frameRightGray);

points3D = reconstructScene(disparityMap, stereoParams);

% Convert to meters and create a pointCloud object
points3D = points3D ./ 1000;
ptCloud = pointCloud(points3D, 'Color', frameLeftRect);

% Create a streaming point cloud viewer
player3D = pcplayer([-3, 3], [-3, 3], [0, 8], 'VerticalAxis', 'y', ...
    'VerticalAxisDir', 'down');

% Visualize the point cloud
view(player3D, ptCloud);


clear cam1
clear cam2