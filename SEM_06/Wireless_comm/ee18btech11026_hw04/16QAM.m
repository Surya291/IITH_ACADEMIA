%%% 16 QAM

M = 16; % Modulation order 
k = log2(M); % Number of bits per symbol
n = 100000; % Number of bits to process
sps = 1; % Number of samples per symbol (oversampling factor)

data_in = randi([0 1],n,1); % Generate vector of binary data

dataInMatrix = reshape(data_in,length(data_in)/k,k);
sym_bit = bi2de(dataInMatrix);  %%% This return the data denoting each symbol [0-15] by dividing into tuples of len 4

mapped_bits = qammod(sym_bit,M,'bin');  %%% x
SNR_vector = [-5, -3,0,3, 5,7,10];
figure
for type = 1:4
    i=1;
    BER_vector = SNR_vector;
    h = channel_type(type,mapped_bits);
    signal = mapped_bits.*h; %%% y= xh
    
    for snr = SNR_vector
        noisy_signal = awgn(signal,snr,'measured');%%% y = xh+n
        demapped_bits = qamdemod(noisy_signal,M,'bin');%%% x_cap
        dataOutMatrix = de2bi(demapped_bits,k);
        data_out = dataOutMatrix(:); % Return data in column vector
        [no,BER] = biterr(data_in,data_out);
        BER_vector(i) = BER;
        i = i+1;
    end
    plot(SNR_vector, BER_vector);
    hold on

end
hold off
legend('Rayleigh','Rician : v = 0.75','Nakagami: m=5','Only AWGN');
title("SNR vs BER for 16 QAM");
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