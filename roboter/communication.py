try:
    import driver
except ModuleNotFoundError:
    pass

from config import Config
from sharedData import SharedData

class Communication:
    """
    Class for establishing a wireless connection to a MQTTX-Server and exchanging information.

    Parameters
    ----------
    config: Object of the Config class
    sharedData: Object of the SharedData class
    """

    def __init__(self, config : Config, sharedData : SharedData):
        # Initializing a client and establishing a connection to a specific topic
        self.config = config
        self.sharedData = sharedData

        try:
            self.client = driver.MessagingClient(self.config.username, self.config.password, self.config.topic)
            self.client.connect()
        except(NameError, AttributeError) as error:
            print("Connection failed - {}".format(error))

        if(self.client.is_connected()):
            print("Connection established to: ", self.client.host, " with the topic ", self.config.topic)
        else:
            print("No connection can be established!")

    def sendMessage(self, id : int, data) -> None:
        """
        Sending a string consisting of an identification number and a specific information to the specified topic.

        Parameters
        ----------
        id: Unique identification number of the transmitted information 
            0 = Approval Kitchen \n
            1 = Approval Counter \n
            2 = Glass Slot
        data: Information that should be transmitted

        Returns
        ----------
        None
        """

        message = [id, data]
        self.client.send(str(message))
        
        print("Sent Message: {} \n".format(message))

    def receiveMessage(self) -> None:
        """
        Searching for an unread message on the specified topic. Saving received information in the SharedData Class.

        Returns
        ----------
        None
        """

        message = self.client.read()

        # Decoding message if possible
        try:
            if(message is not None):
                decodedMessage = eval(message)
                id = decodedMessage[0]
                data = decodedMessage[1]
                self.sharedData.setData(id, data)
                
                print("Received Message: {} \n".format(message))
        except:
            print("Can't evaluate message! \n")