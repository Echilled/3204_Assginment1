import pandas as pd


PATH = 'Webserver_logs/fw_logs.txt'


def get_headers(file):
    f = open(file, "r")
    for line in f:
        if line.startswith("#Fields:"):
            line = line.strip()
            headers = line.split(' ')
    headers.pop(0)
    return headers


def get_columns_with_all_single_values(dataframe):  # remove columns with the same values as it does not help analysis
    same_value_columns = []
    for column in dataframe.columns:
        if (dataframe[column] == dataframe[column][0]).all():
            same_value_columns.append(column)
    return same_value_columns


def format_data(file):
    headers = get_headers(file)
    df = pd.read_csv(
        PATH,
        sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
        engine='python',
        na_values='-',
        header=None,
        usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        names=headers,
    )
    df = df.iloc[4:]
    return df


def main():
    df = format_data(PATH)
    df.reset_index(drop=True, inplace=True)
    print(df)
    # get_columns_with_all_single_values(df)


if __name__ == "__main__":
    main()
