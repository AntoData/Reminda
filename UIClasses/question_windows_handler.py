import sys
import time
sys.path.append("../BE-Logic")
sys.path.append("../Config")
from Questionnaire import QuestionnaireClass
from QuestionLogic import QuestionClass
import LoggerMeta
from window_design import SimpleWindow
import tkinter as tk
from tkinter import ttk
import os
import Config.ConfigLogicClass
from question_windows import *


class QuestionnaireWindowHandler:
    window_question_object = None

    @classmethod
    def handler_question_windows(cls):
        cls.window_question_object.window.destroy()
        time.sleep(Config.ConfigLogicClass.ConfigClass.get_secs_between_questions())

    def __init__(self, filename: str):
        self.filename: str = filename.replace(".pickle", "")
        print(self.filename)
        self.questionnaire: QuestionnaireClass = QuestionnaireClass.\
            load_questionnaire(filename)
        self.questionnaire.shuffle()
        self.secs_to_answer: int = Config.ConfigLogicClass.ConfigClass.get_secs_to_answer()
        i: int = 0
        for question in self.questionnaire:
            if question.get_question_type() == 0:
                QuestionnaireWindowHandler.window_question_object = QuestionOneAnswer(question, i)
            elif question.get_question_type() == 1:
                QuestionnaireWindowHandler.window_question_object = QuestionOneAnswerMultiple(question, i)
            else:
                QuestionnaireWindowHandler.window_question_object = QuestionTwoAnswersMultiple(question, i)
            if i < len(self.questionnaire) - 1:
                QuestionnaireWindowHandler.window_question_object.window.after(
                    self.secs_to_answer*1000, QuestionnaireWindowHandler.window_question_object.window.destroy)
                QuestionnaireWindowHandler.window_question_object.window.mainloop()
                time.sleep(Config.ConfigLogicClass.ConfigClass.get_secs_between_questions())
            else:
                QuestionnaireWindowHandler.window_question_object.window.after(
                    self.secs_to_answer * 1000, QuestionnaireWindowHandler.window_question_object.window.destroy)
                QuestionnaireWindowHandler.window_question_object.window.mainloop()
            i += 1


if __name__ == "__main__":
    c = QuestionnaireWindowHandler("QuestionnaireExample2")


