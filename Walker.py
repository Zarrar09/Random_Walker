import random


class Walker:
    def __init__(self, x, y, color, canvasWidth, canvasHeight):
        self.x = x
        self.y = y
        self.color = color
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        self.alive = True
        self.stepSize = 3
        self.trail = [(x, y)]
        self.maxTrail = 60

    def move(self):
        self.x += random.randint(-self.stepSize, self.stepSize)
        self.y += random.randint(-self.stepSize, self.stepSize)
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.maxTrail:
            self.trail.pop(0)
        self.checkBounds()

    def checkBounds(self):
        # mark walker as dead if it hits any edge
        if self.x <= 0 or self.x >= self.canvasWidth or self.y <= 0 or self.y >= self.canvasHeight:
            self.alive = False

    def reset(self, x, y):
        # bring walker back to a new random position
        self.x = x
        self.y = y
        self.alive = True
        self.trail = [(x, y)]