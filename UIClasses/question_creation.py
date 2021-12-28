from __future__ import annotations

import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
from Questionnaire import QuestionnaireClass
from Current_session import CurrentSession
from QuestionLogic import QuestionClass
from window_design import SimpleWindow
import tkinter as tk


class QuestionCreation(SimpleWindow):
    def question_filled(self):
        return self.question_text.get("0.0", tk.END).translate(str.maketrans('', '', ' \n\t\r')) != ""

    def all_answers_filled_in(self):
        activate: bool = True
        for answer_string_var in self.answers_stringVars:
            if answer_string_var.get().translate(str.maketrans('', '', ' \n\t\r')) == "":
                activate = False
                break
        return activate

    def check_correct_number_checked(self):
        if self.intVars is not None:
            r = len([x.get() for x in self.intVars if x.get() != 0])
            return r == 2 or r == 1
        else:
            return True

    def single_answer_display(self):
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.answer_stringVar1: tk.StringVar = tk.StringVar("")
        self.answer_stringVar1.trace("w", self.answers_entry_command)
        self.first_answer = tk.Entry(self.frame, width=67, textvariable=self.answer_stringVar1)
        self.answers_stringVars: [tk.StringVar] = [self.answer_stringVar1]
        self.first_answer.grid(columnspan=4, column=0, row=0)
        tk.Frame(self.frame, width=15).grid(column=4, row=0)
        self.but = tk.Button(self.frame, text="Add +", command=self.add_more)
        self.but.grid(column=5, row=0)
        self.frame2 = tk.Frame(self.window)
        self.frame2.pack()
        self.button_save = tk.Button(self.frame2, text="Save", state=tk.DISABLED, command=self.button_save_handler)
        self.button_exit = tk.Button(self.frame2, text="Exit")
        self.button_save.grid(row=0, column=0)
        self.button_exit.grid(row=0, column=1)

    def answers_entry_command(self, *args):
        self.button_save["state"] = tk.DISABLED
        if self.check_boxes is not None:
            for checkbox in self.check_boxes:
                checkbox["state"] = tk.DISABLED
        activate = self.all_answers_filled_in()
        if activate and self.check_boxes is not None:
            for checkbox in self.check_boxes:
                checkbox["state"] = tk.NORMAL
        elif activate and self.question_filled() and self.check_boxes is None:
            self.button_save["state"] = tk.NORMAL

    def check_boxes_validation(self):
        if self.check_correct_number_checked() and self.all_answers_filled_in() and self.question_filled():
            self.button_save["state"] = tk.NORMAL
        else:
            self.button_save["state"] = tk.DISABLED

    def add_more(self):
        self.button_save["state"] = tk.DISABLED
        print(self.question_text.get("1.0", "end-1c"))
        self.answer_stringVar.set("Answers")
        self.but.destroy()
        self.check_box_var1 = tk.IntVar()
        self.check_box_1 = tk.Checkbutton(self.frame, variable=self.check_box_var1, state=tk.DISABLED,
                                          command=self.check_boxes_validation)
        self.check_box_1.grid(row=0, column=5)
        self.answers: [tk.Entry] = [self.first_answer]
        self.check_boxes: [tk.Checkbutton] = [self.check_box_1]
        self.intVars: [tk.IntVar] = [self.check_box_var1]
        for i in range(1, 4):
            string_var = tk.StringVar("")
            string_var.trace("w", self.answers_entry_command)
            answer = tk.Entry(self.frame, width=67, textvariable=string_var)
            answer.grid(columnspan=4, column=0, row=i)
            self.answers_stringVars.append(string_var)
            tk.Frame(self.frame, width=15).grid(column=4, row=0)
            check_box_var_i = tk.IntVar(0)
            checkbox = tk.Checkbutton(self.frame, variable=check_box_var_i, state=tk.DISABLED,
                                      command=self.check_boxes_validation)
            checkbox.grid(column=5, row=i)
            self.answers.append(answer)
            self.check_boxes.append(checkbox)
            self.intVars.append(check_box_var_i)
        self.button_less = tk.Button(self.frame2, text="Show -", command=self.show_less_handler)
        self.button_less.grid(row=0, column=3)

    def show_less_handler(self):
        self.frame.destroy()
        self.frame2.destroy()
        self.single_answer_display()

    def check_button_save_question(self):
        if self.question_filled() and self.check_correct_number_checked() and self.all_answers_filled_in():
            self.button_save["state"] = tk.NORMAL
        else:
            self.button_save["state"] = tk.DISABLED
        self.question_text.after(1, self.check_button_save_question)

    def gather_answers(self):
        answers_str: (str | [(str, bool)]) = []
        if self.check_boxes is not None:
            i: int = 0
            for stringVarAnswer in self.answers_stringVars:
                answers_str.append((stringVarAnswer.get(), self.intVars[i].get() == 1))
                i += 1
        else:
            answers_str = self.answer_stringVar1.get()
        return answers_str

    def button_save_handler(self):
        answers_str: str | [(str, bool)] = self.gather_answers()
        question_str: str = self.question_text.get("1.0", "end-1c").strip()
        self.question_result = QuestionClass(question_str, answers_str)
        print(self.question_result)
        self.window.destroy()

    def __init__(self, title):
        SimpleWindow.__init__(self, 600, 500, title)
        self.font = ("TkDefaultFont", 14)
        self.check_boxes = None
        self.question_label: tk.Label = tk.Label(self.window, text="Question", font=self.font)
        self.question_label.pack()
        self.question_text: tk.Text = tk.Text(self.window, width=57, height=7)
        self.question_text.after(1, self.check_button_save_question)
        self.question_text.pack()
        tk.Frame(self.window, height=20).pack()
        self.answer_stringVar = tk.StringVar("")
        self.answer_stringVar.set("Answer")
        self.label_answer = tk.Label(self.window, textvariable=self.answer_stringVar, font=self.font)
        self.label_answer.pack()
        tk.Frame(self.window, height=20)
        self.frame = None
        self.answer_stringVar1: tk.StringVar = None
        self.first_answer = None
        self.answers_stringVars: [tk.StringVar] = None
        self.but = None
        self.frame2 = None
        self.button_save = None
        self.button_exit = None
        self.button_less = None
        self.check_box_var1 = None
        self.check_box_1 = None
        self.answers = None
        self.intVars = None
        self.question_result: QuestionClass = None
        self.single_answer_display()


if __name__ == "__main__":
    qc = QuestionCreation("Example")
    qc.window.mainloop()