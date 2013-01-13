import pygame
from pygame.sprite import Sprite
from vec2d import *

class Star(Sprite):
	def __init__(self, screen, pos, image):
		Sprite.__init__(self)
		self.screen = screen
		self.pos = vec2d(pos)
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = pygame.Rect(pos, (self.image.get_width(), self.image.get_height()))

	def blitme(self):
		self.screen.blit(self.image, self.pos)

