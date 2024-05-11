set dotenv-load
## start date
start-date := "${START_YEAR}-${START_MONTH}"
## end date
end-date := "${END_YEAR}-${END_MONTH}"

setup-currency-data:
    @echo "will setup currency db"
    rye run python bin/setup-currency-db.py --start-date={{start-date}} --end-date={{end-date}}
setup-data:
    @echo "will setup oism input data"
    bin/setup-sqlite-db.sh