 [x,Fs] = audioread("msmn1.wav");
  W = Fs/16;
%soundsc(x,22050);
 L = 110250;
 
 Ts=1/Fs;
 t=-2.5:Ts:2.5-Ts;
 

 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ques (a)
 h1=sinc(t*W);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ques (b)
H1=(fft(h1));
fs=2*pi*(-L/2:(L/2)-1)./L;
fr=Fs*(-L/2:(L/2)-1)./L; 
%%%%%%%%%%%%%%%%%%% plotting H(w)
 figure(2);
 plot(fs,fftshift(abs(H1)))
 title('W = 0.0625Fs wrt w')
 xlabel(' w');
 ylabel('|H(w)|')
 saveas (gcf,'H(w),W=(0.0625Fs).png');
%%%%%%%%%%%%%%%%%%% plotting H(f)
figure(3);
plot(fr,fftshift(abs(H1)));
title('W = 0.0625Fs wrt f')
xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,'H(f),W=(0.0625Fs).png');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ques (d)
X = fft(x);
Y = zeros(length(X),1);
    for i  = 1:length(X)
    Y(i) = X(i)*abs(H1(i));
    end    
    
 y = ifft(Y);
    
audiowrite('tmp_W=(0.0625Fs).wav',y,22050);
soundsc(y,22050);
%% ques (e)
for n =  1:length(X)
    h2(n) = double(h1(n)*((-1)^n));
end    

% % % % % % H2 = fft(h2);


figure(5);
plot(fs,fftshift(abs(H2)));
title('high pass mag plot with w_c_F = 0.9375Fs')
xlabel('w');
ylabel('|H(w)|');
saveas (gcf,'HPF_w :W_C=(0.9375Fs).png');

figure(6);
plot(fr,fftshift(abs(H2)));
title('high pass mag plot with w_c_F = 0.9375Fs')
xlabel('f');
ylabel('|H(f)|');
saveas (gcf,'HPF_f :W_C=(0.9375Fs).png');



