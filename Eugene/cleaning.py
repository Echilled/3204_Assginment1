import pandas as pd
import re
import numpy as np

PORT_REGEX = \
    '^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$'


def sort_values(dataframe, column_header):  # sort data frame by a column
    dataframe.sort_values(by=column_header, ascending=True)
    return dataframe


def remove_null_columns(dataframe):
    dataframe = dataframe.loc[:, ~dataframe.columns.str.match("Unnamed")]
    return dataframe


def detect_null_data(dataframe):
    print(dataframe.isnull())


def remove_df_entry(dataframe, column, list):
    pass


def check_port_numbers(dataframe):  # detect data like ip addresses in ports whatever
    port_columns = ['destination.port', 'source.port']
    for column in port_columns:
        oldlist = dataframe[column].values.tolist()
        correct_list = list(filter(re.compile(PORT_REGEX).match, oldlist))
        wrong_list = (list(set(oldlist) - set(correct_list)))
        remove_df_entry(dataframe, column, wrong_list)
        # print(re.findall(PORT_REGEX, dataframe[column].values))

        # result = re.match(PORT_REGEX, '192.168.91.1')
    # if result:
    #     print("Correct port number.")
    # else:
    #     print("Incorrect port number.")


def output_to_csv(dataframe):
    dataframe.to_csv('port_scan_logs/cleaned.csv')


def main():
    df = pd.read_csv(r'port_scan_logs/sorted.csv')
    # df = remove_null_columns(df)
    check_port_numbers(df)
    # detect_null_data(df)


if __name__ == "__main__":
    main()