import pandas as pd


def sort_values(dataframe, column_header):  # sort data frame by a column
    dataframe.sort_values(by=column_header, ascending=True)
    return dataframe


def remove_null_columns(dataframe):
    dataframe = dataframe.loc[:, ~dataframe.columns.str.match("Unnamed")]
    return dataframe


def detect_null_data(dataframe):
    pass


def main():
    df = pd.read_csv(r'port_scan_logs/sorted.csv')
    df = remove_null_columns(df)
    df.to_csv('port_scan_logs/cleaned.csv')

    # df.sort_values("timestamp")
    # pd.to_datetime('@timestamp', format="%b %d %Y %H:%M:%S.%f").sort_values()
    # convert_timestamp(df)
    # print(df['@timestamp'])


if __name__ == "__main__":
    main()