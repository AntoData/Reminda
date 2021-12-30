import LoggerMeta


@LoggerMeta.class_decorator_logger("INFO")
class CurrentSession(metaclass=LoggerMeta.MetaLogger):
    current_session: {str: bool} = {}

    @classmethod
    def delete_session(cls):
        cls.current_session.clear()
