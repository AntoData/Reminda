import sys
sys.path.append("../BE-Logic")
import shelve
import LoggerMeta


@LoggerMeta.class_decorator_logger("INFO")
class ConfigClass(metaclass=LoggerMeta.MetaLogger):
    """
    This is a static class that contains class attributes the different parameters needed to customize
    the configuration of the application
    ...

    Attributes
    ----------
    config_filename: str
        A string variable that contains the path to the binary file that contains the parameters needed
        to customize the configuration of this application

    config_file_static:
        This class attribute is the shelve object result of opening the file in the path described above

    secs_to_answer: int
        This class attribute is the number of seconds to answer a question loaded from the configuration file

    secs_between_questions: int
        This class attribute is the number of seconds between question in which the application will be sleeping
        so nothing is displayed

    Methods
    -------
    set_secs_to_answer(cls, secs_to_answer: int):
        This class method takes an integer that updates the parameters that controls the seconds to answer a question
        in the binary config file

    get_secs_to_answer(cls) -> int:
        This class method returns the number of seconds to answer a question

    set_secs_between_questions(cls, secs_between_questions: int):
        This class method takes an integer that updates the parameters that controls the seconds that the application
        will be sleeping between question in the binary config file

    get_secs_between_questions(cls) -> int:
        This class method returns the number of seconds the application will be sleeping between questions
    """
    config_filename: str = "{0}/Config/config.cfg".format(LoggerMeta.MetaLogger.get_root())
    try:
        config_file_static = shelve.open(config_filename, "r")
        LoggerMeta.MetaLogger.logger.info("{0}, exists so we will read it".format(config_filename))
        secs_to_answer: int = config_file_static["secs_to_answer"]
        secs_between_questions: int = config_file_static["secs_between_questions"]
    except Exception as e:
        LoggerMeta.MetaLogger.logger.info("{0} does not exist, we will create it".format(config_filename))
        config_file_static = shelve.open(config_filename, "n")
        LoggerMeta.MetaLogger.logger.info("{0} created".format(config_filename))
        config_file_static["secs_to_answer"] = 180
        LoggerMeta.MetaLogger.logger.info("Default value for secs_to_answer is 180")
        config_file_static["secs_between_questions"] = 600
        LoggerMeta.MetaLogger.logger.info("Default value for secs_between_questions is 600")
        secs_to_answer: int = config_file_static["secs_to_answer"]
        secs_between_questions: int = config_file_static["secs_between_questions"]
    finally:
        LoggerMeta.MetaLogger.logger.info("Seconds to answer a question: {0}".format(secs_to_answer))
        LoggerMeta.MetaLogger.logger.info("Seconds between questions: {0}".format(secs_between_questions))
        config_file_static.close()
        LoggerMeta.MetaLogger.logger.info("{0} is closed now".format(config_filename))

    @classmethod
    def set_secs_to_answer(cls, secs_to_answer: int):
        LoggerMeta.MetaLogger.logger.info("Setting the secs to answer a question to {0}".format(secs_to_answer))
        cls.secs_to_answer = secs_to_answer
        try:
            LoggerMeta.MetaLogger.logger.info("Opening file {0}".format(cls.config_filename))
            cls.config_file_static = shelve.open(cls.config_filename, "w")
            LoggerMeta.MetaLogger.logger.info("Updating the file")
            cls.config_file_static["secs_to_answer"] = cls.secs_to_answer
        except Exception as e:
            LoggerMeta.MetaLogger.logger.error("Something went wrong")
            raise FileNotFoundError from e
        finally:
            cls.config_file_static.close()
            LoggerMeta.MetaLogger.logger.info("Closing config file")

    @classmethod
    def get_secs_to_answer(cls) -> int:
        LoggerMeta.MetaLogger.logger.info("Calling get_secs_to_answer")
        LoggerMeta.MetaLogger.logger.info("Getting secs to answer a questions: {0}".format(cls.secs_to_answer))
        return cls.secs_to_answer

    @classmethod
    def set_secs_between_questions(cls, secs_between_questions: int):
        LoggerMeta.MetaLogger.logger.info("Setting the secs between a questions to {0}".format(secs_between_questions))
        cls.secs_between_questions = secs_between_questions
        try:
            LoggerMeta.MetaLogger.logger.info("Opening file {0}".format(cls.config_filename))
            cls.config_file_static = shelve.open(cls.config_filename, "w")
            LoggerMeta.MetaLogger.logger.info("Updating the file")
            cls.config_file_static["secs_between_questions"] = cls.secs_between_questions
        except Exception as e:
            LoggerMeta.MetaLogger.logger.error("Something went wrong")
            raise FileNotFoundError from e
        finally:
            cls.config_file_static.close()
            LoggerMeta.MetaLogger.logger.info("Closing config file")

    @classmethod
    def get_secs_between_questions(cls) -> int:
        LoggerMeta.MetaLogger.logger.info("Calling get_secs_between_questions")
        LoggerMeta.MetaLogger.logger.info("Getting secs between questions: {0}".format(cls.secs_to_answer))
        return cls.secs_between_questions


if __name__ == "__main__":
    secs_to_answer_before: int = ConfigClass.secs_to_answer
    secs_between_questions_before: int = ConfigClass.secs_between_questions
    ConfigClass.set_secs_to_answer(200)
    assert ConfigClass.get_secs_to_answer() == 200
    ConfigClass.set_secs_between_questions(300)
    assert ConfigClass.get_secs_between_questions() == 300
    ConfigClass.set_secs_to_answer(secs_to_answer_before)
    assert secs_to_answer_before == ConfigClass.get_secs_to_answer()
    ConfigClass.set_secs_between_questions(secs_between_questions_before)
    assert secs_between_questions_before == ConfigClass.get_secs_between_questions()
