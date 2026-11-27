cam1 = webcam(1);
cam2 = webcam(3);

peopleDetector = vision.PeopleDetector;

t0 = clock;

while etime(clock, t0) < 15
    % Read the frames.
    frameLeft = snapshot(cam1);
    frameRight = snapshot(cam2);
    
    % Rectify the frames.
    [frameLeftRect, frameRightRect] = ...
        rectifyStereoImages(frameLeft, frameRight, stereoParams);
    
    % Convert to grayscale.
    frameLeftGray  = rgb2gray(frameLeftRect);
    frameRightGray = rgb2gray(frameRightRect);
    
    % Compute disparity. 
    disparityMap = disparitySGM(frameLeftGray, frameRightGray);
    
    % Reconstruct 3-D scene.
    points3D = reconstructScene(disparityMap, stereoParams);
    points3D = points3D ./ 1000;
    ptCloud = pointCloud(points3D, 'Color', frameLeftRect);
    view(player3D, ptCloud);
    
    % Detect people.
    bboxes = peopleDetector.step(frameLeftGray);
    
    if ~isempty(bboxes)
        % Find the centroids of detected people.
        centroids = [round(bboxes(:, 1) + bboxes(:, 3) / 2), ...
            round(bboxes(:, 2) + bboxes(:, 4) / 2)];
        
        % Find the 3-D world coordinates of the centroids.
        centroidsIdx = sub2ind(size(disparityMap), centroids(:, 2), centroids(:, 1));
        X = points3D(:, :, 1);
        Y = points3D(:, :, 2);
        Z = points3D(:, :, 3);
        centroids3D = [X(centroidsIdx), Y(centroidsIdx), Z(centroidsIdx)];
        
        % Find the distances from the camera in meters.
        dists = sqrt(sum(centroids3D .^ 2, 2));
        
        % Display the detect people and their distances.
        labels = cell(1, numel(dists));
        for i = 1:numel(dists)
            labels{i} = sprintf('%0.2f meters', dists(i));
        end
        dispFrame = insertObjectAnnotation(frameLeftRect, 'rectangle', bboxes,...
            labels);
        imshow(dispFrame);
        break
    else
        dispFrame = frameLeftRect;
        imshow(dispFrame);
    end

end

clear cam1
clear cam2