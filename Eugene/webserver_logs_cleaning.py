import pandas as pd
from datetime import datetime
import pytz
import re

PATH = 'Webserver_logs/access.log'


def parse_str(x):
    return x[1:-1]


def parse_datetime(x):

    # timezone will be obtained using the `pytz` library.

    dt = datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S')
    dt_tz = int(x[-6:-3])*60+int(x[-3:-1])
    return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))


def format_data(dataframe):

    # Get resource URI:
    request = dataframe.pop('request').str.split()
    dataframe['resource'] = request.str[1]

    # Filter out non GET requests:
    dataframe = dataframe[(request.str[0] == 'GET')]

    # Filter out undesired resources
    dataframe = dataframe[~dataframe['resource'].str.match(
        r'^/media|^/static|^/admin|^/robots.txt$|^/favicon.ico$')]

    # Filter web crawlers and spiders
    dataframe = dataframe[~dataframe['user_agent'].str.match(
        r'.*?bot|.*?spider|.*?crawler|.*?slurp', flags=re.I).fillna(False)]

    dataframe = dataframe[~dataframe['source_ip'].str.startswith('123.125.71.')]  # Baidu IPs.


def output_to_csv(dataframe):
    dataframe.to_csv(r'Webserver_logs/access_logs.csv')


def main():
    # convert_to_csv(PATH)
    df = pd.read_csv(
        PATH,
        sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
        engine='python',
        na_values='-',
        header=None,
        usecols=[0, 3, 4, 5, 6, 7, 8],
        names=['source_ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
        converters={'time': parse_datetime,
                    'request': parse_str,
                    'status': int,
                    'size': int,
                    'referer': parse_str,
                    'user_agent': parse_str})

    format_data(df)
    print(df.head())
    output_to_csv(df)


if __name__ == "__main__":
    main()
