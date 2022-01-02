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
        self.input_text_var: tk.StringVar = tk.StringVar("")
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
