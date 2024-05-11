# oism-note

## 1. Introduction

this project needs:

- mongoexport
- sqlite3
- python3.10
- just <- the command runner

set the Environment Variables in the .env file
like this:

```sh
## the api key for the currencyapi.com
CURRENCY_API_API_KEY=xxxxx
## the mongodb connection uri
PROD_MONGODB_CONNECTION_URI="mongodb+srv://eliamo:64659027Qy@cluster0.k6d04.mongodb.net/?authSource=admin&replicaSet=atlas-e5y1lc-shard-0&readPreference=primary&ssl=true"
## aggregate  start date to the end date
START_YEAR=2023
END_YEAR=2024
START_MONTH=5
END_MONTH=4
```

then setup data and run the project

```sh
just setup-data
just setup-currency-data
```
