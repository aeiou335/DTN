from Car import Car
from Routes import Route
import random
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class DataGenerator:
	"""
	fast: 1, 3, 7, 9
	medium: 2, 4, 6, 8
	slow: 5
	carIndex: 0 ~ cars_num-1
	routeIndex: 0 ~ routes_num-1
	"""
	def __init__(self, width, height, routes_num, cars_num, base_speed, speed_noise, \
				stage_num, stage_time, drawOnlyRoutes, reassign, speedwNoise):
		self.width  = width
		self.height = height
		self.blocks_num = 9
		self.blocks_width = self.width // 3
		self.blocks_height = self.height // 3
		self.routes_num = routes_num
		self.cars_num = cars_num
		self.base_speed = base_speed
		self.speedwNoise = speedwNoise
		if self.speedwNoise:
			self.speed_noise = speed_noise
		else:
			self.speed_noise = 0
		self.stage_num = stage_num
		self.stage_time = stage_time
		self.reassign = reassign
		self.routes = self.initRoutes()     
		self.cars = self.initCars()
		self.initSpeed()
		if drawOnlyRoutes:
			self.drawRoutes()
		self.drawRoutesAndCars()
		self.generate()
	
	def initRoutes(self):
		routes_block = random.sample(range(1, self.blocks_num+1), min(self.routes_num, self.blocks_num))
		result = {}
		vertical_y = random.randint(self.height // 3, self.height // 3 * 2)
		result[0] = Route(self.blocks_width // 2, vertical_y, self.width * 2 // 3, 0, 2, 0)
		vertical_x = random.randint(self.width // 3, self.height // 3 * 2)
		result[1] = Route(vertical_x, self.blocks_width // 2, 0, self.height * 2 // 3, 3, 0)
		for i in range(2, self.routes_num):
			start_block = routes_block[i % self.blocks_num]
			start_block_midX = (start_block-1) % 3 * self.blocks_width + self.blocks_width // 2
			start_block_midY = (start_block-1) // 3 * self.blocks_height + self.blocks_height // 2
			x = random.randint(start_block_midX - self.blocks_width // 3, start_block_midX + self.blocks_width // 3)
			y = random.randint(start_block_midY - self.blocks_height // 3, start_block_midY + self.blocks_height // 3)
			#b = self.base_speed * self.stage_time / 4
			b = 4500
			w = random.randint(int(b * 0.8), int(b * 1.2))
			h = random.randint(int(b * 0.8), int(b * 1.2))
			if x+w > self.width:
				w = self.width - x
			if y+h > self.height:
				h = self.height - y
			clockwise = random.randint(0,1)
			print(x, y, w, h)
			result[i] = Route(x, y, w, h, 1, clockwise)
		return result

	def initCars(self):
		result = {}
		cars_per_route = self.cars_num // self.routes_num
		for i in range(self.routes_num):
			# selected = [False, False, False, False]
			for j in range(cars_per_route):
				carID = i * cars_per_route + j
				phase = j % 4
				r = self.routes[i]
				x, y = r.random_select(phase)
				result[carID] = Car(carID, x, y, i, phase)
		return result  
	
	def reassignCars(self):
		for i in range(self.cars_num):
			new_route = random.randint(0, self.routes_num-1)
			new_phase = random.randint(0, 3)
			x, y = self.routes[new_route].random_select(new_phase)
			self.cars[i].posX = x
			self.cars[i].posY = y
			self.cars[i].route = new_route

	def initSpeed(self):
		self.speed = {
			1: self.base_speed + self.speed_noise,
			2: self.base_speed,
			3: self.base_speed + self.speed_noise,
			4: self.base_speed,
			5: self.base_speed - self.speed_noise,
			6: self.base_speed,
			7: self.base_speed + self.speed_noise,
			8: self.base_speed,
			9: self.base_speed + self.speed_noise
		}

	def generate(self):
		with open("stage.txt", 'w') as f: 
			for i in range(self.stage_num):
			#with open("stage_{}.txt".format(i+1), 'w') as f: 
				for s in range(self.stage_time):
					for j in range(self.cars_num):
						f.write("{} {} {} {}\n".format(s + i * self.stage_time, j, self.cars[j].posX, self.cars[j].posY))
						car = self.cars[j]
						route = self.routes[car.route]
						block = self.getBlock(car.posX, car.posY)
						speed = self.speed[block]
						if route.clockwise:
							if car.phase == 0:
								if car.posY + speed <= route.coord["y1"]:
									car.posY += speed
								else:
									car.posY = route.coord["y1"]
									car.posX += (car.posY + speed - route.coord["y1"])
									car.phase = 1
							elif car.phase == 1:
								if car.posX + speed <= route.coord["x2"]:
									car.posX += speed
								else:
									car.posX = route.coord["x2"]
									car.posY -= (car.posX + speed - route.coord["x2"])
									car.phase = 2
							elif car.phase == 2:
								if car.posY - speed >= route.coord["y3"]:
									car.posY -= speed
								else:
									car.posY = route.coord["y3"]
									car.posX += (car.posY - speed - route.coord["y3"])
									car.phase = 3
							elif car.phase == 3:
								if car.posX - speed >= route.coord["x0"]:
									car.posX -= speed
								else:
									car.posX = route.coord["x0"]
									car.posY -= (car.posX - speed - route.coord["x0"])
									car.phase = 0
						else:
							if car.phase == 0:
								if car.posY - speed >= route.coord["y0"]:
									car.posY -= speed
								else:
									car.posY = route.coord["y0"]
									car.posX -= (car.posY - speed - route.coord["y0"])
									car.phase = 3
							elif car.phase == 1:
								if car.posX - speed >= route.coord["x1"]:
									car.posX -= speed
								else:
									car.posX = route.coord["x1"]
									car.posY += (car.posX - speed - route.coord["x1"])
									car.phase = 0
							elif car.phase == 2:
								if car.posY + speed <= route.coord["y2"]:
									car.posY += speed
								else:
									car.posY = route.coord["y2"]
									car.posX -= (car.posY + speed - route.coord["y2"])
									car.phase = 1
							elif car.phase == 3:
								if car.posX + speed <= route.coord["x3"]:
									car.posX += speed
								else:
									car.posX = route.coord["x3"]
									car.posY += (car.posX + speed - route.coord["x3"])
									car.phase = 2
			if self.reassign:
				self.reassignCars()
			self.base_speed = random.randint(9,11)
			if self.speedwNoise:
				self.speed_noise = random.randint(0,2)
			self.initSpeed()

	# Given current coordinates, find out the block 
	def getBlock(self, x, y):
		x1 = self.width // 3
		x2 = self.width * 2 // 3
		y1 = self.height // 3
		y2 = self.height * 2 // 3
		if x < x1: 
			x_i = 0
		elif x >= x1 and x < x2: 
			x_i = 1
		else: 
			x_i = 2
		
		if y < y1: 
			y_i = 1
		elif y >= y1 and y < y2:
			y_i = 2
		else: 
			y_i = 3 
		
		return x_i * 3 + y_i
							

	def drawRoutesAndCars(self):
		plt.figure()
		plt.xlim(0, self.width)
		plt.ylim(0, self.height)
		currentAxis = plt.gca()
		for r in self.routes.values():
			#print(r.start_posX, r.start_posY, r.width, r.height)
			currentAxis.add_patch(patches.Rectangle((r.start_posX, r.start_posY), r.width, r.height, linewidth=1,edgecolor='r', fill=None))
		for c in self.cars.values():
			plt.plot(c.posX, c.posY, 'ro')

		plt.savefig("RoutesAndCars.jpg")

	def drawRoutes(self):
		plt.figure()
		plt.xlim(0, self.width)
		plt.ylim(0, self.height)
		currentAxis = plt.gca()
		for r in self.routes.values():
			#print(r.start_posX, r.start_posY, r.width, r.height)
			currentAxis.add_patch(patches.Rectangle((r.start_posX, r.start_posY), r.width, r.height, linewidth=1,edgecolor='r', fill=None))
		
		plt.savefig("Routes.jpg")
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--width', type=int, default = 30000)
	parser.add_argument('--height', type=int, default = 30000)
	parser.add_argument('--routes_num', type=int, default = 15)
	parser.add_argument('--cars_num', type=int, default = 30)
	parser.add_argument('--base_speed', type=int, default = 10)
	parser.add_argument('--speed_noise', type=int, default = 1)
	parser.add_argument('--stage_num', type=int, default = 3)
	parser.add_argument('--stage_time', type=int, default = 1200)
	parser.add_argument('--drawOnlyRoutes', type=bool, default = False)
	parser.add_argument('--reassign', type=bool, default = True)
	parser.add_argument('--speedwNoise', type=bool, default = True)
	args = parser.parse_args()
	DataGenerator(args.width, args.height,\
				args.routes_num, args.cars_num, args.base_speed, args.speed_noise,\
				args.stage_num, args.stage_time, args.drawOnlyRoutes,\
				args.reassign, args.speedwNoise)
