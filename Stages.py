#listing of stages

'''an explanation of the data struct:
	num: number of enemies
	path: the path the enemies will take
	spawn: the places the enemies can spawn from
	time: the milliseconds you get till the next one

'''
STAGES = [
		{"num" : 8, "path": [(480, 400), (120, 420), (200, 100), (320, 240)], "spawn": [(450, 40)], "time": 3200},
		{"num" : 12, "path": [(490, 120), (140, 100), (320, 240)], "spawn": [(600, 400), (600, 325)], "time": 2700},
		{"num" : 27, "path": [(300, 55), (320, 240)], "spawn": [(40, 45), (600, 45)], "time": 1500},
		{"num" : 64, "path": [(320, 240)], "spawn": [(40, 440), (40, 50), (600, 40), (600, 440)], "time": 500}
		]
