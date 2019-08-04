import numpy as np

def initialise_parameters(layers, randomWeight):
	parameters = {} #contains weights and biases
	for i in range(1, len(layers)):
		parameters['W' + str(i)] = randomWeight * np.random.randn(layers[i], layers[i - 1])
		parameters['b' + str(i)] = np.zeros((layers[i], 1))
	return parameters

def sigmoid(z):
	return 1/(1 + np.exp(-z))

def dsigmoid(z):
	return np.exp(-z)/np.square(1 + np.exp(-z))

def relu(z, deriv = False):
    if(deriv):  
        return z>0
    else:
        return np.multiply(z, z>0)

def forward(X, parameters):
	cache = {} #contains activation values for each neuron
	L = len(parameters)//2
	cache["A0"] = X

	for i in range(1, L):
		cache['Z' + str(i)] = np.dot(parameters['W' + str(i)], cache['A' + str(i-1)]) + parameters['b' + str(i)]
		cache['A' + str(i)] = sigmoid(cache['Z' + str(i)])

	#final layer
	cache['Z' + str(L)] = np.dot(parameters['W' + str(L)], cache['A' + str(L-1)]) + parameters['b' + str(L)]
	cache['A' + str(L)] = cache['Z' + str(L)]
	return cache

#AL is last layer activations
def cost_function(AL, Y):
	m = Y.shape[1]
	cost = np.sum(np.square(AL - Y))/m
	return cost

def backpropagation(cache, Y, parameters):
	L = len(parameters)//2
	m = Y.shape[1]
	grads = {}

	#final layer
	grads['dZ' + str(L)] = 2*(cache['A' + str(L)] - Y)
	grads['dW' + str(L)] = np.dot(grads['dZ' + str(L)], cache['A' + str(L-1)].T)/m
	grads['db' + str(L)] = np.sum(grads['dZ' + str(L)], axis=1, keepdims=True)/m

	for i in range(L-1, 0, -1):
		grads['dA' + str(i)] = np.dot(parameters['W' + str(i+1)].T, grads['dZ' + str(i+1)])
		grads['dZ' + str(i)] = np.multiply(grads['dA' + str(i)], dsigmoid(cache['Z' + str(i)]))
		grads['dW' + str(i)] = np.dot(grads['dZ' + str(i)], cache['A' + str(i-1)].T)/m
		grads['db' + str(i)] = np.sum(grads['dZ' + str(i)], axis=1, keepdims=True)/m
	return grads

def train(X_train, Y_train, epochs, layers, learning_rate, randomWeight):
	train_costs = []

	parameters = initialise_parameters(layers, randomWeight)
	L = len(layers) - 1

	for epoch in range(epochs):
		cache = forward(X_train, parameters)
		cost = cost_function(cache["A" + str(L)],Y_train)
		grads = backpropagation(cache, Y_train, parameters)

		for i in range(1, L+1):
			parameters['W' + str(i)] -= learning_rate * grads['dW' + str(i)]
			parameters['b' + str(i)] -= learning_rate * grads['db' + str(i)]

		train_costs.append(cost)
		if epoch%(epochs//10) == 0 or epoch == 0:
			print("Cost after epoch " + str(epoch) + ": " + str(cost))
	print("Training complete!")
	return parameters, train_costs

def evaluate_model(train_costs,parameters,X_train, Y_train, X_test, Y_test):
    L = len(parameters)//2
    
    train_cache = forward(X_train,parameters)
    train_AL = train_cache["A" + str(L)]
    
    print()
    print("The train set MSE is: " + str(cost_function(train_AL,Y_train)))
        
    test_cache = forward(X_test,parameters)
    test_AL = test_cache["A" + str(L)]
    
    print("The test set MSE is: " + str(cost_function(test_AL,Y_test)))
    print()

# print("X Shape:", X_train.shape)
# print("Y Shape:", Y_train.shape)
# print()


# num_epochs = 20000 #number of passes through the training set
# layers_units = [X.shape[0], 10, y.shape[0]] #layer 0 is the input layer - each value in list = number of nodes in that layer
# print("Layer 1:", X.shape[0])
# learning_rate = 1e-1 #size of our step

# print("No. of training examples:", X_train.shape[1])
# print("No. of test examples:", X_test.shape[1])
# print()

# parameters, train_costs = train(X_train, Y_train, num_epochs, layers_units, learning_rate)
# # evaluate_model(train_costs, parameters, X_train, Y_train, X_test, Y_test)