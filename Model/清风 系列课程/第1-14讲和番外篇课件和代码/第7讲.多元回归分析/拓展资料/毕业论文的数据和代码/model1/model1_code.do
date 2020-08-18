// import excel "C:\Users\hc_lzp\Desktop\代码\model1\model1_data.xlsx", sheet("Sheet1") firstrow
// save "C:\Users\hc_lzp\Desktop\代码\model1\model1_data.dta"
// ssc install outreg2
use "C:\Users\hc_lzp\Desktop\代码\model1\model1_data.dta"
tab ADDRESS,gen(A)  
reg SUCCESS INTEREST MONTHS HOUSE CAR Year AGE LNAMOUNT INCOME CREDIT WORKTIME MARRY EDUCATION A1 A2 A4-A31,r
est store m1
outreg2 [m1] using model1.doc,replace
test A1 A2 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 A21 A22 A23 A24 A25 A26 A27 A28 A29 A30 A31
pwcorr CAR HOUSE, sig
pwcorr CAR HOUSE, star(.05)
reg SUCCESS INTEREST MONTHS HOUSE Year AGE LNAMOUNT INCOME CREDIT WORKTIME MARRY EDUCATION A1 A2 A4-A31,r
