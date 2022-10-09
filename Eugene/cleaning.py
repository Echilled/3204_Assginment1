import pandas as pd
import re
import ipaddress
import numpy as np

PORT_REGEX = \
    '^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$'

INTEGER_REGEX = r'^(?:0|(?:[1-9](?:\d{0,2}(?:,\d{3})+|\d*)))$'
MAC_ADDRESS_REGEX = ("^([0-9A-Fa-f]{2}[:-])" +
                     "{5}([0-9A-Fa-f]{2})|" + "([0-9a-fA-F]{4}\\." + "[0-9a-fA-F]{4}\\." + "[0-9a-fA-F]{4})$")


def sort_values(dataframe, column_header):  # sort data frame by a column
    dataframe.sort_values(by=column_header, ascending=True)
    return dataframe


def remove_null_columns(dataframe):
    dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]
    return dataframe


def detect_null_data(dataframe):
    print(dataframe.isnull())


def remove_df_entry(dataframe, column, list):
    for bad_value in list:
        dataframe.drop(dataframe[dataframe[column] == bad_value].index, inplace=True)
    return dataframe


def check_port_numbers(dataframe):  # detect data like ip addresses in ports whatever
    port_columns = ['destination.port', 'source.port']
    validate_values(dataframe, port_columns, PORT_REGEX)
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


def check_mac_adresses(dataframe):
    macaddr_columns = ['destination.mac', 'source.mac', 'host.mac']
    validate_values(dataframe, macaddr_columns, MAC_ADDRESS_REGEX)
    return dataframe


def clean_bytes_values(dataframe):
    bytes_columns = ['destination.bytes', 'network.bytes', 'source.bytes', 'destination.packets', 'network.packets',
                     'source.packets']
    for column in bytes_columns:
        dataframe[column] = dataframe[column].replace('-', '0')
    validate_values(dataframe, bytes_columns, INTEGER_REGEX)
    return dataframe


def validate_values(dataframe, column_list, regex):
    for column in column_list:
        correct_list = list(filter(re.compile(regex).match, dataframe[column].values.tolist()))
        wrong_list = (list(set(dataframe[column].values.tolist()) - set(correct_list)))
        remove_df_entry(dataframe, column, wrong_list)


def replace_empty_bytes(dataframe, column):
    dataframe[column] = dataframe[column].replace('-', '0')

def universal_timestamp_converter():
    pass


def drop_irrelevant_columns():
    pass


def output_to_csv(dataframe):
    dataframe.to_csv('port_scan_logs/cleaned.csv')


def main():
    df = pd.read_csv(r'port_scan_logs/sorted.csv')
    df = df.replace(',', '', regex=True)
    check_port_numbers(df)
    check_ip_addresses(df)
    check_mac_adresses(df)
    clean_bytes_values(df)
    df = remove_null_columns(df)
    output_to_csv(df)


if __name__ == "__main__":
    main()