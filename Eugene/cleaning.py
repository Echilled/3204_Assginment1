import pandas as pd
import re
import ipaddress
import numpy as np

PORT_REGEX = \
    '^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$'

IP_REGEX = ""


def sort_values(dataframe, column_header):  # sort data frame by a column
    dataframe.sort_values(by=column_header, ascending=True)
    return dataframe


def remove_null_columns(dataframe):
    dataframe = dataframe.loc[:, ~dataframe.columns.str.match("Unnamed")]
    return dataframe


def detect_null_data(dataframe):
    print(dataframe.isnull())


def remove_df_entry(dataframe, column, list):
    for bad_value in list:
        dataframe.drop(dataframe[dataframe[column] == bad_value].index, inplace=True)
    return dataframe


def check_port_numbers(dataframe):  # detect data like ip addresses in ports whatever
    port_columns = ['destination.port', 'source.port']
    for column in port_columns:
        oldlist = dataframe[column].values.tolist()
        correct_list = list(filter(re.compile(PORT_REGEX).match, oldlist))
        wrong_list = (list(set(oldlist) - set(correct_list)))
        dataframe = remove_df_entry(dataframe, column, wrong_list)
        # print(dataframe)
    return dataframe


def check_ip_addresses(dataframe):
    ipaddr_columns = ['destination.ip', 'source.ip']
    wrong_list = []
    for column in ipaddr_columns:
        for value in dataframe[column].values:
            try:
                ipaddress.ip_address(value)
            except ValueError:
                wrong_list.append(value)
        dataframe = remove_df_entry(dataframe, column, wrong_list)
    return dataframe


def replace_null_bytes(dataframe):
    bytes_column = ['destination.bytes', 'network.bytes', 'source.bytes']
    for column in bytes_column:
         print(dataframe[column].values)  # replacing the bytes '-' with 0


def output_to_csv(dataframe):
    dataframe.to_csv('port_scan_logs/cleaned.csv')


def main():
    df = pd.read_csv(r'port_scan_logs/sorted.csv')
    df = df.replace(',', '', regex=True)
    # print(df)
    # df = remove_null_columns(df)
    # check_port_numbers(df)
    # check_ip_addresses(df)
    # output_to_csv(df)
    replace_null_bytes(df)
    # detect_null_data(df)


if __name__ == "__main__":
    main()