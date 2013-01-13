import pygame
import numpy
import copy
from pygame.sprite import Sprite
from random import randint, choice
from vec2d import *

ATK_EVENT = 26
STAR_POS = (310, 230)
UNITTYPES = [{"img" : "sextship.png"},
			 {"img" : "quintship.png"},
			 {"img" : "quadship.png"},
			 {"img" : "triship.png"}]

class Unit(Sprite):
	def __init__(self, screen, unitType, initPosition, initDirection, speed, targetList):
		Sprite.__init__(self)
		self.isDead = False
		self.screen = screen
		self.speed = vec2d(speed)
		self.pos = vec2d(initPosition)
		self.direction = vec2d(initDirection).normalized()
		self.base_image = pygame.image.load(UNITTYPES[unitType]["img"]).convert_alpha()
		self.image = self.base_image
		self.size = self.image.get_size()
		self.rect = pygame.Rect(initPosition, self.size)
		self.flow = numpy.array([0, 0])
		self.targetList = copy.deepcopy(targetList)
		self.currTarget = self.targetList[0]

	def update(self, time_passed, flowMat):
		"""The unit owns the flow calculations"""
		#movement
		if (self.isDead): return
		self._change_direction(time_passed)
		self._checkTarget()
		displacement = vec2d(
				self.direction.x * self.speed.x * time_passed,
				self.direction.y * self.speed.y * time_passed)
		self.pos += displacement
		self.flow = numpy.sum(numpy.sum(flowMat, axis=0), axis=0)
		self.speed += vec2d(self.flow)
		if self.speed.x > 0.2:
			self.speed.x = 0.2
		if self.speed.y > 0.2:
			self.speed.y = 0.2
		#if self.speed > 0.1:
		#	self.speed *= 0.9
		#if self.speed < 0.1:
		#	self.speed += 0.02
		#self.pos[0] = int(self.pos[0])
		#self.pos[1] = int(self.pos[1])
		self._checkbounds()

	def blitme(self):
		if (self.isDead): return
		draw_pos = self.image.get_rect().move(
				self.pos.x - self.image.get_width() / 2,
				self.pos.y - self.image.get_height() / 2)
		self.screen.blit(self.image, draw_pos)

	def die(self):
		"""this is a bit of a sop"""
		if (self.isDead): return
		self.pos = (-1000, -1000)
		self.speed = vec2d(0, 0)
		self.isDead = True

	#private
	_counter = 0

	def _checkbounds(self):
		if (self.isDead): return
		self.image_w, self.image_h = self.image.get_size()
		bounds_rect = self.screen.get_rect()
		if self.pos.x < bounds_rect.left:
			self.die()
		elif self.pos.x > bounds_rect.right:
			self.die()
		elif self.pos.y < bounds_rect.top:
			self.die()
		elif self.pos.y > bounds_rect.bottom:
			self.die()

	def _change_direction(self, time_passed):
		if (self.isDead): return
		self.direction = self.currTarget - self.pos
		self.direction = self.direction.normalized()

	def _checkTarget(self):
		if (self.isDead): return
		if self.pos.get_distance(self.currTarget) < ((self.image.get_size()[0] / 2) + 1):
			print "targetList", self.targetList
			if (len(self.targetList) > 0):
				self.currTarget = self.targetList[0]
				self.targetList.pop(0)
			else:
				if (self.currTarget == STAR_POS):
					deathEvent = pygame.event.Event(ATK_EVENT)
					pygame.event.post(deathEvent)
					self.die()
				self.currTarget = STAR_POS
