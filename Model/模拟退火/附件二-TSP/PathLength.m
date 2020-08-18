%函数PathLength，计算各个路径长度
function len=PathLength(D,Chrom)
%%计算各个个体的路线长度
%输入：
%D 两两城市之间的距离
%Chrom 个体的轨迹
[row,col]=size(D);    %得到矩阵D的行数和列数，分别存在变量row，col中
MIND=size(Chrom,1);     %将矩阵chrom的行数赋给变量MIND
len=zeros(MIND,1);
for i=1:MIND
    p=[Chrom(i,:) Chrom(i,1)];
    i1=p(1:end-1);
    i2=p(2:end);
    len(i,1)=sum(D((i1-1)*col+i2));%求两两之间的距离
end