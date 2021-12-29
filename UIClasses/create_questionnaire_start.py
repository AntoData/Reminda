from __future__ import annotations
import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
from Questionnaire import QuestionnaireClass
from Current_session import CurrentSession
from QuestionLogic import QuestionClass
from window_design import SimpleWindow
import tkinter as tk
from question_creation_handler import QuestionCreationHandler


class CreateQuestionnaire(SimpleWindow):
    def validate_input_name(self, *args):
        if self.input_text_var.get().translate(str.maketrans('', '', ' \n\t\r')) == "":
            self.button_save["state"] = tk.DISABLED
        else:
            self.button_save["state"] = tk.NORMAL

    def button_save_handler(self):
        filename: str = self.input_text_var.get()
        self.window.destroy()
        question_creation_loop: QuestionCreationHandler = QuestionCreationHandler(filename)


    def __init__(self):
        SimpleWindow.__init__(self, 100, 300, "New questionnaire")
        self.frame0: tk.Frame = tk.Frame(self.window, height=30)
        self.frame0.pack()
        self.frame1: tk.Frame = tk.Frame(self.window, width=30)
        self.frame1.pack(anchor=tk.CENTER)
        self.input_text_var: tk.StringVar = tk.StringVar("")
        self.input_text_var.trace("w", self.validate_input_name)
        self.name_input: tk.Entry = tk.Entry(self.frame1, width=25, textvariable=self.input_text_var)
        self.name_input.grid(column=0, row=0, columnspan=3)
        self.frame10: tk.Frame = tk.Frame(self.frame1, width=10)
        self.frame10.grid(column=3, row=0)
        self.button_save: tk.Button = tk.Button(self.frame1, text="Save", state=tk.DISABLED,
                                                command=self.button_save_handler)
        self.button_save.grid(column=4, row=0)

if __name__ == "__main__":
    cq = CreateQuestionnaire()
    cq.window.mainloop()