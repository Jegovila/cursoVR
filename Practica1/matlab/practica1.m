clear all
close all

cam = webcam(1);
cam.Resolution = '320x240';
theta = pi/6;

fig = figure(1);
while(1)
    I = snapshot(cam);
    I = rgb2gray(I);

    [m,n] = size(I);
    I2 = zeros(700,700);

    for i = 1:m
        for j = 1:n
            x = ceil(i * cos(theta) + j * sin(theta));
            y = ceil(-i * sin(theta) + j * cos(theta));
            I2(x+150,y+300) = I(i,j);
        end
    end

    [m2,n2] = size(I2);
    for i = 1:m2-1
        for j = 1:n2-1
            if(I2(i,j)==0)
                I2(i,j) = I2(i,j+1);
            end
        end
    end
    
    I2 = uint8(I2);
    imshow(I2)
    
    if ~isempty(get(fig,'CurrentCharacter'))
        break
    end
end

clear cam