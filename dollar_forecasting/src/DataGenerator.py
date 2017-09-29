import os
import pandas as pd
import numpy as np


def symbol_to_path(symbol, base_dir="../data/exchange"):

    # Return CSV file path given ticker symbol.pip
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    df = pd.DataFrame(index=dates)
    if 'dollar' not in symbols:
        symbols.insert(0, 'dollar')
    # TODO  Choose columns to read
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col="date", parse_dates=True,
                              usecols=['date', 'close', 'open', 'high', 'low'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'close': symbol + '_close', 'open': symbol + '_open',
                                          'high': symbol + '_high', 'low': symbol + '_low'})
        df = df.join(df_temp)
    return df


def make_data(start_date, end_date):
    # start_date = '2010-01-01'
    # end_date = '2017-03-31'
    dates = pd.date_range(start_date, end_date)
    # TODO  Choose symbols to read
    #symbols = ['pound', 'euro', 'yuan', 'yen', 'aus', 'hon', 'dollar_index']
    symbols = ['gold', 'pound','yen','yuan','dollar_index']

    df = get_data(symbols, dates)
    df = df.dropna()
    return df


def make_features(start_date, end_date, input_days_control):
    # start_date = '2010-01-01'
    # end_date = '2017-03-31'
    table = make_data(start_date, end_date)
    # TODO  select columns to use
    dollar_close = table['dollar_close']
    # dollar_open = table['dollar_open']
    dollar_high = table['dollar_high']
    dollar_low = table['dollar_low']
    training_sets = []
    target_sets = []
    # TODO  make features
    input_days = input_days_control
    days_before = 10
    print len(dollar_close)
    for time in xrange(len(dollar_close)-input_days):
        close = dollar_close[time:time + input_days]
        high = dollar_high[time:time + input_days]
        low = dollar_low[time:time + input_days]
        daily_feature = np.concatenate((close, high, low))
        # daily_feature = close
        daily_target = dollar_close[time + input_days:time + input_days + days_before]
        training_sets.append(daily_feature)
        target_sets.append(daily_target)
    training_x = training_sets[:-days_before]
    training_y = target_sets[:-days_before]
    test_x = training_sets[-days_before]
    test_y = target_sets[-days_before]
    return training_x, training_y, test_x, test_y

if __name__ == "__main__":
    table = make_data('2010-01-01', '2017-04-07')
    print table.shape
    print table.head(60)
    print table.tail(60)