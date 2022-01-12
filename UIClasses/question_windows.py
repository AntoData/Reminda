import abc
import sys

sys.path.append("../BE-Logic")
sys.path.append("../Config")
from QuestionLogic import QuestionClass
from Current_session import CurrentSession
import LoggerMeta
from window_design import SimpleWindow
import tkinter as tk
from tkinter import ttk
import main_window
import tkinter.font as tkfont


@LoggerMeta.class_decorator_logger("INFO")
class QuestionWindowAbs(SimpleWindow, abc.ABC):
    """
    This is an abstract class that is the base for all our window question classes
    ...

    Attributes
    ----------
    menu: tk.Menu
        This attribute is the main menu in the window

    question: QuestionClass
        This attribute is the object that contains all the information about the question we are displaying

    question_label: tk.Label
        This attribute is the label that will display the question we want the user to answer

    container = ttk.Frame
        Frame that will contain the possible answers to the question

    canvas: tk.Canvas
        This canvas is used to create a scrollable frame to display the possible questions

    scrollbar: ttk.Scrollbar
        This is the scrollbar for the scrollable frame that will contain the possible answers

    scrollable_frame: ttk.Frame
        This is the scrollable frame that will contain all the possible answers to the question

    answer_font: tkfont.Font
        This sets us the font for the different answers displayed

    padding_function:
        This attribute is a function that will return how much padding an answer has to add to fit the scrollable
        frame

    Methods
    -------
    go_back_to_main(self):
        This method is the command for the option Back to main of the menu

    reveal_result_labels(obj, correct: bool):
        This static method is used to reveal if we answer the multiple choice question correctly or not and display
        the correct label

    pack_scrollable_widgets(self):
        This method executes the geometry manager pack for all elements that build the scrollable frame
    """
    def go_back_to_main(self):
        self.window.destroy()
        main_window.MainWindow().window.mainloop()

    @abc.abstractmethod
    def __init__(self, question: QuestionClass, i: int, width: int, height: int):
        self.logger.info("We are going to display question: {0}".format(question))
        SimpleWindow.__init__(self, width=width, height=height, title="Question {0}".format(i))
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
        self.container = ttk.Frame(self.window, width=width - 20)
        self.canvas = tk.Canvas(self.container, width=width - 20)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, width=width - 20)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.answer_font: tkfont.Font = None
        self.padding_function = lambda x: (self.scrollable_frame["width"] - self.answer_font.measure(x[0])) / 2 \
            if len(x[0]) < 540 else 5

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
        label = tk.Label(obj.scrollable_frame, background=colour, foreground="#FFFFFF", text=message,
                         font=("Century", 15, "bold"))
        label.pack()
        try:
            obj.window.after_cancel(obj.func_after)
        except Exception as e:
            obj.logger.warning("Error while trying to cancel func after: {0}".format(e))
        obj.window.after(10000, obj.window.destroy)

    def pack_scrollable_widgets(self):
        self.container.pack()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


