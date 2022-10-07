import pandas as pd
import datetime


def convert_timestamp(dataframe):
    for timestamp in dataframe['@timestamp']:
        old_timestamp = timestamp
        timestamp = timestamp.replace(',', '').split(' @')
        timestamp[0] = str(datetime.datetime.strptime(timestamp[0], '%b %d %Y')).split(' ')[0]
        timestamp = ' '.join(timestamp)


def remove_null_columns(dataframe):
    dataframe = dataframe.loc[:, ~dataframe.columns.str.match("Unnamed")]
    return dataframe


def main():
    df = pd.read_csv(r'port_scan_logs/sorted.csv')
    df = remove_null_columns(df)
    df.to_csv('port_scan_logs/cleaned.csv')
    # print(df)
    # columns = df.columns.values
    # print(columns)
    # columns['destination.port'] = sorted(columns['destination.port'])
    # new_df = df.loc[:, df.columns != "@timestamp"]
    # new_df = new_df.sort_values(by="destination.port", ascending=True)
    # print(new_df)

    # print(type(df['@timestamp'][0]))
    # df.sort_values("timestamp")
    # pd.to_datetime('@timestamp', format="%b %d %Y %H:%M:%S.%f").sort_values()
    # convert_timestamp(df)
    # print(df['@timestamp'])


if __name__ == "__main__":
    main()