from env.session_manager import SessionManager
from env.logging_interface import logging


def main(*args):
    print("pre1.", current_session.objects)
    current_session.objects.get("open_sessions").append(args)
    print("pre2.", current_session.objects)
    logging.write(True, "testing1")
    logging.write(False, "testing2")
    logging.write(True, "testing3", commit_now=True)
    print("pre3.")


for i in range(5):
    current_session = SessionManager()
    current_session.add_variable("a",i)
    print(current_session.get_variable("a"))




