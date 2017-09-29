from sklearn import neural_network as NN
from sklearn.metrics import *
import numpy as np
import pickle
import DataGenerator


if __name__ == "__main__":

    start_date = '2010-01-01'
    end_date = '2017-04-07'
    input_days_control_arrays = (30, 50, 100, 300)
    test_file_set_names =('Test_Model_1.pkl','Test_Model_2.pkl','Test_Model_3.pkl','Test_Model_4.pkl')
    mae_values_set =[]
    for idx, days in enumerate(input_days_control_arrays):
            training_x, training_y, test_x, test_y = DataGenerator.make_features(start_date, end_date, days)
            # # TODO: set parameters
            model = NN.MLPRegressor(hidden_layer_sizes=(150,), activation='tanh', solver='sgd',alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.00001, power_t=0.6, max_iter=1000, shuffle=True, tol=0.00001, verbose=True,  momentum=0.1, beta_1=0.9, beta_2=0.999)
            model.fit(training_x, training_y)
            filename = test_file_set_names[idx]
            pickle.dump(model, open(filename, 'wb'))
            print 'save complete'

            loaded_model = pickle.load(open(filename, 'rb'))
            print 'load complete'
            print loaded_model.get_params()
            predict = loaded_model.predict(test_x)
            print 'mae: ', mean_absolute_error(np.reshape(predict, -1), test_y)
            mae_values_set.insert(idx, mean_absolute_error(np.reshape(predict, -1), test_y))

    for idx, result in enumerate(mae_values_set):
            print 'mae Values for ' + str(input_days_control_arrays[idx]) + ' is ' + str(result)
