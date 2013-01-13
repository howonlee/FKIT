import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((640, 640))
pygame.display.set_caption("FKIT")

ballObj = pygame.image.load('ball.png')
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
mousex, mousey = 0, 0
msg = "Hello World"
fontObj = pygame.font.Font(None, 32)

while True:
	windowSurfaceObj.fill(BLACK)
	windowSurfaceObj.blit(ballObj, (mousex, mousey))
	msgSurfaceObj = fontObj.render(msg, False, BLUE)
	msgRectobj = msgSurfaceObj.get_rect()
	msgRectobj.topleft = (10, 20)
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mousex, mousey = event.pos
		elif event.type == MOUSEBUTTONDOWN:
			mousex, mousey = event.pos
			msg = "World, Hello"
		elif event.type == MOUSEBUTTONUP:
			mousex, mousey = event.pos
			msg = "Hello World"

	pygame.display.update()
	fpsClock.tick(60)

