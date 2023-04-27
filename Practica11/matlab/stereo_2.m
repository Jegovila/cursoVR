cam1 = webcam(1);
cam2 = webcam(3);



t0 = clock;

while etime(clock,t0) < 20

frameLeft =  snapshot(cam1);
frameRight = snapshot(cam2);

[frameLeftRect, frameRightRect] = rectifyStereoImages(frameLeft, frameRight, stereoParams);

frameLeftGray  = rgb2gray(frameLeftRect);
frameRightGray = rgb2gray(frameRightRect);
    
%disparityMap = disparitySGM(frameLeftGray, frameRightGray);
disparityMap = disparityBM(frameLeftGray, frameRightGray);
imshow(disparityMap, [0, 128]);
colormap jet

pause(.01)

end

clear cam1
clear cam2