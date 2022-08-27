CREATE TABLE IF NOT EXISTS delisted_company (
symbol varchar(255) PRIMARY KEY ,
companyName varchar(255),
exchange varchar(255),
ipoDate date,
delistedDate date

)
;

CREATE TABLE IF NOT EXISTS history_dividends (
date date,
label varchar(255),
adjDividend FLOAT8,
dividend FLOAT8,
recordDate date,
paymentDate date,
declarationDate date,
symbol varchar(255)
)