from env.session_manager import current_session
from env.logging_interface import logging


def main(*args):
    print("coincident1.", current_session.objects)
    current_session.objects.get("open_sessions").append(args)
    print("coincident2.", current_session.objects)
    script_type = "coincident"
    logging.write(True, f"{script_type} testing1")
    logging.write(False, f"{script_type} testing2")
    logging.write(True, f"{script_type} testing3", commit_now=True)
    print(f"{script_type}3.")

