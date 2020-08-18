clc;%清除命令窗口的代码
clear;%清除变量
close all;%关闭所有figure窗口
%% 参数初始化
tic%计时toc 终止计时
T0 = 1000;  %初始温度
Tend = 1e-3;  %终止温度
q = 0.9;  %降温速率
L = 200;  % 各温度下的迭代次数（链长）
X=[16.4700  96.1000
   16.4700  94.4400
   20.0900  92.5400
   22.3900  93.3700
   25.2300  97.2400
   22.0000  96.0500
   20.4700  97.0200
   17.2000  96.2900
   16.3000  97.3800
   21.5200  92.5900
   19.4100  97.1300
   20.0900  92.5500];%城市坐标位置
%% 计算城市距离和数量
D=Distance(X);%计算距离矩阵
N=size(D,1);%城市个数

%% 初始解
S1= randperm(N);  %随机产生一个初始路线

%% 画出随机解的路径
DrawPath(S1,X)
pause(0.0001)

%% 输出随机解的路径和总距离
disp('初始种群中的一个随机解:')%disp函数会直接将内容输出在Matlab命令窗口中
OutputPath(S1);
Rlength=PathLength(D,S1);%PathLength计算路径长度
disp(['总距离:',num2str(Rlength)]);

%% 计算迭代的次数Time
Time=ceil(double(solve(['1000*(0.9)^x= ',num2str(Tend)])));
count=0;    %迭代计数
Obj=zeros(Time,1);    %目标值矩阵初始化，减少运行时间
track=zeros(Time,N);    %每代的最优路线矩阵初始化

%% 迭代
while T0>Tend %如果温度大于终止温度
    
    count = count+1; %迭代次数增加
    temp = zeros(L,N+1);%记录每一次抽样的路径和路程
    for k=1:L
        %%产生新解
        S2=NewAnswer2(S1);
        %%Metropplis法则判断是否接受新解
        [S1,R]=Metropolis(S1,S2,D,T0);    %Metropolis抽样算法
        temp(k,:) = [S1 R];    %记录下一路线及其路程
    end
    
   %% 记录每次迭代过程的最优路线
    [d0,index]=min(temp(:,end));    %找出当前温度下最优路线，index是最小值对应的位置
    if count==1||d0<Obj(count-1)
        Obj(count)=d0;    %如果当前温度下最优路径小于上一路程，则记录当前路程
    else
        Obj(count)=Obj(count-1);    %如果当前温度下最优路程大于上一路程，则记录上一路程
    end
    track(count,:)=temp(index,1:end-1);    %记录当前温度下最优路线
    T0=q*T0;    %降温
    fprintf(1,'%d\n',count)    %输出当前迭代次数
end

%% 优化过程迭代图
figure
plot(1:count,Obj)
xlabel('迭代次数')
ylabel('距离')
title('优化过程')

%% 最优解的路径图
DrawPath(track(end,:),X)

%% 输出最优解的路线和总距离
disp('最优解')
S=track(end,:);
p = OutputPath(S);%输出最优路线
disp(['总距离:',num2str(PathLength(D,S))])%输出最优路线长度
toc