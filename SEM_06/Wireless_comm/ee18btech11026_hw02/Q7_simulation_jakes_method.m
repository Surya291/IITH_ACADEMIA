%%% Simulating Rayleigh fading 

% Choosing N0= 40 so that N is not a multiple of 4
N0 = 30;
N = (N0/4) - 0.5;
beta(N) = 0;
w(N) = 0;

ri_temp(N,2001) = 0;
rq_temp(N,2001) = 0;

ri_alpha(1,2001) = 0; %% Only inphase exists since alpha = 0

fi = [1 10 100];
Wi = 2*pi*fi ;
for i  = 1:3
    for n = 1:1:N
        for t = 0:0.001:2 %% 1000 smaples per sec for 2 sec duration.
           w(n) = Wi(i)*cos(2*pi*n/N0) ;
           beta(n) = pi*n/N;
           ri_temp(n,round(1000*t+1)) = 2*cos(beta(n))*cos(w(n)*t);
           rq_temp(n,round(1000*t+1)) = 2*sin(beta(n))*cos(w(n)*t);
           ri_alpha(1,round(1000*t+1)) = 2*cos(Wi(i)*t)/sqrt(2);
        end 
    end
    
    ri = sum(ri_temp) + ri_alpha;
    rq = sum(rq_temp);
    r  = sqrt(ri.^2 + rq.^2);
    
    %finding  the envelope average :  which should be 1
    mean=sum(r)/2001;
    subplot(3,1,i);
    time=0:0.001:2;
    %plot the figure and shift the envelope average to 0dB
    plot(time,(10*log10(r)-10*log10(mean)));
    xlabel('time');
    ylabel('Envelope(dB)');
    
    x = ['fd = ' int2str(fi(i)) ' Hz'];
    title(x);
    
end

