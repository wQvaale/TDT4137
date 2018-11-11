from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules.tanhlayer import TanhLayer
from pybrain.supervised.trainers.backprop import BackpropTrainer

# Run:
# python2 feed_forward_neural_network.py X,
# where X is the desired amount of hidden nodes
from sys import argv
hidden = int(argv[1]) # X

# Expects one dimensional input and target output
ds = SupervisedDataSet(1, 1)
for x in range(1,9):
    ds.addSample(x, x)

# 1 input, X hidden, 1 output
network = buildNetwork(1,hidden,1, hiddenclass=TanhLayer)

# Init BackpropTrainer
trainer = BackpropTrainer(network, dataset=ds)

# Train until convergence
trainer.trainUntilConvergence(verbose=False, validationData=0.15, maxEpochs=1000, continueEpochs=10)


# Activating the network on different integers such as the inputs in the data-set
print("// Hidden nodes: {}".format(hidden))
for x in range(1, 9):
    print("{} --> {}".format(x, network.activate([x])[0]))

# Activating with decimal inputs outside of dataset
print("\nDecimal input outside dataset:")
for x in range(100, 109):
    print("{} --> {}".format(x, network.activate([x * 0.1])[0]))

# Activating with negative numbers outside of data-set
print("\nNegative input:")
for x in range(1, 9):
    print("{} --> {}".format(x, network.activate([x * -1])[0]))

# Activating with numbers outside of [1,8]
print("\nOutside range of [1,8]:")
for x in range(18, 27):
    print("{} --> {}".format(x, network.activate([x])[0]))