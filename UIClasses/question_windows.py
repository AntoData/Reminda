import abc
import sys
import time
sys.path.append("../BE-Logic")
sys.path.append("../Config")
from Questionnaire import QuestionnaireClass
from QuestionLogic import QuestionClass
from Current_session import CurrentSession
import LoggerMeta
from window_design import SimpleWindow
import tkinter as tk
from tkinter import ttk
import os
import Config.ConfigLogicClass


class QuestionWindowAbs(SimpleWindow, abc.ABC):
    """TO DO"""
    def go_back_to_main(self):
        print("HELLO")

    @abc.abstractmethod
    def __init__(self, question: QuestionClass, i: int, width: int, height: int):
        self.logger.info("We are going to display question: {0}".format(question))
        SimpleWindow.__init__(self, width=width, height=height, title="Question {0}".format(i))
        self.window.resizable(width=False, height=False)
        self.logger.info("Set window to no resizable")
        self.menu = tk.Menu(self.window)
        self.logger.info("Creating menu for this window")
        self.window.config(menu=self.menu)
        self.menu.add_command(label="Go back to main", command=self.go_back_to_main)
        self.logger.info("Added option Go back to main")
        self.menu.add_command(label="Exit", command=sys.exit)
        self.logger.info("Added option Exit")
        self.question: QuestionClass = question
        self.question_label = tk.Label(self.window, width=40, height=10, text=question.question,
                                       font=("TkDefaultFont", 20), wraplength=500)
        self.question_label["pady"] = 30
        self.question_label.pack()
        self.logger.info("Created label for the question")

    @staticmethod
    def reveal_result_labels(obj, correct: bool):
        obj.window.geometry("600x600")
        LoggerMeta.MetaAbsLogger.logger.info("Resized window to 600x600")
        if correct:
            LoggerMeta.MetaAbsLogger.logger.info("Answer was correct")
            CurrentSession.current_session[obj.question.question] = True
            message = "Correct"
            colour = "#128301"
        else:
            LoggerMeta.MetaAbsLogger.logger.info("Answer was not correct")
            CurrentSession.current_session[obj.question.question] = False
            message = "Failed"
            colour = "#BF1602"
        tk.Frame(obj.window, height=15).pack()
        label = tk.Label(obj.window, background=colour, foreground="#FFFFFF", text=message,
                         font=("Century", 15, "bold"))
        label.pack()
        obj.window.after_cancel(obj.window)
        obj.window.after(10000, obj.window.destroy)


class QuestionOneAnswer(QuestionWindowAbs):
    def add_result(self, correct: bool):
        self.logger.info("The awswer was {0}".format(correct))
        CurrentSession.current_session[self.question.question] = correct
        self.logger.info("Disabling buttons correct and failed")
        self.button_correct["state"] = tk.DISABLED
        self.button_correct["background"] = "#DDDEDD"
        self.button_failed["state"] = tk.DISABLED
        self.button_failed["background"] = "#DDDEDD"
        self.logger.info("Removing after method from window")
        self.window.after_cancel(self.window)
        self.logger.info("Window will close in 10 secs")
        self.window.after(10000, self.window.destroy)

    def command_button_correct(self):
        self.add_result(True)

    def command_button_failed(self):
        self.add_result(False)

    def reveal_answer(self):
        self.logger.info("Revealing the answer")
        self.logger.info("Disabling the button Reveal Answer")
        self.button_answer["state"] = tk.DISABLED
        self.logger.info("Adding button Correct and Failed")
        self.answer_label = tk.Label(self.window, width=200, height=6, text=self.question.get_correct_answers(),
                                     wraplength=500, font=("TkDefaultFont", 15))
        self.answer_label.pack()
        frame = tk.Frame(self.window, width=600, height=50)
        frame.pack()
        self.button_correct = tk.Button(frame, text="Correct", background="#128301", activebackground="#128301",
                                   disabledforeground="#BDBDBD", activeforeground="#FFFFFF", foreground="#FFFFFF",
                                   font=("Century", 15, "bold"), command=self.command_button_correct)
        self.button_failed = tk.Button(frame, text="Failed", background="#BF1602", activebackground="#BF1602",
                                  disabledforeground="#BDBDBD", activeforeground="#FFFFFF", foreground="#FFFFFF",
                                  font=("Century", 15, "bold"), command=self.command_button_failed)
        self.button_correct.grid(row=0, column=0)
        tk.Frame(frame, width=50).grid(row=0, column=1)
        self.button_failed.grid(row=0, column=2)
        self.logger.info("Window is resized to 600x650")
        self.window.geometry("600x650")

    def __init__(self, question: QuestionClass, i):
        self.logger.info("We create a 600x450 window")
        QuestionWindowAbs.__init__(self, question, i, 600, 450)
        self.button_answer = tk.Button(self.window, text="Reveal answer", command=self.reveal_answer,)
        self.button_answer.pack()
        self.logger.info("Added button to Reveal Answer")
        self.answer_label = None
        self.button_correct = None
        self.button_failed = None


