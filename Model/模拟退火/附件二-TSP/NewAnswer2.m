function S2 = NewAnswer2(S1)
N = length(S1);
a = round(rand(1,2)*(N-1) + 1); %rand(1,2)产生1行2列0和1直接的随机数
S_left = S1(1:min(a)-1);
S_mid = fliplr(S1(min(a):max(a))); %左右翻转中间的矩阵(包括选中的这两个城市和它们之间的所有城市)
S_right = S1(max(a)+1:N);
S2 = [S_left,S_mid,S_right];
end