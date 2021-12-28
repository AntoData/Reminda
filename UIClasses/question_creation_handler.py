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
from question_creation import QuestionCreation

class QuestionCreationHandler(metaclass=LoggerMeta.MetaLogger):
    window_question_object = None

    def __init__(self, filename: str):
        self.questionnaire: QuestionnaireClass = QuestionnaireClass(filename)
        while not QuestionCreation.exit:
            question_creation_window = QuestionCreation("New Question")
            question_creation_window.window.mainloop()
            if question_creation_window.question_result is not None:
                self.questionnaire += question_creation_window.question_result
        QuestionCreation.exit = False
        self.questionnaire.save_questionnaire()


if __name__ == "__main__":
    QuestionCreationHandler("Example")