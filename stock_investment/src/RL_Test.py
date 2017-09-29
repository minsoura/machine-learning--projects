import numpy as np
from src import simulation
from src import DataGenerator as DG
from src.decision_ql import QLearningDecisionPolicy
import operator

def test_simu(policy, initial_budget, initial_num_stocks, prices, features, purchase_unit):

    budget = initial_budget
    num_stocks = initial_num_stocks
    share_value = 0

    for i in range(len(prices) - 1):
        portfolio = budget + num_stocks * share_value
        current_state = np.asmatrix(np.hstack((features[i], budget, num_stocks)))
        print(current_state)
        action = policy.select_action(current_state, i)
        share_value = float(prices[i])
        print("for: %i th day" % i);
        budget, num_stocks, action = simulation.do_action(action, budget, num_stocks, share_value,purchase_unit)
        print("\n")

    portfolio = budget + num_stocks * share_value
    print ('Finally, you have')
    print ('budget: %f won' % budget)
    print ('Shares: %i' % num_stocks)
    print ('Final share value: %f won' % share_value)

    return portfolio

if __name__ == '__main__':
    symbols = ['Hyundai_Mobis', 'Hyundai_Motors', 'Korea_Electric_Power', 'Naver', 'POSCO', 'Samsung_C_T',
               'Samsung_Electronics', 'Samsung_Life', 'Shinhan_Financial', 'SK_Hynix']
   # symbols = ['Samsung_Electronics']

    portfolio_dict= {}
    gain_dict={}
    for idx, item in enumerate(symbols):
        """
            prices, features, pretest_prices, pretest_features = DG.make_features(item, '2017-01-01', '2017-05-04', True)
        print(len(pretest_prices))
        # TODO: define action
        actions = ["Buy", "Sell"]
        avg_price = sum(pretest_prices) / len(pretest_prices)
        budget = 10000000.0
        purchase_unit = int(budget / avg_price)
        num_stocks = 0
        policy = QLearningDecisionPolicy(actions, len(pretest_features[0]) + 2, "LFD_project4_13_" + item, item)
        final_portfolio = test_simu(policy, budget, num_stocks, pretest_prices, pretest_features, purchase_unit)
        portfolio_dict[item] = final_portfolio
        gain_dict[item] = (final_portfolio - 10000000) / avg_price
        print("Final portfolio: %f won" % final_portfolio)
        print("\n");
        print("\n");

        """
        prices, features, pretest_prices, pretest_features = DG.make_features(item, '2017-01-01', '2017-05-04', True)

        print(len(prices))
        # TODO: define action
        actions = ["Buy", "Sell"]
        avg_price = sum(prices) / len(prices)
        budget = 10000000.0
        purchase_unit = int(budget / avg_price)
        num_stocks = 0
        policy = QLearningDecisionPolicy(actions, len(features[0]) + 2, "LFD_project4_13_" + item, item)
        final_portfolio = test_simu(policy, budget, num_stocks, prices, features, purchase_unit)
        portfolio_dict[item] = final_portfolio
        gain_dict[item] = (final_portfolio - 10000000) / avg_price
        print("Final portfolio: %f won" % final_portfolio)
        print("\n");
        print("\n");

    sorted_dict = sorted(portfolio_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("\n")

    for k, v in sorted_dict[:]:
        print(k + ": " + str(v))

    print("\n")

    sorted_dict2 = sorted(gain_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("\n")

    for k, v in sorted_dict2[:]:
        print(k + ": " + str(v))

    print("\n")


 #TODO: feature selection done and run the model for the last n days
    top_n_companies = 3
    total_price = 0
    for k, v in sorted_dict2[:top_n_companies]:
        prices, features, pretest_prices, pretest_features = DG.make_features(k, '2017-01-01', '2017-05-04', True)
        avg_price = sum(prices) / len(prices)
        total_price += avg_price
    portfolio_dict_real = {}
    gain_dict_real = {}
    for k, v in sorted_dict2[:top_n_companies]:

        prices, features, pretest_prices, pretest_features = DG.make_features(k, '2017-01-01', '2017-05-04', True)
        print(k)
        print (len(prices))
        # TODO: define action
        actions = ["Buy", "Sell"]
        avg_price = sum(prices) / len(prices)
        budget = 10000000.0 * (avg_price/total_price)
        initial_budget = int(10000000.0 * (avg_price / total_price))

        purchase_unit = int(budget/ avg_price)
        num_stocks = 0
        policy = QLearningDecisionPolicy(actions, len(features[0]) + 2, "LFD_project4_13_1" + k, k + "_2",)
        final_portfolio_real = test_simu(policy, budget, num_stocks, prices, features, purchase_unit)
        portfolio_dict_real[k]=final_portfolio_real
        gain_dict_real[k] = (final_portfolio_real - initial_budget)/avg_price
        print ("Final portfolio: %f won" % final_portfolio_real)
        print ("\n");
        print("\n");

    sorted_dict_real = sorted(portfolio_dict_real.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict2_real = sorted(gain_dict_real.items(), key=operator.itemgetter(1), reverse=True)
    total_portfolio =0
    print("\n")

    for k, v in sorted_dict_real[:]:
        print(k + ": " + str(v))
        total_portfolio += v

    print("\n")
    for k, v in sorted_dict2_real[:]:
        print(k + ": " + str(v))
    print("\n")

    print(total_portfolio)


