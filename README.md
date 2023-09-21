# gradient_descent
Gradient descent for multiple linear and logistic regression with feature scaling and regularization.
Usage:
    ./gradient_descent.py <X_file> <y_file> -bin -rate [alpha] (-wfile [w_file] OR -w [w_value]) -b [b_value] -logistic -regularize -lambda [lambda] -print -plot -help
Mandatory arguments:
    <X_file>    path to the file with feature data
    <y_file>    path to the file with target data
Options:
    -bin        use when files are binary; by default they are assumed to be text files
    -rate       input learning rate [alpha]; by default it is", default_a
    -wfile      input path to the file [w_file] with starting values of w parameters -- in the case when there is more than one feature; by default they are set to zeros
    -w          input starting value of w parameter [w_value] -- in the case when there is only one feature; by default it is set to zero
    -b          input starting value of b parameter [b_value]; by default it is set to zero
    -logistic   calculates logistic gradient descent instead of linear
    -regularize perform parameters regularization
    -lambda     input regularization parameter [lambda]; by default it is default_l
    -print      prints results of the steps in gradient descent
    -plot       plots the cost function versus iterations
    -help       prints this help
Version 1.4, 2023-09-11
