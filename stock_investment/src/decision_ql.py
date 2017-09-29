#encoding: utf-8
from tensorflow.python.platform import gfile

import tensorflow as tf
import numpy as np
import random

from .decision_rand import DecisionPolicy
from .model import mlp


class QLearningDecisionPolicy(DecisionPolicy):
    def __init__(self, actions, input_dim, model_dir, scopeName):
        # select action function hyper-parameters
        self.epsilon = 0.5
        # q functins hyper-parameters
        self.gamma = 0.01
        # neural network hyper-parmetrs
        self.lr = 0.01

        self.actions = actions
        output_dim = len(actions)

        # neural network input and output placeholder
        self.x = tf.placeholder(tf.float32, [None, input_dim])
        self.y = tf.placeholder(tf.float32, [output_dim])

        # hidden layer dimension
        h1_dim = 20

        # model inference
        self.q = mlp("NN" + "_" + scopeName, self.x, input_dim, h1_dim, output_dim)

        # loss
        loss = tf.square(self.y - self.q)

        # train operation
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(loss)

        # session
        self.sess = tf.Session()

        # initalize
        init_op = tf.initialize_all_variables()
        # init_op = tf.global_variables_initializer
        self.sess.run(init_op)

        # saver
        self.saver = tf.train.Saver(tf.trainable_variables())

        # laod model
        ckpt = tf.train.get_checkpoint_state(model_dir)
        if ckpt and ckpt.model_checkpoint_path:
            print ("load model: %s" % ckpt.model_checkpoint_path)
            self.saver.restore(self.sess, ckpt.model_checkpoint_path)

    def select_action(self, current_state, step):
        threshold = min(self.epsilon, step/1000.)

        if random.random() < threshold:
            action_q_vals = self.sess.run(self.q, feed_dict={self.x: current_state})
            action_idx = np.argmax(action_q_vals)
            action = self.actions[action_idx]
        else:
            # random choice
            action = self.actions[random.randint(0, len(self.actions)-1)]

        return action

    def update_q(self, state, action, reward, next_state):
        # Q(s, a)
        action_q_vals = self.sess.run(self.q, feed_dict={self.x: state})
        # Q(s', a')
        next_action_q_vals = self.sess.run(self.q, feed_dict={self.x: next_state})
        # a' index
        next_action_idx = np.argmax(next_action_q_vals)
        # create target
        action_q_vals[0, next_action_idx] = reward + self.gamma * next_action_q_vals[0, next_action_idx]
        # delete minibatch dim
        action_q_vals = np.squeeze(np.asarray(action_q_vals))
        self.sess.run(self.train_op, feed_dict={self.x: state, self.y: action_q_vals})

    def save_model(self, output_dir, step):
        if not gfile.Exists(output_dir):
            gfile.MakeDirs(output_dir)

        checkpoint_path = output_dir + '/model.ckpt'
        self.saver.save(self.sess, checkpoint_path, global_step=step)

