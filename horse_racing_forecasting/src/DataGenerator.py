
import os
import pandas as pd
import codecs
import sys
import re



def is_number(num):
    try:
        judge = str(float(num))
        return False if(judge == 'nan' or judge == 'inf' or judge == '-inf') else True
    except(ValueError):  # num을 float으로 변환 할 수 없는 경우
        return False


def load_data():
    # ========================  input all data ===========================
    # TODO: load more data and JOIN
    for root, dirs, files in os.walk('../data/score/'):
        files.sort()

    data_set = []

    for file in files:
        file_name = file
        training_file = open("../data/score/" + file_name, 'r')
        train_datas = training_file.readlines()


        for dx,line in enumerate(train_datas):
            data_set.append(re.split(r'\t+', line.rstrip('\t')))
            # data_set.append(line.decode('cp949')) # for KOREAN

    return data_set

def find_file_with_correct_date(year, month, date, num_days_before):
    one_month_before_ends_with_31 = ['02','04','06','08','09','11','01']
    one_month_before_ends_with_30 = ['05','07','10','12']
    one_month_before_ends_with_28 = ['03']

    new_date = int(date) - num_days_before
    new_month =int(month)
    new_year = int(year)

    if new_date <= 0:
        if month in one_month_before_ends_with_31:
             date_controller = 31
        elif month in one_month_before_ends_with_30:
            date_controller = 30
        else:
            date_controller = 28
        new_date = new_date + date_controller
        new_month = new_month -1
        if new_month <=0:
            new_month = 12
            new_year = new_year -1

    final_new_year = str(new_year)
    final_new_month = "0" + str(new_month)
    final_new_date = "0" + str(new_date)

    if len(final_new_month) ==3:
        final_new_month = final_new_month[1:]
    if len(final_new_date) ==3:
        final_new_date = final_new_date[1:]
    return final_new_year, final_new_month, final_new_date

def join_more_features(horse_name, race_day):
    data_container = []
    #bring features from a horse file

    winning_history_1st =0
    winning_history_2nd =0
    recent_winning_history_1st=0
    recent_winning_history_2nd=0
    total_games_played =0
    total_money_won= 0
    #총출전게임수 대비 1위 2위 비율 OR 승률
    odds =0.00001
    rating =0

    year = race_day.split('-')[0]
    month = race_day.split('-')[1]
    date =race_day.split('-')[2]
    horse_info_set =[]
    new_year, new_month, new_date = find_file_with_correct_date(year, month, date, 2)
    file_name = "horse_"+ new_year + new_month + new_date + ".txt"

    if(os.path.exists("../data/horse/" + file_name)):
        horse_info_datas = open("../data/horse/" + file_name, 'r')
    else:
        new_year, new_month, new_date = find_file_with_correct_date(year, month, date, 3)
        file_name = "horse_" + new_year + new_month + new_date + ".txt"
        horse_info_datas = open("../data/horse/" + file_name, 'r')

    horse_info_data = horse_info_datas.readlines()
    for dx,item in enumerate(horse_info_data):
        horse_info_set.append(re.split(r'\t+', item.rstrip('\t')))
        #print("joining data...." + str(dx) + " of " + str(len(horse_info_data)))
    for line in horse_info_set:

        #print (str(line[0]))
        if horse_name == line[0]:

            total_games_played = line[11]
            winning_history_1st = line[12]
            winning_history_2nd = line[13]
            #recent_winning_history_1st = line[15]
            #recent_winning_history_2nd = line[16]
            try:
                rating = line[18]
            except IndexError:
                rating = 0
            if int(total_games_played) > 0:
                odds = (int(winning_history_1st) + int(winning_history_2nd)) / int(total_games_played)
            try:
                total_money_won = line[17]
            except IndexError:
                total_money_won = 0

            #data_container.append(line.split())
    return winning_history_1st, odds, rating


def join_more_features_jockey(jockey_name, race_day):
    data_container = []
    #bring features from a horse file
    winning_history_1st_jockey =0
    winning_history_2nd_jockey =0
    recent_winning_history_1st_jockey=0
    recent_winning_history_2nd_jockey=0
    total_games_played_jockey =0

    #총출전게임수 대비 1위 2위 비율 OR 승률
    odds_jockey =0.00001

    year = race_day.split('-')[0]
    month = race_day.split('-')[1]
    date =race_day.split('-')[2]
    jockey_info_set =[]
    new_year, new_month, new_date = find_file_with_correct_date(year, month, date, 2)
    file_name = "jockey_"+ new_year + new_month + new_date + ".txt"

    if(os.path.exists("../data/jockey/" + file_name)):
        jockey_info_datas = open("../data/jockey/" + file_name, 'r')
    else:
        new_year, new_month, new_date = find_file_with_correct_date(year, month, date, 3)
        file_name = "jockey_" + new_year + new_month + new_date + ".txt"
        jockey_info_datas = open("../data/jockey/" + file_name, 'r')

    jockey_info_data = jockey_info_datas.readlines()
    for dx,item in enumerate(jockey_info_data):
        jockey_info_set.append(re.split(r'\t+', item.rstrip('\t')))
        #print("joining data...." + str(dx) + " of " + str(len(horse_info_data)))
    for line in jockey_info_set:

        #print (str(line[0]))
        if jockey_name == line[0]:

            total_games_played_jockey = line[7]
            winning_history_1st_jockey = line[8]
            winning_history_2nd_jockey = line[9]
           # recent_winning_history_1st_jockey = line[11]
           # recent_winning_history_2nd_jockey = line[12]
            if int(total_games_played_jockey) > 0:
                odds_jockey = (int(winning_history_1st_jockey) + int(winning_history_2nd_jockey)) / int(total_games_played_jockey)

            #data_container.append(line.split())
    return winning_history_1st_jockey, odds_jockey

