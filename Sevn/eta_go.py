import time
import pygame
from Vec2 import Vec2
from sevn import Game, ScoreBoard, makeBackground
from mcts import MCTreeSearch
import tensorflow as tf
import numpy as np

def subsets(s):
	sets = []
	for i in range(1, 1 << len(s)):
		subset = [s[bit] for bit in range(len(s)) if (i & (1 << bit) > 0)]
		sets.append(subset)
	return sets

class EtaGo:

	def __init__(self, checkpoint_path=None, verbose=True):
		self.inputSize = 410
		self.model = tf.keras.models.Sequential([
			tf.keras.layers.Dense(self.inputSize, input_shape=(self.inputSize,)),
			tf.keras.layers.Dense(403),
			tf.keras.layers.Dense(201),
			tf.keras.layers.Dense(1, activation='sigmoid')
		])

		if verbose:
			print(self.model.summary())

		loss_fn = tf.keras.losses.MeanSquaredLogarithmicError()

		self.model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['mean_absolute_error'])

		if checkpoint_path != None:
			self.model.load_weights(checkpoint_path)

		self.bestMoveSet = None

	def getWinProb(self, inputs):
		return self.model(inputs.reshape(1,self.inputSize)).numpy()

	def formatInputs(self, board, scores):
		inputs = np.array([])

		for row in board:
			for tile in row:
				for i in range(-1, 7):
					inputs = np.append(inputs, float(tile == i))

		for score in scores:
			inputs = np.append(inputs,score/7)

		takable = [0,0,0,0,0,0,0]
		for y in range(7):
			for x in range(7):
				if Game.checkTakable(board, x, y):
					takable[board[y][x]] += 1

		for x in takable:
			inputs = np.append(inputs, x)

		inputs = np.append(inputs, int(Game.winnable(board, scores, for_left_player=True)))
		inputs = np.append(inputs, int(Game.winnable(board, scores, for_left_player=False)))
		inputs = np.append(inputs, int(Game.canWinInOne(board, scores, for_left_player=True)))
		inputs = np.append(inputs, int(Game.hasWon(board, scores, for_left_player=False)))

		return inputs

	def decodeInputFlags(self, inputs):
		return (inputs[-4], inputs[-3], inputs[-2], inputs[-1])

	def makeMove(self, game, scoreBoard):
		if self.bestMoveSet == None:
			takableColors = [[], [], [], [], [], [], []]
			for x, y in game.takable:
				if game.board[y][x] != -1:
					takableColors[game.board[y][x]].append((x, y))

			possibleMoves = []
			for takable in takableColors:
				for s in subsets(takable):
					possibleMoves.append(s)

			bestProb = -float("inf")
			moveResult = None
			for moveSet in possibleMoves:
				peekBoard, peekScores = game.peek(moveSet)
				if scoreBoard.player1:
					peekScores = [-x for x in peekScores]
				inputs = self.formatInputs(peekBoard, peekScores)
				prob = self.getWinProb(inputs)
				if prob > bestProb:
					bestProb = prob
					self.bestMoveSet = moveSet
			print("AI win probability:", int(bestProb*100*10)/10)
			return

		if len(self.bestMoveSet) == 0:
			self.bestMoveSet = None
			game.nextPlayer()
			return

		cx, cy = self.bestMoveSet.pop()
		game.makeMove(cx, cy)

	def playGame(self, game, scoreBoard):

		data_x = []
		data_y = []

		mcts = MCTreeSearch(self, game.board, scoreBoard.scores)

		while True:#board.state == 0:
			takableColors = [[], [], [], [], [], [], []]
			for x, y in game.takable:
				if game.board[y][x] != -1:
					takableColors[game.board[y][x]].append((x, y))

			possibleMoves = []
			for takable in takableColors:
				for s in subsets(takable):
					possibleMoves.append(s)

			bestProb = -float("inf")
			bestMoveSet = None
			moveResult = None
			for moveSet in possibleMoves:
				peekBoard, peekScores = game.peek(moveSet)
				if scoreBoard.player1: #flip scores so AI always wants positives scores
					peekScores = [-x for x in peekScores]
				inputs = self.formatInputs(peekBoard, peekScores)
				prob = self.getWinProb(inputs)
				if prob > bestProb:
					bestProb = prob
					bestMoveSet = moveSet
					moveResult = inputs

			data_x.append(moveResult)

			leftCanWin, rightCanWin, leftCanWinInOne, hasWon = self.decodeInputFlags(moveResult)
			if hasWon or not leftCanWin:
				data_y.append([1.0])
			elif leftCanWinInOne or not rightCanWin:
				data_y.append([0.0])
			else:
				mcts.makeMove(bestMoveSet)
				data_y.append([mcts.getWinProb()])

			game.makeMoves(bestMoveSet)
			if not game.nextPlayer():
				break;

		# data_size = len(data_x)
		# for i in range(data_size):
		# 	leftCanWin, rightCanWin, leftCanWinInOne, hasWon = self.decodeInputFlags(data_x[i])
		# 	#left player is always opponent, who is about make a move
		# 	if hasWon or not leftCanWin:
		# 		data_y.append([1.0])
		# 	elif leftCanWinInOne or not rightCanWin:
		# 		data_y.append([0.0])
		# 	else:
		# 		data_y.append([0.5 + (2*((i + game.state)%2) - 1)*0.5*(i + 1)/data_size])

		return (np.array(data_x), np.array(data_y), game.state)

