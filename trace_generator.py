import random
import numpy as np
class Car():
	def __init__(self, id, start_pos, pos, x_range, y_range, clock_wise):
		self.pos = pos
		self.start_pos = start_pos
		self.id = id
		self.x_range = x_range
		self.y_range = y_range
		self.clock_wise = clock_wise
		self.phase = 0 # 0~3

WIDTH = 30000
LENGTH = 30000

trace = []
p = []
N, M = 6, 6
for i in range(1, N+1):
	for j in range(1, M+1):
		# print(i, j)
		clock_wise = random.sample((True, False), 1)
		clock_wise = clock_wise[0]

		if clock_wise:
			try:
				x = random.randint(0, WIDTH - (WIDTH / N)*i + 1)
				y = random.randint(0, LENGTH - (LENGTH / M)*j + 1)
			except ValueError:
				continue
		else:
			try:
				x = random.randint((WIDTH / N)*i + 1, WIDTH)
				y = random.randint((LENGTH / M)*j + 1, LENGTH)
			except ValueError:
				continue
		trace.append((x, y, (WIDTH / N) * i, (LENGTH / M)*j, clock_wise))
		p.append(1/(i*j))

K = 15
#trace = random.sample(trace, K)
p = np.array(p) / sum(np.array(p))
selected = np.random.choice(range(len(trace)), K, p = p, replace=False)
trace = [trace[i] for i in selected]

#for i in range(K):
	#print(trace[i][2], trace[i][3])

cars = []
RIGHT = np.array((1, 0))
LEFT = np.array((-1, 0))
UP = np.array((0, 1))
DOWN = np.array((0, -1))

for i in range(K):
	cars.append(Car(i, np.array((trace[i][0], trace[i][1])), np.array((trace[i][0], trace[i][1])), \
						 trace[i][2], trace[i][3], trace[i][4]))

#for car in cars:
	# print(car.id, car.pos[0], car.pos[1], car.start_pos[0] + car.x_range, car.start_pos[1] + car.y_range, car.clock_wise)

SEC = 1800
V = 9
fd = open('../data/output.txt', 'w')
with open ('../data/output.txt', 'w') as f:
    for s in range(SEC):
        for car in cars:
            if car.clock_wise:
                if car.phase == 0:
                    car.pos += V * UP
                elif car.phase == 1:
                    car.pos += V * RIGHT
                elif car.phase == 2:
                    car.pos += V * DOWN
                elif car.phase == 3:
                    car.pos += V * LEFT
                if car.pos[0] < car.start_pos[0] or car.pos[0] > car.start_pos[0] + car.x_range or\
                    car.pos[1] < car.start_pos[1] or car.pos[1] > car.start_pos[1] + car.y_range:
                    car.phase = (car.phase + 1) % 4
                car.pos[0] = max(car.pos[0], car.start_pos[0])
                car.pos[0] = min(car.pos[0], car.start_pos[0] + car.x_range)
                car.pos[1] = max(car.pos[1], car.start_pos[1])
                car.pos[1] = min(car.pos[1], car.start_pos[1] + car.y_range)
            else:
                if car.phase == 0:
                    car.pos += V * LEFT
                elif car.phase == 1:
                    car.pos += V * DOWN
                elif car.phase == 2:
                    car.pos += V * RIGHT
                elif car.phase == 3:
                    car.pos += V * UP
                if (car.pos[0] < car.start_pos[0] or car.pos[0] > car.start_pos[0] + car.x_range or\
                    car.pos[1] < car.start_pos[1] or car.pos[1] > car.start_pos[1] + car.y_range):
                    car.phase = (car.phase + 1) % 4
                car.pos[0] = max(car.pos[0], car.start_pos[0])
                car.pos[0] = min(car.pos[0], car.start_pos[0] + car.x_range)
                car.pos[1] = max(car.pos[1], car.start_pos[1])
                car.pos[1] = min(car.pos[1], car.start_pos[1] + car.y_range)
            print(s, car.id, car.pos[0], car.pos[1], file=f)
		# fd.write(line)