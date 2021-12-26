import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
from window_design import SimpleWindow
import tkinter as tk
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
        qualification: float = round((n_correct_questions/total_questions) * 100,1)
        self.colour_font: str = ""
        if 70.0 > qualification >= 50.0:
            self.colour_font = "#FF5733"
        elif qualification >= 70.0:
            self.colour_font = "#128301"
        else:
            self.colour_font = "#BF1602"
        self.qualification_font = ("TkDefaultFont", 30)
        self.label_qualification: tk.Label = tk.Label(self.window, text="You got {0}%".format(qualification),
                                                      font=self.qualification_font, foreground=self.colour_font)
        self.label_qualification.pack(anchor=tk.CENTER)
        tk.Frame(self.window, height=20).pack()
        print(qualification)
        scrollbar = tk.Scrollbar(self.window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.item_font = ("TkDefaultFont", 10)
        mylist = tk.Listbox(self.window, yscrollcommand=scrollbar.set, width=400, font=self.item_font)
        i: int = 0
        for vkey in CurrentSession.current_session.keys():
            result: str = ""
            if CurrentSession.current_session[vkey]:
                result = "Correct"
            else:
                result = "Failed"
            mylist.insert(tk.END, "{0} − {1} − {2}".format(i, vkey, result))
            i += 1

        mylist.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.CENTER)
        scrollbar.config(command=mylist.yview)


if __name__ == "__main__":
    CurrentSession.current_session["What do you say to a person in the morning?"] = False
    CurrentSession.current_session["What of the following ones are Python basic types?"] = False
    CurrentSession.current_session["Which of the following countries belong to the European Union"] = True
    w = ExecutionSummary()
    w.window.mainloop()