if __name__ == "__main__":
	pygame.init()
	xSize, ySize = 700, 700
	screen = pygame.display.set_mode((xSize, ySize))
	pygame.display.set_caption("Sevn")

	etaGoFirst = False

	background = pygame.Surface(screen.get_size())
	makeBackground(background,
		(178, 165, 201),#(222, 213, 155),#(178, 209, 214),
		(219, 82, 61)#(159, 136, 179)
	)

	scoreSurf = pygame.Surface((400, 200), pygame.SRCALPHA, 32)
	if etaGoFirst:
		scoreBoard = ScoreBoard(scoreSurf, "EtaGo", "Player")
	else:
		scoreBoard = ScoreBoard(scoreSurf, "Player", "EtaGo")

	scorePos = Vec2(xSize/2 - scoreSurf.get_size()[0]/2, 40)

	boardSurf = pygame.Surface((400, 400), pygame.SRCALPHA, 32)
	game = Game(scoreBoard, boardSurf)
	boardPos = Vec2(xSize/2 - boardSurf.get_size()[0]/2, 250)

	etaGo = EtaGo("models/410_403_201_1/phase_0/cp.ckpt")

	# print(np.array(etaGo.model.get_layer(index=0).get_weights()[0][0]))
	# exit()

	clock = pygame.time.Clock()
	frameCount = 0
	done = False
	mouseHold = False
	while not done:
		frameCount += 1
		keys = pygame.key.get_pressed()
		mx, my = pygame.mouse.get_pos()

		userDone = False
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseHold = True

			if event.type == pygame.MOUSEBUTTONUP:
				mouseHold = False

				mask = pygame.mask.from_surface(boardSurf)
				relClick = Vec2(mx, my).addVec(boardPos.mult(-1))
				try: 
					if mask.get_at(relClick.toInts()) and scoreBoard.player1 != etaGoFirst:
						game.click(relClick)
				except IndexError:
					pass

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					game.nextPlayer()

		game.draw()
		scoreBoard.draw()

		screen.blit(background, (0, 0))
		screen.blit(scoreSurf, scorePos.toInts())
		screen.blit(boardSurf, boardPos.toInts())

		pygame.display.flip()

		if game.state == 0 and scoreBoard.player1 == etaGoFirst and frameCount % 60 == 0:
			etaGo.makeMove(game, scoreBoard)

		clock.tick(60)

	pygame.quit()