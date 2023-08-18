import os
from datetime import datetime

import psutil
import pymysql
from dotenv import load_dotenv


def get_greptime_db_connection() -> pymysql.Connection:
    load_dotenv()
    return pymysql.connect(
        host=os.environ.get("GREPTIME_HOST"),
        port=int(os.environ.get("GREPTIME_PORT")),
        user=os.environ.get("GREPTIME_USERNAME"),
        password=os.environ.get("GREPTIME_PASSWORD"),
        db=os.environ.get("GREPTIME_DB"),
        charset="utf8",
    )


def get_cpu_percent(interval: int = 2) -> list:
    cpu_percent = psutil.cpu_percent(interval=interval, percpu=True)
    return cpu_percent


def create_cpu_usage_table(ttl_days: int = 7) -> None:
    with get_greptime_db_connection() as conn:
        with conn.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS `cpu_usage` (" \
                "`cpu` STRING PRIMARY KEY, " \
                "`cpu_usage` DOUBLE, " \
                "`ts` TIMESTAMP DEFAULT CURRENT_TIMESTAMP TIME INDEX, " \
                ") with(ttl='%sd');"
            cursor.execute(sql, (ttl_days,))


def insert_cpu_usage(numbers: list) -> None:
    with get_greptime_db_connection() as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO `cpu_usage` (`cpu`, `cpu_usage`) VALUES "
            values = ", ".join(
                [f"('cpu_{idx}', {float(number)})"
                 for idx, number in enumerate(numbers)])
            sql += values
            cursor.execute(sql)


def main():
    create_cpu_usage_table()
    while True:
        numbers = get_cpu_percent()
        try:
            insert_cpu_usage(numbers)
            print(f"Inserted @ {datetime.now()}")
        except pymysql.err.OperationalError:
            print("MySQL connection error, ignored.")
            continue
        except KeyboardInterrupt:
            print("Bye.")
            break


if __name__ == "__main__":
    main()
