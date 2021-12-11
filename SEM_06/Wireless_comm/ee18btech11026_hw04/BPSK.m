

%%%%%%%%  For BPSK
n = 100000;
numBPSCS = 1 ; %%% log(M) : M = 2


bits = randi([0 1],n,1);
mapped_bits = wlanConstellationMap(bits,numBPSCS);
SNR_vector = [-5, -3,0,3, 5,7,10];
figure
for type = 1:4
    i=1;
    BER_vector = SNR_vector;
    h = channel_type(type,bits);
    signal = mapped_bits.*h;
    
    for snr = SNR_vector
        noisy_signal = awgn(signal,snr,'measured');
        decoded_bits = (noisy_signal>0);
        [no,BER] = biterr(bits,decoded_bits);
        BER_vector(i) = BER;
        i = i+1;
    end
    
    plot(SNR_vector, BER_vector);
    hold on

end
hold off
legend('Rayleigh','Rician : v = 0.75','Nakagami : m = 5','Only AWGN');
title("SNR vs BER for BPSK");
xlabel("SNR (in dB)");
ylabel("BER ");

function h = channel_type(type,bits)
    if type == 1
        h = random('Rayleigh',sqrt(1/2),size(bits)); 
    
    elseif type == 2
        v = 0.75;
        sigma = sqrt((1-v^2)/2);
        h =  random('Rician',v,sigma,size(bits));
    
    elseif type == 3
        m =5 ;
        h = random('Nakagami',m,1,size(bits));
    
    elseif type ==4
        h = ones(size(bits));
    end
end
    
    

