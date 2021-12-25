import sys
import re
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
import Config.ConfigLogicClass
from window_design import SimpleWindow
import tkinter as tk
from tkinter import ttk
import abc
from tkinter import messagebox


@LoggerMeta.class_decorator_logger("INFO")
class ConfigPopUp(SimpleWindow):
    label_text_secs_to_answer: str = "Seconds to answer"
    label_text_secs_between_questions: str = "Seconds between questions"

    def handler_button_save(self):
        self.logger.info("We pressed the button Save")
        old_secs_to_answers: int = Config.ConfigLogicClass.ConfigClass.get_secs_to_answer()
        old_secs_between_questions: int = Config.ConfigLogicClass.ConfigClass.get_secs_between_questions()
        new_secs_to_answers: int = int(self.secs_to_answer_StringVar.get())
        new_secs_between_questions: int = int(self.secs_between_questions_StringVar.get())
        if old_secs_to_answers != new_secs_to_answers:
            self.logger.info("Seconds to answer has been updated")
            Config.ConfigLogicClass.ConfigClass.set_secs_to_answer(new_secs_to_answers)
        if old_secs_between_questions != new_secs_between_questions:
            self.logger.info("Seconds between questions has been updated")
            Config.ConfigLogicClass.ConfigClass.set_secs_between_questions(new_secs_between_questions)
        self.logger.info("Button Save is disabled now")
        self.button_save.config(state=tk.DISABLED)
        messagebox.showinfo("Changes Saved", "Your changes in configuration have been saved")

    def only_digits(self, id, ix, act):
        if self.secs_to_answer_StringVar.get() != "":
            secs_to_answer_digits = str(re.search(r"\d+", self.secs_to_answer_StringVar.get()).group(0))
            self.secs_to_answer_StringVar.set(secs_to_answer_digits)
        if self.secs_between_questions_StringVar.get() != "":
            secs_between_questions = str(re.search(r"\d+", self.secs_between_questions_StringVar.get()).group(0))
            self.secs_between_questions_StringVar.set(secs_between_questions)

    def enable_button_save(self, id, ix, act):
        old_secs_to_answers: str = str(Config.ConfigLogicClass.ConfigClass.get_secs_to_answer())
        old_secs_between_questions: str = str(Config.ConfigLogicClass.ConfigClass.get_secs_between_questions())
        new_secs_to_answers: str = str(self.secs_to_answer_StringVar.get())
        new_secs_between_questions: str = str(self.secs_between_questions_StringVar.get())
        if (old_secs_to_answers != new_secs_to_answers or old_secs_between_questions != new_secs_between_questions)\
                and (self.secs_to_answer_StringVar.get() != "" and self.secs_between_questions_StringVar.get() != ""):
            self.logger.info("A value has been updated so we enable the button Save")
            self.button_save.config(state=tk.ACTIVE)
        elif self.secs_to_answer_StringVar.get() == "" or self.secs_between_questions_StringVar.get() == "":
            self.logger.info("We deleted one of the values so we disable the button Save again")
            self.button_save["state"] = tk.DISABLED

    def __init__(self, height: int, width: int, title: str):
        SimpleWindow.__init__(self, height, width, title)
        label_secs_to_answer = tk.Label(self.window, text=ConfigPopUp.label_text_secs_to_answer)
        label_secs_to_answer.grid(column=0, row=0, padx=2)
        self.secs_to_answer_StringVar = tk.StringVar(self.window,
                                                     value=str(Config.ConfigLogicClass.ConfigClass.secs_to_answer))
        self.secs_to_answer_StringVar.trace("w", callback=self.only_digits)
        self.secs_to_answer_StringVar.trace("w", callback=self.enable_button_save)
        entry_secs_to_answer = tk.Entry(self.window, textvariable=self.secs_to_answer_StringVar)
        entry_secs_to_answer.grid(column=1, row=0)
        label_secs_between_questions = tk.Label(self.window, text=ConfigPopUp.label_text_secs_between_questions)
        label_secs_between_questions.grid(column=0, row=1, padx=2)
        self.secs_between_questions_StringVar = tk.StringVar(
            self.window, value=str(Config.ConfigLogicClass.ConfigClass.secs_between_questions))
        self.secs_between_questions_StringVar.trace("w", callback=self.only_digits)
        self.secs_between_questions_StringVar.trace("w", self.enable_button_save)
        entry_secs_between_questions = tk.Entry(self.window, textvariable=self.secs_between_questions_StringVar)
        entry_secs_between_questions.grid(column=1, row=1)
        self.font_button_save = ("Century", 14, "bold")
        self.button_save = tk.Button(self.window, text="Save", command=self.handler_button_save, state=tk.DISABLED,
                                     background="#128301", activebackground="#128301", disabledforeground="#CACACA",
                                     activeforeground="#FFFFFF", foreground="#FFFFFF", font=self.font_button_save,
                                     padx=2, pady=2)
        self.button_save.grid(row=2, columnspan=2, padx=10, pady=10)


if __name__ == "__main__":
    c = ConfigPopUp(120, 287, "Configuration")
    c.window.mainloop()
