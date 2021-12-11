%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% THIS SECTION OF THE CODE IS IMPLEMENTING THE NOTCH FILTER!

% READING THE INPUT WAV FILE WITH Fs = 11025 
[x,Fs] = audioread("cutafew.wav");
fn = 5000;
L= length(x);
fr=Fs*(-L/2:(L/2)-1)./L;


H1 = fft(x);
n=0:length(x) - 1;

% NOISE IS A COSINE SIGNAL WITH f = 5000
noise  = cos(2*pi*n*fn/Fs);
H2 = fft(noise);

% ADDING NOISE TO THE INPUT WAV FILE
y = x+transpose(noise);
H3 = fft(y);


% APPLYING THE NOTCH FILTER !!!
wo = fn*2/Fs;
bw =  wo;
[b,a] = iirnotch(wo,bw);
z = filter(b,a,y);
H4 = fft(z);
soundsc(y,Fs)

figure(1)
plot(fr,fftshift(abs(H1)))
title("H1 -- > INPUT ")
xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,' ONLY INPUT.png');


figure(2)
plot(fr,fftshift(abs(H2)))
title("H2 -- > NOISE")
xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,' ONLY NOISE.png');

figure(3)
plot(fr,fftshift(abs(H3)))
title("H3 --> INPUT + NOISE")
xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,'  NOISE + INPUT.png');

figure(4)
plot(fr,fftshift(abs(H4)))
title("H4 --> FILTERED OUTPUT")
xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,' OUTPUT.png');



%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% THIS SECTION OF CODE IS IMPLEMNTING THE MOVING AVERAGE FILTER WHICH DOES
% THE JOB OF A LOW PASS FILTER!!

% READING THE INPUT WAV FILE WITH Fs = 11025
[x,Fs] = audioread("cutafew.wav");
fn = 5000;
L= length(x);
fr=Fs*(-L/2:(L/2)-1)./L;

H1 = fft(x);
n=0:length(x) - 1;

% NOISE IS A COSINE SIGNAL WITH f = 5000
noise  = cos(2*pi*n*fn/Fs);
H2 = fft(noise);

% ADDING NOISE TO THE INPUT WAV FILE
y = x+transpose(noise);
H3 = fft(y);

% APPLYING THE TWO POINT MOVING AVG !!
z = movmean(y,2);
H4 = fft(z);
%soundsc(z,Fs)


figure(1)
plot(fr,fftshift(abs(H1)))
title("H1 --> INPUT ")
xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,'2-ONLY INPUT.png');

figure(2)
plot(fr,fftshift(abs(H2)))
title("H2 --> NOISE")
xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,'2- ONLY NOISE.png');

figure(3)
plot(fr,fftshift(abs(H3)))
title("H3 --> INPUT + NOISE")
xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,' 2- INPUT + NOISE.png');

figure(4)
plot(fr,fftshift(abs(H4)))
title("H4 --> FILTERED OUTPUT")

xlabel('freq(Hz)');
ylabel('|H(f)|');
saveas (gcf,'2- OUTPUT.png');


