import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
from window_design import SimpleWindow
import tkinter as tk
from Current_session import CurrentSession
import main_window

@LoggerMeta.class_decorator_logger("INFO")
class ExecutionSummary(SimpleWindow):
    """
        This is a window class that represents the window that is displayed when we have gone through all the questions
        in the questionnaire and we display the results
        ...

        Attributes
        ----------
        total_questions: int
            Number of questions that compose the questionnaire

        correct_questions
            This is an array of string that contains all the questions that were answered correctly

        n_correct_questions: int
            Number of questions answered correctly

        qualification: float
            This attribute is the result of rounding to one decimals the following:
            (n_correct_questions/total_questions) * 100

        colour_font: str
            This attribute will set the colour of the font depending on the qualifications we got in the
            message that displays the results of the test

        qualification_font
            This attribute sets the font for the message that displays the results we got in the test

        label_qualification: tk.Label
            This label displays a message that contains the result of the test

        scrollbar: tk.Scrollbar
            This attribute is the scrollbar in the list that contains each question and the result (if answered
            correctly or not)

        item_font:
            This attribute sets the font of the questions with their results we will display in the list

        mylist: tk.Listbox
            This attribute is the list in which each question with its result is displayed

        Methods
        -------
        exit_handler(self):
            This method customizes the default window exit button to destroy the window and display the main window
        """
    def exit_button_handler(self):
        self.window.destroy()
        main_window.MainWindow().window.mainloop()

    def __init__(self):
        SimpleWindow.__init__(self, 400, 400, "Summary")
        self.logger.info("400x400 window created")
        tk.Frame(self.window, height=20).pack()
        total_questions: int = len(CurrentSession.current_session)
        self.logger.info("The questionnaire had {0} questions".format(total_questions))
        correct_questions = [x for x in CurrentSession.current_session.keys() if CurrentSession.current_session[x]]
        n_correct_questions: int = len(correct_questions)
        self.logger.info("You got {0} answers correct".format(n_correct_questions))
        qualification: float = round((n_correct_questions/total_questions) * 100, 1)
        self.logger.info("You got {0}%".format(qualification))
        self.colour_font: str = ""
        if 70.0 > qualification >= 50.0:
            self.colour_font = "#FF5733"
        elif qualification >= 70.0:
            self.colour_font = "#128301"
        else:
            self.colour_font = "#BF1602"
        self.logger.info("We set the font for the qualification label")
        self.qualification_font = ("TkDefaultFont", 30)
        self.label_qualification: tk.Label = tk.Label(self.window, text="You got {0}%".format(qualification),
                                                      font=self.qualification_font, foreground=self.colour_font)
        self.label_qualification.pack(anchor=tk.CENTER)
        self.logger.info("We created a label to display the qualification and packed it")
        tk.Frame(self.window, height=20).pack()
        self.logger.info("We create and empty frame for separation")
        scrollbar = tk.Scrollbar(self.window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.logger.info("We place the scrollbar")
        self.item_font = ("TkDefaultFont", 10)
        mylist = tk.Listbox(self.window, yscrollcommand=scrollbar.set, width=400, font=self.item_font)
        self.logger.info("We create the ListBox for this view and set the scrollbar as y scrollbar")
        i: int = 1
        self.logger.info("We go through every question")
        for vkey in CurrentSession.current_session.keys():
            result: str = ""
            if CurrentSession.current_session[vkey]:
                result = "Correct"
            elif CurrentSession.current_session[vkey] is None:
                result = "N/A"
            else:
                result = "Failed"
            loggerline: str = "We insert element: {0} − {1} − {2}".format(i, vkey, result)
            self.logger.info(loggerline.encode("UTF−8"))
            mylist.insert(tk.END, "{0} − {1} − {2}".format(i, vkey, result))
            i += 1

        mylist.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.CENTER)
        self.logger.info("We pack the list")
        scrollbar.config(command=mylist.yview)
        self.logger.info("Finish configuration for scrollbar")
        self.window.protocol("WM_DELETE_WINDOW", self.exit_button_handler)


if __name__ == "__main__":
    CurrentSession.current_session["What do you say to a person in the morning?"] = False
    CurrentSession.current_session["What of the following ones are Python basic types?"] = False
    CurrentSession.current_session["Which of the following countries belong to the European Union"] = True
    w = ExecutionSummary()
    w.window.mainloop()
