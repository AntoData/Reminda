import LoggerMeta


@LoggerMeta.class_decorator_logger("INFO")
class CurrentSession(metaclass=LoggerMeta.MetaLogger):
    """
    This class is used to represent a session when we are answering the questions of a questionnaire

    ...

    Attributes
    ----------
    current_session : {str: bool}
        Class attribute: A dictionary it has a string key which is the question and a boolean which is True if we
        answered the question correctly

    Methods
    -------
    delete_session(cls)
        Class method used to restart a session (cleaning the dictionary)
    """
    current_session: {str: bool} = {}

    @classmethod
    def delete_session(cls):
        cls.current_session.clear()
