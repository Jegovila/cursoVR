clear all
close all

cam = webcam(1);
cam.ExposureMode = 'manual';
cam.Exposure =-3;

preview(cam);
pause(5)
closePreview(cam);

I = snapshot(cam);
%Seleccionar ROI
%doble click al polígono
[BW,x,y] = roipoly(I);

clear('cam')

imshow(I(ceil(min(y)):ceil(max(y)),ceil(min(x)):ceil(max(x)),:))

R = I(ceil(min(y)):ceil(max(y)),ceil(min(x)):ceil(max(x)),1);
G = I(ceil(min(y)):ceil(max(y)),ceil(min(x)):ceil(max(x)),2);
B = I(ceil(min(y)):ceil(max(y)),ceil(min(x)):ceil(max(x)),3);

%Media
Ar = mean(R(:));
Ag = mean(G(:));
Ab = mean(B(:));

%convertir a double
Rd = double(R);
Gd = double(G);
Bd = double(B);

%STD
Dr = std(Rd(:));
Dg = std(Gd(:));
Db = std(Bd(:));

I2(:,:,1) = R;
I2(:,:,2) = G;
I2(:,:,3) = B;
imshow(I2)
