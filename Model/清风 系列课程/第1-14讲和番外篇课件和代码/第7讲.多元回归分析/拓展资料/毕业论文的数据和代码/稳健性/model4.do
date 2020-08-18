// import excel "C:\Users\hc_lzp\Desktop\代码\稳健性\model4_data.xlsx", sheet("Sheet1") firstrow
// save "C:\Users\hc_lzp\Desktop\代码\稳健性\model4_data.dta"
clear
use "C:\Users\hc_lzp\Desktop\代码\稳健性\model4_data.dta"
tab RAGION,gen(R)  
reg SUCCESS INTEREST MONTHS HOUSE CAR Year AGE LNAMOUNT INCOME CREDIT WORKTIME MARRY EDUCATION R1-R6,r
est store m1
outreg2 [m1] using model4.doc,replace
test R1 R2 R3 R4 R5 R6