class QuestionOneAnswerMultiple(QuestionWindowAbs):
    def reveal_result(self):
        self.logger.info("Revealing the correct answer")
        self.logger.info("Disabling all the radio buttons")
        for radio_button in self.radio_buttons:
            radio_button["state"] = tk.DISABLED
        correct: bool = self.answer_group.get() == 1
        self.logger.info("Answer was {0}".format(correct))
        QuestionWindowAbs.reveal_result_labels(self, correct)

    def __init__(self, question: QuestionClass, i):
        QuestionWindowAbs.__init__(self, question, i, 600, 550)
        self.radio_buttons = []
        self.logger.info("We created the IntVar for the group of radio buttons")
        self.answer_group: tk.IntVar = tk.IntVar(0)
        self.logger.info("Our font is size 12")
        self.radio_button_font = ("TkDefaultFont", 12)
        i: int = 0
        for entry in self.question.answers:
            if entry[1]:
                value: int = 1
            else:
                i -= 1
                value: int = i
            self.logger.info("Creating radio button")
            radio_button = tk.Radiobutton(self.window, text=entry[0], value=value, variable=self.answer_group,
                                          command=self.reveal_result, font=self.radio_button_font)
            radio_button.deselect()
            radio_button.pack()
            self.radio_buttons.append(radio_button)


class QuestionTwoAnswersMultiple(QuestionWindowAbs):
    def checking_box(self):
        self.checks_done += 1
        self.logger.info("We have checked {0} boxes already".format(self.checks_done))
        checked_answers: [str] = []
        correct: bool = True
        if self.checks_done == 2:
            self.logger.info("As we have already checked 2 boxes, we are going to check if we checked the correct "
                             "answers")
            i: int = 0
            for check_box in self.check_boxes:
                self.logger.info("We disable the checkbox")
                check_box["state"] = tk.DISABLED
                if self.vars_int[i].get() == 1:
                    self.logger.info("We checked the following answer: {0}".format(check_box["text"]))
                    checked_answers.append(check_box["text"])
                i += 1
            self.logger.info("Now we check if our chosen answers are the correct ones")
            for answer in self.question.get_correct_answers():
                if answer not in checked_answers:
                    correct = False
                    break
            self.logger.info("Our answers were {0}".format(correct))
            QuestionWindowAbs.reveal_result_labels(self, correct)
        else:
            pass

    def __init__(self, question: QuestionClass, i):
        self.logger.info("We create a 600x550 window")
        QuestionWindowAbs.__init__(self, question, i, 600, 550)
        self.check_boxes = []
        self.logger.info("The size of our font is 12")
        self.check_button_font = ("TkDefaultFont", 12)
        self.checks_done: int = 0
        self.vars_int: [tk.IntVar] = []
        for entry in self.question.answers:
            self.logger.info("We create an IntVar for a check box")
            var_int: tk.IntVar = tk.IntVar()
            self.logger.info("We create the checkbox with text {0}".format(entry[0]))
            self.logger.info("With command self.checking_box")
            check_box = tk.Checkbutton(self.window, text=entry[0], font=self.check_button_font,
                                       command=self.checking_box, variable=var_int)
            self.vars_int.append(var_int)
            check_box.pack()
            self.check_boxes.append(check_box)


if __name__ == "__main__":
    q0 = QuestionClass("What do you say to a person in the morning?", "Good morning")
    qa = QuestionOneAnswer(q0, 3)
    qa.window.mainloop()

    q1 = QuestionClass("What of the following ones are Python basic types?", [("Fire", False), ("Bool", True),
                                                                              ("Normal", False), ("Basic", False)])
    qa1 = QuestionOneAnswerMultiple(q1, 4)
    qa1.window.mainloop()
    q2 = QuestionClass("Which of the following countries belong to the European Union",
                                     [("Serbia", False), ("Latvia", True), ("Norway", False), ("Malta", True)])
    qa2 = QuestionTwoAnswersMultiple(q2, 5)
    qa2.window.mainloop()
