function GraphRGB (Filas,Col,NumEspacio,VectorAGraficar)
subplot(Filas,Col,NumEspacio);
bar(VectorAGraficar(1,:),'r');
subplot(Filas,Col,NumEspacio+Col);
bar(VectorAGraficar(1,:),'g');
subplot(Filas,Col,NumEspacio+2*Col);
bar(VectorAGraficar(1,:),'b');
end