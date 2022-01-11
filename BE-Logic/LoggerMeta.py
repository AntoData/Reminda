from datetime import datetime
import os
import abc
from logging.handlers import RotatingFileHandler


class MetaAbsLogger(abc.ABCMeta):
    """
    This is an abstract metaclass. This will be the base for our logging feature. This metaclass will add
    a logger to every abstract class
    ...

    Attributes
    ----------
    logger : logging.Logger
        Class attribute: This attribute will contain the log object that will create our logs and log from every class

    Methods
    -------
    get_root()
        Static method used to get the full path to the project folder

    __new__(mcs, name: str, bases: tuple, members: dict):
        Method that will overwrite the method __new__ in every child class, so we add the logger (if it was not added
        previously)
    """
    logger = None

    @staticmethod
    def get_root() -> str:
        root_path: str = os.getcwd()
        root_path_index: int = root_path.find("ProjectR")
        return root_path[0: root_path_index + 8]

    def __new__(mcs, name: str, bases: tuple, members: dict):
        try:
            import logging
        except ImportError as e:
            raise RuntimeError from e
        obj = abc.ABCMeta.__new__(mcs, name, bases, members)
        if MetaAbsLogger.logger is None:
            MetaAbsLogger.logger_starter = True
            now = datetime.now()
            filename_date: str = now.strftime("%Y-%m-%d_%H-%M-%S")
            try:
                filename = "{0}/Logs/{1}".format("./", filename_date)
                logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                    filename="{0}.log".format(filename),
                                    datefmt='%H:%M:%S',
                                    level=logging.INFO)
            except FileNotFoundError:
                filename = "{0}/Logs/{1}".format("../", filename_date)
                logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                    filename="{0}.log".format(filename),
                                    datefmt='%H:%M:%S',
                                    level=logging.INFO)

            MetaAbsLogger.logger = logging.getLogger(str(filename))
            MetaAbsLogger.logger.info("Log has been created and started")
        obj.logger = MetaAbsLogger.logger
        obj.logger.info("Metaclass {0}: Starting class {1}".format(mcs.__name__, name))
        return obj


def class_decorator_logger(level: str):
    """
    This is the class decorator that will be the complement to our metaclasses. Using this decorator conjoined
    with the metaclass we will include in the log any call to any attribute/method of a class
    :param level: str
        This is the level of the lines of we want to include in the log (for instance: INFO, ERROR...)
    :return:
    """
    def class_decorator_logger_inner(class_):
        def logger_level(cls, log_line: str):
            if level == "INFO":
                cls.logger.info(log_line)
            elif level == "DEBUG":
                cls.logger.debug(log_line)
            else:
                cls.logger.warning(log_line)
        class_.__getattribute__orig__ = class_.__getattribute__

        def __getattribute__logger__(self, item: str):
            obj = class_.__getattribute__orig__(self, item)
            if not callable(obj):
                log_line: str = "Getting attribute: {0}".format(item)
            else:
                log_line: str = "Getting method: {0}".format(item)
            logger_level(class_, log_line)
            return obj
        class_.__getattribute__ = __getattribute__logger__
        class_.__setattr__orig__ = class_.__setattr__

        def __setattr__logger__(self, key: str, value):
            log_line: str = "Setting member: {0} to value={1}".format(key, value)
            logger_level(class_, log_line)
            return class_.__setattr__orig__(self, key, value)
        class_.__setattr__ = __setattr__logger__
        class_.__init__orig__ = class_.__init__

        def __init__logger__(self, *args, **kwargs):
            log_line: str = "Getting into __init__ for class: {0}".format(type(self).__name__)
            logger_level(class_, log_line)
            log_line: str = "Attributes in args: {0}".format(args)
            logger_level(class_, log_line)
            log_line: str = "Attributes in kwargs: {0}".format(kwargs)
            logger_level(class_, log_line)
            return class_.__init__orig__(self, *args, **kwargs)
        class_.__init__ = __init__logger__
        return class_
    return class_decorator_logger_inner


class MetaLogger(type, metaclass=MetaAbsLogger):
    """
    This is a concrete metaclass. This is the concrete metaclass child of MetaAbsLogger
    ...

    Methods
    -------
    __new__(mcs, name: str, bases: tuple, members: dict):
        Method that will overwrite the method __new__ in every child class, so we add the logger (if it was not added
        previously)
    """
    def __new__(mcs, name: str, bases: tuple, members: dict):
        obj = MetaAbsLogger.__new__(mcs, name, bases, members)
        return obj


if __name__ == "__main__":
    print("Test")

    @class_decorator_logger("INFO")
    class Wizard(metaclass=MetaLogger):
        def __init__(self, name: str, spells: [str]):
            self.name: str = name
            self.spells: [str] = spells

        def get_name(self) -> str:
            return self.name

        def set_name(self, name: str):
            self.name = name

    w = Wizard("Soromyr", ["Magic Arrow", "Shield", "Find path"])
    print(w.name)
    w.name = "Soromyr The Great"
    print(w.get_name())
    w.set_name("Soromyr III")
    print(w.spells)
    w.spells = ["Fireball", "Shield", "Teleport"]
    print(w.spells)

    @class_decorator_logger("INFO")
    class Knight(metaclass=MetaLogger):
        def __init__(self, name: str, attacks: [str]):
            self.name: str = name
            self.attacks: [str] = attacks

        def get_attacks(self) -> [str]:
            return self.attacks

        def set_attacks(self, attacks: [str]):
            self.attacks = attacks

    k = Knight("Gawain", ["Punch", "Sword fight", "Arrow"])
    print(k.name)
    k.name = "Sir Gawain"
    print(k.name)
    print(k.get_attacks())
    k.set_attacks(["Kick", "Sword fight", "Horse attack"])
    print(k.attacks)
