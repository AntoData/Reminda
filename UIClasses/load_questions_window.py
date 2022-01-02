import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
from window_design import SimpleWindow
import tkinter as tk
from tkinter import ttk
import os
import question_windows_handler
import main_window


@LoggerMeta.class_decorator_logger("INFO")
class LoadQuestionnaire(SimpleWindow):
    def exit_button_handler(self):
        self.window.destroy()
        main_window.MainWindow().window.mainloop()

    def command(self):
        filename: str = self.combo.get().replace(".pickle","")
        self.window.destroy()
        q = question_windows_handler.QuestionnaireWindowHandler(filename)

    def __init__(self):
        SimpleWindow.__init__(self, 60, 150, "New Window")
        self.project_folder: str = "{0}/Data/Questionnaires".format(LoggerMeta.MetaLogger.get_root())
        self.dirs = [item for item in os.listdir(self.project_folder)
                     if not os.path.isdir(self.project_folder + "/" + item)]
        self.window.protocol("WM_DELETE_WINDOW", self.exit_button_handler)
        self.combo = ttk.Combobox(self.window, values=self.dirs)
        self.combo.set("Pick an Option")
        self.combo.pack(padx=5, pady=5)
        self.button = tk.Button(self.window, text="Load", command=self.command)
        self.button.pack()


if __name__ == "__main__":
    c = LoadQuestionnaire()
    c.window.mainloop()