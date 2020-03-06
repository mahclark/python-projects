import pygame
import time
import random
from math import ceil
from Vec2 import Vec2

colors = {
		0 : (252, 208, 86),
		1 : (235, 164, 171),
		2 : (130, 101, 86),
		3 : (122, 73, 138),
		4 : (245, 241, 208),
		5 : (71, 71, 69),
		6 : (159, 200, 207)
}

white = (240, 240, 240)

def makeBackground(surf, topColor, bottomColor):
	xSize, ySize = surf.get_size()
	for y in range(0, ySize):
		col = (
			topColor[0] + (bottomColor[0] - topColor[0])*y/ySize,
			topColor[1] + (bottomColor[1] - topColor[1])*y/ySize,
			topColor[2] + (bottomColor[2] - topColor[2])*y/ySize
			)
		pygame.draw.line(surf, col, (0, y), (xSize - 1, y))

class ScoreBoard:

	lineWidth = 1

	def __init__(self, surf):
		self.surf = surf
		self.xSize, self.ySize = surf.get_size()

		self.gridHeight = int(min(self.xSize*(3/5)*(7/15), self.ySize - 50))
		self.gridHeight += self.lineWidth - (self.gridHeight % 7)
		self.gridPos = Vec2((self.xSize - self.gridHeight*15/7)/2, 50)

		self.grid = pygame.Surface((int(self.gridHeight*15/7), self.gridHeight), pygame.SRCALPHA, 32)
		self.scores = [0, 0, 0, 0, 0, 0, 0]

		self.player1 = True
		self.currentColor = None
		self.state = 0
		self.taken = 0
		self.p1Score = 0
		self.p2Score = 0

		self.smallFont = pygame.font.SysFont("Bahnschrift", 20)
		self.bigFont = pygame.font.SysFont("Bahnschrift", 50)

	def draw(self):
		self.surf.fill((255,255,255,0))
		self.grid.fill((255,255,255,0))
		#self.surf.set_alpha(255)

		xCell = (self.grid.get_size()[0] - self.lineWidth)//15
		yCell = (self.grid.get_size()[1] - self.lineWidth)//7

		lineCol = (196, 187, 173)
		selectedCol = (242, 193, 44)

		for x in range(0, 16):
			pygame.draw.line(self.grid, lineCol, (x*xCell, 0), (x*xCell, 7*yCell), self.lineWidth)

		for y in range(0, 8):
			pygame.draw.line(self.grid, lineCol, (0, y*yCell), (7*xCell, y*yCell), self.lineWidth)
			pygame.draw.line(self.grid, lineCol, (8*xCell, y*yCell), (15*xCell, y*yCell), self.lineWidth)

		for i in range(0, 7):
			pygame.draw.rect(self.grid, white, ((self.scores[i] + 7)*xCell, i*yCell, xCell + self.lineWidth, yCell + self.lineWidth))
			pygame.draw.rect(self.grid, colors[i], ((self.scores[i] + 7)*xCell + self.lineWidth, i*yCell + self.lineWidth, xCell - self.lineWidth, yCell - self.lineWidth))

		self.surf.blit(self.grid, self.gridPos.toInts())

		pygame.draw.line(self.surf, selectedCol if self.player1 else lineCol, (10, 40), (self.gridPos.x + self.gridHeight - 1, 40), 2)
		pygame.draw.line(self.surf, lineCol if self.player1 else selectedCol, (self.gridPos.x + int(self.gridHeight*8/7), 40), (self.xSize - 10, 40), 2)

		p1Label = self.smallFont.render("Player 1", 1, selectedCol if self.player1 else lineCol)
		p2Label = self.smallFont.render("Player 2", 1, lineCol if self.player1 else selectedCol)

		score1Label = self.bigFont.render(str(self.p1Score), 1, white)
		score2Label = self.bigFont.render(str(self.p2Score), 1, white)

		self.surf.blit(p1Label, (10, 10))
		self.surf.blit(p2Label, (self.xSize - 83, 10))
		self.surf.blit(score1Label, (10, 50))
		self.surf.blit(score2Label, (self.xSize - 35, 50))

	def select(self, color):
		if self.state == 0 and self.currentColor in [None, color]:
			self.currentColor = color
			self.taken += 1
			self.scores[color] += 1 - 2*self.player1

			if self.scores[color] == -1 and self.player1:
				self.p1Score += 1
			elif self.scores[color] == 0 and self.player1:
				self.p2Score -= 1
			elif self.scores[color] == 1 and not self.player1:
				self.p2Score += 1
			elif self.scores[color] == 0 and not self.player1:
				self.p1Score -= 1

			if self.scores[color] in [-7, 7] or self.taken == 49:
				if self.scores[color] == 7:
					self.p1Score = 0
					self.p2Score = 7
				elif self.scores[color] == -7:
					self.p1Score = 7
					self.p2Score = 0

				self.state = 1 + (self.p2Score > self.p1Score)
			return True

		return False

	def nextPlayer(self):
		if self.state == 0 and self.currentColor != None:
			self.player1 = not self.player1
			self.currentColor = None

