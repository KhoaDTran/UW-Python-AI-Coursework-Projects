'''binary_perceptron.py
One of the starter files for use in CSE 415, Winter 2021
Assignment 6.

Version of Feb. 18, 2021

'''


def student_name():
    return "Khoa Tran"  # Replace with your own name.


def classify(weights, x_vector):
    '''Assume weights = [w_0, w_1, ..., w_{n-1}, biasweight]
       Assume x_vector = [x_0, x_1, ..., x_{n-1}]
         Note that y (correct class) is not part of the x_vector.
       Return +1 if the current weights classify this as a Positive,
          or  -1 if it seems to be a Negative.
    '''
    # Replace this code with your own:
    result = 0
    for i in range(len(weights) - 1):
        result += weights[i] * x_vector[i]
    result += weights[len(weights) - 1]
    if result > 0:
        return 1
    else:
        return -1


def train_with_one_example(weights, x_vector, y, alpha):
    '''Assume weights are as in the above function classify.
       Also, x_vector is as above.
       Here y should be +1 if x_vector represents a positive example,
        and -1 if it represents a negative example.
       Learning rate is specified by alpha.
    '''
    temp = classify(weights, x_vector)
    mult = []
    checker = False
    if temp < y:
        weights[len(weights) - 1] = weights[len(weights) - 1] + alpha
        for item in x_vector:
            mult.append(item * alpha)
        for i in range(len(weights) - 1):
            weights[i] = weights[i] + mult[i]
        checker = True
    elif temp > y:
        weights[len(weights) - 1] = weights[len(weights) - 1] - alpha
        for j in range(len(x_vector)):
            mult.append(x_vector[j] * alpha)
        for i in range(len(weights) - 1):
            weights[i] = weights[i] - mult[i]
        checker = True
    else:
        checker = False
    return (weights, checker)


# From here on use globals that can be easily imported into other modules.
WEIGHTS = [0, 0, 0]
ALPHA = 0.5


def train_for_an_epoch(training_data, reporting=True):
    '''Go through the given training examples once, in the order supplied,
    passing each one to train_with_one_example.
    Update the global WEIGHT vector and return the number of weight updates.
    (If zero, then training has converged.)
    '''
    global WEIGHTS, ALPHA
    changed_count = 0
    for item in training_data:
        y = item[len(item) - 1]
        x_vector = item[:len(item) - 1]
        weight, check = train_with_one_example(WEIGHTS, x_vector, y, ALPHA)
        WEIGHTS = weight
        if check:
            for item in WEIGHTS:
                if item != 0:
                    changed_count += 1
    return changed_count


TEST_DATA = [
    [-2, 7, +1],
    [1, 10, +1],
    [3, 2, -1],
    [5, -2, -1]]


def test():
    print("Starting test with 3 epochs.")
    for i in range(3):
        train_for_an_epoch(TEST_DATA)
    print(WEIGHTS)
    print("End of test.")


if __name__ == '__main__':
    test()
