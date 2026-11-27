clear all
close all

cam = webcam(1);
cam.Resolution = '320x240';

fig = figure(1)

while(1)
    I = snapshot(cam);
    Ig = rgb2gray(I);
    Ig_mod = double(Ig);
    Ig_mod = Ig_mod * 0.3 + 80;

    subplot(2,2,1)
    imshow(Ig)
    subplot(2,2,2)
    imhist(Ig)
    subplot(2,2,3)
    imshow(uint8(Ig_mod))
    subplot(2,2,4)
    imhist(uint8(Ig_mod))

    %% ADAPTACIÓN AUTOMÁTICA DEL CONTRASTE
%     I = snapshot(cam);
%     Ig = rgb2gray(I);
%     Ig_mod = double(Ig);
%     Ig_mod = Ig_mod * 0.3 + 80;
% 
%     %crear imagen destino
%     [m,n] = size(Ig_mod);
%     Iad = zeros(m,n);
%     
%     alto = max(max(Ig_mod));
%     bajo = min(min(Ig_mod));
%     
%     for i=1:m
%         for j=1:n
%             Iad(i,j) = ((Ig_mod(i,j) - bajo) / (alto - bajo)) * 255;
%         end
%     end
%     
%     Iad = uint8(Iad);
%     Ig_mod = uint8(Ig_mod);
%     
%     subplot(2,2,1)
%     imshow(Ig_mod)
%     subplot(2,2,2)
%     imhist(Ig_mod)
%     subplot(2,2,3)
%     imshow(Iad)
%     subplot(2,2,4)
%     imhist(Iad)

%% Ecualización lineal del histograma
% I = snapshot(cam);
% Ig = rgb2gray(I);
% Ig_mod = double(Ig);
% Ig_mod = Ig_mod * 0.3 + 80;
% Ig = uint8(Ig_mod);
% 
% [m,n] = size(Ig);
% 
% [cont, x] = imhist(Ig);
% va = 0;
% 
% %Histograma ACUMULADO
% for i = 1:256
%     H(i) = cont(i) + va; 
%     va = H(i);
% end
% 
% % ECUALIZACIÓN
% for i = 1:m
%     for j = 1:n
%         Ieq(i,j) = H(Ig(i,j)+1) * (255 / (m*n));
%     end
% end
% 
% %Calcular histogramas de imagen ecualizada
% [cont_eq, x_eq] = imhist(Ieq);
% va_eq = 0;
% 
% %Histograma ACUMULADO
% for i = 1:256
%     H_eq(i) = cont_eq(i) + va_eq; 
%     va_eq = H_eq(i);
% end
% 
% Ieq = uint8(Ieq);
% 
% subplot(2,3,1)
% imshow(Ig)
% subplot(2,3,2)
% imhist(Ig)
% subplot(2,3,3)
% stem(x,H)
% 
% subplot(2,3,4)
% imshow(Ieq)
% subplot(2,3,5)
% imhist(Ieq)
% subplot(2,3,6)
% stem(x_eq,H_eq)


end