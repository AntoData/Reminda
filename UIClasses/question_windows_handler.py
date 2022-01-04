import sys
import time
sys.path.append("../BE-Logic")
sys.path.append("../Config")
from Questionnaire import QuestionnaireClass
from Current_session import CurrentSession
import LoggerMeta
import Config.ConfigLogicClass
import question_windows
from execution_summary import ExecutionSummary


@LoggerMeta.class_decorator_logger("INFO")
class QuestionnaireWindowHandler(metaclass=LoggerMeta.MetaLogger):
    """
    This class handles the loop that displays the windows to answer the questions that compose a questionnaire
    after we loaded one from a file
    ...

    Attributes
    ----------
    window_question_object
        This class attribute will contain the window that displays the current question to be answered

    filename: str
        Name of the file we want to load

    questionnaire: QuestionnaireClass
        This attribute is object that contains the questionnaire loaded from the file whose name is contained in
        the attribute above

    secs_to_answer: int
        This attribute is the number of seconds to answer a question

    icon_filename: str
        This is the path to the file that will be used as icon for these windows

    Methods
    -------
    handler_question_windows(cls):
        This method destroys the current window and sleep the application for the number of seconds set between
        question
    """
    window_question_object = None

    @classmethod
    def handler_question_windows(cls):
        cls.window_question_object.window.destroy()
        time.sleep(Config.ConfigLogicClass.ConfigClass.get_secs_between_questions())

    def __init__(self, filename: str):
        self.logger.info("Opening file {0}".format(filename))
        self.filename: str = filename.replace(".pickle", "")
        self.questionnaire: QuestionnaireClass = QuestionnaireClass.\
            load_questionnaire(filename)
        self.logger.info("Loading questionnaire from file {0}".format(filename))
        self.questionnaire.shuffle()
        self.logger.info("Questions have been shuffled")
        self.secs_to_answer: int = Config.ConfigLogicClass.ConfigClass.get_secs_to_answer()
        self.logger.info("We got the seconds to answer a question {0}".format(self.secs_to_answer))
        i: int = 1
        self.logger.info("We go through every question in the questionnaire")
        for question in self.questionnaire:
            if question.get_question_type() == 0:
                self.logger.info("Question {0} is type 0".format(i))
                QuestionnaireWindowHandler.window_question_object = question_windows.QuestionOneAnswer(question, i)
                self.logger.info("Created window from class QuestionOneAnswer")
            elif question.get_question_type() == 1:
                self.logger.info("Question {0} is type 1".format(i))
                QuestionnaireWindowHandler.window_question_object = question_windows.QuestionOneAnswerMultiple(question, i)
                self.logger.info("Created window from class QuestionOneAnswerMultiple")
            else:
                self.logger.info("Question {0} is type 2".format(i))
                QuestionnaireWindowHandler.window_question_object = question_windows.QuestionTwoAnswersMultiple(question, i)
                self.logger.info("Created window from class QuestionTwoAnswersMultiple")
            QuestionnaireWindowHandler.window_question_object.func_after = QuestionnaireWindowHandler.\
                window_question_object.window.after(self.secs_to_answer * 1000, QuestionnaireWindowHandler.
                                                    window_question_object.window.destroy)
            self.logger.info("We set the window to be destroyed after {0} seconds using after".format(
                self.secs_to_answer))
            QuestionnaireWindowHandler.window_question_object.window.lift()
            QuestionnaireWindowHandler.window_question_object.window.attributes("-topmost", True)
            self.logger.info("We make the window the primary focus")
            QuestionnaireWindowHandler.window_question_object.window.mainloop()
            self.logger.info("We display the window")
            if i < len(self.questionnaire):
                self.logger.info("As it is not the last question, we sleep for {0}".format(
                    Config.ConfigLogicClass.ConfigClass.get_secs_between_questions()))
                time.sleep(Config.ConfigLogicClass.ConfigClass.get_secs_between_questions())
            else:
                pass
            i += 1
            if question.question not in CurrentSession.current_session.keys():
                self.logger.info("If we did not answer the question, we added it to the execution list as None")
                CurrentSession.current_session[question.question] = None
        self.logger.info("We finished the questionnaire")
        summary: ExecutionSummary = ExecutionSummary()
        self.logger.info("We created an execution summary window")
        CurrentSession.delete_session()
        self.logger.info("We don´t need the information about the current execution anymore, so we deleted it")
        self.logger.info("We display the execution window")
        summary.window.mainloop()


if __name__ == "__main__":
    c = QuestionnaireWindowHandler("Example")
