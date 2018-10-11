from random import random
from math import exp
STEP = "step"
SIGN = "sign"
SIGMOID = "sigmoid"
LIN = "lienar"

class Perceptron:
    """
    Perceptron class used to implement an Artificial Neural Network
    """

    """
    Initializer
    
    :param t: Threshold value that is set to 0.2 in our given assignment
    """
    def __init__(self, t):
        self.weights = [random() - 0.5 for _ in range(2)]
        self.threshold = t
        self.outPut = []
        self.learningRate = 0.1
        self.hyperPlane = []

    """
    Runs the Perceptron through one epoch
        1. Initialize
        2. Activate by applying inputs
        3. Train the weights
        4. Iterate until convergence
        
    :param inputs: Cosists f x1 and x2 e.g. [[0,0,1,1], [0,1,0,1]]
    :param desired_output: What we want the input to be classified to
    :return: Returns the p'th epochs hyperplane 
    """
    def one_epoch(self, inputs, desired_output):
        hyperPlane = []
        for i in range(len(inputs[0])):
            temp = sum(inputs[x][i]*self.weights[x] for x in range(len(inputs)))
            hyperPlane.append(hard_limiter(temp))
            error = desired_output[i] - hyperPlane[i]

            # Lets train some weights
            for j in range(len(inputs)):
                self.weights[j] = self.weights[j-1] + self.weight_correction(inputs[j-1], error)

        self.hyperPlane = hyperPlane
        return hyperPlane


    """
    :param x: Input value for x in iteration p
    :param error: Is defined as (desired_output - actual_output)
    :return: correction for the Perceptron's weights
    """
    def weight_correction(self, x, error):
        return self.learningRate * x * error



"""
Activation functions of a neuron

:param net_input: Takes in an X
:return: Returns 0, -1, +1 or X, conditionally
"""
def hard_limiter(net_input, case=STEP):
    if case == STEP: return 1 if net_input >= 0 else 0
    elif case == SIGN: return 1 if net_input>= 0 else -1
    elif case == SIGMOID: return 1/(1 + exp(net_input))
    return net_input



"""
Main function to test methods
"""
def main():
    input_list = [[0, 0, 1, 1], [0, 1, 0, 1]]
    desired_and = [0, 0, 0, 1]
    desired_or = [0, 1, 1, 1]

    for _ in  range(100):
        p = Perceptron(0.2)
        print(p.weights)


if __name__ == '__main__':
    main()