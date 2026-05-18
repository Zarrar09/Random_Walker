from Walker import Walker


# vivid colors for each walker
COLORS = [
    "#FF2D55", "#00F5FF", "#FFD60A", "#30D158", "#BF5AF2",
    "#FF6F00", "#00E5FF", "#FF375F", "#34C759", "#FF9F0A",
    "#64D2FF", "#FF453A", "#32D74B", "#FF9F0A", "#AC8FFF",
    "#FF6B35", "#00FFAA", "#FF3CAC", "#41EAD4", "#FFBE0B"
]


class Controller:
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        self.walkers = []

    def createWalkers(self, count):
        self.walkers = []
        centerX = self.canvasWidth // 2
        centerY = self.canvasHeight // 2
        for i in range(count):
            color = COLORS[i % len(COLORS)]
            self.walkers.append(Walker(centerX, centerY, color, self.canvasWidth, self.canvasHeight))

    def update(self):
        centerX = self.canvasWidth // 2
        centerY = self.canvasHeight // 2
        for walker in self.walkers:
            walker.move()
            if not walker.alive:
                # respawn dead walker back at the center
                walker.reset(centerX, centerY)