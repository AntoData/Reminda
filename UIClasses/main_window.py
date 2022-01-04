from __future__ import annotations
import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
import load_questions_window
from create_questionnaire_start import CreateQuestionnaire
from window_design import SimpleWindow
from config_pop_up import ConfigPopUp
import tkinter as tk
import random
from tkinter import messagebox


@LoggerMeta.class_decorator_logger("INFO")
class MainWindow(SimpleWindow):
    """
    This is a window class that represents the main window displayed when we start the application and the one
    we return to
    ...

    Attributes
    ----------
    menu: tk.Menu
        This attribute represents the menu displayed in this window

    file_menu: tk.Menu
        This attribute represents the File menu

    label_main: tk.Label
        This attribute is the big label that is displayed in the window

    button_frame: tk.Frame
        This attribute is a frame to place the buttons New and Load

    button_font
        This attribute sets the font for the buttons New and Load

    button_new: tk.Button
        This attribute is the button New (that starts the process to create a new questionnaire)

    button_load: tk.Button
        This attribute is the button Load (that starts the process to start answering the question in a questionnaire)

    Methods
    -------
    button_new_handler(self):
        This method destroy the main window and start the process to create a new questionnaire, it launches the
        window to provide a name for the questionnaire. This is the command linked to button New

    button_load_handler(self):
        This is the command that is assigned to the button Load. It starts the process to load a questionnaire,
        it displays the window to load the file that contains the questionnaire

    config_handler(self):
        This is the command that is assigned to the menu section Config. It displays the modal to change the
        configuration of the application is

    handler_intro_label(event=None)
        This is the event handler that is linked to the label displaying the name of the application. Every time
        you click there, the colour of the label changes and a message box is displayed
    """
    def button_new_handler(self):
        self.window.destroy()
        new = CreateQuestionnaire()
        new.window.mainloop()

    def button_load_handler(self):
        self.window.destroy()
        load = load_questions_window.LoadQuestionnaire()
        load.window.mainloop()

    def config_handler(self):
        self.window.destroy()
        c = ConfigPopUp(120, 287, "Configuration")
        c.window.mainloop()

    @staticmethod
    def handler_intro_label(event=None):
        r = lambda: random.randint(0, 255)
        new_colour = '#%02X%02X%02X' % (r(), r(), r())
        event.widget["bg"] = new_colour
        messagebox.showinfo("About",
                            "· To create a new questionnaire click the button New. It will display an assistant to "
                            "create it easily.\n· If you have already created a questionnaire, click Load and we will"
                            " allow you to pick which one you want to start.\n")

    def __init__(self):
        SimpleWindow.__init__(self, 230, 650, "Reminda")
        self.menu: tk.Menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.file_menu: tk.Menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu, underline=0)
        self.file_menu.add_command(label="New", command=self.button_new_handler)
        self.file_menu.add_command(label="Load file", command=self.button_load_handler)
        self.file_menu.add_command(label="Exit", command=self.window.destroy)
        self.menu.add_command(label="Config", command=self.config_handler)
        tk.Frame(self.window, height=50).pack()
        self.label_main: tk.Label = tk.Label(self.window,
                                             text="Welcome to Reminda, an app to help you prepare for exams",
                                             font=("Arial Baltic", "15", "bold"), bg="#1A4AC1", fg="white")
        self.label_main["padx"] = 20
        self.label_main["pady"] = 20
        self.label_main.bind("<Button-1>", self.handler_intro_label)
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
