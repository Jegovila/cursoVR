opticFlow = opticalFlowHS

cam = webcam(1);
cam.Resolution = '640x480';

h = figure;

while (1)
    frameRGB = snapshot(cam);
    frameGray = im2gray(frameRGB);  

    flow = estimateFlow(opticFlow,frameGray);

    imshow(frameRGB)
    hold on
    plot(flow,'DecimationFactor',[5 5],'ScaleFactor',120);
    hold off
    pause(10^-3)
    text(10,30,sprintf('%.6f',max(max(flow.Magnitude))), 'Color', [1,0,0], 'FontSize', 24)
    if ~isempty(get(h,'CurrentCharacter'))
        break
    end

end

clear cam
close all