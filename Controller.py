import random
from walker import Walker


# different colors for each walker
COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
    "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9",
    "#F0B27A", "#82E0AA", "#F1948A", "#AED6F1", "#A9DFBF",
    "#FAD7A0", "#D7BDE2", "#A3E4D7", "#FDEBD0", "#D5DBDB"
]


class Controller:
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        self.walkers = []

    def createWalkers(self, count):
        self.walkers = []
        for i in range(count):
            x = random.randint(100, self.canvasWidth - 100)
            y = random.randint(100, self.canvasHeight - 100)
            color = COLORS[i % len(COLORS)]
            self.walkers.append(Walker(x, y, color, self.canvasWidth, self.canvasHeight))

    def update(self):
        for walker in self.walkers:
            walker.move()
            if not walker.alive:
                # respawn dead walker at a new random spot
                newX = random.randint(100, self.canvasWidth - 100)
                newY = random.randint(100, self.canvasHeight - 100)
                walker.reset(newX, newY)