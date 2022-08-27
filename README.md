# data-engineer-assignment

This repository provides for to Data engineer project
## About the Project

The Project builds by Docker image
This allows you to run a local environment 
to develop and test pipeline, custom plugins, and dependencies 
before deploying to production.

### Programing
Python, Dagster (Framework) and Docker (Infra)

### Objective
- Get the data from a free financial data API called FMP (https://site.financialmodelingprep.com/developer/docs/)

Historical Dividends (https://site.financialmodelingprep.com/developer/docs/#Historical-Dividends)

- Delisted companies ((https://site.financialmodelingprep.com/developer/docs/delisted-companies-api/))

- Store the retrieved data in any database you are comfortable working with

### Step Detail
- Extract Requests Get API by Python and validation API Json
- Transform Data 
- Loading Data to Postgresql
- run by ``` docker-compose -f docker-compose.yml up --build --no-recreate -d ```
- stop by ``` docker-compose -f docker-compose.yml down -v ```
