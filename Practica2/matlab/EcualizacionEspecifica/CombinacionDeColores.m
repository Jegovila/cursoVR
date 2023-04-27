clearvars;
clc
close all;
Im1=imread("Desert.jpg");%Leemos Imagenes
Im2=imread("im1.jpg");

[m,n,p,Ha1,Hi1]=HistogramaAcumulado(Im1); %Sacamos Histogramas
[~,~,~,Ha2,Hi2]=HistogramaAcumulado(Im2);

figure(1)  %Graficamos
sgtitle("Imagen 1")
GraphRGB(3,2,1,Hi1);
GraphRGB(3,2,2,Ha1);
figure(2)
sgtitle("Imagen 2")
GraphRGB(3,2,1,Hi2);
GraphRGB(3,2,2,Ha2);
%Creamos matrices en ceros para rellenar, Imr es la imagen final
Imr = zeros(m,n,p);

for k=1:p %Normalizamos
    for i=1:256
        Ha1(k,i) = round(Ha1(k,i)*255);
        Ha2(k,i) = round(Ha2(k,i)*255);
    end
end

for k=1:p %contador para pixeles y canales para armar la imagen final
    for i=1:m
        for j=1:n
            z=1;%Valor de intensidad del acumulado
            Sk = Ha1(k,Im1(i,j,k)+1); %Se busca la intensidad del pixel de la imagen origen en el histograma acumulado
            while Ha2(k,z)-Sk < 0 %Se busca el valor de la intensidad en el segundo histograma acumulado con su diferencia hasta que se encuentre y de 0 su resta
                z=z+1;
                if z==257 %Si llega hasta el final sin encontrar su valor, se iguala al valor del histograma acumulado 1 para que se cierre el ciclo y tome el valor de coincidencia.
                    Ha2(k,z)=Sk;
                end
            end
            Imr(i,j,k)=z; %se asigna su nuevo color o intensidad y empieza de nuevo hasta sustituir todos los pixeles
        end
    end
end
Imr=uint8(Imr);
figure(3) %Mostramos las 3 imagenes
subplot(1,3,1)
imshow(Im1)
title("Imagen Origen");
subplot(1,3,2)
imshow(Im2)
title("Imagen Destino");
subplot(1,3,3)
imshow(uint8(Imr))
title("Imagen Resultante");
[~,~,~,Ha3,Hi3]=HistogramaAcumulado(Imr);
figure(4)
sgtitle("Imagen Resultante")
GraphRGB(3,2,1,Ha2);
GraphRGB(3,2,2,Ha3);