class QuestionOneAnswer(QuestionWindowAbs):
    """
    This is a window class that display a question that only has one possible answer that we have to reveal
    and then we give the user the option to click if he answered correctly or not
    ...

    Attributes
    ----------
    button_answer: tk.Button
        This attribute is the button to reveal the only answer

    answer_label
        This attribute is a label that displays the only answer for this question after we reveal it

    button_correct: tk.Button
        This attribute is the button that we click when we answered the question correctly after revealing
        the answer

    button_failed: tk.Button
        This attribute is the button that we click when we answered the question incorrectly after revealing
        the answer

    Methods
    -------
    add_result(self, correct: bool):
        This method adds the result of this question to the current execution session object of the loop

    command_button_correct(self):
        This method adds the result of this question to the current execution session object of the loop as correct

    command_button_failed(self):
        This method adds the result of this question to the current execution session object of the loop as incorrect

    reveal_answer(self):
        This method is the command linked to the button Reveal Answer that will display the answer and the buttons
        Correct and Failed
    """
    def add_result(self, correct: bool):
        self.logger.info("The awswer was {0}".format(correct))
        CurrentSession.current_session[self.question.question] = correct
        self.logger.info("Disabling buttons correct and failed")
        self.button_correct["state"] = tk.DISABLED
        self.button_correct["background"] = "#DDDEDD"
        self.button_failed["state"] = tk.DISABLED
        self.button_failed["background"] = "#DDDEDD"
        self.logger.info("Removing after method from window")
        try:
            self.window.after_cancel(self.func_after)
        except Exception as e:
            self.logger.warning("Error while trying to remove after func: {0}".format(e))
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
        self.container["width"] = 510
        self.canvas["width"] = 510
        self.scrollable_frame["width"] = 510
        self.answer_font = tkfont.Font(family="TkDefaultFont", size=15)
        self.answer_label = tk.Label(self.scrollable_frame, width=200, height=6,
                                     text=self.question.get_correct_answers(),
                                     wraplength=500, font=self.answer_font)
        self.answer_label.pack()
        frame = tk.Frame(self.scrollable_frame, width=600, height=50)
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
        self.scrollable_frame.pack()
        self.pack_scrollable_widgets()
        self.logger.info("Window is resized to 600x650")
        self.window.geometry("600x650")

    def __init__(self, question: QuestionClass, i):
        self.logger.info("We create a 600x450 window")
        QuestionWindowAbs.__init__(self, question, i, 600, 450)
        self.button_answer = tk.Button(self.window, text="Reveal answer", command=self.reveal_answer, )
        self.button_answer.pack()
        self.logger.info("Added button to Reveal Answer")
        self.answer_label = None
        self.button_correct = None
        self.button_failed = None


class QuestionOneAnswerMultiple(QuestionWindowAbs):
    """
    This is a window class that display a question that only has four possible answers and only one of them is correct
    The answers are displayed as radio buttons
    ...

    Attributes
    ----------
    radio_buttons: [tk.Radiobutton]
        This attribute is a list that will contain all 4 radio buttons that represent the different possible answers

    answer_group: tk.IntVar
        This attribute is an observable IntVar that is assigned to all radio buttons so all of them belong to the
        same group (so we can only answer clicking one answer)

    answer_font = tkfont.Font
        This attribute sets the font for the four possible answers in the radio buttons

    Methods
    -------
    reveal_result(self):
        This is the command linked to all radio buttons that will disable them and display if we answered
        the question correctly or not
    """
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
        self.answer_group: tk.IntVar = tk.IntVar()
        self.answer_group.set(0)
        self.logger.info("Our font is size 12")
        self.answer_font = tkfont.Font(family="TkDefaultFont", size=12)
        i: int = 0
        for entry in self.question.answers:
            if entry[1]:
                value: int = 1
            else:
                i -= 1
                value: int = i
            self.logger.info("Creating radio button")
            radio_button = tk.Radiobutton(self.scrollable_frame, text=entry[0], value=value, variable=self.answer_group,
                                          command=self.reveal_result, font=self.answer_font,
                                          padx=self.padding_function(entry), wraplength=540, anchor=tk.CENTER)
            radio_button.deselect()
            radio_button.pack()
            self.radio_buttons.append(radio_button)
        self.pack_scrollable_widgets()


class QuestionTwoAnswersMultiple(QuestionWindowAbs):
    """
    This is a window class that display a question that only has four possible answers and only two of them is correct
    The answers are displayed as radio buttons
    ...

    Attributes
    ----------
    check_boxes: [tk.Checkbutton]
        This attribute is a list that will contain all 4 check buttons that represent the different possible answers

    answer_font = tkfont.Font
        This attribute sets the font for the four possible answers in the radio buttons

    checks_done: int
        If 1 it means we have checked 2 boxes

    vars_int: [tk.IntVar]
        This attribute is a list that contain all four observable IntVar linked to the check buttons that display
        the four possible question

    Methods
    -------
    checking_box(self):
        This is the command linked to all check buttons that will check if two buttons were selected if so we will
        disable the check buttons and display if we answered correctly or we failed the question
    """
    def checking_box(self):
        self.checks_done = sum([v.get() for v in self.vars_int])
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
        self.answer_font = tkfont.Font(family="TkDefaultFont", size=12, weight="normal")
        self.checks_done: int = 0
        self.vars_int: [tk.IntVar] = []
        for entry in self.question.answers:
            self.logger.info("We create an IntVar for a check box")
            var_int: tk.IntVar = tk.IntVar()
            self.logger.info("We create the checkbox with text {0}".format(entry[0]))
            self.logger.info("With command self.checking_box")
            check_box = tk.Checkbutton(self.scrollable_frame, text=entry[0], font=self.answer_font,
                                       command=self.checking_box, variable=var_int, wraplength=540,
                                       padx=self.padding_function(entry), anchor=tk.CENTER)
            self.vars_int.append(var_int)
            check_box.pack(in_=self.scrollable_frame, anchor="c")
            self.check_boxes.append(check_box)
            self.container.pack()
            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")


