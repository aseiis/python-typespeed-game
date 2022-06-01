import tkinter as tk
from app import *
import cfg


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Type Speed Game")
    root.geometry("800x480")
    root.configure(bg=cfg.default_bg)
    main_app = MainApp(root)
    main_app.mainloop()