import parseText
from sklearn.neural_network import MLPRegressor
import numpy as np



#speeds, xs, ys, zs, key_inputs = parseText.getData()

def get_model(path):
	distCenter, headings, steers = parseText.getData(path)
	X=[]
	for i in range(len(distCenter)):
		X.append([distCenter[i], headings[i]])
	X = np.asarray(X)
	y = np.asarray(steers)

	return X,y
