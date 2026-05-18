import tkinter as tk
from tkinter import ttk
from Controller import Controller


CANVAS_WIDTH = 960
CANVAS_HEIGHT = 600
UPDATE_DELAY = 20

BG = "#080810"
PANEL = "#0f0f1a"
TEXT = "#d0d0e8"
DIM = "#3a3a52"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Walker")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.running = False
        self.controller = Controller(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.buildUI()

    def buildUI(self):
        wrapper = tk.Frame(self.root, bg=BG)
        wrapper.pack(padx=28, pady=(20, 14))

        # title
        tk.Label(
            wrapper,
            text="R A N D O M   W A L K E R",
            font=("Courier", 15, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(0, 18))

        # control bar
        bar = tk.Frame(wrapper, bg=PANEL, padx=22, pady=14)
        bar.pack(fill="x", pady=(0, 12))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "S.Horizontal.TScale",
            background=PANEL,
            troughcolor=DIM,
            sliderlength=14,
            sliderrelief="flat"
        )

        self.walkerCount = tk.IntVar(value=5)
        self.speedVar = tk.IntVar(value=4)

        self.addSlider(bar, "walkers", self.walkerCount, 1, 5, 180)

        tk.Frame(bar, bg=DIM, width=1, height=28).pack(side="left", padx=20)

        self.addSlider(bar, "speed", self.speedVar, 1, 8, 130)

        tk.Frame(bar, bg=BG, width=1).pack(side="left", expand=True)

        self.startBtn = self.makeBtn(bar, "start", self.toggleStart, TEXT)
        self.startBtn.pack(side="left", padx=(0, 8))

        self.makeBtn(bar, "reset", self.reset, DIM).pack(side="left", padx=(0, 8))
        self.makeBtn(bar, "save", self.saveImage, DIM).pack(side="left")

        # canvas
        self.canvas = tk.Canvas(
            wrapper,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=BG,
            highlightthickness=1,
            highlightbackground=DIM
        )
        self.canvas.pack()

    def addSlider(self, parent, label, variable, low, high, length):
        group = tk.Frame(parent, bg=PANEL)
        group.pack(side="left", padx=(0, 4))

        tk.Label(
            group,
            text=label,
            font=("Courier", 8),
            bg=PANEL,
            fg=DIM
        ).pack(anchor="w")

        row = tk.Frame(group, bg=PANEL)
        row.pack()

        ttk.Scale(
            row,
            from_=low,
            to=high,
            variable=variable,
            orient="horizontal",
            length=length,
            style="S.Horizontal.TScale",
            command=lambda v: variable.set(int(float(v)))
        ).pack(side="left")

        tk.Label(
            row,
            textvariable=variable,
            font=("Courier", 13, "bold"),
            bg=PANEL,
            fg=TEXT,
            width=3
        ).pack(side="left", padx=(8, 0))

    def makeBtn(self, parent, label, command, fg):
        return tk.Button(
            parent,
            text=label,
            command=command,
            bg=PANEL,
            fg=fg,
            font=("Courier", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=8,
            activebackground="#1e1e30",
            activeforeground=TEXT,
            bd=0
        )

    def toggleStart(self):
        if self.running:
            self.running = False
            self.startBtn.config(text="start", fg=TEXT)
        else:
            self.canvas.delete("all")
            self.controller.createWalkers(self.walkerCount.get())
            self.applySpeed()
            self.running = True
            self.startBtn.config(text="pause", fg="#ff4466")
            self.loop()

    def applySpeed(self):
        for walker in self.controller.walkers:
            walker.stepSize = self.speedVar.get()

    def reset(self):
        self.running = False
        self.startBtn.config(text="start", fg=TEXT)
        self.canvas.delete("all")
        self.controller.walkers = []

    def saveImage(self):
        try:
            from PIL import ImageGrab
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            ImageGrab.grab(bbox=(x, y, x + w, y + h)).save("walker.png")
        except ImportError:
            pass

    def loop(self):
        if not self.running:
            return
        self.applySpeed()
        self.controller.update()
        self.draw()
        self.root.after(UPDATE_DELAY, self.loop)

    def draw(self):
        self.canvas.delete("all")
        for walker in self.controller.walkers:
            if len(walker.trail) >= 2:
                self.canvas.create_line(walker.trail, fill=walker.color, width=2, smooth=True)