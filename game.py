import cv2, pygame, sys
import cv2.cv as cv
from pygame.locals import *
from numpy import *

def draw_flow(im, flow, step=16):
	"""Plot optical flow"""
	h, w = im.shape[:2]
	y, x = mgrid[step/2:h:step, step/2:w:step].reshape(2, -1)
	fx, fy = flow[y, x].T

	lines = vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
	lines = int32(lines)

	vis = cv.CreateMat(im.shape[0], im.shape[1], cv.CV_8UC3)
	#vis = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
	#vis = zeros((im.shape[0], im.shape[1], 3))
	for (x1, y1), (x2, y2) in lines:
		cv.Line(vis, (x1, y1), (x2, y2), (255, 255, 255), 1)
	#print vis
	return vis

if __name__ == '__main__':

	#webcam init
	cap = cv2.VideoCapture(0)
	ret, im = cap.read()
	prev_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

	#pygame init
	pygame.init()
	fpsClock = pygame.time.Clock()
	windowSurfaceObj = pygame.display.set_mode((im.shape[0], im.shape[1]))
	pygame.display.set_caption("FKIT")

	while True:
		ret, im = cap.read()
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, 0.5, 1, 3, 1, 3, 5, 1)
		prev_gray = gray
		vis = draw_flow(gray, flow)
		pgVis = pygame.image.frombuffer(vis.tostring(), cv.GetSize(vis), "RGB")
		windowSurfaceObj.blit(pgVis, (0,0))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