def join_more_features_trainer(trainer_name, race_day):
    data_container = []
    #bring features from a trainer file
    winning_history_1st_trainer =0
    winning_history_2nd_trainer =0
    recent_winning_history_1st_trainer=0
    recent_winning_history_2nd_trainer=0
    total_games_played_jockey =0

    #총출전게임수 대비 1위 2위 비율 OR 승률
    odds_trainer =0.00001

    year = race_day.split('-')[0]
    month = race_day.split('-')[1]
    date =race_day.split('-')[2]
    trainer_info_set =[]
    new_year, new_month, new_date = find_file_with_correct_date(year, month, date, 2)
    file_name = "trainer_"+ new_year + new_month + new_date + ".txt"

    if(os.path.exists("../data/trainer/" + file_name)):
        trainer_info_datas = open("../data/trainer/" + file_name, 'r')
    else:
        new_year, new_month, new_date = find_file_with_correct_date(year, month, date, 3)
        file_name = "trainer_" + new_year + new_month + new_date + ".txt"
        trainer_info_datas = open("../data/trainer/" + file_name, 'r')

    trainer_info_data = trainer_info_datas.readlines()
    for dx,item in enumerate(trainer_info_data):
        trainer_info_set.append(re.split(r'\t+', item.rstrip('\t')))
        #print("joining data...." + str(dx) + " of " + str(len(horse_info_data)))
    for line in trainer_info_set:

        #print (str(line[0]))
        if trainer_name == line[0]:

            total_games_played_trainer = line[5]
            winning_history_1st_trainer = line[6]
            winning_history_2nd_trainer = line[7]
            #recent_winning_history_1st_trainer= line[9]
           # recent_winning_history_2nd_trainer = line[10]
            if int(total_games_played_trainer) > 0:
                odds_trainer = (int(winning_history_1st_trainer) + int(winning_history_2nd_trainer)) / int(total_games_played_trainer)

            #data_container.append(line.split())
    return winning_history_1st_trainer,odds_trainer


def make_daily_data(data_set):
    total_set = []
    race_day_set = []
    rating =0
    # ======================== make data group in day ============================
    # TODO: make features and exception handling
    for dx,line in enumerate(data_set):
        temp = []
        race_day = line[0]
        race_num = int(line[1])
        race_distance = line[2]
        year = race_day.split('-')[0]
        month = race_day.split('-')[1]
        date = race_day.split('-')[2]
        race_day_ref = int(str(year + month + date));

        age =0
        bdweight =0
        rank =0
        horse_num =0
        winning_history_1st =0
        winning_history_1st_jockey = 0
        winning_history_1st_trainer = 0
        odds =0
        print("========step1========make daily data:" + str(dx) + " of " + str(len(data_set)))
        if race_day_ref < 20170429:


            if is_number(line[6]):
                rank = int(line[5])
                horse_num = int(line[6])
                age = int(line[10].replace("세",""))
                horse_name =(line[7])
                jockey_name=line[13]
                trainer_name =line[14]
                bdweight = float(line[11])
               # rating = int(line[12])

            else:
                rank = 30
                horse_num = int(line[5])
                age = int(line[9].replace("세",""))
                horse_name = (line[6])
                jockey_name = line[12]
                trainer_name = line[13]
                bdweight = float(line[10])
               # rating = int(line[11])


            winning_history_1st, odds, horse_rating =join_more_features(horse_name, race_day)
            winning_history_1st_trainer, odds_trainer = join_more_features_trainer(trainer_name, race_day)
            winning_history_1st_jockey, odds_jockey = join_more_features_jockey(jockey_name, race_day)

        elif race_day_ref == 20170429:

            if is_number(line[3]):

                rank = int(line[2])
                horse_num = int(line[3])
                horse_name = (line[4])
                jockey_name = (line[9])
                trainer_name = (line[10])
                winning_history_1st, odds, horse_rating = join_more_features(horse_name, race_day)
                winning_history_1st_trainer, odds_trainer = join_more_features_trainer(trainer_name, race_day)
                winning_history_1st_jockey, odds_jockey = join_more_features_jockey(jockey_name, race_day)


            # 기본: 날짜, 경기번호, 순위, 마번, 나이, 부담중량

        temp = [race_day, race_num, rank, horse_num, age, bdweight, race_distance, odds, odds_trainer, odds_jockey]

        total_set.append(temp)

    for line in total_set:
        race_day_set.append(line[0])

    race_day_set = list(set(race_day_set))
    race_day_set.sort()

    daily_set = []
    for day in race_day_set:
        daily_temp = []
        race_temp = []
        race = 1
        for line in total_set:
            if line[0] == day:
                daily_temp.append(line)

        daily_set.append([day, daily_temp])

    return daily_set


