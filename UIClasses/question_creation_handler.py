from __future__ import annotations
import sys
sys.path.append("../BE-Logic")
sys.path.append("../Config")
import LoggerMeta
from Questionnaire import QuestionnaireClass
from question_creation import QuestionCreation


@LoggerMeta.class_decorator_logger("INFO")
class QuestionCreationHandler(metaclass=LoggerMeta.MetaLogger):
    """
    This class is used for the loop in which we create the questions to compose a questionnaire until we click
    the button Exit
    ...

    Attributes
    ----------
    questionnaire: QuestionnaireClass
        This attribute is the questionnaire we are creating

    question_creation_window: QuestionCreation
        This attribute is the window we display to create a new question for the questionnaire

    Methods
    -------
    N/A
    """
    window_question_object = None

    def __init__(self, filename: str):
        self.logger.info("Creating object of class QuestionnaireClass")
        self.questionnaire: QuestionnaireClass = QuestionnaireClass(filename)
        self.logger.info("While flag exit is not True, that means we have not clicked the button Exit")
        while not QuestionCreation.exit:
            self.logger.info("We try to create a new window of class QuestionCreation")
            question_creation_window = QuestionCreation("New Question")
            self.logger.info("We start the mainloop")
            question_creation_window.window.mainloop()
            self.logger.info("If we clicked the button Save or the button Exit we go on execution")
            self.logger.info("If the attribute question_result (the attribute that contains the question "
                             "created in the window) is not none, it means we clicked the button Save")
            if question_creation_window.question_result is not None:
                self.logger.info("Then, we add the question to the questionnaire")
                self.questionnaire += question_creation_window.question_result
        self.logger.info("If we exit the loop, if means we clicked the button Exit")
        self.logger.info("In that case, we set the flag exit to False again")
        QuestionCreation.exit = False
        self.logger.info("Then we save the questionnaire to a file")
        self.questionnaire.save_questionnaire()


if __name__ == "__main__":
    QuestionCreationHandler("Example")
