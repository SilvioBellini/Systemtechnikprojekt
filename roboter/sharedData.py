class SharedData():
    """
    This class saves the data the gets sent to and received from the partner robot.
    """

    def __init__(self):
        self.approvalKitchen = None
        self.approvalCounter = None
        self.glassSlot = None
    
    def setData(self, id, data):
        """
        Saving the data according to its identification number

        Prameters:
            ID: Unique identification number of the transmitted information
                0 = Approval Kitchen
                1 = Approval Counter
                2 = Glass Slot
            Data: Information that should get saved
        """

        match id:
            case 0:
                self.approvalKitchen = data
            case 1: 
                self.approvalCounter = data
            case 2: 
                self.glassSlot = data
            case _:
                print("Invalid ID! Unable to set data")

    def getData(self, id):
        """
        Returning the data according to its identification number

        Paramters:
            ID: Unique identification number of the transmitted information 
                0 = Approval Kitchen
                1 = Approval Counter
                2 = Glass Slot
        """
        
        match id:
            case 0:
                return self.approvalKitchen
            case 1:
                return self.approvalCounter
            case 2:
                return self.glassSlot
            case _:
                print("Invalid ID! Unable to get data")
                return None
