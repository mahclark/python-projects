from sevn import Game, ScoreBoard
from eta_go import EtaGo
import tensorflow as tf
import numpy as np
import os

class Trainer:

	def __init__(self, checkpoint_path=None):
		self.etaGo = EtaGo(checkpoint_path)

		self.train_x = np.array([]).reshape(0,self.etaGo.inputSize)#18,7,7)
		self.train_y = np.array([]).reshape(0,1)#,1)
		self.test_x = np.array([]).reshape(0,self.etaGo.inputSize)#,18,7,7)
		self.test_y = np.array([]).reshape(0,1)#,1)

	def makeTrainingData(self, numGames=20, verbose=False):
		self.train_x, self.train_y = self._makeData(numGames, verbose)

	def makeTestData(self, numGames=5, verbose=False):
		self.test_x, self.test_y = self._makeData(numGames, verbose)

	def _makeData(self, numGames, verbose):
		x, y = np.array([]).reshape(0,self.etaGo.inputSize), np.array([]).reshape(0, 1)
		for i in range(numGames):
			scoreBoard = ScoreBoard()
			game = Game(scoreBoard)
			data_x, data_y, state = self.etaGo.playGame(game, scoreBoard)
			x = np.concatenate((x, data_x), axis=0)
			y = np.concatenate((y, data_y), axis=0)

			milestone = int(10*i/numGames)*10
			lastMilestone = int(10*(i - 1)/numGames)*10
			if verbose and milestone != lastMilestone:
				print(str(milestone) + "%")
				#print("Played " + str(i + 1) + " / " + str(numGames))

		return (x, y)

	def saveTrainingData(self, path):
		np.savetxt(path + "_x.csv", self.train_x, delimiter=',')
		np.savetxt(path + "_y.csv", self.train_y, delimiter=',')

	def loadTrainingData(self, path, lower, upper):
		for i in range(lower, upper + 1):
			x = np.loadtxt(open(path + str(i) + "_x.csv", "rb"), delimiter=",")
			y = np.loadtxt(open(path + str(i) + "_y.csv", "rb"), delimiter=",")
			self.train_x = np.concatenate((self.train_x, x), axis=0)
			self.train_y = np.concatenate((self.train_y, y.reshape(y.shape[0], 1)), axis=0)

	def train(self, epochs=5, callback=None):
		# predictions = self.model(self.test_x[:10]).numpy()
		# print(predictions.flatten())

		if callback == None:
			callbacks = []
		else:
			callbacks = [callback]

		self.etaGo.model.fit(self.train_x, self.train_y, epochs=epochs, callbacks=callbacks)

	def evaluate(self):
		self.etaGo.model.evaluate(self.test_x,  self.test_y, verbose=2)

		# predictions = self.model(self.test_x[:10]).numpy()
		# print(predictions.flatten())

if __name__ == "__main__":

	trainer = Trainer("models/410_403_201_1/phase_0/cp.ckpt")

	trainer.loadTrainingData("data/410/trainging_set_", 0, 7)
	cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath="models/410_403_201_1/phase_" + "0" + "/cp.ckpt",
	                                                 save_weights_only=True,
	                                                 verbose=1)

	trainer.train(5, cp_callback)
	exit()

	i = 0
	while True:
		print("Making training set", i)
		trainer.makeTrainingData(10, verbose=True)
		trainer.saveTrainingData("data/410/trainging_set_" + str(i))
		
		cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath="models/410_403_201_1/phase_" + str(i) + "/cp.ckpt",
	                                                 save_weights_only=True,
	                                                 verbose=1)

		#trainer.train(5, cp_callback)
		i += 1