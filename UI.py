import tkinter as tk
from tkinter import ttk
from controller import Controller


CANVAS_WIDTH = 960
CANVAS_HEIGHT = 580
WALKER_RADIUS = 5
UPDATE_DELAY = 20

BG_DARK = "#0e0e14"
BG_PANEL = "#16161f"
BG_CANVAS = "#0a0a10"
ACCENT = "#5c6bc0"
ACCENT_SECONDARY = "#26a69a"
TEXT_PRIMARY = "#e8e8f0"
TEXT_MUTED = "#6b6b80"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Walker")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)
        self.running = False
        self.controller = Controller(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.buildUI()

    def buildUI(self):
        # outer wrapper with padding
        wrapper = tk.Frame(self.root, bg=BG_DARK)
        wrapper.pack(padx=24, pady=20, fill="both")

        # header row
        header = tk.Frame(wrapper, bg=BG_DARK)
        header.pack(fill="x", pady=(0, 16))

        tk.Label(
            header,
            text="Random Walker",
            font=("Helvetica", 22, "bold"),
            bg=BG_DARK,
            fg=TEXT_PRIMARY
        ).pack(side="left")

        tk.Label(
            header,
            text="watch cells wander until they disappear",
            font=("Helvetica", 11),
            bg=BG_DARK,
            fg=TEXT_MUTED
        ).pack(side="left", padx=(14, 0), pady=(6, 0))

        # control panel
        panel = tk.Frame(wrapper, bg=BG_PANEL, padx=20, pady=14)
        panel.pack(fill="x", pady=(0, 14))

        # walker count control
        countGroup = tk.Frame(panel, bg=BG_PANEL)
        countGroup.pack(side="left", padx=(0, 30))

        tk.Label(
            countGroup,
            text="WALKERS",
            font=("Helvetica", 9, "bold"),
            bg=BG_PANEL,
            fg=TEXT_MUTED
        ).pack(anchor="w")

        sliderRow = tk.Frame(countGroup, bg=BG_PANEL)
        sliderRow.pack(fill="x", pady=(4, 0))

        self.walkerCount = tk.IntVar(value=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Horizontal.TScale",
            background=BG_PANEL,
            troughcolor="#2a2a38",
            sliderlength=18
        )

        slider = ttk.Scale(
            sliderRow,
            from_=1,
            to=20,
            variable=self.walkerCount,
            orient="horizontal",
            length=200,
            style="Custom.Horizontal.TScale",
            command=lambda v: self.walkerCount.set(int(float(v)))
        )
        slider.pack(side="left")

        self.countDisplay = tk.Label(
            sliderRow,
            textvariable=self.walkerCount,
            font=("Helvetica", 14, "bold"),
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            width=3
        )
        self.countDisplay.pack(side="left", padx=(12, 0))

        # speed control
        speedGroup = tk.Frame(panel, bg=BG_PANEL)
        speedGroup.pack(side="left", padx=(0, 30))

        tk.Label(
            speedGroup,
            text="SPEED",
            font=("Helvetica", 9, "bold"),
            bg=BG_PANEL,
            fg=TEXT_MUTED
        ).pack(anchor="w")

        speedRow = tk.Frame(speedGroup, bg=BG_PANEL)
        speedRow.pack(fill="x", pady=(4, 0))

        self.speedVar = tk.IntVar(value=3)

        speedSlider = ttk.Scale(
            speedRow,
            from_=1,
            to=8,
            variable=self.speedVar,
            orient="horizontal",
            length=140,
            style="Custom.Horizontal.TScale",
            command=lambda v: self.speedVar.set(int(float(v)))
        )
        speedSlider.pack(side="left")

        self.speedDisplay = tk.Label(
            speedRow,
            textvariable=self.speedVar,
            font=("Helvetica", 14, "bold"),
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            width=2
        )
        self.speedDisplay.pack(side="left", padx=(12, 0))

        # buttons
        btnGroup = tk.Frame(panel, bg=BG_PANEL)
        btnGroup.pack(side="right")

        self.startBtn = tk.Button(
            btnGroup,
            text="  Start  ",
            command=self.toggleStart,
            bg=ACCENT,
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=8,
            activebackground="#7986cb",
            activeforeground="white",
            bd=0
        )
        self.startBtn.pack(side="left", padx=(0, 8))

        resetBtn = tk.Button(
            btnGroup,
            text="  Reset  ",
            command=self.reset,
            bg="#2a2a38",
            fg=TEXT_MUTED,
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=8,
            activebackground="#3a3a4a",
            activeforeground=TEXT_PRIMARY,
            bd=0
        )
        resetBtn.pack(side="left")

        # canvas
        canvasFrame = tk.Frame(wrapper, bg="#1a1a24", padx=1, pady=1)
        canvasFrame.pack()

        self.canvas = tk.Canvas(
            canvasFrame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=BG_CANVAS,
            highlightthickness=0
        )
        self.canvas.pack()

        # status bar
        self.statusVar = tk.StringVar(value="press start to begin")
        tk.Label(
            wrapper,
            textvariable=self.statusVar,
            font=("Helvetica", 10),
            bg=BG_DARK,
            fg=TEXT_MUTED
        ).pack(pady=(10, 0), anchor="w")

    def toggleStart(self):
        if self.running:
            self.running = False
            self.startBtn.config(text="  Start  ", bg=ACCENT)
            self.statusVar.set("paused")
        else:
            # apply current speed to all walkers
            self.controller.createWalkers(self.walkerCount.get())
            self.applySpeed()
            self.running = True
            self.startBtn.config(text="  Pause  ", bg="#ef5350")
            self.statusVar.set(f"running {self.walkerCount.get()} walkers")
            self.loop()

    def applySpeed(self):
        for walker in self.controller.walkers:
            walker.stepSize = self.speedVar.get()

    def reset(self):
        self.running = False
        self.startBtn.config(text="  Start  ", bg=ACCENT)
        self.canvas.delete("all")
        self.controller.walkers = []
        self.statusVar.set("press start to begin")

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
            # draw trail as connected lines
            if len(walker.trail) > 1:
                self.canvas.create_line(
                    walker.trail,
                    fill=walker.color,
                    width=1,
                    smooth=True
                )
            # draw walker head
            x1 = walker.x - WALKER_RADIUS
            y1 = walker.y - WALKER_RADIUS
            x2 = walker.x + WALKER_RADIUS
            y2 = walker.y + WALKER_RADIUS
            self.canvas.create_oval(x1, y1, x2, y2, fill=walker.color, outline="")