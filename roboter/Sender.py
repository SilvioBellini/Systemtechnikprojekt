import flink
import driver
import time
import Network

class Sender(Network):
    def __init__(self):
        Network.__init__(self)

    def sendMessage(self, id, data):
        message = [id, data]
        self.client.send(str(message))
    

