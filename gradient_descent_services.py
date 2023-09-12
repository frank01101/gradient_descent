# Auxilary functions for gradient-descent.py
# author: Franciszek Humieja
# email: frank.humieja@gmail.com
# version 1.2 -- 2023-09-10

from sys import argv
import read_argv as ra
import numpy as np
import matplotlib.pyplot as plt

def help_needed():
    option_help = "-help"
    help_request = ra.is_option(option_help, start_from = 1)
    return help_request
    
def print_help(default_a, default_l):
    print("Gradient descent for multiple linear and logistic regression with feature scaling and regularization. Usage:")
    print("./gradient_descent.py <X_file> <y_file> -bin -rate [alpha] (-wfile [w_file] OR -w [w_value]) -b [b_value] -logistic -regularize -lambda [lambda] -print -plot -help")
    print("Mandatory arguments:")
    print("<X_file>\tpath to the file with feature data")
    print("<y_file>\tpath to the file with target data")
    print("Options:")
    print("-bin\t\tuse when files are binary; by default they are assumed to be text files")
    print("-rate\t\tinput learning rate [alpha]; by default it is", default_a)
    print("-wfile\t\tinput path to the file [w_file] with starting values of w parameters -- in the case when there is more than one feature; by default they are set to zeros")
    print("-w\t\tinput starting value of w parameter [w_value] -- in the case when there is only one feature; by default it is set to zero")
    print("-b\t\tinput starting value of b parameter [b_value]; by default it is set to zero")
    print("-logistic\tcalculates logistic gradient descent instead of linear")
    print("-regularize\tperform parameters regularization")
    print("-lambda\t\tinput regularization parameter [lambda]; by default it is", default_l)
    print("-print\t\tprints results of the steps in gradient descent")
    print("-plot\t\tplots the cost function versus iterations")
    print("-help\t\tprints this help")
    print("Version 1.3, 2023-09-10")

def load_data():
    Xfile_in, yfile_in = argv[1], argv[2]
    option_bin = "-bin"
    bin_files = ra.is_option(option_bin)
    if bin_files:
        X_train = np.load(Xfile_in)
        y_train = np.load(yfile_in)
    else:
        X_train = np.loadtxt(Xfile_in)
        y_train = np.loadtxt(yfile_in)
    return (X_train, y_train)

def load_initial_param(default_a, default_l, n, mu, sigma):
    option_a = "-rate"
    option_w = "-w"
    option_wfile = "-wfile"
    option_b = "-b"
    option_logistic = "-logistic"
    option_regularize = "-regularize"
    option_lambda = "-lambda"
    option_print = "-print"
    option_plot = "-plot"
    if ra.is_option(option_a):
        a = float(ra.find_option_arg(option_a))
    else:
        a = default_a
    if ra.is_option(option_wfile):
        w_in = np.loadtxt(ra.find_option_arg(option_wfile))
        w_init = sigma*w_in
    elif ra.is_option(option_w):
        w_in = np.array([float(ra.find_option_arg(option_w))])
        w_init = sigma*w_in
    else:
        w_init = np.zeros(n)
    if ra.is_option(option_b):
        b_in = float(ra.find_option_arg(option_b))
        b_init = b_in+np.sum(w_init*mu/sigma)
    else:
        b_init = 0.0+np.sum(w_init*mu/sigma)
    logistic_regr = ra.is_option(option_logistic)
    regularization = ra.is_option(option_regularize)
    if ra.is_option(option_lambda):
        l = float(ra.find_option_arg(option_lambda))
    else:
        l = default_l
    print_loop = ra.is_option(option_print)
    plot_j = ra.is_option(option_plot)
    return (a, w_init, b_init, logistic_regr, regularization, l, print_loop, plot_j)

def make_plot(j_hist):
    k = [i for i in range(1,len(j_hist)+1)]
    plt.plot(k, j_hist)
    plt.title("Cost vs. iteration")
    plt.ylabel("J(w,b)")
    plt.xlabel("k")
    if len(k) > 10:
        xticks = range(1, len(k), 9)
        new_xticks = [10**i for i in range(len(xticks))]
        plt.xticks(xticks, new_xticks)
    plt.grid(True)
    plt.show()
