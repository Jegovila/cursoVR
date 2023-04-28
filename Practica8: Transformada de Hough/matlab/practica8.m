close all
clear all

cam = webcam(1);
cam.Resolution = '320x240';
cam.ExposureMode = 'manual';
cam.Exposure = -3;

fig = figure(1);
fig.WindowState = 'maximized';


while(1)
    % Obtener imagen y binarizar
    I = snapshot(cam);
    Ig = rgb2gray(I);
    % Suavizado
    BW = edge(Ig,'sobel');
    subplot(2,2,[2])
    imshow(BW)
    
    % Espacio de parámetros de Hough
    [H,T,R] = hough(BW);
    subplot(2,2,[1,3])
    imshow(H,[],'XData',T,'YData',R,'InitialMagnification','fit');
    axis on, axis normal;
    hold on;
    
    % Encontrar los picos en el espacio de parámetros de Hough
    P = houghpeaks(H,15);
    x = T(P(:,2));
    y = R(P(:,1));
    plot(x,y,'s','color','red');
    
    % Encontrar las líneas a partir de los picos
    lines = houghlines(BW,T,R,P);
    subplot(2,2,4)
    imshow(I);
    hold on;

    for k = 1:length(lines)
       % Graficar las líneas
       xy = [lines(k).point1;lines(k).point2];
       plot(xy(:,1),xy(:,2),'LineWidth',3,'Color','green');
    end

   if ~isempty(get(fig,'CurrentCharacter'))
        break
   end
   pause(.01)

end

clear cam

