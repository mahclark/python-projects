import time
import pygame
from Vec2 import Vec2
from sevn import Game, ScoreBoard, makeBackground
import tensorflow as tf
import numpy as np

def subsets(s):
	sets = []
	for i in range(1, 1 << len(s)):
		subset = [s[bit] for bit in range(len(s)) if (i & (1 << bit) > 0)]
		sets.append(subset)
	return sets

class EtaGo:

	def __init__(self, checkpoint_path=None):
		self.model = tf.keras.models.Sequential([
			tf.keras.layers.Conv2D(64, (3,3), input_shape=(7,7,18)), # 7 tile states + 7 scores + 4 flags = 18
			tf.keras.layers.MaxPooling2D(2,2),
			tf.keras.layers.Flatten(),
			tf.keras.layers.Dense(256),
			tf.keras.layers.Dense(1, activation='sigmoid')
		])

		print(self.model.summary())

		loss_fn = tf.keras.losses.MeanSquaredLogarithmicError()

		self.model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['mean_absolute_error'])

		if checkpoint_path != None:
			self.model.load_weights(checkpoint_path)

		self.bestMoveSet = None

	def getWinProb(self, inputs):
		return self.model(inputs.reshape(1,7,7,18)).numpy()

	def _formatInputs(self, board, scores):
		inputs = np.array([]).reshape(0,7,7)

		for i in range(7):
			inputs = np.concatenate((inputs, np.array([[[int(tile == i) for tile in row] for row in board]])), axis=0)

		for i in range(7):
			inputs = np.concatenate((inputs, np.ones((1,7,7))*scores[i]), axis=0)

		winnableLeft = int(Game.winnable(board, scores, for_left_player=True))
		winnableRight = int(Game.winnable(board, scores, for_left_player=False))
		canWin = int(Game.canWinInOne(board, scores, for_left_player=True))
		hasWon = int(Game.hasWon(board, scores, for_left_player=False))

		inputs = np.concatenate((inputs, np.ones((1,7,7))*winnableLeft), axis=0)
		inputs = np.concatenate((inputs, np.ones((1,7,7))*winnableRight), axis=0)
		inputs = np.concatenate((inputs, np.ones((1,7,7))*canWin), axis=0)
		inputs = np.concatenate((inputs, np.ones((1,7,7))*hasWon), axis=0)

		return inputs

	def _decodeInputFlags(self, inputs):
		return (inputs[-4][0][0], inputs[-3][0][0], inputs[-2][0][0], inputs[-1][0][0])

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
				inputs = self._formatInputs(peekBoard, peekScores)
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
				inputs = self._formatInputs(peekBoard, peekScores)
				prob = self.getWinProb(inputs)
				if prob > bestProb:
					bestProb = prob
					bestMoveSet = moveSet
					moveResult = inputs

			data_x.append(moveResult)

			game.makeMoves(bestMoveSet)
			if not game.nextPlayer():
				break;

		data_size = len(data_x)
		for i in range(data_size):
			leftCanWin, rightCanWin, leftCanWinInOne, hasWon = self._decodeInputFlags(data_x[i])
			#left player is always opponent, who is about make a move
			if hasWon or not leftCanWin:
				data_y.append([1.0])
			elif leftCanWinInOne or not rightCanWin:
				data_y.append([0.0])
			else:
				data_y.append([0.5 + (2*((i + game.state)%2) - 1)*0.5*(i + 1)/data_size])

		return (np.array(data_x), np.array(data_y), game.state)

if __name__ == "__main__":
	pygame.init()
	xSize, ySize = 700, 700
	screen = pygame.display.set_mode((xSize, ySize))
	pygame.display.set_caption("Sevn")

	background = pygame.Surface(screen.get_size())
	makeBackground(background,
		(178, 165, 201),#(222, 213, 155),#(178, 209, 214),
		(219, 82, 61)#(159, 136, 179)
	)

	scoreSurf = pygame.Surface((400, 200), pygame.SRCALPHA, 32)
	scoreBoard = ScoreBoard(scoreSurf, "Player", "EtaGo")
	scorePos = Vec2(xSize/2 - scoreSurf.get_size()[0]/2, 40)

	boardSurf = pygame.Surface((400, 400), pygame.SRCALPHA, 32)
	game = Game(scoreBoard, boardSurf)
	boardPos = Vec2(xSize/2 - boardSurf.get_size()[0]/2, 250)

	etaGo = EtaGo("models/conv18_64_256_1/phase_8/cp.ckpt")

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
					if mask.get_at(relClick.toInts()) and scoreBoard.player1:
						game.click(relClick)
				except IndexError:
					pass

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					game.nextPlayer()	

		if frameCount > 60*60*10:
			done = True

		game.draw()
		scoreBoard.draw()

		screen.blit(background, (0, 0))
		screen.blit(scoreSurf, scorePos.toInts())
		screen.blit(boardSurf, boardPos.toInts())

		pygame.display.flip()

		if game.state == 0 and not scoreBoard.player1 and frameCount % 60 == 0:
			etaGo.makeMove(game, scoreBoard)

		clock.tick(60)

	pygame.quit()