import os
import pandas as pd
import numpy as np


def symbol_to_path(symbol, base_dir="../data"):
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    df = pd.DataFrame(index=dates)
    # TODO:  Choose columns to read

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col="Date", parse_dates=True,
                              usecols=['Date', 'Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Close': symbol + '_close', })
        df = df.join(df_temp)
    return df


def make_data(start_date, end_date):
    dates = pd.date_range(start_date, end_date)

    # TODO:  Choose symbols to read
    symbols = ['Hyundai_Mobis', 'Hyundai_Motors', 'Korea_Electric_Power', 'Naver', 'POSCO', 'Samsung_C_T','Samsung_Electronics', 'Samsung_Life', 'Shinhan_Financial', 'SK_Hynix']
    # symbols = ['Samsung_Life']
    df = get_data(symbols, dates)

    df = df.dropna()
    return df


def make_features(feature_name, start_date, end_date, test=False):
    table = make_data(start_date, end_date)
    print (table.info())
    column = "_close"
    feature_temp = feature_name + column
    # TODO:  select columns to use

    s_close = table[feature_temp]
    s_open = table[feature_temp]
    s_high = table[feature_temp]
    s_low = table[feature_temp]
    price_diff = np.diff(s_close)


    # TODO:  data processing to make features

    hist = 7
    features = list()
    print (len(s_close), len(features))
    for a in range(len(s_close)-hist+1):
        # TODO:  set features to use
        close = s_close[a:a+hist]
        change = price_diff[a:a + hist]
        opena = s_open[a:a+hist]
        high = s_high[a:a+hist]
        low = s_low[a:a+hist]
        daily_diff = high - low

        features.append(close)

    s_close = s_close[hist-1:]
    print (len(s_close), len(features))

    if test:
        pretest_s_close = s_close[:-10]
        pretest_features= features[:-10]
        test_s_close = s_close[-10:]
        test_features = features[-10:]
        return test_s_close, test_features, pretest_s_close, pretest_features

    return s_close, features

if __name__ == "__main__":
    table1, table2 = make_features('2000-01-01', '2017-04-30')
    print (table1)
    print (table2)

