from sevn import Game, ScoreBoard
from random import random

def subsets(s):
	sets = []
	for i in range(1, 1 << len(s)):
		subset = [s[bit] for bit in range(len(s)) if (i & (1 << bit) > 0)]
		sets.append(subset)
	return sets

class TreeNode:

	def __init__(self, etaGo, board, scores, takable, player1):
		self.etaGo = etaGo
		self.board = board
		self.scores = scores
		self.takable = takable
		self.player1 = player1
		self.player = 1 if player1 else 2
		self.children = []
		self.visited = False

		inputScores = self.scores
		if not self.player1: #flip if previous player is player 1
			inputScores = [-x for x in inputScores]

		inputs = etaGo.formatInputs(board, inputScores)
		self.winProb = etaGo.getWinProb(inputs)[0][0]
		# print(inputScores)
		# print("Eta says", self.winProb)
		#_, _, _, self.hasWon = etaGo.decodeInputFlags(inputs)
		self.hasWon = Game.hasWon(self.board, inputScores, for_left_player=True)
		self.hasLost = Game.hasWon(self.board, inputScores, for_left_player=False)
		# print(self.hasWon, self.hasLost, self.player)

	def makeChildren(self):
		if self.children != [] or self.hasWon or self.hasLost:
			return

		bestChildProb = -float("inf")

		for moveSet in self._getPossibleMoves(self.board, self.takable):
			childBoard, childScores, childTakable = self.applyMoveSet(moveSet, self.board, self.scores, self.player1, self.takable)
			child = TreeNode(self.etaGo, childBoard, childScores, childTakable, not self.player1)
			self.children.append((child, moveSet))

			if child.winProb > bestChildProb:
				bestChildProb = child.winProb
				self.bestChild = child

	def clearFlag(self):
		self.visited = False
		for child, _ in self.children:
			child.clearFlag()

	def evaluateGame(self, epsilon):
		retVisited = self.visited
		self.visited = True
		if self.hasWon:
			return (self.player, retVisited)
		if self.hasLost:
			return (2 if self.player1 else 1, retVisited)

		self.makeChildren()

		if random() > epsilon:
			return self.bestChild.evaluateGame(epsilon)

		probSum = 0
		for child, _ in self.children:
			probSum += child.winProb

		rand = random()*probSum
		accProb = 0
		for child, _ in self.children:
			accProb += child.winProb
			if accProb > rand:
				return child.evaluateGame(epsilon)

	def _getPossibleMoves(self, board, takable):
		takableColors = [[], [], [], [], [], [], []]
		for x, y in takable:
			if board[y][x] != -1:
				takableColors[board[y][x]].append((x, y))

		possibleMoves = []
		for takable in takableColors:
			for s in subsets(takable):
				possibleMoves.append(s)

		return possibleMoves

	def applyMoveSet(self, moveSet, board, scores, left_player_moved, takable):
		board, scores = self.copyBoard(board), self.copyScores(scores)
		newTakable = set()
		for pos in takable:
			newTakable.add(pos)

		for x, y in moveSet:
			assert board[y][x] != -1

			newTakable.remove((x, y))

			if left_player_moved:
				scores[board[y][x]] -= 1
			else:
				scores[board[y][x]] += 1

			board[y][x] = -1

		for x, y in moveSet:
			for cx, cy in [(x - 1, y), (x + 1, y), (x, y -1), (x, y + 1)]:
				if Game.checkTakable(board, cx, cy):
					newTakable.add((cx, cy))

		return (board, scores, newTakable)

	def copyBoard(self, board):
		return [[tile for tile in row] for row in board]

	def copyScores(self, scores):
		return [score for score in scores]


class MCTreeSearch:

	def __init__(self, etaGo, board, scores):
		self.etaGo = etaGo
		#self.root = TreeNode(etaGo, board, scores, {(0,0),(1,0)}, True)
		self.root = TreeNode(etaGo, board, scores, {(0,0),(0,6),(6,0),(6,6)}, True)
		self.root.makeChildren()

	def makeMove(self, moveSet):
		for child, childMoves in self.root.children:
			if sum([not move in childMoves for move in moveSet]) == 0 and len(moveSet) == len(childMoves):
				self.root = child
				return

		print(moveSet)
		print(self.root.children)
		print(self.root.board)
		raise Exception("Move set not found in children")


	def getWinProb(self, sampleSize=100, epsilon=0.5):
		uniqueSampleSize = 0
		winSum = 0

		for i in range(sampleSize):
			winner, visited = self.root.evaluateGame(epsilon)
			if not visited:
				uniqueSampleSize += 1
			if winner != self.root.player: #since we assume it's next player's go
				winSum += 1

		print("Unique sample size: " + str(uniqueSampleSize))
		print("Win prob", winSum/sampleSize)
		return winSum/sampleSize

if __name__ == "__main__":
	etaGo = EtaGo("models/410_403_201_1/phase_10/cp.ckpt", verbose=False)

	scoreBoard = ScoreBoard()
	board = Game(ScoreBoard).board
	scores = scoreBoard.scores

	mcts = MCTreeSearch(etaGo, board, scores)
	for _ in range(100):
		print("Win prob:", mcts.getWinProb())