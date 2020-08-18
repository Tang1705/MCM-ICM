function S2 = NewAnswer(S1)%产生新解
%%输入
%S1:当前解
%%输出
%S2:新解
N=length(S1);
S2=S1;
a=round(rand(1,2)*(N-1)+1);    %产生两个随机位置用来交换
%round函数 四舍五入取整；ceil；floor；
W=S2(a(1));
S2(a(1))=S2(a(2));
S2(a(2))=W;    %得到一个新路线
end