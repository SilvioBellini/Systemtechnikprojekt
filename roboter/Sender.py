import Network

class Sender(Network):
    def __init__(self):
        Network.__init__(self)

    def sendMessage(self, id, data):
        """
        Sending a string consisting of an identification number and a specific information 
        to the topic specified in its parent class
        """

        message = [id, data]
        self.client.send(str(message))
        
        print("Sent Message: ", message)
    

