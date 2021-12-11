clear all;
clc;

%%% t bus

Y11 = 15 ; Y12 = 10 ; Y13 = 5 ; Y14 = 0 ;
Y21 = 10 ; Y22 = 18 ; Y23 = 0 ; Y24 =  8;
Y31 = 5  ; Y32 = 0  ; Y33 = 10; Y34 =  5;
Y41 = 0  ; Y42 = 8  ; Y43 = 5 ; Y44 = 13;

t11 = -(pi/2) ; t12 = (pi/2)   ; t13 = (pi/2) ; t14 = 0 ;
t21 =  (pi/2) ; t22 = -(pi/2)  ; t23 = 0;  t24 =  (pi/2);
t31 =  (pi/2) ; t32 = 0   ; t33 = -(pi/2); t34 = (pi/2);
t41 =  0 ; t42 = (pi/2)   ; t43 =  (pi/2); t44 = -(pi/2);

%%% Power 
P1 = 0.8; P2 = -0.6; P3 = -0.8;
Q2 = -0.7; Q3 = -0.7;


%%% Defining the known states..
d4 = 0; v1 = 1.04; v4 = 1.04;

%%% init unknowns ...
d1 = 0; d2 = 0; d3 = 0; 
v2 = 1; v3 = 1;

X = [d1; d2; d3; v2; v3];
disp(X');

for m = 1:30
  
  printf("Iteration %d\n\n", m);
  
  fp1 =       Y11*v1*v1*cos(t11) ;
  fp1 = fp1 + Y12*v2*v1*cos(t12 + d2 - d1);
  fp1 = fp1 + Y13*v3*v1*cos(t13 + d3 - d1);
  fp1 = fp1 + Y14*v4*v1*cos(t14 + d4 - d1);
  fp1 = fp1 - P1; 
  
  
  fp2 =       Y21*v1*v2*cos(t21 + d1 - d2);
  fp2 = fp2 + Y22*v2*v2*cos(t22);
  fp2 = fp2 + Y23*v3*v2*cos(t23 + d3 - d2);
  fp2 = fp2 + Y24*v4*v2*cos(t24 + d4 - d2);
  fp2 = fp2 - P2;
  
  
  fp3 =       Y31*v1*v3*cos(t31 + d1 - d3);
  fp3 = fp3 + Y32*v2*v3*cos(t32 + d2 - d3);
  fp3 = fp3 + Y33*v3*v3*cos(t33 );
  fp3 = fp3 + Y34*v4*v3*cos(t34 + d4 - d3);
  fp3 = fp3 - P3;
  
  
  fq2 =       -Y21*v1*v2*sin(t21 + d1 - d2);
  fq2 = fq2 + -Y22*v2*v2*sin(t22 );
  fq2 = fq2 + -Y23*v3*v2*sin(t23 + d3 - d2);
  fq2 = fq2 + -Y24*v4*v2*sin(t24 + d4 - d2);
  fq2 = fq2 - Q2;
  
  
  
  fq3 =       -Y31*v1*v3*sin(t31 + d1 - d3);
  fq3 = fq3 + -Y32*v2*v3*sin(t32 + d2 - d3);
  fq3 = fq3 + -Y33*v3*v3*sin(t33);
  fq3 = fq3 + -Y34*v4*v3*sin(t34 + d4 - d3);
  fq3 = fq3 - Q3;
  
  fx = [fp1 ; fp2 ; fp3 ;fq2 ; fq3];
  %%%%% Jacobian....
  
  J11 = Y12*v1*v2*sin(t12 +d2 - d1) + Y13*v1*v3*sin(t13 +d3 - d1) + Y14*v1*v4*sin(t14 +d4 - d1);
  J12 = -Y12*v1*v2*sin(t12 +d2 - d1);
  J13 = -Y13*v1*v3*sin(t13 +d3 - d1);
  J14 = Y12*v1*cos(t12 +d2 - d1);
  J15 = Y13*v1*cos(t13 +d3 - d1);
  
  
  
  J21 = -Y21*v1*v2*sin(t21 + d1 - d2);
  J22 = Y21*v1*v2*sin(t21 + d1 - d2) + Y23*v3*v2*sin(t23 + d3 - d2) + Y24*v4*v2*sin(t24 + d4 - d2);
  J23 = -Y23*v3*v2*sin(t23 + d3 - d2);
  J24 = Y21*v1*cos(t21 + d1 - d2) + 2*Y22*v2*cos(t22) + Y23*v3*cos(t23 + d3 - d2) + Y24*v4*cos(t24 + d4 - d2);
  J25 = Y23*v2*cos(t23 +d3 - d2);
  
  
  J31 = -Y31*v1*v3*sin(t31 + d1 - d3);
  J32 = -Y32*v2*v3*sin(t32 + d2 - d3);
  J33 =  Y31*v1*v3*sin(t31 + d1 - d3) + Y32*v2*v3*sin(t32 + d2 - d3) + Y34*v4*v3*sin(t34 + d4 - d3);
  J34 =  Y32*v3*cos(t32 + d2 - d3);
  J35 =  Y31*v1*cos(t31 + d1 - d3) + Y32*v2*cos(t32 + d2 - d3) + 2*Y33*v3*cos(t33) + Y34*v4*cos(t34 + d4 - d3);
  
  J41 = -Y21*v1*v2*cos(t21 + d1 - d2);
  J42 =  Y21*v1*v2*cos(t21 + d1 - d2) + Y23*v3*v2*cos(t23 + d3 - d2) + Y24*v4*v2*cos(t24 + d4 - d2);
  J43 = -Y23*v3*v2*cos(t23 + d3 - d2);
  J44 = -Y21*v1*sin(t21 + d1 - d2) + -2*Y22*v2*sin(t22 ) + -Y23*v3*sin(t23 + d3 - d2) + -Y24*v4*sin(t24 + d4 - d2);
  J45 = -Y23*v2*sin(t23 + d3 - d2);
  
  
  J51 = -Y31*v1*v3*cos(t31 + d1 - d3);
  J52 = -Y32*v2*v3*cos(t32 + d2 - d3);
  J53 =  Y31*v1*v3*cos(t31 + d1 - d3) + Y32*v2*v3*cos(t32 + d2 - d3) + Y34*v4*v3*cos(t34 + d4 - d3);
  J54 = -Y32*v3*sin(t32 + d2 - d3);
  J55 = -Y31*v1*sin(t31 + d1 - d3) + -Y32*v2*sin(t32 + d2 - d3) + -2*Y33*v3*sin(t33) + -Y34*v4*sin(t34 + d4 - d3);
  
  
  J = [J11 J12 J13 J14 J15 ; J21 J22 J23 J24 J25 ; J31 J32 J33 J34 J35 ; J41 J42 J43 J44 J45 ; J51 J52 J53 J54 J55];
  X = X - J\fx;
  
  d1 = X(1) ; d2 = X(2) ; d3 = X(3) ; v2 = X(4) ; v3 = X(5);
  
  %disp(X);
  disp('');
  
  printf("Mag. of v1 : %.5f , Phase(in deg) of v1 : %.5f\n" , 1.04000,d1*(180/pi) );
  #printf("Q1 value : %.5f\n",Q1);
  printf("Mag. of v2 : %.5f , Phase(in deg) of v2 : %.5f\n" , v2,d2*(180/pi) );
  printf("Mag. of v3 : %.5f , Phase(in deg) of v3 : %.5f\n" , v3,d3*(180/pi) );

  printf('\n')
  
end
