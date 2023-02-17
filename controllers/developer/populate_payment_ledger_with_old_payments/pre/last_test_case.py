"""
This test script is to run specific utilities before executing main url
such as switching payment_ledger flag to True.
"""
from utility.config_utility import update_feature_flag
import time


def main(*args):
    update_feature_flag("payment_ledger", "True")
    time.sleep(15)

