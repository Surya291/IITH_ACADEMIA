clc
clear 
%% Reading the mp3 file

[X,Fs] = audioread('jersey.mp3');
disp(Fs);
audiowrite('jersey_0.wav',X,Fs);
Z = audioread('jersey_0.wav');
Y = zeros(10*Fs,1);
for i = 1: length(Z)
    Y(i,1) = Z(i,1);
end
L = length(Y);
%% Downsampling
a = zeros(length(Y)/3,1);
%Y = downsample(X,2);
for i = 1:length(Y)/18
    a(i) = Y(18*i);
end
%% Playing the audio
 PO = audioplayer(Y,Fs);
 play(PO);
%% Plotting the time domain .
t = 1:L;
plot(t,Y)

%% Plotting the freq domain.
Y_f = fft(Y);
Y_f = fftshift(Y_f);
f = Fs/2*linspace(-1,1,L);

plot(f,abs(Y_f)/Fs);

%% Plotting Sinc wave.
W = Fs;
Ts=1/Fs;
t=-2.5:Ts:2.5-Ts;
h1=sin(pi*t*W)/(pi*t*W);
%h1 = fftshift(h1);
%f = Fs/2*linspace(-1,1,L);
plot(t,h1);
 
