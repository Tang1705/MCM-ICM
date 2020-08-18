import excel "C:\Users\hc_lzp\Desktop\代码\model4\model4_data.xlsx", sheet("Sheet1") firstrow
save "C:\Users\hc_lzp\Desktop\代码\model4\model4_data.dta"
// ssc install outreg2
reg SUCCESS PerGDP INTEREST MONTHS HOUSE CAR Year AGE LNAMOUNT INCOME CREDIT WORKTIME MARRY EDUCATION A1 A2 A4-A31,r
