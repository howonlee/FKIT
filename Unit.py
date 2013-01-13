import pygame
import numpy
from pygame.sprite import Sprite
from random import randint, choice
from vec2d import *

FLOW_FACTOR = 1 #how much we're affected by flow
ACC_FACTOR = 0.003 #how much we're affected by acceleration
DECEL_FACTOR = 0.7 #how much we go towards equilibrium
NAT_ACCEL = 0.09#how much we accelerate naturally
ININC_TIME = 700 #how much we are invincible for at the start
EQUIB_POINT = (0.1, 0.1) #the speed we go towards
UNITTYPES = [{"img" : "triship.png"},
			 {"img" : "quadship.png"},
			 {"img" : "quintship.png"},
			 {"img" : "sextship.png"}]

class Unit(Sprite):
	def __init__(self, screen, unitType, initPosition, initDirection, speed, targetList):
		Sprite.__init__(self)
		self.screen = screen
		self.speed = vec2d(speed)
		self.acc = vec2d(0, 0)
		self.pos = vec2d(initPosition)
		self.direction = vec2d(initDirection).normalized()
		self.base_image = pygame.image.load(UNITTYPES[unitType]["img"]).convert_alpha()
		self.image = self.base_image
		self.size = self.image.get_size()
		self.flow = numpy.array([0, 0])
		self.targetList = targetList
		self.entered = False

	def update(self, time_passed, flowMat):
		"""The unit owns the flow calculations"""
		#movement
		self._change_direction(time_passed)
		self.image = pygame.transform.rotate(self.base_image, -self.direction.angle)
		self.size = self.image.get_size()
		displacement = vec2d(
				self.direction.x * self.speed.x * time_passed,
				self.direction.y * self.speed.y * time_passed)
		self.pos += displacement
		self.flow = FLOW_FACTOR * numpy.sum(numpy.sum(flowMat, axis=0), axis=0)
		print self.flow
		#acceleration
		self.acc += (self.flow)
		self.acc *= DECEL_FACTOR
		self.speed += (ACC_FACTOR * self.acc)
		if self.speed > EQUIB_POINT:
			self.speed *= DECEL_FACTOR
		if self.speed < EQUIB_POINT:
			self.speed += NAT_ACCEL
		self.pos[0] = int(self.pos[0])
		self.pos[1] = int(self.pos[1])
		if (self.entered):
			self._checkbounds()


	def blitme(self):
		draw_pos = self.image.get_rect().move(
				self.pos.x - self.image_w / 2,
				self.pos.y - self.image_h / 2)
		self.screen.blit(self.image, draw_pos)

	def die(self):
		pass

	#private
	_counter = 0

	def _checkbounds(self):
		self.image_w, self.image_h = self.image.get_size()
		bounds_rect = self.screen.get_rect().inflate(
							-self.image_w, -self.image_h)
		if self.pos.x < bounds_rect.left:
			self.die()
		elif self.pos.x > bounds_rect.right:
			self.die()
		elif self.pos.y < bounds_rect.top:
			self.die()
		elif self.pos.y > bounds_rect.bottom:
			self.die()

	def _change_direction(self, time_passed):
		self._counter += time_passed
		if self._counter > randint(1600, 1750):
			self.direction.rotate(randint(-45, 45))
			self._counter = 0
