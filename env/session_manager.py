import inspect
from env.custom_errors import InvalidName


class SessionManager:
    def __init__(self):
        self.objects = {"open_sessions": []}

    def session_cleanup(self):
        for session in self.objects["open_sessions"]:
            try:
                session.close_connection()
            # TODO: catch specific exceptions
            except Exception:
                pass
        for attr in inspect.getmembers(self):
            if not inspect.ismethod(attr[1]) and not attr[0].startswith("__"):
                self.remove_variable(attr[0])
        self.objects = {"open_sessions": []}

    def add_variable(self, name: str, value):
        if hasattr(self, name):
            raise AttributeError(f"{name} already exists.")
        elif name.startswith("__"):
            raise InvalidName("Variable name starting with '__' not allowed")
        else:
            setattr(self, name, value)

    def update_variable(self, name: str, new_value):
        if not hasattr(self, name):
            raise AttributeError(f"{name} doesn't exists.")
        else:
            setattr(self, name, new_value)

    def get_variable(self, name: str):
        if not hasattr(self, name):
            raise AttributeError(f"{name} doesn't exists.")
        else:
            return getattr(self, name)

    def remove_variable(self, name: str):
        if not hasattr(self, name):
            raise AttributeError(f"{name} doesn't exists.")
        else:
            delattr(self, name)

    def has_variable(self, name: str):
        return hasattr(self, name)


current_session = SessionManager()
