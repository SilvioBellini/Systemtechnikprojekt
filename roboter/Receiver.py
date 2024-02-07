import flink
import driver
import time
import Network

class Receiver(Network):
    def __init__(self):
        Network.__init__(self)

    def receiveMessage(self):
        message = self.client.read()

        if(message is not None):
            decodedMessage = eval(message)
            id = decodedMessage[0]
            data = decodedMessage[1]
            self.sharedData.setData(id, data)

            