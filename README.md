# Connecting to Greptime Cloud Using PyMySQL

## TL;DR

This example demonstrates how to connect to GreptimeCloud using PyMySQL.

## Usage

To begin, create a service on [GreptimeCloud][0]. The service is free for tech preview.

Rename the file `example.env` to `.env` and fill in the necessary values. You can obtain the connection information from the cloud dashboard.

> By default, the port for connecting via MySQL protocol is 4002.

Install the required dependencies by running `pip install -r requirements.lock`, then execute `python main.py`.

> Alternatively, if you are using [Rye][1], run `rye sync` followed by `rye run up`.

## Where's the Data

You can query your data using the SQL Explorer or create dashboards using the Prometheus workbench in your GreptimeCloud service.

If you wish to remove all test data after completing your testing, simply execute `DROP TABLE` in the SQL Explorer.

## License

- License: WTFPL
- Author: GUAN Xiaoyu

[0]: https://www.greptime.com/product/cloud
[1]: https://rye-up.com
