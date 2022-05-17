# Imports

import numpy as np
from matplotlib import pyplot as plt
from os.path import isfile
import pandas as pd
from sklearn.model_selection import train_test_split

import tensorflow.compat.v1 as tf


tf.disable_v2_behavior()


class SVR(object):
    def __init__(self, epsilon=0.5):
        self.epsilon = epsilon
        
    def fit(self, X, y, epochs=100, learning_rate=0.1):
        self.sess = tf.Session()
        
        feature_len = X.shape[-1] if len(X.shape) > 1 else 1
        
        if len(X.shape) == 1:
            X = X.vreshape(-1, 1)
        if len(y.shape) == 1:
            y = y.values.reshape(-1, 1)
        
        self.X = tf.placeholder(dtype=tf.float32, shape=(None, feature_len))
        self.y = tf.placeholder(dtype=tf.float32, shape=(None, 1))
        
        self.W = tf.Variable(tf.random_normal(shape=(feature_len, 1)))
        self.b = tf.Variable(tf.random_normal(shape=(1,)))
        
        self.y_pred = tf.matmul(self.X, self.W) + self.b
        
        #self.loss = tf.reduce_mean(tf.square(self.y - self.y_pred))
        #self.loss = tf.reduce_mean(tf.cond(self.y_pred - self.y < self.epsilon, lambda: 0, lambda: 1))
        
        # Second part of following equation, loss is a function of how much the error exceeds a defined value, epsilon
        # Error lower than epsilon = no penalty.
        self.loss = tf.norm(self.W)/2 + tf.reduce_mean(tf.maximum(0., tf.abs(self.y_pred - self.y) - self.epsilon))
#         self.loss = tf.reduce_mean(tf.maximum(0., tf.abs(self.y_pred - self.y) - self.epsilon))
        
        opt = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
        opt_op = opt.minimize(self.loss)

        self.sess.run(tf.global_variables_initializer())
        
        for i in range(epochs):
            loss = self.sess.run(
                self.loss, 
                {
                    self.X: X,
                    self.y: y
                }
            )
            print("{}/{}: loss: {}".format(i + 1, epochs, loss))
            
            self.sess.run(
                opt_op, 
                {
                    self.X: X,
                    self.y: y
                }
            )
            
        return self
            
    def predict(self, X, y=None):
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
            
        y_pred = self.sess.run(
            self.y_pred, 
            {
                self.X: X 
            }
        )
        return y_pred
    
    
dataset_path = 'server/data/dataset.csv'

if isfile(dataset_path):
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')


    X = data.iloc[:, 0:-1]
    y = data.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=100
    )

    
    model = SVR(epsilon=0.2)
    model.fit(X_train, y_train)
    
    print(model.predict(X_test))
    

else:
    print('Dataset not found ')

