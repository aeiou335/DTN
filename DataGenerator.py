from Car import Car
from Routes import Route
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class DataGenerator:
    """
    fast: 1, 3, 7, 9
    medium: 2, 4, 6, 8
    slow: 5
    """
    def __init__(self, cars_num = 15, routes_num = 5, blocks_num = 9, drawOnlyRoutes = False):
        self.width  = 30000
        self.height = 30000
        self.blocks_num = blocks_num
        self.blocks_width = self.width / 3
        self.blocks_height = self.height / 3
        self.routes_num = routes_num
        self.cars_num = cars_num
        self.base_speed = 10
        self.stage_num = 3
        self.stage_time = 1800
        self.routes = self.init_routes()     
        self.cars = self.init_cars()
        if drawOnlyRoutes:
            self.drawRoutes()
        self.drawRoutesAndCars()
        self.generate()
    
    def init_routes(self):
        routes_block = random.sample(range(1, self.blocks_num+1), min(self.routes_num, self.blocks_num))
        result = {}
        for i in range(self.routes_num):
            start_block = routes_block[i % self.blocks_num]
            start_block_midX = (start_block-1) % 3 * self.blocks_width + self.blocks_width // 2
            start_block_midY = (start_block-1) // 3 * self.blocks_height + self.blocks_height // 2
            x = random.randint(start_block_midX - self.blocks_width // 5, start_block_midX + self.blocks_width // 5)
            y = random.randint(start_block_midY - self.blocks_height // 5, start_block_midY + self.blocks_height // 5)
            b = self.base_speed * self.stage_time / 4
            w = random.randint(int(b * 0.8), int(b * 1.2))
            h = random.randint(int(b * 0.8), int(b * 1.2))
            if x+w > self.width:
                w = self.width - x
            if y+h > self.height:
                h = self.height - y
            result[i] = Route(x, y, w, h, True)
        return result

    def init_cars(self):
        result = {}
        cars_per_route = self.cars_num // self.routes_num
        for i in range(self.routes_num):
            # selected = [False, False, False, False]
            for j in range(cars_per_route):
                carID = i * cars_per_route + j
                phase = j % 4
                r = self.routes[i]
                x, y = r.random_select(phase)
                result[carID] = Car(carID, x, y, r.clockwise, i)
        return result                

    def generate(self):
        for i in range(self.stage_num):
            with open("stage_{}.txt".format(i+1), 'w') as f: 
                for s in range(self.stage_time):
                    for j in range(self.cars_num):
                        print(s, j, self.cars[j].posX, self.cars[j].posY, file=f)
                        car = self.cars[j]
                        route = self.routes[car.route]
                        if car.clockwise:
                            

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
        

DataGenerator()