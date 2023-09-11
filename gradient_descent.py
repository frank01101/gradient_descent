#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Gradient descent for multiple linear and logistic regression with feature scaling and regularization
# author: Franciszek Humieja
# email: frank.humieja@gmail.com
# version 1.4 -- 2023-09-11

import numpy as np
import time, copy
import gradient_descent_services as aux

def zscore_norm(X):
    """
    Computes X, z-score-normalized by columns.
    Args:
        X (ndarray (m,n))       : data, m training examples with n features
    Returns:
        X_norm (ndarray (m,n)   : input normalized by column
        mu (ndarray (n,))       : mean of each column (feature)
        sigma (ndarray(n,))     : standard deviation of each column (feature)
    """
    mu = np.mean(X, axis=0)     # mean of each column of X
    sigma = np.std(X, axis=0)   # standard deviation of each column of X
    X_norm = (X-mu)/sigma       # z-score normalized data
    return (X_norm, mu, sigma)

def cost_func(X, y, w, b, logistic_regr = False, regularization = False, l = 0):
    """
    Cost function for given training examples (X, y) and parameters w (weight) and b (bias).
    Args:
        X (ndarray (m,n))    : data, m training examples with n features
        y (ndarray (m,))     : m target examples
        w (ndarray (n,))     : n model parameters, weights
        b (scalar)           : model parameter, bias
        logistic_regr (bool) : True: logistic cost is calculated; False: linear cost is calculated
        regularization (bool): perform a regularization of weight parameters?
        l (scalar)           : regularization parameter
    Returns:
        j (scalar)           : value of cost function for given args 
    """
    m = X.shape[0]                          # number of examples
    if logistic_regr:
        f = 1.0/(1+np.exp(-X@w-b))          # logistic model, prediction for all training examples
        prod_j = np.prod(f**y*(1-f)**(1-y)) # product inside the logarithm in logistic cost function
        j = -np.log(prod_j)/m               # final logistic cost function
    else:
        f = X@w+b                           # linear model, prediction for all training examples
        j = np.sum((f-y)**2)/(2*m)          # final linear cost function
    if regularization:
        j += l/(2*m)*np.sum(w**2)           # regularization term for parameters w
    return j

def fit_parameters(X, y, w_init, b_init, a, logistic_regr = False, regularization = False, l = 0, print_loop = False, store_j = False):
    """
    Fits parameters w (weights) and b (bias) using the method of gradient descent for multiple linear or logistic regression for given training examples (X, y).
    Args:
        X (ndarray (m,n))       : data, m training examples with n features
        y (ndarray (m,))        : m target examples
        w_init (ndarray (n,))   : n initial model parameters, weights
        b_init (scalar)         : initial model parameter, bias
        a (scalar)              : learning rate
        logistic_regr (bool)    : True: logistic gradient descent is calculated; False: linear gradient descent is calculated
        regularization (bool)   : perform a regularization of weight parameters?
        l (scalar)              : regularization parameter
        print_loop (bool)       : print updates of parameters during the loop?
        store_j (bool)          : store values of cost function during the loop?
    Returns:
        w (ndarray (n,))        : n fitted model parameters, weights
        b (scalar)              : fitted model parameter, bias
        k (integer)             : total number of iterations
        toc-tic (float)         : time duration of the loop
        j_history (list)        : history of value of cost function
    """
    m, n = X.shape              # number of examples (m) and features (n)
    w = copy.deepcopy(w_init)   # model parameter to be updated; avoid modifying the global w_init variable.
    b = b_init                  # model parameter which will be being updated
    j_history = []              # history of the cost function values to be plotted
    convergence = False         # bool saying whether to terminate the loop
    if logistic_regr:
        conv_accuracy = 1e-5    # level of increment/decrement at which to terminate the loop for logistic regresion
    else:
        conv_accuracy = 1e-10   # level of increment/decrement at which to terminate the loop for linear regression
    max_iter = 1e+7             # maximal number of iterations of the loop in case of divergence
    k = 0                       # index to make sure the loop is terminated in case the divergence cannot be acheived
    tic = time.time()           # capture start time
    while not convergence and k < max_iter:
        k += 1                              # count the iterations to finish the loop if their number is too large
        f = X@w+b                           # linear model function (hypothesis) for all examples
        if logistic_regr:
            f = 1.0/(1+np.exp(-f))          # logistic model function (hypothesis) for all examples
        sum_w = np.sum((f-y)*X.T,axis=1)    # sum appearing in the formula for vector w
        sum_b = np.sum(f-y)                 # sum appearing in the formula for b
        if regularization:
            w *= 1-a*l/m                    # regularization factor
        w -= a/m*sum_w                      # update of the weight parameter
        b -= a/m*sum_b                      # update of the bias parameter
        if print_loop or store_j:
            k_10_pow_floor = 10**(int(np.log10(k)))   # floor of k to the nearest integer power of 10
            if k%(int(k/k_10_pow_floor)*k_10_pow_floor) == 0:
                if print_loop:
                    print(f"k: {k},\tw = {w},\tb = {b:.8f},\ta*dJ/dw = {a/m*sum_w+regularization*a*l/m*w},\ta*dJ/db = {a/m*sum_b:.8e},\tJ(w,b) = {cost_func(X, y, w, b, logistic_regr, regularization, l):.8f}")
                if store_j:
                    j_history.append(cost_func(X, y, w, b, logistic_regr))
        if np.max(abs(a/m*sum_w+regularization*a*l/m*w)) < conv_accuracy and abs(a/m*sum_b) < conv_accuracy:
            convergence = True      # if all the increments/decrements for w and b are small, finish the loop
    toc = time.time()               # capture end time
    return (w, b, k, toc-tic, j_history)

if __name__ == "__main__":
    default_a = 0.1     # default learning rate, alpha
    default_l = 1.0     # default regularization parameter, lambda
    if aux.help_needed():
        aux.print_help(default_a, default_l)
    else:
        X_train, y_train = aux.load_data()
        m = X_train.shape[0]
        if X_train.ndim == 1:
            X_train = X_train.reshape(m,1)
        n = X_train.shape[1]
        X_norm, mu, sigma = zscore_norm(X_train)
        a, w_init, b_init, logistic_regr, regularize, l, print_loop, plot_j = aux.load_initial_param(default_a, default_l, n, mu, sigma)
        w, b, k, dur, j_hist = fit_parameters(X_norm, y_train, w_init, b_init, a, logistic_regr, regularize, l, print_loop, plot_j)
        j_init = cost_func(X_norm, y_train, w_init, b_init, logistic_regr, regularize, l)
        j_end = cost_func(X_norm, y_train, w, b, logistic_regr, regularize, l)
        print(f"w_norm = {w}, b_norm = {b:.8f}, number of iterations: {k}, duration: {dur:.4f} sec")
        print(f"w = w_norm/sigma = {w/sigma}, b = b_norm-sum(w_norm*mu/sigma) = {b-np.sum(w*mu/sigma):.8f}")
        print(f"Cost function: for initial parameters: {j_init:.8f}, for final parameters: {j_end:.8f}")
        if plot_j:
            aux.make_plot(j_hist)
