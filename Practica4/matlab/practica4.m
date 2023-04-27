% close all
% clear all
% 
% I = imread('lena.bmp');
% Ig = rgb2gray(I);
% F = fft2(Ig);
% 
% imshow((log(abs(F))),[])
% 
% figure
% imshow((Ig))
% 
% N=15;
% h = ones(N,N)*(1/(N*N));
% h(size(Ig,1),size(Ig,2))=0; %Rellenar la imagen con 0s
% figure
% imshow(h,[])
% 
% H = fft2(h);
% figure
% imshow(fftshift(log(abs(H))),[])
% 
% %Filtrado
% tstart = tic;
% G = F .* H;
% telapsed = toc(tstart)
% figure
% imshow((log(abs(G))),[])
% 
% %inversa fft
% g = ifft2(G);
% figure
% imshow(g,[]);

close all
clear all

I = imread('lena.bmp');
Ig = rgb2gray(I);
F = fftshift(fft2(Ig));

imshow(fftshift(Ig));
figure
imshow((log(abs(F))),[])

[x,y] = meshgrid(-256:255,-256:255);
z = sqrt(x.^2 + y.^2);
c = z > 30;

G = F .* c;
figure
imshow((log(abs(G))),[])

g = ifft2(G);
figure
imshow(g > 30,[]);

% 
% clear all
% close all
% 
% I = imread('lena.bmp');
% Ig = rgb2gray(I);
% 
% N=151;
% h = ones(N,N)*(1/(N*N));
% 
% tstart = tic;
% G = imfilter(Ig,h);
% telapsed = toc(tstart)

