import pandas as pd
import re
import ipaddress
import datetime

PORT_REGEX = \
    '^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$'

INTEGER_REGEX = r'^(?:0|(?:[1-9](?:\d{0,2}(?:,\d{3})+|\d*)))$'
MAC_ADDRESS_REGEX = ("^([0-9A-Fa-f]{2}[:-])" +
                     "{5}([0-9A-Fa-f]{2})|" + "([0-9a-fA-F]{4}\\." + "[0-9a-fA-F]{4}\\." + "[0-9a-fA-F]{4})$")

TIME_REGEX = ""


def sort_values(dataframe, column_header):  # sort data frame by a column
    dataframe.sort_values(by=column_header, ascending=True)
    return dataframe


def remove_null_columns(dataframe):
    dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]
    return dataframe


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


def universal_timestamp_converter(dataframe):
    new_timestamp_list = []
    for timestamp in dataframe['@timestamp'].values:
        timestamp = timestamp.split(' @')
        timestamp[0] = str(datetime.datetime.strptime(timestamp[0], '%b %d %Y')).split(' ')[0]
        timestamp = ' '.join(timestamp)
        # timestamp = '\'' + timestamp  # for excel
        new_timestamp_list.append(timestamp)
    dataframe['@timestamp'] = new_timestamp_list
    return dataframe


def sort_time_ascending(dataframe): # dont look at timestamp but event.start instead
    pass


def get_columns_with_all_same_values(dataframe):  # remove columns with the same values as it does not help analysis
    pass


def filtering_redundant_columns():
    pass


def output_to_csv(dataframe):
    dataframe.to_csv('port_scan_logs/cleaned.csv', date_format='%Y-%m-%d %H:%M:%S.%f')


def main():
    df = pd.read_csv(r'port_scan_logs/real_port_scan_requests_2.csv', on_bad_lines='skip')
    df = df.replace(',', '', regex=True)
    print(df)
    # check_port_numbers(df)
    # check_ip_addresses(df)
    # check_mac_adresses(df)
    # clean_bytes_values(df)
    # df = remove_null_columns(df)
    print(df.isnull().any())

    # print(df.columns[df.isna().any()].tolist())

    # df = universal_timestamp_converter(df)
    # output_to_csv(df)


if __name__ == "__main__":
    main()