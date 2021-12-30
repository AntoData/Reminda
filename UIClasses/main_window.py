from __future__ import annotations
import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
from load_questions_window import LoadQuestionnaire
from create_questionnaire_start import CreateQuestionnaire
from window_design import SimpleWindow
from config_pop_up import ConfigPopUp
import tkinter as tk
import random
from tkinter import messagebox


@LoggerMeta.class_decorator_logger("INFO")
class MainWindow(SimpleWindow):
    def button_new_handler(self):
        self.window.destroy()
        new = CreateQuestionnaire()
        new.window.mainloop()

    def button_load_handler(self):
        self.window.destroy()
        load = LoadQuestionnaire()
        load.window.mainloop()

    @staticmethod
    def config_handler():
        c = ConfigPopUp(120, 287, "Configuration")
        c.window.mainloop()

    @staticmethod
    def handlerIntroLabel(event=None):
        r = lambda: random.randint(0, 255)
        new_colour = '#%02X%02X%02X' % (r(), r(), r())
        event.widget["bg"] = new_colour
        messagebox.showinfo("About",
                            "· To create a new questionnaire click the button New. It will display an assistant to "
                            "create it easily.\n· If you have already created a questionnaire, click Load and we will"
                            " allow you to pick which one you want to start.\n")

    def __init__(self):
        SimpleWindow.__init__(self, 230, 650, "Reminda")
        self.window.resizable(height=False, width=False)
        self.menu: tk.Menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.file_menu: tk.Menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu, underline=0)
        self.file_menu.add_command(label="New", command=self.button_new_handler)
        self.file_menu.add_command(label="Load file", command=self.button_load_handler)
        self.file_menu.add_command(label="Exit", command=self.window.destroy)
        self.menu.add_command(label="Config", command=MainWindow.config_handler)
        tk.Frame(self.window, height=50).pack()
        self.label_main: tk.Label = tk.Label(self.window,
                                             text="Welcome to Reminda, an app to help you prepare for exams",
                                             font=("Arial Baltic", "15", "bold"), bg="#1A4AC1", fg="white")
        self.label_main["padx"] = 20
        self.label_main["pady"] = 20
        self.label_main.bind("<Button-1>", self.handlerIntroLabel)
        self.label_main.pack()
        tk.Frame(self.window, height=20).pack()
        self.button_frame: tk.Frame = tk.Frame(self.window)
        self.button_frame.pack()
        self.button_font = ("TkDefaultFont", 16, "bold")
        self.button_new: tk.Button = tk.Button(self.button_frame, text="New", font=self.button_font,
                                               command=self.button_new_handler)
        self.button_new.grid(column=0, row=0)
        tk.Frame(self.button_frame, width=30).grid(row=0, column=1)
        self.button_load: tk.Button = tk.Button(self.button_frame, text="Load", font=self.button_font,
                                                command=self.button_load_handler)
        self.button_load.grid(column=2, row=0)


if __name__ == "__main__":
    main = MainWindow()
    main.window.mainloop()
