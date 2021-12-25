import sys
sys.path.append("./BE-Logic")
import LoggerMeta

@LoggerMeta.class_decorator_logger("INFO")
class Example(metaclass=LoggerMeta.MetaLogger):
    pass

e = Example()