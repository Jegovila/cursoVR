clear all
close all

cam = webcam(1);
cam.Resolution = '640x480';

fig = figure(1);
while(1)
    I = snapshot(cam);
    Ig = rgb2gray(I);

    [m,n] = size(Ig);
    U = zeros(m,n);
    V = zeros(m,n);
    S = zeros(m,n);
    
    h = ones(7,7)*(1/49);
    Id = double(Ig);
    If = imfilter(Id,h);
    
    Hx = [-1 0 1];
    Hy = [-1;0;1];
    
    Ix = imfilter(If,Hx);
    Iy = imfilter(If,Hy);
    
    Ixx = imfilter(Ix,Hx);
    Iyy = imfilter(Iy,Hy);
    
    Ixy = Ix .* Iy;
    
    %%%% ----- Harris ----- %%%%
    HE11 = Ix .* Ix;
    HE22 = Iy .* Iy;
    HE12 = Ix .* Iy; % = HE21
    
    Hg = [0 1 2 1 0;
        1 3 5 3 1;
        2 5 9 5 2;
        1 3 5 3 1;
        0 1 2 1 0]*(1/57);
    
    A = imfilter(HE11,Hg);
    B = imfilter(HE22,Hg);
    C = imfilter(HE12,Hg);
    
    alpha = 0.04;
    
    V = ((A .* B) - (C .* C)) - alpha * (A + B).^2;
    
    U = V > 200;
    
    
    vecindad = 10;
    
    for r = 1:m
        for  c = 1:n
           if (U(r,c)) 
            
               I1 = [r-vecindad 1];
               I2 = [r+vecindad m];
               I3 = [c-vecindad 1];
               I4 = [c+vecindad n];
               
               datxi = max(I1);
               datxs = min(I2);
               datyi = max(I3);
               datys = min(I4);
               
               Bloc = V(datxi:1:datxs, datyi:1:datys);
               MaxB = max(max(Bloc));
               
               if V(r,c) == MaxB
                   S(r,c) = 1;
               end
               
           end
        end
    end
    imshow(Ig)
    hold on
    for r = 1:m
        for c = 1:n
            if S(r,c)
                plot(c,r,'go')
            end
        end
    end
    hold off

    
    if ~isempty(get(fig,'CurrentCharacter'))
        break
    end
    pause(.01)
end

clear cam
close all