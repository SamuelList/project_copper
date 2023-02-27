import pygame, sys
from settings import *
from debug import debug
from level import Level

# this is a work in progress

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
		self.clock = pygame.time.Clock()
		
		self.level = Level()

		# change title
		pygame.display.set_caption("Scrappy")
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.screen.fill('black')
			self.level.run()
			# debug('hello world')
			
			# display FPS in the top right corner
			debug(int(self.clock.get_fps()), 10, WIDTH - 50)

			
			# update the display
			pygame.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	game = Game()
	game.run()