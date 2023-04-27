function [m,n,p,Ha,Histo]=HistogramaAcumulado(Im)
[m,n,p]=size(Im);
for c=1:p
  %Matriz 3x256 Histo(canales,linea de 0 a 256)
    Histo(c,:)=linspace(0,0,256); %Espacio Lineal desde 0 a 256 con valor 0
     for q=1:m
        for r=1:n
            Histo(c,Im(q,r,c)+1)=Histo(c,Im(q,r,c)+1)+1; %Recorrer 1 todos los pixeles a la derecha para que sean reconocidos por matlab
        end
     end

     for i=1:256 %Normalizamos todo Histo
        Histo(c,i)=Histo(c,i)/(m*n);    
     end

    Ha(c,1)=Histo(c,1)/(m*n); %Normalizamos los valores entre 0 y 1 de nuevo
    for i=2:256
        Ha(c,i)=Ha(c,i-1)+Histo(c,i); %Suma todos los pixeles por canal dando asi tres filas con acumulados; una fila por cada canal
    end 
end
end