class Board:

	gridWidth = 5

	def __init__(self, surf, scoreBoard):
		self.surf = surf
		self.grid = pygame.Surface(surf.get_size(), pygame.SRCALPHA, 32)
		self.xSize, self.ySize = surf.get_size()
		self.xCell = (self.xSize - self.gridWidth)//7
		self.yCell = (self.ySize - self.gridWidth)//7
		self.scoreBoard = scoreBoard
		self.taken = set()
		self.takable = {(0, 0), (0, 6), (6, 0), (6, 6)}
		self.newTakable = set()
		self.state = 0
		self.fallOffset = {}

		self.bigFont = pygame.font.SysFont("Bahnschrift", 60)

		remaining = {
			0 : 7, 
			1 : 7, 
			2 : 7,
			3 : 7,
			4 : 7,
			5 : 7,
			6 : 7
		}

		self.board = []

		for y in range(0, 7):
			row = []
			for x in range(0, 7):
				choice = random.choice(list(remaining.keys()))
				row.append(choice)
				remaining[choice] -= 1
				if remaining[choice] == 0:
					del remaining[choice]
			self.board.append(row)

	def draw(self):
		self.surf.fill((255,255,255,0))
		self.grid.fill((255,255,255,0))

		for y in range(0, 7):
			for x in range(0, 7):
				if not (x, y) in self.taken:
					if (x, y) in self.takable:
						pygame.draw.rect(self.grid, (255,255,255), (
							x*self.xCell + ceil(self.gridWidth/2),
							y*self.yCell + ceil(self.gridWidth/2),
							self.xCell - ceil(self.gridWidth/2),
							self.yCell - ceil(self.gridWidth/2))
						)
						pygame.draw.rect(self.grid, colors[5], (
							x*self.xCell + self.gridWidth,
							y*self.yCell + self.gridWidth,
							self.xCell - self.gridWidth - self.gridWidth//2,
							self.yCell - self.gridWidth - self.gridWidth//2)
						)
						pygame.draw.rect(self.grid, colors[self.board[y][x]], (
							x*self.xCell + self.gridWidth + 1,
							y*self.yCell + self.gridWidth + 1,
							self.xCell - self.gridWidth - self.gridWidth//2 - 2,
							self.yCell - self.gridWidth - self.gridWidth//2 - 2)
						)
					else:
						pygame.draw.rect(self.grid, colors[self.board[y][x]], (
							x*self.xCell + self.gridWidth,
							y*self.yCell + self.gridWidth,
							self.xCell - self.gridWidth - self.gridWidth//2,
							self.yCell - self.gridWidth - self.gridWidth//2)
						)

		if self.state != 0:
			self.grid.set_alpha(self.grid.get_alpha()*0.9)
			winLabel = self.bigFont.render("Player " + str(self.state) + " wins!", 1, white)
			self.surf.blit(winLabel, (self.xSize/2 - 195, self.ySize/2 - 40))
		else:
			self.surf.blit(self.grid, (0,0))

	def nextPlayer(self):
		self.takable.update(self.newTakable)
		self.newTakable.clear()
		scoreBoard.nextPlayer()


	def click(self, pos):
		cx = int(pos.x/self.xCell)
		cy = int(pos.y/self.yCell)

		if self.state == 0 and (cx, cy) in self.takable and self.scoreBoard.select(self.board[cy][cx]):
			self.state = scoreBoard.state
			self.taken.add((cx, cy))
			self.takable.remove((cx, cy))

			for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]:
				if (self._checkTakable(nx, ny)):
					self.newTakable.add((nx, ny))

	def _inBounds(self, x, y):
		return not (x < 0 or x > 6 or y < 0 or y > 6)

	def _isEmpty(self, x, y):
		return (not self._inBounds(x, y)) or (x, y) in self.taken

	def _checkTakable(self, x, y):
		if not self._inBounds(x, y):
			return False

		count = 0
		check = 0
		if self._isEmpty(x - 1, y):
			count += 1
			check += 1

		if self._isEmpty(x, y + 1):
			count += 1

		if self._isEmpty(x + 1, y):
			count += 1
			check += 1

		if self._isEmpty(x, y - 1):
			count += 1

		if count > 1 and not (count == 2 and check % 2 == 0):
			return True

		return False

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
	scoreBoard = ScoreBoard(scoreSurf)
	scorePos = Vec2(xSize/2 - scoreSurf.get_size()[0]/2, 40)

	boardSurf = pygame.Surface((400, 400), pygame.SRCALPHA, 32)
	board = Board(boardSurf, scoreBoard)
	boardPos = Vec2(xSize/2 - boardSurf.get_size()[0]/2, 250)

	clock = pygame.time.Clock()
	frameCount = 0
	done = False
	mouseHold = False
	while not done:
		frameCount += 1
		keys = pygame.key.get_pressed()
		mx, my = pygame.mouse.get_pos()
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
					if mask.get_at(relClick.toInts()):
						board.click(relClick)
				except IndexError:
					pass

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					board.nextPlayer()

		if frameCount > 60*60*10:
			done = True

		board.draw()
		scoreBoard.draw()

		screen.blit(background, (0, 0))
		screen.blit(scoreSurf, scorePos.toInts())
		screen.blit(boardSurf, boardPos.toInts())

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
