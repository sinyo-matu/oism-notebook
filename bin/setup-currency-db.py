import os
import sqlite3
from time import sleep
from pydantic import BaseModel
import argparse
import httpx
from dotenv import load_dotenv

load_dotenv()

currency_api_api_key = os.environ["CURRENCY_API_API_KEY"]
dbname = "db_data/currency-data.db"
conn = sqlite3.connect(dbname)
table_name = "currency_history"


# response:
#    {
#   "meta": {
#     "last_updated_at": "2024-05-01T23:59:59Z"
#   },
#   "data": {
#     "CNY": {
#       "code": "CNY",
#       "value": 7.208121339
#     },
#     "JPY": {
#       "code": "JPY",
#       "value": 155.6946121063
#     }
#   }
# }
class Meta(BaseModel):
    last_updated_at: str


class CurrencyData(BaseModel):
    code: str
    value: float


class Data(BaseModel):
    CNY: CurrencyData
    JPY: CurrencyData


class CurrencyApiResponseBody(BaseModel):
    meta: Meta
    data: Data


def fetch_currency_data(year, month, day=1):
    url = f"https://api.currencyapi.com/v3/historical?apikey={currency_api_api_key}&currencies=CNY%2CJPY&date={year}-{month}-{day}"
    response = httpx.get(url)
    return CurrencyApiResponseBody.model_validate(response.json())


def check_data_exists(year, month):
    date = f"{year}-{month}-01"
    cursor = conn.execute(
        f"select count(*) from {table_name} where date = ? and currency = 'CNY'",
        (date,),
    )
    cny_existed = cursor.fetchone()[0] > 0
    cursor = conn.execute(
        f"select count(*) from {table_name} where date = ? and currency = 'JPY'",
        (date,),
    )
    jpy_existed = cursor.fetchone()[0] > 0
    return cny_existed and jpy_existed


def insert_data(year, month):
    date = f"{year}-{month}-01"
    if check_data_exists(year, month):
        return
    print(f"fetching data for {date}")
    data = fetch_currency_data(year, month)
    print("suceessfully fetched data")
    print("inserting data to db")
    conn.execute(
        f"insert into {table_name} (date, currency, rate) values (?, ?, ?)",
        (date, "CNY", data.data.CNY.value),
    )
    conn.execute(
        f"insert into {table_name} (date, currency, rate) values (?, ?, ?)",
        (date, "JPY", data.data.JPY.value),
    )
    conn.commit()
    print("successfully inserted data")


# TEST.dbを作成する
# すでに存在していれば、それにアスセスする。
def maim():
    # parse args input like start_date=2023-05 end_date=2024-05
    conn.execute(
        f"create table if not exists {table_name} (date text, currency text, rate real)"
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", type=str)
    parser.add_argument("--end-date", type=str)
    args = parser.parse_args()
    start_date = args.start_date
    end_date = args.end_date
    start_year, start_month = start_date.split("-")
    end_year, end_month = end_date.split("-")
    for year in range(int(start_year), int(end_year) + 1):
        for month in range(1, 13):
            if year == int(start_year) and month < int(start_month):
                continue
            if year == int(end_year) and month > int(end_month):
                continue
            if check_data_exists(year, month):
                print(f"currency data for {year}-{month} already exists")
                continue
            insert_data(year, month)
            print("sleeping for 6 second")
            sleep(6)


if __name__ == "__main__":
    try:
        maim()
    finally:
        conn.close()
