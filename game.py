import cv2, pygame, sys
from pygame.locals import *
from numpy import *

def draw_flow(im, flow, step=16):
	"""Plot optical flow"""
	h, w = im.shape[:2]
	y, x = mgrid[step/2:h:step, step/2:w:step].reshape(2, -1)
	fx, fy = flow[y, x].T

	lines = vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
	lines = int32(lines)

	#vis = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
	vis = zeros((im.shape[0], im.shape[1], 3))
	for (x1, y1), (x2, y2) in lines:
		cv2.line(vis, (x1, y1), (x2, y2), (255, 255, 255), 1)
		cv2.circle(vis, (x1, y1), 1, (255,255,255), -1)
	#print vis
	return vis

cap = cv2.VideoCapture(0)

ret, im = cap.read()
prev_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

while True:
	ret, im = cap.read()
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, 0.5, 1, 3, 1, 3, 5, 1)
	prev_gray = gray
	cv2.imshow('Optical Flow', draw_flow(gray, flow))
	if cv2.waitKey(10) == 27:
		break
