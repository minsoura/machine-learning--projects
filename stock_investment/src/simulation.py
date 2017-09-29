# encoding: utf-8
import numpy as np


def do_action(action, budget, num_stocks, share_value, purchase_unit):
    # TODO: define action's operation
    portfolio = budget + num_stocks * share_value

    if action == "Buy" and budget >= purchase_unit*share_value:
        budget -= purchase_unit*share_value
        num_stocks += purchase_unit
    elif action == "Sell" and num_stocks > 0:
        budget += purchase_unit* share_value
        num_stocks -= purchase_unit
    else:
        action = "Hold"

    print("Action taken:" + action)
    print ('budget: %f won' % budget)
    print ('Asset:' + str( num_stocks * share_value))
    portfolio = budget + num_stocks * share_value
    print("Portfolio:" + str(portfolio))
    return budget, num_stocks, action


def run_simu(policy, initial_budget, initial_num_stocks, prices, features, purchase_unit):
    # initialization
    budget = initial_budget
    num_stocks = initial_num_stocks
    share_value = 0

    for i in range(len(prices) - 1):

        # the state is a hist+2 dim vector
        # TODO: define state
        current_state = np.asmatrix(np.hstack((features[i], budget, num_stocks)))

        # calc current protfolio value
        current_portfolio = budget + num_stocks * share_value

        # select action
        action = policy.select_action(current_state, i)

        # share value
        share_value = float(prices[i])

        # update portfolio values based on action
        budget, num_stocks, action = do_action(action, budget, num_stocks, share_value, purchase_unit)

        # calc new portofolio after tacking action
        new_portfolio = budget + num_stocks * share_value

        # calc reward from tacking an action at a state
        # TODO: define reward
        reward = new_portfolio - current_portfolio

        # TODO: define next state
        next_state = np.asmatrix(np.hstack((features[i+1], budget, num_stocks)))

        # update the policy after experiencing a new action
        policy.update_q(current_state, action, reward, next_state)

    # compute final portfolio worth
    portfolio = budget + num_stocks * share_value

    print ('${} budget\t{} shares\t{} share value\t portfolio ${}'.format(budget, num_stocks, share_value, portfolio))
    return portfolio


def run_simus(policy, budget, num_stocks, prices, features, num_tries, purchase_unit):
    final_portofolios = list()

    for i in range(num_tries):
        print ("simulation no.%d" % i)
        final_portofolio = run_simu(policy, budget, num_stocks, prices, features, purchase_unit)
        final_portofolios.append(final_portofolio)
    avg, std = np.mean(final_portofolios), np.std(final_portofolios)
    return avg, std
