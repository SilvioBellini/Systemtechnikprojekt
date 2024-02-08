import driver
import flink
import time
from network import *
from sharedData import *

if(__name__ == "__main__"):
    print("Initializing")
    network = Network()
    sharedData = SharedData()

    while True:
        sharedData.setData(0, True)
        print(sharedData.getData(0))
        time.sleep(3)
        sharedData.setData(0, False)
        print(sharedData.getData(0))
        time.sleep(3)