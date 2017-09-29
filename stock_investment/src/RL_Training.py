
from src.decision_ql import QLearningDecisionPolicy
from src import DataGenerator
from src import simulation
from src.decision_rand import  RandomDecisionPolicy
from multiprocessing import Process
import operator

if __name__ == '__main__':
    symbols = ['Hyundai_Mobis', 'Hyundai_Motors', 'Korea_Electric_Power', 'Naver', 'POSCO', 'Samsung_C_T',
               'Samsung_Electronics', 'Samsung_Life', 'Shinhan_Financial', 'SK_Hynix']
    portfolio_dict ={}
    gain_dict = {}
    for idx, item in enumerate(symbols):
        prices, features = DataGenerator.make_features(item,'2017-01-01', '2017-05-04',)
        # TODO: define action
        actions = ["Buy", "Sell"]
        #policy = RandomDecisionPolicy(actions)
        policy = QLearningDecisionPolicy(actions, len(features[0]) + 2, "model", item)
        avg_price = sum(prices) / len(prices)
        budget = 10000000.0
        purchase_unit = int(budget / avg_price)
        num_stocks = 0
        num_tries = 100

        avg, std = simulation.run_simus(policy, budget, num_stocks, prices, features, num_tries, purchase_unit)

        policy.save_model("LFD_project4_13_" + str(item), num_tries)
        policy.save_model("LFD_project4_13_1" + str(item), num_tries)
        portfolio_dict[item] = avg
        gain_dict[item] = (avg - 10000000) / avg_price
        print("Portfolio avg: $%f, std: %f" % (avg, std))
        print("\n\n")
    sorted_dict = sorted(portfolio_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("\n")

    for k, v in sorted_dict[:]:
        print(k + ": " + str(v))
    print("\n")
    sorted_dict2 = sorted(gain_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("\n")

    for k, v in sorted_dict2[:]:
        print(k + ": " + str(v))
