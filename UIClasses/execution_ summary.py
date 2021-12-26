import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
from window_design import SimpleWindow
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
from question_windows_handler import QuestionnaireWindowHandler
from Questionnaire import QuestionnaireClass
from Current_session import CurrentSession


class ExecutionSummary(SimpleWindow):
    def __init__(self):
        SimpleWindow.__init__(self, 400, 400, "Summary")
        tk.Frame(self.window, height=20).pack()
        total_questions: int = len(CurrentSession.current_session)
        correct_questions = [x for x in CurrentSession.current_session.keys() if CurrentSession.current_session[x]]
        n_correct_questions: int = len(correct_questions)
        qualification: int = round((n_correct_questions/total_questions) * 100,1)
        self.qualification_font = ("TkDefaultFont", 30)
        self.label_qualification: tk.Label = tk.Label(self.window,text="You got {0}%".format(qualification),
                                                      font=self.qualification_font)
        self.label_qualification.pack(anchor=tk.CENTER)
        tk.Frame(self.window, height=20).pack()
        print(qualification)
        scrollbar = Scrollbar(self.window)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.item_font = ("TkDefaultFont", 10)
        mylist = Listbox(self.window, yscrollcommand=scrollbar.set, width=400, font=self.item_font)
        i: int = 0
        for vkey in CurrentSession.current_session.keys():
            result: str = ""
            if CurrentSession.current_session[vkey]:
                result = "Correct"
            else:
                result = "Failed"
            mylist.insert(END, "{0} − {1} − {2}".format(i, vkey, result))
            i += 1

        mylist.pack(side=LEFT, fill=BOTH, anchor=CENTER)
        scrollbar.config(command=mylist.yview)

        mainloop()

if __name__ == "__main__":
    CurrentSession.current_session["What do you say to a person in the morning?"] = True
    CurrentSession.current_session["What of the following ones are Python basic types?"] = False
    CurrentSession.current_session["Which of the following countries belong to the European Union"] = True
    w = ExecutionSummary()
    w.window.mainloop()