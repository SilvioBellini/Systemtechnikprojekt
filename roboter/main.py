try:
    import driver
    import flink
    import time
except ModuleNotFoundError:
    pass
from sharedData import *
from network import *

username = "test" #Team2
password = "test" #rHGpIGxo0o1k
topic = "test/team2" #Coop

if(__name__ == "__main__"):
    print("State: Initializing Objects")

    sharedData = SharedData()
    network = Network(username, password, topic, sharedData)
    switch = False

    while True:
        #switch = not switch
        #network.sendMessage(0, switch)
        #time.sleep(2)
        network.receiveMessage()
        print(sharedData.getData(0))
        print(sharedData.getData(1))
        print(sharedData.getData(2), "\n")
        time.sleep(3)
