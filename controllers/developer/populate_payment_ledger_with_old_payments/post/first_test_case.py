"""
This test script is to run specific utilities after executing main url
such as switching payment_ledger flag to False.
"""
from utility.config_utility import update_feature_flag
import time


def main(*args):
    update_feature_flag("payment_ledger", "False")
    time.sleep(15)

