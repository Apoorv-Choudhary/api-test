from env.session_manager import current_session
from env.logging_interface import logging


def main(*args):
    print("post1.", current_session.objects)
    current_session.objects.get("open_sessions").append(args)
    print("post2.", current_session.objects)
    script_type = "post"
    logging.write(True, f"{script_type} testing1")
    logging.write(False, f"{script_type} testing2")
    logging.write(True, f"{script_type} testing3", commit_now=True)
    print(f"{script_type}3.")
