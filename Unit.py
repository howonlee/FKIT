import pygame
import numpy
from pygame.sprite import Sprite
from random import randint, choice
from vec2d import *

FLOW_FACTOR = 0.01 #how much we're affected by flow
UNITTYPES = [{"img" : "triship.png"},
			 {"img" : "quadship.png"},
			 {"img" : "quintship.png"},
			 {"img" : "sextship.png"}]

class Unit(Sprite):
	def __init__(self, screen, unitType, initPosition, initDirection, speed):
		Sprite.__init__(self)
		self.screen = screen
		self.speed = speed
		self.pos = vec2d(initPosition)
		self.direction = vec2d(initDirection).normalized()
		self.base_image = pygame.image.load(UNITTYPES[unitType]["img"]).convert_alpha()
		self.image = self.base_image
		self.size = self.image.get_size()
		self.flow = vec2d(0, 0)

	def update(self, time_passed, flowMat):
		"""The unit owns the flow calculations"""
		self._change_direction(time_passed)
		self.image = pygame.transform.rotate(self.base_image, -self.direction.angle)
		self.size = self.image.get_size()
		displacement = vec2d(
				self.direction.x * self.speed * time_passed,
				self.direction.y * self.speed * time_passed)
		displacement += (self.flow * FLOW_FACTOR)
		self.pos += displacement
		self.pos[0] = int(self.pos[0])
		self.pos[1] = int(self.pos[1])
		self.flow += numpy.sum(numpy.sum(flowMat, axis=0), axis=1)
		print self.flow

		self.image_w, self.image_h = self.image.get_size()
		bounds_rect = self.screen.get_rect().inflate(
							-self.image_w, -self.image_h)
		if self.pos.x < bounds_rect.left:
			self.pos.x = bounds_rect.left
			self.direction.x *= -1
		elif self.pos.x > bounds_rect.right:
			self.pos.x = bounds_rect.right
			self.direction.x *= -1
		elif self.pos.y < bounds_rect.top:
			self.pos.y = bounds_rect.top
			self.direction.y *= -1
		elif self.pos.y > bounds_rect.bottom:
			self.pos.y = bounds_rect.bottom
			self.direction.y *= -1

	def blitme(self):
		draw_pos = self.image.get_rect().move(
				self.pos.x - self.image_w / 2,
				self.pos.y - self.image_h / 2)
		self.screen.blit(self.image, draw_pos)

	#private
	_counter = 0

	def _change_direction(self, time_passed):
		self._counter += time_passed
		if self._counter > randint(1600, 1750):
			self.direction.rotate(randint(-45, 45))
			self._counter = 0
