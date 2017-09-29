from hmmlearn.hmm import GaussianHMM
from sklearn.metrics import *
import numpy as np
import pickle
import DataGenerator

numberStart = 1
numberEnd = 31
input_days_control_arrays = list(range(numberStart, numberEnd))
mae_values_set = []


if __name__ == "__main__":

    start_date = '2016-04-25'
    end_date = '2017-04-25'

    for idx, days in enumerate(input_days_control_arrays):
        training_x, test_x, past_price, target_price = DataGenerator.make_features(start_date, end_date, days)
        # # TODO: set parameters
        n_components = 4
        model = GaussianHMM(n_components=n_components, covars_prior=0.01, covariance_type='diag',
                            params='stmc', transmat_prior=1.0, covars_weight=1, init_params='stmc',
                            random_state=None, tol=0.01, means_prior=0, algorithm='viterbi', verbose=False,
                            n_iter=10, means_weight=0, startprob_prior=1.0, min_covar=0.001)
        model.fit(training_x)

        hidden_states = model.predict(test_x)

        print(hidden_states)
        print(len(hidden_states))

        # the stat of each state
        for i in range(model.n_components):
            print("{0}th hidden state".format(i))
            print("mean = ", model.means_[i])
            print("var = ", np.diag(model.covars_[i]))

        # print 'trans', model.transmat_
        print('means', model.means_)
        expected_returns_and_volumes = np.dot(model.transmat_, model.means_)
        returns_and_volumes_columnwise = list(zip(*expected_returns_and_volumes))
        returns = returns_and_volumes_columnwise[0]

        print('erv')
        print(expected_returns_and_volumes)
        print('rvc')
        print(returns_and_volumes_columnwise)
        print('returns')
        print(returns)

        p_price = []
        test_days = 10
        for idx in range(test_days):
            state = hidden_states[idx]
            current_price = past_price[idx]
            p_price.append(current_price + returns[state])
        predict = np.array(p_price)

        # print predicted_prices
        print('past', len(past_price), np.array(past_price))
        print('real', len(target_price), np.array(target_price))
        print('expected', len(p_price), p_price)

        print('mae', mean_absolute_error(target_price, predict))
        mae_values_set.insert(idx, mean_absolute_error(target_price, predict))

    # run the model with different input_days_value
    # and select the smallest MAE
    # save the model file
    input_value_for_minimum_mae = 0
    min_mae = 0
    for idx, result in enumerate(mae_values_set):
        input_value = idx + 1
        print('for input_day_value  ' + str(input_value))
        print('mae is ' + str(result))
        if idx == 0:
            min_mae = result
            input_value_for_minimum_mae = idx + 1
        elif idx != 0 and idx != numberEnd-2:
            if result <= min_mae:
                min_mae = result
                input_value_for_minimum_mae = idx + 1
        elif idx == numberEnd-2:
            if result <= min_mae:
                min_mae = result
                input_value_for_minimum_mae = idx + 1
            print('================================')
            print('Minimum MAE Value is ' + str(min_mae))
            print('when input_days_value is ' + str(input_value_for_minimum_mae))
            training_x2, test_x2, past_price2, target_price2 = DataGenerator.make_features(start_date, end_date, input_value_for_minimum_mae)
            n_components2 = 4
            model2 = GaussianHMM(n_components2)
            model2.fit(training_x2)
            filename = '13_model.pkl'
            pickle.dump(model2, open(filename, 'wb'))
            print('save complete')
            ####################
            #  For EVALUATION  #
            ####################

            loaded_model = pickle.load(open(filename, 'rb'))
            print('load complete')
            print(loaded_model.get_params())