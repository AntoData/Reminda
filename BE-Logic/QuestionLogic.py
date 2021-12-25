from __future__ import annotations
import LoggerMeta


get_anon_correct = lambda answers: [answer[0] for answer in answers if answer[1]]


@LoggerMeta.class_decorator_logger("INFO")
class QuestionClass(metaclass=LoggerMeta.MetaLogger):
    def __init__(self, question: str, answers: str | [(str, bool)]):
        self.__question: str = question
        self.__answers: str | [(str, bool)] = answers

    def get_question_type(self) -> int:
        if not isinstance(self.__answers, list):
            self.logger.info("This question is a single answer question: Text input: value 0")
            return 0
        else:
            true_answers = get_anon_correct(self.__answers)
            if len(true_answers) == 1:
                self.logger.info("This question is a multiple choice question with a single answer: Radio button: "
                                 "value 1")
                return 1
            elif len(true_answers) == 2:
                self.logger.info("This question is a multiple choice question with two answers: Checkboxes: value 2")
                return 2
            else:
                e = "Questions can have up to two correct answers"
                self.logger.error(e)
                raise ValueError(e)

    def get_correct_answers(self) -> str | [str]:
        question_type: int = self.get_question_type()
        if question_type == 0:
            self.logger.info("The correct answer is {0}".format(self.__answers))
            return self.__answers
        else:
            correct_answers: [str] = get_anon_correct(self.__answers)
            self.logger.info("Correct answers are {0}".format(correct_answers))
            return correct_answers

    @property
    def answers(self) -> str | [(str, bool)]:
        return self.__answers

    @property
    def question(self) -> str:
        return self.__question

    def __str__(self) -> str:
        return "{0}: {1}".format(self.question,self.answers)


if __name__ == "__main__":
    q0 = QuestionClass("What do you say to a person in the morning?", "Good morning")
    print(q0)
    assert q0.get_question_type() == 0
    assert q0.get_correct_answers() == "Good morning"
    assert q0.question == "What do you say to a person in the morning?"
    q1 = QuestionClass("What of the following ones are Python basic types?", [("Fire", False), ("Bool", True),
                                                                              ("Normal", False), ("Basic", False)])
    assert q1.get_question_type() == 1
    assert q1.get_correct_answers() == ["Bool"]
    assert q1.question == "What of the following ones are Python basic types?"
    q2 = QuestionClass("Which of the following countries belong to the European Union", [("Serbia", False),
                                                                                         ("Latvia", True),
                                                                                         ("Norway", False),
                                                                                         ("Malta", True)])
    assert q2.get_question_type() == 2
    assert q2.get_correct_answers() == ["Latvia","Malta"]
    assert q2.question == "Which of the following countries belong to the European Union"
    try:
        q3 = QuestionClass("What of the following are Python basic type", [("Bool", True), ("Integer", True),
                                                                           ("Float", True), ("Point", False)])
    except ValueError:
        assert True
    try:
        q2 = QuestionClass("Which of the following countries belong to the European Union", [("Serbia", False),
                                                                                             ("San Marino", False),
                                                                                             ("Norway", False),
                                                                                             ("UK", False)])
    except ValueError:
        assert True
