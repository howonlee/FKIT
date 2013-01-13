#listing of stages

'''an explanation of the data struct:
	num: number of enemies
	path: the path the enemies will take
	spawn: the places the enemies can spawn from
	time: the milliseconds you get till the next one

'''
STAGES = [
		{"num" : 8, "path": [(520, 70), (490, 420), (120, 300), (320, 240)], "spawn": [(450, 0)], "time": 3200},
		{"num" : 16, "path": [(130, 450), (520, 290), (320, 240)], "spawn": [(0, 420), (0, 325)], "time": 2700},
		{"num" : 32, "path": [(300, 55), (320, 240)], "spawn": [(0, 45), (640, 45)], "time": 2200},
		{"num" : 64, "path": [(320, 240)], "spawn": [(0, 480), (0, 0), (640, 0), (640, 480)], "time": 1800}
		]
