import random
class Route():
    def __init__(self, start_posX, start_posY, width, height, rtype, clockwise):
        self.start_posX = start_posX
        self.start_posY = start_posY
        self.width = width
        self.height = height
        self.type = rtype # 1: square, 2: vertical line, 3: horizontal line
        self.clockwise = clockwise
        self.coord = self.init_coord()
    
    def init_coord(self):
        result = {}
        result["x0"] = self.start_posX
        result["y0"] = self.start_posY
        result["x1"] = self.start_posX
        result["y1"] = self.start_posY + self.height
        result["x2"] = self.start_posX + self.width
        result["y2"] = self.start_posY + self.height
        result["x3"] = self.start_posX + self.width
        result["y3"] = self.start_posY

        return result
    
    def random_select(self, phase):
        x, y = -1, -1
        if phase == 0:
            x = self.coord["x0"]
            y = random.randint(self.coord["y0"], self.coord["y1"])
        elif phase == 1:
            x = random.randint(self.coord["x1"], self.coord["x2"])
            y = self.coord["y1"]
        elif phase == 2:
            x = self.coord["x2"]
            y = random.randint(self.coord["y3"], self.coord["y2"])
        elif phase == 3:
            x = random.randint(self.coord["x0"], self.coord["x3"])
            y = self.coord["y3"]
        return x, y