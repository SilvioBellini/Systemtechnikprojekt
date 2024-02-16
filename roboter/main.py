try:
    import driver
    import flink
    import time
except ModuleNotFoundError:
    pass
from sharedData import *
from communication import *
from api import *
from stopWatch import *

username = "test" #team2
password = "test" #rHGpIGxo0o1k
topic = "test/team2" #Coop

if(__name__ == "__main__"):
    mirbot = API()
    sharedData = SharedData()
    com = Communication(username, password, topic, sharedData)
    watch = StopWatch()
    mode = 0