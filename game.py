import cv2, pygame, sys
import cv2.cv as cv
from pygame.locals import *
from numpy import *
from random import randint, choice
from math import * #pollute that namespace, baby
from Unit import *
from Stages import *
from Star import *

MAX_STAGES = 3

def change_stage(gameState):
	gameState["currStage"] += 1
	currStage = gameState["currStage"] #just a local thing
	if gameState["currStage"] > MAX_STAGES:
		end_game()
	gameState["numUnits"] = STAGES[currStage]["num"]
	gameState["currPath"] = STAGES[currStage]["path"]
	gameState["currSpawn"] = STAGES[currStage]["spawn"]
	gameState["currTime"] = STAGES[currStage]["time"]
	pygame.time.set_timer(SPAWN_EVENT, gameState["currTime"])

def lose_life(unit, gameState):
	unit.die()
	gameState["numLives"] -= 1
	if gameState["numLives"] <= 0:
		end_game()

def end_game(gameoverscreen=False):
	pygame.quit()
	sys.exit()

def draw_flow(im, flow, step=32):
	"""Plot optical flow"""
	h, w = im.shape[:2]
	y, x = mgrid[step/2:h:step, step/2:w:step].reshape(2, -1)
	fx, fy = flow[y, x].T
	#print flow.shape

	lines = vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
	lines = int32(lines)

	#vis = cv.CreateMat(im.shape[0], im.shape[1], cv.CV_8UC3)
	vis = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
	#vis = zeros((im.shape[0], im.shape[1], 3))
	for (x1, y1), (x2, y2) in lines:
		cv2.line(vis, (x1, y1), (x2, y2), (255, 255, 255), 1)
	return vis

def make_star():
	global star
	star = Star(screen, STAR_POS, "star.png")

if __name__ == '__main__':

	#webcam init
	cap = cv2.VideoCapture(0)
	ret, im = cap.read()
	prev_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	flow = cv2.cv.CreateMat(im.shape[0], im.shape[1], cv2.cv.CV_32FC2)

	#pygame init
	pygame.init()
	fpsClock = pygame.time.Clock()
	SCREEN_WIDTH, SCREEN_HEIGHT = im.shape[1], im.shape[0]#this is a bit of a mysterious hack
	#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), (pygame.FULLSCREEN | pygame.HWSURFACE))
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("FKIT")

	#game init
	gameState = {}
	gameState["numLives"] = 5000
	gameState["numUnits"] = -1
	gameState["currStage"] = -1
	gameState["currPath"] = []
	gameState["currSpawn"] = []
	gameState["currTime"] = 0
	SPAWN_EVENT = 25
	STAR_POS = (305, 225)#hardcoded cuz of 640x480.
	change_stage(gameState)
	make_star()
	units = []
	pygame.time.set_timer(SPAWN_EVENT, gameState["currTime"])

	while True:
		timePassed = fpsClock.tick(60)
		for event in pygame.event.get():
			if event.type == SPAWN_EVENT:
				if (numUnits >= 0):
					print "spawn"
					print currStage
					print numUnits
					numUnits -= 1
				else:
					if (len(units) == 0): #wait for them to clear stage
						change_stage(gameState)
					print "change stage"
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					end_game()
			if event.type == QUIT:
				end_game()
		#begin actual stuff here
		ret, im = cap.read()
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		gray = cv2.equalizeHist(gray)
		flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, 0.5, 2, 3, 2, 6, 1.1, 1)
		prev_gray = gray
		pgVis = pygame.surfarray.make_surface(draw_flow(gray, flow))
		pgVis = pygame.transform.rotate(pgVis, 270)
		pgVisRect = pgVis.get_rect()
		screen.blit(pgVis, pgVisRect)
		star.blitme()
		for unit in units:
			step = 4
			top = min(unit.pos[1] + (unit.size[1] / 2), SCREEN_HEIGHT)
			bottom = max(unit.pos[1] - (unit.size[1] / 2), 0)
			left = max(unit.pos[0] - (unit.size[0] / 2), 0)
			right = min(unit.pos[0] + (unit.size[0] / 2), SCREEN_WIDTH)
			#print top, bottom, left, right
			flowMat = flow[bottom:top:step, left:right:step,:] * 0.1
			#print unit.pos
			unit.update(timePassed, flowMat)
			unit.blitme()
		pygame.display.update()