if __name__ == "__main__":
    q0 = QuestionClass("What do you say to a person in the morning?", "Well, it depends on the day. Good morning when "
                                                                      "I am pumped about the day. Just morning when I "
                                                                      "tired. Nothing when I am sad. Also nothing if "
                                                                      "I don't know that person. Hi if it is something "
                                                                      "familiar. It really depends on so many factors. "
                                                                      "The best thing is to smile to that person and "
                                                                      "move on.")
    qa = QuestionOneAnswer(q0, 3)
    qa.window.mainloop()

    q1 = QuestionClass("What of the following ones are Python basic types?", [("Fire", False), ("Bool", True),
                                                                              ("Normal", False), ("Basic", False)])
    qa1 = QuestionOneAnswerMultiple(q1, 4)
    qa1.window.mainloop()
    q2 = QuestionClass("Which of the following countries belong to the European Union",
                       [("Norway entered the EU in 1995. It is one of the core members of the European "
                         "Union, being a bigger contributor than Germany. Norway has hold the presidency"
                         "of the European Union Several times ", False), ("Latvia entered the European "
                                                                          "Union in 2004. It is one of the most "
                                                                          "promising economies. It has a land border"
                                                                          " with Russia and access to the Baltic Sea. "
                                                                          "Riga is one of the most important cities in "
                                                                          "the area.", True),
                        ("Serbia entered the European Union in 2007. It has become the biggest supporter of the "
                         "European Union in the area. 90% of its population are glad Serbia entered the European Union."
                         " Belgrade has plans to ask to hold some institutions that were previously located in the UK."
                         , False),
                        ("Malta entered the European Union is 2004. A nation fully integrated in the European Union "
                         "now. It is also a country whose currency is the Euro. Before it was the Maltese Lira.",
                         True)])
    qa2 = QuestionTwoAnswersMultiple(q2, 5)
    qa2.window.mainloop()
    q3 = QuestionClass("What of the following ones are Python basic types?",
                       [("We didn't start the fire", False), ("Bool", True),
                        ("Normal is not how I would describe "
                         "this test", False), ("Basic. But this is a basic question too. If you don't know this, "
                                               "review the basics of Python. Maybe going back to PCEP would be "
                                               "a good idea. A basic type might be a good idea too. But do we have "
                                               "it currently? If you think so, select this one.", False)])
    qa3 = QuestionTwoAnswersMultiple(q3, 6)
    qa3.window.mainloop()
    q4 = QuestionClass("Which of the following countries belong to the European Union",
                       [("Norway entered the EU in 1995. It is one of the core members of the European "
                         "Union, being a bigger contributor than Germany. Norway has hold the presidency"
                         "of the European Union Several times ", False), ("Latvia entered the European "
                                                                          "Union in 2004. It is one of the most "
                                                                          "promising economies. It has a land border"
                                                                          " with Russia and access to the Baltic Sea. "
                                                                          "Riga is one of the most important cities in "
                                                                          "the area.", True),
                        ("Serbia entered the European Union in 2007. It has become the biggest supporter of the "
                         "European Union in the area. 90% of its population are glad Serbia entered the European Union."
                         " Belgrade has plans to ask to hold some institutions that were previously located in the UK."
                         , False),
                        ("San Marino entered the European Union is 2004. A nation fully integrated in the European "
                         "Union now. It is also a country whose currency is the Euro. Before it was the Lira.",
                         False)])
    qa4 = QuestionOneAnswerMultiple(q4, 6)
    qa4.window.mainloop()

