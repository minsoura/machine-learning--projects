#encoding:utf-8

import tensorflow as tf


# TODO:  make q function to use
def mlp(scope_name, x, input_dim, h1_dim, output_dim):
    # neural network with one hidden layer
    with tf.variable_scope(scope_name) as scope:
        fc1 = fc('fc1', x, [input_dim, h1_dim], [h1_dim])
        q = fc('fc2', fc1, [h1_dim, output_dim], [output_dim])

        # neural network output is approximate of q function
    return q


def fc(scope_name, inputs, shape, bias_shape, wd=0.000001, reuse=None, trainable=True):
    with tf.variable_scope(scope_name) as scope:
        if reuse is True:
            scope.reuse_variables()
        flat = tf.reshape(inputs, [-1, shape[0]])
        weights = _variable_with_weight_decay(
            'weights',
            shape,
            stddev=0.1,
            wd=wd,
            trainable=trainable
        )
        biases = _variable_on_gpu('biases', bias_shape, tf.constant_initializer(0.1))
        fc = tf.nn.relu_layer(flat, weights, biases, name=scope.name)
        return fc


def _variable_with_weight_decay(name, shape, stddev, wd, trainable=True):
    var = _variable_on_gpu(name, shape, tf.truncated_normal_initializer(stddev=stddev))
    if wd:
        weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')
        tf.add_to_collection('losses', weight_decay)
    return var


def _variable_on_gpu(name, shape, initializer):
    var = tf.get_variable(name, shape, initializer=initializer)
    return var
