import copy, numpy as np
np.random.seed(0)

# Compute sigmoid nonlinearity
def sigmoid(x):
    return 1/(1+np.exp(-x))


# Convert output of sigmoid func to derivate
def sigmoid_output_to_derivative(out):
    return out*(1-out)

# Training dataset
int2bin = {}
binary_dim = 8

largest_number = pow(2, binary_dim)
binary = np.unpackbits(
    np.array([range(largest_number)], dtype=np.uint8).T, axis=1)
for i in range(largest_number):
    int2bin[i] = binary[i]


# Input variables
alpha = 0.1
input_dim = 2
hidden_dim = 16
output_dim = 1


# Init neural network weights
synapse_0 = 2*np.random.random((input_dim, hidden_dim)) - 1
synapse_1 = 2*np.random.random((hidden_dim, output_dim)) - 1
synapse_h = 2*np.random.random((hidden_dim, hidden_dim)) - 1

synapse_0_update = np.zeros_like(synapse_0)
synapse_1_update = np.zeros_like(synapse_1)
synapse_h_update = np.zeros_like(synapse_h)


# Training logic
for j in range(10000):

    # Generate a simple addition problem (a + b = c)
    a_int = np.random.randint(largest_number/2) # int version
    a = int2bin[a_int] # binary

    b_int = np.random.randint(largest_number/2) # int version
    b  = int2bin[b_int] # binary

    # True answer
    c_int = a_int + b_int
    c = int2bin[c_int]

    # Storage for our best guess
    d = np.zeros_like(c)

    overallError = 0

    layer_2_deltas = list()
    layer_1_values = list()
    layer_1_values.append(np.zeros(hidden_dim))


    # moving along the positions in the binary encoding
    for pos in range(binary_dim):

        x = np.array([[a[binary_dim - pos - 1], b[binary_dim - pos - 1]]])
        y = np.array([[c[binary_dim - pos - 1]]]).T

        # Hidden layer
        layer_1 = sigmoid(np.dot(x, synapse_0) + np.dot(layer_1_values[-1], synapse_h))

        # Output
        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # Error
        layer_2_error = y - layer_2
        layer_2_deltas.append((layer_2_error)*sigmoid_output_to_derivative(layer_2))
        overallError += np.abs(layer_2_error[0])

        # decode estimate so we can print it out
        d[binary_dim - pos - 1] = np.round(layer_2[0][0])

        # store hidden layer so we can use it in the next timestep
        layer_1_values.append(copy.deepcopy(layer_1))


    # Init future layer
    future_layer_1_delta = np.zeros(hidden_dim)

    for pos in range(binary_dim):

        x = np.array([[a[pos],b[pos]]])
        layer_1 = layer_1_values[-pos-1]
        prev_layer_1 = layer_1_values[-pos-2]

        # Error @ output layer
        layer_2_delta = layer_2_deltas[-pos-1]

        # Error @ hidden layer
        layer_1_delta = (future_layer_1_delta.dot(synapse_h.T) + layer_2_delta.dot(
            synapse_1.T)) * sigmoid_output_to_derivative(layer_1)

        # Update weights
        synapse_1_update += np.atleast_2d(layer_1).T.dot(layer_2_delta)
        synapse_h_update += np.atleast_2d(prev_layer_1).T.dot(layer_1_delta)
        synapse_0_update += x.T.dot(layer_1_delta)

        # Update future layer
        future_layer_1_delta = layer_1_delta

    synapse_0 += synapse_0_update * alpha
    synapse_1 += synapse_1_update * alpha
    synapse_h += synapse_h_update * alpha

    synapse_0_update *= 0
    synapse_1_update *= 0
    synapse_h_update *= 0

    # print out progress
    if (j % 1000 == 0):
        print("Error:" + str(overallError))
        print("Pred:" + str(d))
        print("True:" + str(c))
        out = 0
        for index, x in enumerate(reversed(d)):
            out += x * pow(2, index)
        print(str(a_int) + " + " + str(b_int) + " = " + str(out))

        # Check if correct prediction
        check = np.array_equal(d,c)
        if check:
            print("S U C C E S S!!!")
        print("----------------------")