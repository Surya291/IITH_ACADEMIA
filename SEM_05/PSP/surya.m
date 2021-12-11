clc;
clear all;

%Question 1
y11 = -15i;
y12 = 10i;
y13 = 5i;
y14 = 0;

y21 = 10i;
y22 = -18i;
y23 = 0;
y24 = 8i;

y31 = 5i;
y32 = 0;
y33 = -10i;
y34 = 5i;

y41 = 0;
y42 = 8i;
y43 = 5i;
y44 = -13i;

%known data
%Bus 1 is generator bus
P1 = 0.8;
v1 = 1.04;
%Bus 2 is load bus
P2 = -0.6;
Q2  = -0.7;
%Bus 3 is load bus
P3 = -0.8;
Q3  = -0.7;
%Bus 4 is slack bus with generator
v4 = 1.04;


%unknown data
v2 = 1;
v3 = 1;

for m = 1:30
    
    Q1 = -abs(y11)*abs(v1)*abs(v1)*sin(angle(y11)+angle(v1)-angle(v1)) -abs(y12)*abs(v2)*abs(v1)*sin(angle(y12)+angle(v2)-angle(v1))  -abs(y13)*abs(v3)*abs(v1)*sin(angle(y13)+angle(v3)-angle(v1))  -abs(y14)*abs(v1)*abs(v4)*sin(angle(y14)+angle(v4)-angle(v1));
    v1 = (((P1-(Q1*1i))/conj(v1)) - (y12*v2) - (y13*v3) - (y14*v4))*(1/y11);
    v1 = (v1/abs(v1))*1.04;
    
    v2 = (((P2-(Q2*1i))/conj(v2)) - (y21*v1) - (y23*v3) - (y24*v4))*(1/y22);
    v3 = (((P3-(Q3*1i))/conj(v3)) - (y31*v1) - (y32*v2) - (y34*v4))*(1/y33);
    
    disp(m)
    disp([abs(v1) angle(v1)])
    
    disp([abs(v2) angle(v2)])
    disp([abs(v3) angle(v3)])
    
   
end

%Question 3
Y = [y11-5i,y12,y13,y14;y21,y22,y23,y24;y31,y32,y33,y34;y41,y42,y43,y44-10i];
Z = inv(Y);

ifa = 1/Z(2,2);
ifb = 1/Z(3,3);

disp(ifa)
disp(ifb)



