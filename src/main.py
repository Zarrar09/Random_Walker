import tkinter as tk
from UI import App


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    app = App(root)
    root.mainloop()