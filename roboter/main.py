try:
    import driver
    import flink
    import time
except ModuleNotFoundError:
    pass
from sharedData import *
from network import *

username = "team2"
password = "1234"
topic = "coop"

if(__name__ == "__main__"):
    print("State: Initializing Objects")

    network = Network(username, password, topic)
    sharedData = SharedData()
