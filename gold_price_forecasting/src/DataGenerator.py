import os
import pandas as pd
import numpy as np


def symbol_to_path(symbol, base_dir="../data/exchange"):
    # Return CSV file path given ticker symbol.
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def symbol_to_path2(symbol, base_dir="../data/commodities"):
    # Return CSV file path given ticker symbol.
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    global df_temp

    df = pd.DataFrame(index=dates)
    if 'gold' not in symbols:
        symbols.insert(0, 'gold')

    # TODO:  Choose columns to read

    for symbol in symbols:
        if symbol == 'dollar'or symbol == 'yuan':
            df_temp = pd.read_csv(symbol_to_path(symbol), index_col="date", parse_dates=True,
                                  usecols=['date', 'close', 'open', 'high', 'low'], na_values=['nan'])
            df_temp = df_temp.rename(columns={'close': symbol + '_close', 'open': symbol + '_open',
                                              'high': symbol + '_high', 'low': symbol + '_low'})

        elif symbol == 'gold' or symbol == 'silver' or symbol == 'copper' or symbol == 'wgold' or symbol == 'natural_gas' or symbol == 'brent_oil':
            df_temp = pd.read_csv(symbol_to_path2(symbol), index_col="date", parse_dates=True,
                                  usecols=['date', 'close', 'open', 'high', 'low'], na_values=['nan'])
            df_temp = df_temp.rename(columns={'close': symbol + '_close', 'open': symbol + '_open',
                                              'high': symbol + '_high', 'low': symbol + '_low'})

        df = df.join(df_temp)
    return df


def make_data(start_date, end_date):
    # start_date = '2010-01-01'
    # end_date = '2017-03-31'
    dates = pd.date_range(start_date, end_date)

    # TODO:  Choose symbols to read

    # symbols = ['silver' ,'copper', 'wgold', 'brent_oil', 'WTI_oil', 'heating_oil', 'natural_gas']
    # symbols = ['dollar']
    symbols = ['dollar']
    df = get_data(symbols, dates)

    df = df.dropna()
    return df


def make_features(start_date, end_date, days):
    # start_date = '2010-01-01'
    # end_date = '2017-03-31'
    table = make_data(start_date, end_date)

    # TODO:  select columns to use

    gold_close = table['gold_close']
    gold_high = table['gold_high']
    gold_low = table['gold_low']

    training_sets = []
    target_sets = []
    gold_change = np.diff(gold_close)
    gold_close = gold_close[1:]

    # print len(gold_close), len(gold_change)
    # print gold_close[0], gold_change[0]

    # TODO:  make features

    input_days = days
    for time in range(len(gold_close)-input_days):
        changing = gold_change[time:time + input_days]
        close = gold_close[time:time + input_days]
        high = gold_high[time:time + input_days]
        low = gold_low[time:time + input_days]

        # daily_feature = np.concatenate((changing[::-1], close))
        daily_feature = np.concatenate((changing, close, high, low))
        #  daily_feature = np.concatenate((changing, close,))
        training_sets.append(daily_feature)

    training_x = training_sets[:-10]
    test_x = training_sets[-10:]
    past_price = gold_close[-11:-1]
    target_price = gold_close[-10:]

    # return gold_change
    return training_x, test_x, past_price, target_price

if __name__ == "__main__":
    table1, table2, table3, table4 = make_features('2016-04-25', '2017-04-25')
    print(table1)
    print(table2)
    print(table3)
    print(table4)