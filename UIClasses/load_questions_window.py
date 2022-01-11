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
    """
    This is a window class that represents the window that is displayed when we want to load a questionnaire to start
    a test and answer the questions
    ...

    Attributes
    ----------
    project_folder: str
        This contains the full path to the project/file we want to load

    dirs: [str]
        This attribute contains a list with all the files that contain questionnaires

    combo: ttk.Combobox
        This attribute is the list with all the questionnaires we found in the default directory

    button: tk.Button
        This attribute is the button that start the test loading the file we selected and starting
        the loop of questions of that questionnaire

    Methods
    -------
    exit_button_handler(self):
        This method customizes the default window exit button to destroy the window and display the main window

    command(self):
        This is the command that is assigned to the button Load. It loads the file selected, creating a questionnaire
        and start the loop that goes through all the questions in that questionnaire
    """

    def exit_button_handler(self):
        self.window.destroy()
        main_window.MainWindow().window.mainloop()

    def command(self):
        filename: str = self.combo.get().replace(".pickle", "")
        self.window.destroy()
        q = question_windows_handler.QuestionnaireWindowHandler(filename)

    def __init__(self):
        SimpleWindow.__init__(self, 60, 150, "New Window")
        try:
            self.project_folder: str = "{0}/Data/Questionnaires".format(".")
            self.dirs = [item for item in os.listdir(self.project_folder)
                         if not os.path.isdir(self.project_folder + "/" + item)]
        except FileNotFoundError:
            self.project_folder: str = "{0}/Data/Questionnaires".format("..")
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
