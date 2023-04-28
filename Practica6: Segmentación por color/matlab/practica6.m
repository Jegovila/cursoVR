%Correr primero 'color.m'
cam = webcam(1);
cam.Resolution = '320x240';
cam.ExposureMode = 'manual';
cam.Exposure = -3;
IBW = zeros([240,320]);

I = snapshot(cam);
[m,n,o] = size(I);
Hblob = vision.BlobAnalysis;

fig = figure(1);
s = 4;
while(1)
    I = snapshot(cam);

    for i = 1:m
        for j = 1:n
            if (I(i,j,1) > (Ar - s*Dr)) &&...
                    (I(i,j,1) < (Ar + s*Dr)) &&...
                    (I(i,j,2) > (Ag - s*Dg)) &&...
                    (I(i,j,2) < (Ag + s*Dg)) &&... 
                    (I(i,j,3) > (Ab - s*Db)) &&...
                    (I(i,j,3) < (Ab + s*Db)) 
                IBW(i,j) = 1;
            else
                IBW(i,j) = 0;
            end
        end
    end
    
    IBW = logical(IBW);
    %imshow(IBW)
    [area,centroid,bbox] = Hblob(IBW);
    [value, index] = (max(area(:)));
    imshow(I);

    if value > 20
        hold on
        rectangle('Position',bbox(index,:),...
             'EdgeColor','r','LineWidth',2,'LineStyle','-')
        hold off
    end

    if ~isempty(get(fig,'CurrentCharacter'))
        break
    end
    pause(.01)
 end

clear cam
close all