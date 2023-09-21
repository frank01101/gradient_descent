# gradient_descent
This is an implementation of gradient descent for multiple linear and logistic regression with feature scaling and regularization. It utilizes NumPy arrays and its matrix/vector operations which improves performance significantly by parallel computations based on C loops instead of Python loops through elements. There is no fixed number of iterations---the loop finishes when the gradient of cost function is small enough (currently, set to 1e-10 for each component of the gradient vector for linear regression and 1e-5 for logistic regression; maximum number of iterations set to 1e+7). On request, it plots cost function versus algorithm steps in a custom scale of `steps in k*10**l`, where `k in {1,..., 9}` and `l in non-negative Integers`.

## Usage:
    ./gradient_descent.py <X_file> <y_file> -bin -rate [alpha] (-wfile [w_file] OR -w [w_value]) -b [b_value] -logistic -regularize -lambda [lambda] -print -plot -help

### Mandatory arguments:
    <X_file>    path to the file with feature data, whitespace separated;
    <y_file>    path to the file with target data, whitespace separated;

### Options:
    -bin        use when files are binary; by default they are assumed to be text files;
    -rate       input learning rate [alpha]; by default it is default_a;
    -wfile      input path to the file [w_file] with starting values of w parameters -- in the case when there is more than one feature; by default they are set to zeros;
    -w          input starting value of w parameter [w_value] -- in the case when there is only one feature; by default it is set to zero;
    -b          input starting value of b parameter [b_value]; by default it is set to zero;
    -logistic   calculates logistic gradient descent instead of linear;
    -regularize perform parameters regularization;
    -lambda     input regularization parameter [lambda]; by default it is default_l;
    -print      prints results of the steps in gradient descent;
    -plot       plots the cost function versus iterations;
    -help       prints this help;

Version 1.4, 2023-09-11
