import LoggerMeta
import QuestionLogic
import random
import pickle
import copy


@LoggerMeta.class_decorator_logger("INFO")
class QuestionnaireClass(metaclass=LoggerMeta.MetaLogger):
    def __init__(self, name: str):
        self.__name: str = name
        self.questions: [QuestionLogic.QuestionClass] = []
        self.__position: int = 0

    @property
    def name(self) -> str:
        return self.__name

    def __iadd__(self, question_new: QuestionLogic.QuestionClass):
        self.questions.append(question_new)
        return self

    def __isub__(self, index: int):
        try:
            self.questions.pop(index)
        except IndexError as e:
            self.logger.error("There is no question with index {0} for questionnaire {1}".format(index, self.__name))
            raise LookupError from e
        return self

    def __getitem__(self, pos: int) -> QuestionLogic.QuestionClass:
        try:
            res = self.questions[pos]
        except IndexError as e:
            self.logger.error("There is no question {0} in Questionnaire {1}".format(self.questions, self.__name))
            raise IndexError from e
        return res

    def shuffle(self):
        random.shuffle(self.questions)

    def __iter__(self):
        return self

    def __next__(self) -> QuestionLogic.QuestionClass:
        if self.__position >= len(self.questions):
            self.__position = 0
            raise StopIteration
        question_pos: QuestionLogic.QuestionClass = self.questions[self.__position]
        self.__position += 1
        return question_pos

    def __len__(self) -> int:
        return len(self.questions)

    def __str__(self) -> str:
        lines = [str(line) for line in self.questions]
        return "Questionnaire: {0}\nQuestions:\n".format(self.__name)+"\n".join(lines)

    def save_as_file(self, path: str):
        self.logger.info("We are saving the questionnaire {0} to file {1}".format(self.__name, path))
        try:
            pickle.dump(self, open(path, "wb"))
        except Exception as e:
            self.logger.error("There was an error trying to save questionnaire {0} to file {1}".
                              format(self.__name, path))
            self.logger.error(e)
            raise pickle.PickleError from e

    def save_questionnaire(self):
        path: str = LoggerMeta.MetaLogger.get_root() + "/Data/Questionnaires/{0}.pickle".format(self.__name)
        self.save_as_file(path)

    @staticmethod
    def load_from_file(file_path: str):
        try:
            LoggerMeta.MetaLogger.logger.info("Loading a questionnaire from file: {0}".format(file_path))
            return pickle.load(open(file_path, "rb"))
        except Exception as e:
            LoggerMeta.MetaLogger.logger.error("Error when trying to load a questionnaire from file: {0}".
                                               format(file_path))
            raise pickle.PickleError from e

    @staticmethod
    def load_questionnaire(name: str):
        path: str = LoggerMeta.MetaLogger.get_root() + "/Data/Questionnaires/{0}.pickle".format(name)
        print(path)
        return QuestionnaireClass.load_from_file(path)


if __name__ == "__main__":
    q0 = QuestionLogic.QuestionClass("What do you say to a person in the morning?", "Good morning")
    q1 = QuestionLogic.QuestionClass("What of the following ones are Python basic types?", [("Fire", False),
                                                                                            ("Bool", True),
                                                                                            ("Normal", False),
                                                                                            ("Basic", False)])
    q2 = QuestionLogic.QuestionClass("Which of the following countries belong to the European Union",
                                     [("Serbia", False), ("Latvia", True), ("Norway", False), ("Malta", True)])
    qq = QuestionnaireClass("QuestionnaireExample")
    assert len(qq) == 0
    qq += q0
    qq += q1
    qq += q2
    for q in qq:
        print(str(q))
    print(qq)
    print(qq[1])
    assert qq[1] == q1
    assert len(qq) == 3
    questions_orders = copy.deepcopy(qq.questions)
    qq.shuffle()
    print(qq)
    questions_orders_shuffle = copy.deepcopy(qq.questions)
    assert len(questions_orders) == len(questions_orders_shuffle)
    same_order: bool = True
    for i in range(0, len(questions_orders)):
        if questions_orders[i] != questions_orders_shuffle[i]:
            same_order = False
            break
    assert not same_order
    print("Iteration")
    i: int = 0
    for question in qq:
        i += 1
        print(question)
    assert i == 3
    print("Slice")
    print(qq[1:])
    qq -= 2
    qq -= 0
    try:
        qq -= 4
        assert False
    except LookupError:
        assert True
    try:
        qq[3]
        assert False
    except IndexError:
        assert True
    assert len(qq) == 1
    print(qq)
    qq.save_questionnaire()
    qq2: QuestionnaireClass = QuestionnaireClass.load_questionnaire("QuestionnaireExample")
    print("Loaded")
    print(qq2)
    try:
        qq2.save_as_file("../fake_path/log.pickle")
        assert False
    except pickle.PickleError:
        assert True
    try:
        qq3 = QuestionnaireClass.load_questionnaire("Non-existing")
        assert False
    except pickle.PickleError:
        assert True

