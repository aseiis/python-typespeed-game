import linecache
import random
import tkinter as tk
import cfg
from playsound import playsound


class MainApp(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        #mainframe and stuff
        self.configure(bg=cfg.default_bg)
        self.pack(expand=True)

        self.score = 0

        self.central_frame = tk.Frame(self, bg=cfg.default_bg)
        self.central_frame.grid(row=0, column=0)
        self.any_key_label = tk.Label(self.central_frame, text="Press any key to start...", font=("Arial", 12),
                               fg=cfg.default_fg, bg=cfg.default_bg)
        self.any_key_label.pack()

        self.score_label = tk.Label(self, text="0", font=cfg.arial_font_tuple,
                                    fg=cfg.default_fg, bg=cfg.default_bg)
        self.score_label.grid(row=1, column=0, sticky="E")
        self.final_score_label = tk.Label(self, text=" \n ", font=cfg.arial_font_tuple,
                                    fg=cfg.default_strong_fg, bg=cfg.default_bg)
        self.score_label.configure(text=str(self.score))
        self.replay_button = tk.Button(self, text="Replay", command=lambda: self.replay(), font=("Arial", 12),
                                       relief="flat", fg=cfg.default_fg, bg=cfg.default_light_bg)

        #Word
        self.filestream = open("dict.txt")
        self.total_words = len(self.filestream.readlines())
        #print(f"Total words: {self.total_words}")
        self.word_value = ""
        self.word_label = tk.Label(self.central_frame, text="<...>", font=cfg.default_font_tuple,
                                   fg=cfg.default_strong_fg, bg=cfg.default_bg)
        self.word_label.pack()
        self.entry_box = tk.Entry(self.central_frame, width=16, font=cfg.default_font_tuple,
                                  fg=cfg.default_focus_fg, bg=cfg.default_light_bg, insertwidth=3, relief="flat",
                                  insertbackground=cfg.default_focus_fg, insertontime=750, insertofftime=750)
        self.entry_box.focus_set()
        self.entry_box.pack()

        #Bindings
        self.parent.bind("<Key>", (lambda event: self.start_run()))
        self.parent.bind("<Return>", (lambda event: self.enter_word()))
        self.parent.bind("<Escape>", (lambda event: self.abort_game()))

        #Time
        self.running = False
        self.is_game_over = False
        self.timeleft_value = 60

        self.timeframe = tk.Frame(self, bg=cfg.default_bg, width=120, height=120)
        self.timeframe.grid(row=1, column=0, sticky="W")
        self.timeleft_label = tk.Label(self.timeframe, bg=cfg.default_bg, fg=cfg.default_fg, font=cfg.arial_font_tuple,
                                       text="60 sec.")
        self.timeleft_label.pack()
        self.timeleft_label.after(1000, self.step)

        self.new_word()

    def reinitialize(self):
        self.score_label.configure(text=str(self.score))
        self.any_key_label.pack()
        self.score = 0
        self.timeleft_value = 60
        self.timeleft_label.configure(text=str(self.timeleft_value) + " sec.")
        self.new_word()

    def uninitialize(self):
        self.score_label.configure(text=str(self.score))
        self.final_score_label.grid_forget()
        self.word_label.configure(text="<...>")
        self.entry_box.delete(0, 'end')

    def new_word(self) -> None:
        random.seed()
        # r is a random word picked in the text file opened in self.filestream
        r = random.randrange(self.total_words)
        #print(f"Choosen word: {r}")
        w = ""
        while w == "":
            w = linecache.getline("dict.txt", r, module_globals=None)
        self.word_value = w.strip()
        self.word_label.configure(text=self.word_value)
        #print("w:" + w)
        self.update()

    def step(self):
        if self.running is True:
            self.timeleft_value -= 1
            if self.timeleft_value == 0:
                self.game_over()
            self.timeleft_label.configure(text=f"{self.timeleft_value} sec.")
        self.timeleft_label.after(1000, self.step)

    def start_run(self, *args, **kwargs):
        if not self.is_game_over and not self.running:
            self.running = True
            self.any_key_label.configure(text="")
            self.final_score_label.configure(text="")

    def enter_word(self, *args, **kwargs):
        if self.entry_box.get() == self.word_value and not self.is_game_over:
            playsound("sfx/hit_sfx.wav")
            self.score += 1
            self.score_label.configure(text=self.score)
            self.entry_box.delete(0, 'end')
            self.new_word()

    def game_over(self):
        self.is_game_over = True
        self.running = False
        self.replay_button.grid(row=3, column=0, pady=20)
        if self.score > 20:
            self.final_score_label.configure(text="Score: " + str(self.score) + "\nCongrats!")
        elif self.score > 1:
            self.final_score_label.configure(text="Score: " + str(self.score) + "\nTry again to score 20+! :)")
        else:
            self.final_score_label.configure(text="Score: " + str(self.score) + "\nYou didn't play! :s")
        self.final_score_label.grid(row=2, column=0)
        playsound("sfx/finish.wav")

    def replay(self):
        # restoring default values
        self.score = 0
        self.word_value = ""
        self.is_game_over = False
        self.running = False
        self.uninitialize()
        # and packing plus misc
        self.reinitialize()

    def abort_game(self):
        if self.running and not self.is_game_over:
            self.timeleft_value = 1


