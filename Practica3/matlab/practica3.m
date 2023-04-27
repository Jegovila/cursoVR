clear all
close all

cam = webcam(1);
cam.Resolution = '320x240';

fig = figure;
while(1)
    I = snapshot(cam);
    Ig = rgb2gray(I);

    %BOX
    n = 3;
    h_box = ones(n,n)*(1/(n*n));
    I_box = imfilter(Ig,h_box);

    %GAUSS
    h_g = [0 1 2 1 0;
        1 3 5 3 1;
        3 5 9 5 3;
        1 3 5 3 1;
        0 1 2 1 0];
    h_g = h_g *(1/(sum(sum(h_g))));
    I_g = imfilter(I,h_g);

    %BORDES
    %SOBEL
    hx = [-1 0 1;
        -2 0 2;
        -1 0 1];
    hy = [-1 -2 -1;
        0 0 0;
        1 2 1];
    
    % %ROBERTS
    % hx = [0 1;
    %     -1 0];
    % hy = [-1 0;
    %     0 1];
    
    Ix = imfilter(Ig,hx);
    Iy = imfilter(Ig,hy);
    
    Ix = abs(Ix);
    Iy = abs(Iy);
    
    umbral = 100;
    Ix = Ix > umbral;
    Iy = Iy > umbral;
    
    Is = Ix + Iy;

    %KIRSCH (COMPÁS)
%     H0 = [-1 0 1;-2 0 2;-1 0 1];
%     H1 = [-2 -1 0;-1 0 1;0 1 2];
%     H2 = [-1 -2 -1;0 0 0;1 2 1];
%     H3 = [0 -1 -2;1 0 -1;2 1 0];
%     H4 = -H0;
%     H5 = -H1;
%     H6 = -H2;
%     H7 = -H3;
%     
%     D0 = imfilter(Ig,H0);
%     D1 = imfilter(Ig,H1);
%     D2 = imfilter(Ig,H2);
%     D3 = imfilter(Ig,H3);
%     D4 = -D0;
%     D5 = -D1;
%     D6 = -D2;
%     D7 = -D3;
%     
%     y0 = max(D0,D1);
%     y1 = max(y0,D2);
%     y2 = max(y1,D3);
%     y3 = max(y2,D4);
%     y4 = max(y3,D5);
%     y5 = max(y4,D6);
%     y6 = max(y5,D7);
%     
%     Ik = y6;
%     Ik = Ik > 80;

    %NITIDEZ
    L = [1 1 1;1 -8 1;1 1 1];
    w = 1.15;
    
    IL = imfilter(Ig,L); %BORDES
    IN = Ig - w*IL;

%     subplot(2,2,1)
%     imshow(I_box)
%     subplot(2,2,2)
%     imshow(I_g)
%     subplot(2,2,3)
%     imshow(Is)
%     subplot(2,2,4)
%     imshow(IN)

    pause(.01)
    if ~isempty(get(fig,'CurrentCharacter'))
        break
    end
    
end

clear cam
close all