def make_data(daily_set, test_day):
    # ============================== make training and test data ============================
    training_X_1 = []
    training_X_2 = []
    training_X_3 = []
    training_Y = []

    test_X_1 = []
    test_X_2 = []
    test_X_3 = []
    test_Y = []
    test_data = []
    #TODO: here
    for a in range(len(daily_set)):
        print("========step2========make data for the model:" + str(a) + " of " + str(len(daily_set)))
        if daily_set[a][0] in test_day:
            for b in range(len(daily_set[a][1])):
                test_X_1.append(daily_set[a][1][b][4:10])
                test_X_2.append(daily_set[a][1][b][7:8])
                test_X_3.append(daily_set[a][1][b][-1:])

               # if daily_set[a][1][b][2] < 3:
               #     test_Y.append(1)
              #  else:
             #       test_Y.append(0)
                test_data.append(daily_set[a][1][b][:])
        else:
            for b in range(len(daily_set[a][1])):
                training_X_1.append(daily_set[a][1][b][4:10])
                training_X_2.append(daily_set[a][1][b][7:8])
                training_X_3.append(daily_set[a][1][b][-1:])
                if daily_set[a][1][b][2] < 3:
                    training_Y.append(1)
                else:
                    training_Y.append(0)
    return training_X_1, training_Y, test_X_1, test_data, training_X_2, training_X_3, test_X_2, test_X_3

def make_data_test(daily_set, test_day):
    # ============================== make training and test data ============================
    training_X = []
    training_Y = []
    test_X = []
    test_Y = []
    test_data = []

    for a in range(len(daily_set)):

        if daily_set[a][0] in test_day:
            print ("for testing data: [" + str(a) + "][0]" + str(daily_set[a][0]))
            for b in range(len(daily_set[a][1])):


                print( "for testing data[" + str(a)+ "][" + str(b) + "][4:] =" + str(daily_set[a][1][b][6:7]))
                print ("for **testing data[" + str(a) + "][" + str(b) + "][2] =" + str(daily_set[a][1][b][2]))
                test_X.append(daily_set[a][1][b][6:7])
                #if the ranking of the horse is less than 3
                if daily_set[a][1][b][2] < 3:
                    test_Y.append(1)

                else:
                    test_Y.append(0)

                test_data.append(daily_set[a][1][b][:4])
                print ("this is test_Y" + str(test_Y))
        else:
            print ("for training data: [" + str(a) + "][1]" + str(daily_set[a][1]))
            for b in range(len(daily_set[a][1])):
                print ("for training data[" + str(a) + "][" + str(b) + "][4:] =" + str(daily_set[a][1][b][6:7]))
                training_X.append(daily_set[a][1][b][6:7])
                if daily_set[a][1][b][2] < 3:
                    print ("good horse ranking *training")
                    training_Y.append(1)
                else:
                    print ("bad horse ranking *training")
                    training_Y.append(0)
    print ("length of training_x" + str(len(training_X)))
    print ("length of training_Y" + str(len(training_Y)))
    print ("length of test_X" + str(len(test_X)))
    print ("length of test_Y" + str(len(test_Y)))
    print ("length of test_data" + str(len(test_data)))

    return training_X, training_Y, test_X, test_Y, test_data


def make_test_result_data(test_data, test_prob, test_prob_2, test_prob_3):
    test_result = []
    for a in range(len(test_data)):
        print("========step3========make_test_result_data:" + str(a) + " of " + str(len(test_data)))
        raceDate = test_data[a][0]
        raceNo = test_data[a][1]
        order = test_data[a][2]
        Horse_num = test_data[a][3]
        predict = test_prob[a][1]
        predict2 = test_prob_2[a][1]
        predict3 = test_prob_3[a][1]

        winning_history_1st_odds= test_data[a][7]
        #winning_history_1st_jockey= test_data[a][7]
       # winning_history_1st_trainer= test_data[a][8]
       # predict_total = predict + predict2 + predict3


        test_result.append([raceDate, raceNo, order, Horse_num, predict, winning_history_1st_odds])


    return pd.DataFrame(test_result).set_index([0, 1, 2])


def load_price_rate(test_day):
    race_price = []
    for day in test_day:
        file_name = day.split('-')[0] + day.split('-')[1] + day.split('-')[2] + ".txt"
        rate_prices_datas = open("../data/boksung_price_rate/" + file_name, 'r')
        rate_prices_data = rate_prices_datas.readlines()
        for line in rate_prices_data:
            race_price.append(line.split())

    return race_price

if __name__ == '__main__':
    data_set = load_data()
    daily_set = make_daily_data(data_set)
    test_day = ['2017-04-22', '2017-04-23']
    make_data_test(daily_set, test_day)



