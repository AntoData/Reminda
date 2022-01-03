import sys
import re
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
import Config.ConfigLogicClass
from window_design import SimpleWindow
import tkinter as tk
from tkinter import messagebox
import main_window


@LoggerMeta.class_decorator_logger("INFO")
class ConfigPopUp(SimpleWindow):
    """
    This is a window class that represents the window that is displayed when we want to check or change the
    configuration of the application
    ...

    Attributes
    ----------
    label_text_secs_to_answer: str
        This class attribute contains the string "Seconds to answer" that will be displayed in the label for
        that input

    label_text_secs_between_questions: str
        This class attribute contains the string "Seconds between questions" that will be displayed in the label for
        that input

    label_secs_to_answer: tk.Label
        This is the label that displays the String Seconds to answer next to the input that displays and allows
        us to update the seconds to answer a question

    secs_to_answer_StringVar: tk.StringVar
        This is the observable variable that contains and displays and is used to update the number of
        seconds to answer a question and linked to the input for that purpose

    entry_secs_to_answer: tk.Entry
        This is the input that displays and allows the user to update the seconds to answer the question using
        the observable variable described above

    label_secs_between_questions: tk.Label
        This label displays the message seconds between question next to the input that allows the user to update
        the seconds the application will be sleeping between question

    secs_between_questions_StringVar: tk.StringVar
        This is the observable variable that contains and displays and is used to update the number of
        seconds the application will be sleeping between questions and linked to the input for that purpose

    entry_secs_between_questions: tk.Entry
        This is the input that displays and allows the user to update the seconds the application will be sleeping
        between question using the observable variable described above

    font_button_save
        This attribute contains the configuration of the font that will be used in the button Save

    self.button_save: tk.Button
        This attribute is the button Save used to save changes in the configuration

    Methods
    -------
    handler_button_save(self)
        This method is the command assigned to the button Save. It saves the changes in the configuration parameters
        and saves them to the configuration file

    only_digits(self, id, ix, act):
        This method is assigned as a trace to the StringVars that are the observable variables to the inputs
        that display and allow the user to update the configuration parameters. In particular, this function
        will only allow you to input digits. If you press an alphabetic character, nothing will be added to the field

    enable_button_save(self, id, ix, act):
        This method is also added as a trace to the StringVars that are observable variables to the inputs
        that display and allow the user to update the configuration parameters. In particular, this function
        that will enable the button Save when we change one of the fields

    exit_handler(self):
        This method customizes the default window exit button to destroy the window and display the main window
    """
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

    def exit_handler(self):
        self.window.destroy()
        main_window.MainWindow().window.mainloop()

    def __init__(self, height: int, width: int, title: str):
        self.logger.info("We create a {0}x{1} with title {2}".format(height, width, title))
        SimpleWindow.__init__(self, height, width, title)
        self.logger.info("We create and place a label that says: {0}".format(ConfigPopUp.label_text_secs_to_answer))
        label_secs_to_answer: tk.Label = tk.Label(self.window, text=ConfigPopUp.label_text_secs_to_answer)
        label_secs_to_answer.grid(column=0, row=0, padx=2)
        self.logger.info("We create an Entry with StringVar with traces in mode w only_digits and enable_button_save")
        self.secs_to_answer_StringVar: tk.StringVar = tk.StringVar(self.window,
                                                                   value=str(Config.ConfigLogicClass.ConfigClass.
                                                                             secs_to_answer))
        self.secs_to_answer_StringVar.trace("w", callback=self.only_digits)
        self.secs_to_answer_StringVar.trace("w", callback=self.enable_button_save)
        self.entry_secs_to_answer: tk.Entry = tk.Entry(self.window, textvariable=self.secs_to_answer_StringVar)
        self.entry_secs_to_answer.grid(column=1, row=0)
        self.logger.info("We create and place a label that says: {0}".format(ConfigPopUp.
                                                                             label_text_secs_between_questions))
        self.label_secs_between_questions: tk.Label = tk.Label(self.window, text=ConfigPopUp.
                                                          label_text_secs_between_questions)
        self.label_secs_between_questions.grid(column=0, row=1, padx=2)
        self.logger.info("We create an Entry with StringVar with traces in mode w only_digits and enable_button_save")
        self.secs_between_questions_StringVar: tk.StringVar = tk.StringVar(
            self.window, value=str(Config.ConfigLogicClass.ConfigClass.secs_between_questions))
        self.secs_between_questions_StringVar.trace("w", callback=self.only_digits)
        self.secs_between_questions_StringVar.trace("w", self.enable_button_save)
        self.entry_secs_between_questions: tk.Entry = tk.Entry(self.window, textvariable=self.
                                                          secs_between_questions_StringVar)
        self.entry_secs_between_questions.grid(column=1, row=1)
        self.logger.info("Create a button called Save with command handler_button_save and disabled by default")
        self.font_button_save = ("Century", 14, "bold")
        self.button_save: tk.Button = tk.Button(self.window, text="Save", command=self.handler_button_save,
                                                state=tk.DISABLED, background="#128301", activebackground="#128301",
                                                disabledforeground="#CACACA", activeforeground="#FFFFFF",
                                                foreground="#FFFFFF", font=self.font_button_save,
                                                padx=2, pady=2)
        self.button_save.grid(row=2, columnspan=2, padx=10, pady=10)
        self.window.protocol("WM_DELETE_WINDOW", self.exit_handler)


if __name__ == "__main__":
    c = ConfigPopUp(120, 287, "Configuration")
    c.window.mainloop()
