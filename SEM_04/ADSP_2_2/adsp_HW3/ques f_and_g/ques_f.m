a = 0.9;
Fs = 22050;
L = 110250;

syms z
H = (1-a)/(1-(a/z));
h = iztrans(H);%%%%%%%%%%%%%%%%%%%%%% h(n) is (9/10)^n/10 ; for only n >= 0
fprintf('h(n) is %s ; for only n >= 0',h)

n = linspace(0,5*Fs - 1, 5*Fs);

b = [0.1,0];
a = [1,-0.9];
[k,~] = impz(b,a,110250);

K = fft(k);%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% K IS THE FFT OF THE GIVEN H(z)
fs=2*pi*(-L/2:(L/2)-1)./L;

figure(1);
plot(fs,fftshift((K)));
title('The mag. plot of the TF of H(z)')
xlabel('w');
ylabel('|H(w)|');

figure(2);
zplane(b,a)
title("The pole-zero plot of H(z)")
saveas (gcf,'pole_zero_plot.png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% APPLYING h(n) TO THE GIVEN INPUT x(n)
[x,~] = audioread("msmn1.wav");
X = fft(x);
Y = zeros(length(X),1);
    for i  = 1:length(X)
    Y(i) = X(i)*abs(K(i));
    end    
    
y = ifft(Y);

audiowrite('tmp_q_f(applying LP H(z)).wav',y,22050);
%soundsc(y,22050)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 
b2 = [-0.1,0];
a2 = [-1,-0.9];

[high,t] = impz(b2,a2,110250);

A = fft(high);%%%%%%%%% A IS THE FFT OF THE highpass filter H(z)
fs=2*pi*(-L/2:(L/2)-1)./L;
%%%%%%%%%%%%%%%%%%%%%%% HIGH PASS TRANSFORMATION 
%%% for high pass  H(w-pi) is the highpass TF which trasforms H(z)--> H(-z)
%%% for high pass H(z) = (1-a)/(1+(a/z))
 
figure(2);
plot(fs,fftshift((A)));
title('The mag. plot of the "HIGH PASS form" of H(z)')
xlabel('w');
ylabel('|H_(w)|');

saveas(gcf,"mag_plot of high pass form.png")

[x,Fs] = audioread("msmn1.wav");
X = fft(x);
U = zeros(length(X),1);
    for i  = 1:length(X)
    U(i) = X(i)*abs(A(i));
    end 
figure  (6);  

plot(fs,fftshift(X));
hold on
plot(fs,fftshift(Y));
hold on
plot(fs,fftshift(U));
title('mag. plots for different TFs')
legend('INPUT:X','OUTPUT with LPF','OUTPUT with HPF')
xlabel('w');
ylabel('|H_(w)|');
hold off
saveas(gcf,"TF of input and output.png")

y_h = ifft(U);
audiowrite('tmp_q_g(applying HP H(z)).wav',y_h,22050);
soundsc(y_h,22050)

