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
    print(df)


def main():
    format_data(PATH)


if __name__ == "__main__":
    main()
