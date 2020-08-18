clear
use "C:\Users\hc_lzp\Desktop\代码\稳健性\model5_data.dta"
tab ADDRESS,gen(A)  
logit SUCCESS INTEREST MONTHS HOUSE CAR Year AGE LNAMOUNT INCOME CREDIT WORKTIME MARRY EDUCATION A1 A2 A4-A31,or
est store m1
outreg2 [m1] using model5.doc,replace
predict yhat
estat clas  //计算预测准确的百分比
margins,dydx(*)  //所有解释变量的平均边际效应
test A1 A2 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 A21 A22 A23 A24 A25 A26 A27 A28 A29 A30 A31
