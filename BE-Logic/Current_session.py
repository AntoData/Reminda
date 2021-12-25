import LoggerMeta


class CurrentSession(LoggerMeta.MetaLogger):
    current_session: {str: bool} = {}

    @classmethod
    def delete_session(cls):
        cls.current_session.clear()
