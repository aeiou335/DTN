class Car():
	def __init__(self, id, posX, posY, route, phase):
		self.posX = posX
		self.posY = posY
		#self.start_pos = start_pos
		self.id = id
		self.phase = phase # 0: up, 1: right, 2: down, 3: left
		self.route = route