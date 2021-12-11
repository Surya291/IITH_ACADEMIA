%%%%%%%%%%%%%%% LOW PASS TO HIGH PASS CONVERSION
%%%%%%% WE DO IT BY SHIFTING H(w) TO H(w - pi)
%%%%%%% its multiplied by (-1)^n in h(n)

 [x,Fs] = audioread("msmn1.wav");
  W = Fs/2;
   L = 110250;
 
 Ts=1/Fs;
 t=-2.5:Ts:2.5-Ts;
 
  h1=sinc(t*W);
  
fs=2*pi*(-L/2:(L/2)-1)./L;
fr=Fs*(-L/2:(L/2)-1)./L; 
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ques (e)
for n =  1:length(X)
    h2(n) = double(h1(n)*((-1)^n));
end    

H2 = fft(h2);

%%%%%%%%%%%%%%%%%%%%%%% PLOTTING MAG OF TRANSFER FUNCTIONS WRT w and f
figure(5);
plot(fs,fftshift(abs(H2)));
title('high pass mag plot with w_c_F = 0.50Fs')
xlabel('w');
ylabel('|H(w)|');
saveas (gcf,'HPF_w W_C=(0.50Fs).png');

figure(6);
plot(fr,fftshift(abs(H2)));
title('high pass mag plot with w_c_F = 0.50Fs')
xlabel('f');
ylabel('|H(f)|');
saveas (gcf,'HPF_f W_C=(0.50Fs).png');

%%%%%%%%%%%%%%%%%%%%%%%% GENERATING OUTPUT
X = fft(x);
Y = zeros(length(X),1);
    for i  = 1:length(X)
    Y(i) = X(i)*abs(H2(i));
    end    
    
 y = ifft(Y);
    
audiowrite('high_pass_w_C=(0.50Fs).wav',y,22050);
soundsc(y,22050);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% here we cannot hear the low frequency components at all.
