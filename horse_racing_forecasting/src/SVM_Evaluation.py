#-*- coding: utf-8 -*-

import os
from sklearn import svm
import pandas as pd
import pickle
from src import DataGenerator

if __name__ == '__main__':
    data_set = DataGenerator.load_data()
    daily_set = DataGenerator.make_daily_data(data_set)
    test_day_new = ['2017-04-29']
    test_day = ['2017-04-15', '2017-04-16','2017-04-22', '2017-04-23']
    training_X, training_Y, test_X, test_data, training_X_2, training_X_3, test_X_2, test_X_3= DataGenerator.make_data(daily_set, test_day)

    # ================================ make SVM model=========================================
    # TODO: set parameters
    print('make model and training...')
   # model = svm.SVC(probability=True, class_weight='balanced',)
    model = svm.SVC(C=1, kernel='rbf', degree=3, gamma='auto', coef0=0.0,
                    shrinking=True, probability=True, tol=0.001, cache_size=500,
                    class_weight='balanced', verbose=False, max_iter=-1, decision_function_shape=None, random_state=None)
    model.fit(training_X, training_Y)
    model2 = svm.SVC(C=1, kernel='rbf', degree=3, gamma='auto', coef0=0.0,
                    shrinking=True, probability=True, tol=0.001, cache_size=500,
                    class_weight='balanced', verbose=False, max_iter=-1, decision_function_shape=None,
                    random_state=None)
    model2.fit(training_X_2, training_Y)
    model3 = svm.SVC(C=1, kernel='rbf', degree=3, gamma='auto', coef0=0.0,
                    shrinking=True, probability=True, tol=0.001, cache_size=500,
                    class_weight='balanced', verbose=False, max_iter=-1, decision_function_shape=None,
                    random_state=None)
    model3.fit(training_X_3, training_Y)

    print('training done...')
    filename = 'model_02.pkl'
    pickle.dump(model, open(filename, 'wb'))
    #print 'save complete'
    #

    loaded_model = pickle.load(open(filename, 'rb'))
    #print 'load complete'

    #print loaded_model.get_params()

    # ================================ predict result ========================================
    print('predict result')
    test_prob = model.predict_proba(test_X)
    test_prob2 = model2.predict_proba(test_X_2)
    test_prob3 = model3.predict_proba(test_X_3)


    test_result = DataGenerator.make_test_result_data(test_data, test_prob, test_prob2, test_prob3)

    test_result.to_csv("test_result.csv")
    test_result = pd.read_csv("test_result.csv", index_col=[0, 1, 2])

    '''
    indexing_new = []
    race_date_containers = ['2017-04-29']
    race_num_containers = [1,2,3,4,5,6,7,8,9,10,11]
    for race_num in race_num_containers:
        indexing_new.append(tuple(['2017-04-29',race_num]))

    for index1 in indexing_new:

        # test_result [[date, race_no, rank_order, horse_no, classified_prob, 1st, 2nd, 1st_recent, 2nd_recent, total_money_won]]
        result = test_result.ix[index1]

        result.columns = ['number', 'prob', '1st']


        result2 = result.sort_values(by=['prob', '1st'], ascending=[False, False]).iloc[:3]
        result3 = result.sort_values(by=['prob', '1st'], ascending=[False, False])
        print('result for result2')
        print(result2[:])
        top = list(result2['number'])
        print(index1[0], 'race ', index1[1])
        print("my bet:" + str(top[0]) + " and " + str(top[1]))
    
    '''


    # =================================== real result ========================================
    price_rate = DataGenerator.load_price_rate(test_day)

    indexing = []
    indexing1 = []
    indexing2 = []
    target = []
    for a in range(len(price_rate)):
        date = price_rate[a][0]
        race = int(price_rate[a][1])
        indexing1.append(date)
        indexing2.append(race)
        indexing.append(tuple([date, race]))
        target.append(price_rate[a][2:])
    #print ("race price before indexing")
    #print (price_rate)
    race_price = pd.DataFrame(target, index=[indexing1, indexing2])
    #print ("race price: ")
    #print (race_price)
    #print ("indexing structure")
    #print (indexing)
    money = 5000000
    win = 0
    lose = 0
    total_games_played = len(indexing)
    win_percentage =0;
    betting_price = 100000

    double_win =0
    double_lose=0

    half_win =0
    half_lose =0


    half_win_2 =0
    half_lose_2=0

    print('Your starting money is %i won' % money)
    # =========================== check the result and scoring =============================
    #indexing [(date, race_no),(date, race_no)...]
    
    
    for index1 in indexing:
        money -= betting_price
        #test_result [[date, race_no, rank_order, horse_no, classified_prob, 1st, 2nd, 1st_recent, 2nd_recent, total_money_won]]
        result = test_result.ix[index1]

        result.columns = ['number', 'prob','odds']

        result2 = result.sort_values(by=['prob', 'odds', 'number'], ascending=[False, False, True]).iloc[:3]
        result3 =  result.sort_values(by=['prob', 'number'], ascending=[False, False])
        print('result value after columns')
        print(result3)
        # print ('result for result2')
        #print (result2[:2])
        # top = list(result3['3'])
        top = list(result2['number'])
        real = race_price.ix[index1]

        real_list = [int(list(real)[0]), int(list(real)[1]),]
        real_list2 = [int(list(real)[0]), int(list(real)[1])]
        real_first= int(list(real)[0])
        real_second = int(list(real)[1])

        print(index1[0], 'race ', index1[1])
        print("my bet:" + str(top[0]) + " and " +str(top[1]) + " /// real: " +str(real_list[0]) + " and " + str(real_list[1]))
        if top[0] in real_list and top[1] in real_list:
            win += 1
            got = float(real[2]) * betting_price
            money += got
            print('win! you got %i won' % got)
        else:
            print('lost money')
            lose += 1
            # 쌍복승식 순서에 상관있게 맞추기
        if top[0] == real_list[0] and top[1] == real_list[1]:
            double_win += 1
        else:
             double_lose += 1
          #연승식 1~3등안에 들어올 말 1두를 적중시키는 방식
        if top[0] in real_list2 :
            half_win += 1
        else:
            half_lose += 1

        # 연승식 1~3등안에 들어올 말 1두를 적중시키는 방식
        if top[0] in real_list2 and top[1] in real_list2:
            half_win_2 += 1
        else:
            half_lose_2 += 1
        print ("")
        print ("")
    #############################
    #       For Evaluation      #
    #############################
    print('win %i times and lose %i times  for 복승식 승률 %.3f' % (win, lose, win/(total_games_played)))
    print('win %i times and lose %i times  for 쌍복승식 승률 %.3f' % (double_win, double_lose, double_win / (total_games_played)))
    print('half_win %i times and half_lose %i times for 연승식' % (half_win, half_lose))
    print('half_win_2 %i times and half_lose_2 %i times for 복연승식' % (half_win_2, half_lose_2))
    print('Finally, you have %i won by investing %i won' % (money, betting_price*total_games_played))
