%-------进来先清空环境-------%
clc;
clear all;
close all;
%----------设置参数----------%
T = 1000;         %初始温度（尽量高）
T_min = 1;     %最低温度
a = 0.9;         %降温系数
n = 0;           %迭代计数
lb = 0;          %下界
ub = 10;         %上界
X = lb + rand * (ub - lb);          %在上界、下界之间随机产生初始点

%----------开始迭代----------%
while T > T_min
        %随机取新解
        X1 = lb + rand * (ub - lb);

        %计算函数值差值
        EX = fitness(X1) - fitness(X);

        if EX < 0
            break
        elseif rand < exp(-EX /  T)
            break
      
    end
    
    %更新解
    X = X1;
    
    %将X存储进历史记录
    n = n + 1;              %迭代记数增加
    S(n, :) = X;              %存储当前路径
    History_FX(n, :) = func(X);    %存储当前路径的长度
    %降温
    T = T * a;
end
fprintf('模拟退火算法：\n')
fprintf('****************迭代结果****************\n')
fprintf('最小值点为： %f\n', X)
fprintf('最小函数值为： %f\n', func(X))
fprintf('****************************************\n')
fprintf('end\n')