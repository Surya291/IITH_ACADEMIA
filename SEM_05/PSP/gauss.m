clear all;
clc;


v1 = 1.04;
v4 = 1.04;
v1_abs = 1.04;

P1 = 0.8;
P2 = -0.6;
P3 = -0.8;

Q2 = -0.7;
Q3 = -0.7;



y11 = -15i;
y12 = 10i ;
y13 =  5i;
y14 = 0;

y21 = 10i;
y22 = -18i;
y23 = 0 ;
y24 = 8i;

y31 = 5i;
y32 = 0;
y33 = -10i;
y34 = 5i;

y41 = 0;
y42 = 8i;
y43 = 5i;
y44 = -13i;

%%% guess variables
v2 = 1;
v3 = 1;

for i =  1: 20
  
  printf("Iteration %d\n",i);

  
%    Q1 = -abs(y11)*abs(v1)*abs(v1)*sin(angle(y11)+angle(v1)-angle(v1)) -abs(y12)*abs(v2)*abs(v1)*sin(angle(y12)+angle(v2)-angle(v1))  -abs(y13)*abs(v3)*abs(v1)*sin(angle(y13)+angle(v3)-angle(v1))  -abs(y14)*abs(v1)*abs(v4)*sin(angle(y14)+angle(v4)-angle(v1));
%    v1 = (((P1-(Q1*1i))/conj(v1)) - (y12*v2) - (y13*v3) - (y14*v4))*(1/y11);
%    v1 = (v1/abs(v1))*1.04;
%    
%    v2 = (((P2-(Q2*1i))/conj(v2)) - (y21*v1) - (y23*v3) - (y24*v4))*(1/y22);
%    v3 = (((P3-(Q3*1i))/conj(v3)) - (y31*v1) - (y32*v2) - (y34*v4))*(1/y33);
%    
%    disp([abs(v1) angle(v1)])
%    %disp(Q1)
%    disp([abs(v2) angle(v2)])
%    disp([abs(v3) angle(v3)])
    
    
    
  Q1 = -1*abs(y11)*abs(v1)*abs(v1) * sin( angle( y11) + angle(v1) - angle(v1) )  - abs(y12) *abs(v1) *abs(v2) * sin( angle( y12) + angle(v2) - angle(v1) )  - (abs(y13) *abs(v1) *abs(v3) ) * sin( angle( y13) + angle(v3) - angle(v1) )  -abs(y14) *abs(v1) *abs(v4)  * sin( angle( y14) + angle(v4) - angle(v1) ) ;
  
  v1 = (1/ y11) * ( ( (P1 -i*Q1)/conj(v1) ) - ( y12*v2 + y13*v3 + y14*v4 ) );
  v1 = ( v1/abs(v1) )*1.04;
  
  v2 = (1/y22) * ( ( (P2 -i*Q2)/conj(v2) ) - ( y21*v1 + y23*v3 + y24*v4 ) );

  v3 = (1/y33) * ( ( (P3 -i*Q3)/conj(v3) ) - ( y31*v1 + y32*v2 + y34*v4 ) );
  
      disp([abs(v1) angle(v1)])
    %disp(Q1)
    disp([abs(v2) angle(v2)])
    disp([abs(v3) angle(v3)])
  
    
end