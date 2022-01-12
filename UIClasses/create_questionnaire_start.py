from __future__ import annotations
import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
from window_design import SimpleWindow
import tkinter as tk
from question_creation_handler import QuestionCreationHandler
from pathvalidate import sanitize_filepath
import main_window


@LoggerMeta.class_decorator_logger("INFO")
class CreateQuestionnaire(SimpleWindow):
    """
    This is a window class that represents the window that is displayed as the first step to create a new
    questionnaire. The window in which we fill in the name of the new questionnaire and click Save and move
    on to the window to create and add question to the questionnaire
    ...

    Attributes
    ----------
    frame0: tk.Frame
        This frame only adds a little padding at the start of the window

    frame1: tk.Frame
        This attribute is the frame in which we will place the elements in this window

    input_text_var: tk.StringVar
        This attribute is the observable variable used in the input where we fill in the name of the new
        questionnaire and file where it will be saved

    name_input: tk.Entry
        This attribute is the input where we fill in the name of the new questionnaire that will be saved to a
        file of the same name

    frame10: tk.Frame
        This attribute is a frame inside frame1 that will add some padding between the input and the button Save

    button_save: tk.Button
        This attribute is the button Save that will be enabled when we provide a valid file name

    question_creation_loop: QuestionCreationHandler
        This attribute is used to create a QuestionCreationHandler when we click the button Save after filling
        a correct filename

    Methods
    -------
    validate_input_name(self, *args)
        This method is observable trace method assigned to the StringVar linked to the input to provide a valid
        filename. When we provide a valid filename the button is enabled and when we add an invalid character
        the button save is disabled

    button_save_handler(self)
        This method is the command for the button Save. Once we click the button Save, we destroy the current
        window and start a loop of windows to create each of the questions of the questionnaire, one at a time

    enable_button_save(self, id, ix, act):
        This method is also added as a trace to the StringVars that are observable variables to the inputs
        that display and allow the user to update the configuration parameters. In particular, this function
        that will enable the button Save when we change one of the fields

    valid_filename(self, id, ix, act):
        This method is observable trace method assigned to the StringVar linked to the input to provide a valid
        filename. When we press an invalid character, the character is not added to the input

    exit_handler(self):
        This method customizes the default window exit button to destroy the window and display the main window
    """
    def validate_input_name(self, *args):
        self.logger.info("We validate if the input contains only whitespaces")
        if self.input_text_var.get().translate(str.maketrans('', '', ' \n\t\r')) == "":
            self.logger.info("If it does we disable the button Save")
            self.button_save["state"] = tk.DISABLED
        else:
            self.logger.info("Otherwise we enable the button Save")
            self.button_save["state"] = tk.NORMAL

    def button_save_handler(self):
        self.logger.info("We clicked the button Save")
        filename: str = self.input_text_var.get()
        self.logger.info("We got the name of the new file: {0}".format(filename))
        self.logger.info("We destroy the window")
        self.window.destroy()
        self.logger.info("We start the loop to create questions")
        self.question_creation_loop: QuestionCreationHandler = QuestionCreationHandler(filename)

    def valid_filename(self, id, ix, act):
        self.logger.info("If the input is not empty, we check if the filename is valid")
        if self.input_text_var.get() != "":
            self.logger.info("The original string in the input was: {0}".format(self.input_text_var.get()))
            correct_input: str = sanitize_filepath(self.input_text_var.get())
            self.logger.info("After the sanitation is: {0}".format(correct_input))
            self.input_text_var.set(correct_input)

    def button_exit_handler(self):
        self.window.destroy()
        main_window.MainWindow().window.mainloop()

    def __init__(self):
        self.logger.info("We create a 100x300 SimpleWindow with title New questionnaire")
        SimpleWindow.__init__(self, 100, 300, "New questionnaire")
        self.frame0: tk.Frame = tk.Frame(self.window, height=30)
        self.frame0.pack()
        self.frame1: tk.Frame = tk.Frame(self.window, width=30)
        self.frame1.pack(anchor=tk.CENTER)
        self.logger.info("We create an Entry for the filename with a StringVar and two traces in mode w "
                         "validate_input_name and valid_filename and place it")
        self.input_text_var: tk.StringVar = tk.StringVar()
        self.input_text_var.set("")
        self.input_text_var.trace("w", self.validate_input_name)
        self.input_text_var.trace("w", self.valid_filename)
        self.name_input: tk.Entry = tk.Entry(self.frame1, width=25, textvariable=self.input_text_var)
        self.name_input.grid(column=0, row=0, columnspan=3)
        self.frame10: tk.Frame = tk.Frame(self.frame1, width=10)
        self.frame10.grid(column=3, row=0)
        self.logger.info("We create a button called Save with command button_save_handler and place it next to the "
                         "Entry")
        self.button_save: tk.Button = tk.Button(self.frame1, text="Save", state=tk.DISABLED,
                                                command=self.button_save_handler)
        self.button_save.grid(column=4, row=0)
        self.question_creation_loop: QuestionCreationHandler = None
        self.window.protocol("WM_DELETE_WINDOW", self.button_exit_handler)


if __name__ == "__main__":
    cq = CreateQuestionnaire()
    cq.window.mainloop()
