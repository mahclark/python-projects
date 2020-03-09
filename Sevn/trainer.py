from sevn import Game, ScoreBoard
from eta_go import EtaGo
import tensorflow as tf
import numpy as np
import os

class Trainer:

	def __init__(self, checkpoint_path=None):
		self.etaGo = EtaGo(checkpoint_path)

		self.train_x = np.array([])
		self.train_y = np.array([])
		self.test_x = np.array([])
		self.test_y = np.array([])

	def makeTrainingData(self, numGames=20):
		self.train_x, self.train_y = self._makeData(numGames)

	def makeTestData(self, numGames=5):
		self.test_x, self.test_y = self._makeData(numGames)

	def _makeData(self, numGames):
		x, y = np.array([]).reshape(0, 399), np.array([]).reshape(0, 1)
		for i in range(numGames):
			scoreBoard = ScoreBoard()
			game = Game(scoreBoard)
			data_x, data_y, state = self.etaGo.playGame(game, scoreBoard)
			x = np.concatenate((x, data_x), axis=0)
			y = np.concatenate((y, data_y), axis=0)

			#print("Played " + str(i + 1) + " / " + str(numGames))

		return (x, y)

	def saveTrainingData(self, path):
		np.savetxt(path + "_x.csv", self.train_x, delimiter=',')
		np.savetxt(path + "_y.csv", self.train_y, delimiter=',')

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

	trainer = Trainer()#"models/phase_" + "17" + "/cp.ckpt")#"shower_model/cp.ckpt")

	i = 0
	while True:
		print("Making training set", i)
		trainer.makeTrainingData(10)
		trainer.saveTrainingData("data/trainging_set_" + str(i))
		print("Made data")
		
		cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath="models/399_399_199_1/phase_" + str(i) + "/cp.ckpt",
	                                                 save_weights_only=True,
	                                                 verbose=1)

		trainer.train(10, cp_callback)
		i += 1


	# print("Making training data...")
	# eta.makeTrainingData(1000)

	# print("Making test data...")
	# eta.makeTestData(100)

	# print("Training...")
	# eta.train(20, cp_callback)

	# eta.evaluate()