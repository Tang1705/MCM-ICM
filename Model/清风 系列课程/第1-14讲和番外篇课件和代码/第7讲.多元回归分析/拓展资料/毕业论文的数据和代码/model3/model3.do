clear
use "C:\Users\hc_lzp\Desktop\代码\model3\model3.dta"
tab ADDRESS,gen(A)  
reg DEFAULT INTEREST MONTHS HOUSE CAR Year AGE LNAMOUNT INCOME CREDIT WORKTIME MARRY EDUCATION A1 A2 A4-A31 if SUCCESS==1,r
est store e1
outreg2 [e1] using model3.doc,replace
test A1 A2 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 A21 A22 A23 A24 A25 A26 A27 A28 A29 A30 A31
clear 
use "C:\Users\hc_lzp\Desktop\代码\model3\model3_result1.dta"
pwcorr 因变量为违约率的回归系数 因变量为成功率的回归系数 , sig
clear 
use "C:\Users\hc_lzp\Desktop\代码\model3\model3_result2.dta"
pwcorr 因变量为违约率的回归系数 因变量为成功率的回归系数 , sig

