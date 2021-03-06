#!/usr/bin/python
''' adaline_gd replaces the activation function by the identity
    function, and adds a differentiable cost function, such as a 
    Sum of Squared Errors (SSE) 
    
    The gradient of the errors is used to adjust the weights.
    
    The learning rate is plotted for several different 'eta' multipliers
    of the gradient. Also, the effect on the learning rate of standardizing
    the features before training is shown.
    
    The decision regions are plotted.
    
    The cost function error versus Epochs is plotted
    
Created on Jun 20, 2016

from Python Machine Learning by Sebastian Raschka under the following license

The MIT License (MIT)

Copyright (c) 2015, 2016 SEBASTIAN RASCHKA (mail@sebastianraschka.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@author: richard lyman
'''
import ocr_utils
import numpy as np
import matplotlib.pyplot as plt

#############################################################################
# read features 

# retrieve 500 sets of target numbers and column sums
#    y: the target is ascii characters 48 and 51 ('0', '3')
#    X: the features to fit is the sum of the vertical pixels in the rows in 
#        horizontal columns 9 and 17
  

ascii_characters_to_train=(48,49)
columnsXY = (9,17)       
nchars=500
y, X, y_test,  X_test, labels  = ocr_utils.load_E13B(chars_to_train = ascii_characters_to_train , columns=columnsXY,nChars=120) 

y = np.where(y==ascii_characters_to_train[1],-1,1)

#############################################################################
# Adaline implementation from Python Machine Learning
class AdalineGD(object):
    """ADAptive LInear NEuron classifier.

    Parameters
    ------------
    eta : float
        Learning rate (between 0.0 and 1.0)
    n_iter : int
        Passes over the training dataset.

    Attributes
    -----------
    w_ : 1d-array
        Weights after fitting.
    errors_ : list
        Number of misclassifications in every epoch.

    """
    def __init__(self, eta=0.01, n_iter=50):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        """ Fit training data.

        Parameters
        ----------
        X : {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values.

        Returns
        -------
        self : object

        """
        self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for i in range(self.n_iter):
            output = self.net_input(X)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        """Calculate net input"""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        """Compute linear activation"""
        return self.net_input(X)

    def predict(self, X):
        """Return class label after unit step"""
        
        return np.where(self.activation(X) >= 0.0, 1, -1)
title = 'Gradient Descent Learning rate 0.01'

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
ada1 = AdalineGD(n_iter=10, eta=0.01).fit(X, y)
ax[0].plot(range(1, len(ada1.cost_) + 1), np.log10(ada1.cost_), marker='o')
ax[0].set_xlabel('Epochs')
ax[0].set_ylabel('log(Sum-squared-error)')
ax[0].set_title('Adaline - Learning rate 0.01')
ada2 = AdalineGD(n_iter=10, eta=0.0001).fit(X, y)

ax[1].plot(range(1, len(ada2.cost_) + 1), ada2.cost_, marker='o')
ax[1].set_xlabel('Epochs')
ax[1].set_ylabel('Sum-squared-error')
ax[1].set_title('Adaline - Learning rate 0.0001')
ocr_utils.show_figures(plt, title)



# 
# plt.plot(range(1,len(ada1.cost_)+1), np.log10(ada1.cost_), marker='o',label = title)
# plt.title(title)
# ocr_utils.show_figures(plt, title)
# 
# ada2 = AdalineGD(n_iter=15, eta=0.0001).fit(X, y)
# title = 'Gradient Descent Learning rate 0.0001'
# plt.plot(range(1,len(ada2.cost_)+1), np.log10(ada2.cost_) ,marker='x',label = title)
# plt.title(title)
# ocr_utils.show_figures(plt, title)
# standardize features
X_std = np.copy(X)
X_std[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()

ada = AdalineGD(n_iter=15, eta=0.01)
ada.fit(X_std, y)
ocr_utils.plot_decision_regions(X=X_std, 
                            y=y,
                            classifier=ada, 
                            labels= labels,
                            title='Adaline - Gradient Descent standardized rate 0.01')

title = 'Standardized Gradient Descent Learning rate 0.01'
plt.plot(range(1,len(ada2.cost_)+1), np.log10(ada2.cost_) ,marker='x',label = title)
plt.title(title)
ocr_utils.show_figures(plt, title)

plt.plot(range(1,len(ada.cost_)+1), np.log10(ada.cost_), marker='v', label='standardized rate 0.01')
plt.xlabel('Epochs')
plt.ylabel('log(Sum-squared-error)')
plt.legend(loc='lower left')
plt.title('Adaline - Gradient Descent')
plt.tight_layout()
ocr_utils.show_figures(plt, 'Adaline - Gradient Descent')

print ('\n########################### No Errors ####################################')