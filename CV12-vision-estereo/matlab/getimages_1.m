cam1 = webcam(1);
cam2 = webcam(3);

cam1.FocusMode = 'manual'
cam2.FocusMode = 'manual'

cam1.Focus = 0
cam2.Focus = 0

preview(cam1)
preview(cam2)

for i=1:20
    I1 = snapshot(cam1);
    I2 = snapshot(cam2);

    outputFileName1 = fullfile('G:\My Drive\clases\vision robotica\11 Geometria epipolar\D\', ['img' num2str(i) '.jpg']);
    outputFileName2 = fullfile('G:\My Drive\clases\vision robotica\11 Geometria epipolar\I\', ['img' num2str(i) '.jpg']);
    
    pause
    
    imwrite(I1, outputFileName1);
    imwrite(I2, outputFileName2);
end

clear cam1
clear cam2