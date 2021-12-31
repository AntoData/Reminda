from __future__ import annotations
import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
from Questionnaire import QuestionnaireClass
from Current_session import CurrentSession
from QuestionLogic import QuestionClass
from window_design import SimpleWindow
import tkinter as tk


@LoggerMeta.class_decorator_logger("INFO")
class QuestionCreation(SimpleWindow):
    exit: bool = False

    def question_filled(self):
        self.logger.info("We check if the textarea for the question have been filed properly")
        self.logger.info("That means the text is not only whitespaces")
        self.logger.info("This is one of the conditions to enable the button Save")
        return self.question_text.get("0.0", tk.END).translate(str.maketrans('', '', ' \n\t\r')) != ""

    def all_answers_filled_in(self):
        self.logger.info("We check if all answers have been filled in properly")
        self.logger.info("We suppose first that they have, so we set the flag activate to True")
        activate: bool = True
        self.logger.info("We go through each StringVar that has been set in each answer input")
        for answer_string_var in self.answers_stringVars:
            self.logger.info("If this input contains only whitespaces")
            if answer_string_var.get().translate(str.maketrans('', '', ' \n\t\r')) == "":
                self.logger.info("That means not all answers have been filled in correctly")
                self.logger.info("Then we set the flag activate to False")
                activate = False
                self.logger.info("In this case we don't have to keep looking")
                break
        self.logger.info("The result of the flag activate is {0}".format(activate))
        self.logger.info("If this condition is true, the checkboxes to set answers as correct is enabled")
        return activate

    def check_correct_number_checked(self):
        self.logger.info("Now we check if we checked one or two boxes")
        self.logger.info("If the attribute intVars is not None, it means the are displaying the view with 4 possible"
                         "answers")
        if self.intVars is not None:
            self.logger.info("We get how many boxes we checked")
            r = len([x.get() for x in self.intVars if x.get() != 0])
            self.logger.info("We checked {0} boxes".format(r))
            self.logger.info("Then we return {0}".format(r == 2 or r == 1))
            return r == 2 or r == 1
        else:
            self.logger.info("In this case, we are displaying the view for just one answer, so we return True")
            return True

    def single_answer_display(self):
        self.logger.info("We proceed to display the view for just one answer")
        self.logger.info("We create and pack a Frame")
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.logger.info("We create a StringVar for the unique answer")
        self.answer_stringVar1: tk.StringVar = tk.StringVar("")
        self.logger.info("We set a trace when setting that StringVar and set as command the function "
                         "answers_entry_command")
        self.answer_stringVar1.trace("w", self.answers_entry_command)
        self.logger.info("We create and Entry called first_answer to be filled in with the answer")
        self.first_answer = tk.Entry(self.frame, width=67, textvariable=self.answer_stringVar1)
        self.logger.info("We set a list of StringVar for the answers, but only contains the StringVar for our unique"
                         "Entry for the answer")
        self.answers_stringVars: [tk.StringVar] = [self.answer_stringVar1]
        self.logger.info("We place the Entry using Grid")
        self.first_answer.grid(columnspan=4, column=0, row=0)
        self.logger.info("We add and place a void Frame to give padding between the Entry and a new button")
        tk.Frame(self.frame, width=15).grid(column=4, row=0)
        self.logger.info("We create a button to display more answers to fill called Add + with command add_more")
        self.but = tk.Button(self.frame, text="Add +", command=self.add_more)
        self.logger.info("We place the button in the same line")
        self.but.grid(column=5, row=0)
        self.logger.info("We create a new frame and place it below")
        self.frame2 = tk.Frame(self.window)
        self.frame2.pack()
        self.logger.info("We create a button called Save with command button_save_handler disabled by default")
        self.button_save = tk.Button(self.frame2, text="Save", state=tk.DISABLED, command=self.button_save_handler)
        self.logger.info("We create a button called Exit with command button_exit_handler")
        self.button_exit = tk.Button(self.frame2, text="Exit", command=self.button_exit_handler)
        self.logger.info("We place both buttons")
        self.button_save.grid(row=0, column=0)
        self.button_exit.grid(row=0, column=1)

    def answers_entry_command(self, *args):
        self.logger.info("We check if all answers have been filled in correctly")
        self.logger.info("We set the button Save to disabled")
        self.button_save["state"] = tk.DISABLED
        self.logger.info("If the attribute check_boxes is not None, it means that we have displayed multiple answers")
        if self.check_boxes is not None:
            self.logger.info("We need to check every check button then")
            for checkbox in self.check_boxes:
                self.logger.info("By default we set every check button as disabled")
                checkbox["state"] = tk.DISABLED
        self.logger.info("If all answers have been filled and check_boxes is not None (which means we are displaying"
                         "multiple answers")
        activate = self.all_answers_filled_in()
        if activate and self.check_boxes is not None:
            self.logger.info("We enable all checkboxes")
            for checkbox in self.check_boxes:
                checkbox["state"] = tk.NORMAL
        elif activate and self.question_filled() and self.check_boxes is None:
            self.logger.info("If the unique answer has been filled and the question has been filled")
            self.logger.info("We enable the button Save")
            self.button_save["state"] = tk.NORMAL

    def check_boxes_validation(self):
        self.logger.info("We check in the checkboxes have been filled in correctly and proceed accordingly")
        self.logger.info("If we checked one or two boxes only, all answers have been filled in properly and the "
                         "question has been filled in properly")
        if self.check_correct_number_checked() and self.all_answers_filled_in() and self.question_filled():
            self.logger.info("We enable the button Save")
            self.button_save["state"] = tk.NORMAL
        else:
            self.logger.info("Otherwise, we disable the button Save")
            self.button_save["state"] = tk.DISABLED

    def add_more(self):
        self.logger.info("We have clicked the button Add +")
        self.logger.info("We disable the button Save")
        self.button_save["state"] = tk.DISABLED
        self.logger.info("We change the label of the section for Answers to Answers")
        self.answer_stringVar.set("Answers")
        self.logger.info("We destroy the button Add + to remove it frow view")
        self.but.destroy()
        self.logger.info("We create and IntVar and and check box for the first answers and we place it next to the "
                         "input for the first answer")
        self.check_box_var1 = tk.IntVar()
        self.check_box_1 = tk.Checkbutton(self.frame, variable=self.check_box_var1, state=tk.DISABLED,
                                          command=self.check_boxes_validation)
        self.check_box_1.grid(row=0, column=5)
        self.logger.info("We create a list of Entry for the answer that contains the input for the first answer "
                         "already")
        self.answers: [tk.Entry] = [self.first_answer]
        self.logger.info("We create a list of checkbuttons for all the answers that already contains the checkbutton "
                         "for the first one")
        self.check_boxes: [tk.Checkbutton] = [self.check_box_1]
        self.logger.info("We create a list for the IntVar for each checkbutton that contains already the one for the "
                         "first Entry for the first answer")
        self.intVars: [tk.IntVar] = [self.check_box_var1]
        self.logger.info("We create the other 3 inputs, checkboxes and IntVar for the other three answers in a loop")
        for i in range(1, 4):
            self.logger.info("Input creation: {0}".format(i))
            self.logger.info("I create a StringVar for the Entry for the answer")
            string_var = tk.StringVar("")
            self.logger.info("I set a trace in mode w with command answers_entry_command for that StringVar")
            string_var.trace("w", self.answers_entry_command)
            self.logger.info("I create the Entry that will contain that answer and place it")
            answer = tk.Entry(self.frame, width=67, textvariable=string_var)
            answer.grid(columnspan=4, column=0, row=i)
            self.logger.info("I add the StringVar for this Entry to the list of StringVar")
            self.answers_stringVars.append(string_var)
            self.logger.info("I place a Frame between the entry and the checkbox")
            tk.Frame(self.frame, width=15).grid(column=4, row=0)
            self.logger.info("I create a IntVar for the checkbutton")
            check_box_var_i = tk.IntVar(0)
            self.logger.info("I create a checkbutton to set that answer as True or False with pointing to"
                             "the IntVar created above and disabled by default with command "
                             "check_boxes_validation and place it")
            checkbox = tk.Checkbutton(self.frame, variable=check_box_var_i, state=tk.DISABLED,
                                      command=self.check_boxes_validation)
            checkbox.grid(column=5, row=i)
            self.logger.info("I add that Entry to the list of Entry for all the answers")
            self.answers.append(answer)
            self.logger.info("I add the checkbutton to the list of checkbuttons")
            self.check_boxes.append(checkbox)
            self.logger.info("I add the IntVar created above to the list of IntVar")
            self.intVars.append(check_box_var_i)
        self.logger.info("I add a button called Show - to to the bar of buttons with command show_less_handler")
        self.button_less = tk.Button(self.frame2, text="Show -", command=self.show_less_handler)
        self.button_less.grid(row=0, column=3)

    def show_less_handler(self):
        self.logger.info("We clicked the button Show -")
        self.logger.info("We change the label Answers to Answer")
        self.answer_stringVar.set("Answer")
        self.logger.info("We set all the lists to None")
        if self.check_boxes is not None:
            self.check_boxes.clear()
            self.check_boxes = None
        if self.answers is not None:
            self.answers.clear()
            self.answers = None
        if self.intVars is not None:
            self.intVars.clear()
            self.intVars = None
        self.logger.info("We destroy the frames with the entries, check buttons, buttons...")
        self.frame.destroy()
        self.frame2.destroy()
        self.logger.info("We call the function that displays the view for unique answers again")
        self.single_answer_display()

    def check_button_save_question(self):
        if self.question_filled() and self.check_correct_number_checked() and self.all_answers_filled_in():
            self.button_save["state"] = tk.NORMAL
        else:
            self.button_save["state"] = tk.DISABLED
        self.after_func = self.question_text.after(1, self.check_button_save_question)

    def gather_answers(self):
        self.logger.info("We are getting all answers provided")
        answers_str: (str | [(str, bool)]) = []
        self.logger.info("If the attribute check_boxes is not None, that means we expect 4 answers")
        if self.check_boxes is not None:
            i: int = 0
            self.logger.info("For each StringVar in the list of StringVar")
            for stringVarAnswer in self.answers_stringVars:
                self.logger.info("We add to the list of answers the tuple formed by the text of the question"
                                 "recovred for the StringVar of the Entry and if they were selected True or False"
                                 "using the IntVar associated to the checkbox for that answers")
                answers_str.append((stringVarAnswer.get(), self.intVars[i].get() == 1))
                i += 1
        else:
            self.logger.info("We have one unique answers, so we get its text")
            answers_str = self.answer_stringVar1.get()
        self.logger.info("We return the variable that will contain the answer or answers")
        return answers_str

    def button_save_handler(self):
        self.logger.info("We clicked the button Save")
        self.logger.info("We call the function gather_answers and assign its result to a variable")
        answers_str: str | [(str, bool)] = self.gather_answers()
        self.logger.info("We assign the text in the textarea for the question to a variable")
        question_str: str = self.question_text.get("1.0", "end-1c").strip()
        self.logger.info("We create an object QuestionClass and assign it to attribute question_result")
        self.question_result = QuestionClass(question_str, answers_str)
        self.logger.info("We remove the function after in the widget for the question")
        self.question_text.after_cancel(self.after_func)
        self.logger.info("We destroy the window")
        self.window.destroy()

    def button_exit_handler(self):
        self.logger.info("We clicked the button Exit")
        self.logger.info("We set the flat Exit to True")
        QuestionCreation.exit = True
        self.logger.info("Remove all after calls")
        self.question_text.after_cancel(self.after_func)
        self.logger.info("We destroy the window")
        self.window.destroy()

    def __init__(self, title):
        self.logger.info("We create a 600x500 SimpleWindow")
        SimpleWindow.__init__(self, 600, 500, title)
        self.window.protocol("WM_DELETE_WINDOW", self.button_exit_handler)
        self.font = ("TkDefaultFont", 14)
        self.check_boxes = None
        self.logger.info("We create and pack a label that says Question")
        self.question_label: tk.Label = tk.Label(self.window, text="Question", font=self.font)
        self.question_label.pack()
        self.logger.info("We create a textarea for the question with after 1 ns check_button_save_question")
        self.question_text: tk.Text = tk.Text(self.window, width=57, height=7)
        self.after_func = self.question_text.after(1, self.check_button_save_question)
        self.question_text.pack()
        tk.Frame(self.window, height=20).pack()
        self.logger.info("We create a label with text Answer that changes to Answers")
        self.answer_stringVar = tk.StringVar("")
        self.answer_stringVar.set("Answer")
        self.label_answer = tk.Label(self.window, textvariable=self.answer_stringVar, font=self.font)
        self.label_answer.pack()
        tk.Frame(self.window, height=20)
        self.logger.info("We create all the attributes we might need in the future to None")
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
        self.after_func = None
        self.logger.info("We execute single_answer_display to display the view for a unique answer")
        self.single_answer_display()


if __name__ == "__main__":
    qc = QuestionCreation("Example")
    qc.window.mainloop()
