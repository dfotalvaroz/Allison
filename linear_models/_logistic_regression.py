# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from utils.functions.activation import Sigmoid

from utils.functions.loss import binary_cross_entropy

from utils.metrics import predict_labels

class LogisticRegression():

  def __init__(self):
    self.weights=None
    self.bias=np.random.rand(1,1)
    self.linear_convination=None
    self.regularization=None
    self.loss_function=None
    self.learning_ratio=None
    self.metrics=None
    self.function_of_activation=None

  def optimizers(self,function_of_activation,loss_function,lr,metrics,regularization=None):
    self.function_of_activation=function_of_activation
    self.loss_function=loss_function
    self.learning_ratio=lr
    self.metrics=metrics
    self.regularization=regularization

    
  def init_params(self,features):
    if features.ndim==1:
      self.weights=np.random.rand(1,1)
    else :
      self.weights=np.random.rand(1,features.shape[0])


  def foward(self,features):
    self.linear_convination=self.bias + self.weights@features
    prediction=self.function_of_activation(self.linear_convination)
    return prediction


  def  bacward(self,labels,predictions, features):
  

    gradient=self.loss_function(labels, predictions,True)*self.function_of_activation(self.linear_convination,True)
    
    gradient=np.mean(gradient)

    gradient_weights=gradient*np.mean(features, axis=1)

    self.bias =self.bias-self.learning_ratio*gradient
    self.weights= self.weights-self.learning_ratio*gradient_weights

  def train(self,n_iters,features, labels, callbacks_period=2):
    self.init_params(features)

    history_train={
        'iter':[],
        'loss':[],
        'accuracy':[]
    }

    for i in range(n_iters):
      predictions=self.foward(features)
      self.bacward(labels, predictions, features)
      if (i+1)%callbacks_period==0:
        score=self.metrics(labels,predictions[0])
        loss=self.loss_function(labels, predictions)
        history_train['loss'].append(loss)
        history_train['accuracy'].append(score)
        history_train['iter'].append(i+1)
        print('Iter:\t{}\t{}\t accuracy:\t{:.2f}% \n\n'.format(i+1,50*'='+'>',score))

    return history_train


  def predict (self,features):
    predictions=self.foward(features)
    global predict_labels
    predictions =predict_labels(predictions[0])
    return predictions
  
  def save_weights(self,path):
    with open(path, 'wb') as f:
      np.save(f,self.bias)
      np.save(f,self.weights)

  
  def load_weights(self,path):
    with open(path, 'rb') as f:
      bias = np.load(f)
      weights = np.load(f)
    self.bias= bias
    self.weights=weights
        
        
    
