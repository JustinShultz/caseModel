syms ca cw hwin hwa
A0 = diag([cw,ca]);
A1 = [hwa, -hwa; -hwa, hwa+hwin];
Z = zeros(2,2);
Z2 = zeros(4,4);
B0 = [ A0+A1, Z; -A0, A0];
B1 = [Z,-A0; Z Z];
n = 3;
An = [B0 zeros(4,4*(n-1));
    zeros(4*(n-1),4*(n))];
for i = 1:(n-1)
    An((i*4+1):(i+1)*4,(i*4+1):(i+1)*4) = B0;
    An((i*4+1):(i+1)*4,((i-1)*4+1):i*4) = B1;
end
% invB0 = inv(B0);
% C = B1*invB0;
invA01 = inv(A0+A1);
A0invA01 = A0*invA01;
invB0 = [invA01, Z; invA01, inv(A0)];
C =  [-A0*invA01, -eye(2); Z Z];
invB0C = [-invA01*A0*invA01, -invA01;
    -invA01*A0*invA01, -invA01];
invAn = [invB0 zeros(4,4*(n-1));
    zeros(4*(n-1),4*(n))];
for j = 0:(n-1)
    for i = 1:n
        ind = ((i-1)*4+1):i*4
        invAn(ind,ind-j*4) = invB0;
    end
end
