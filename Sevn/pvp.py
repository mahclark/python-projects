import pygame
import time
from sevn import Game, ScoreBoard, makeBackground
from Vec2 import Vec2

if __name__ == "__main__":
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
	game = Game(scoreBoard, boardSurf)
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
		clock.tick(60)

	pygame.quit()
