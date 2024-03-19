class SharedData:
    """
    Class for saving the data the gets sent to and received from the partner robot.
    """

    def __init__(self):
        self.approvalKitchen = False
        self.approvalCounter = False
        self.glassSlot = 99
    
    def setData(self, id : int, data) -> None:
        """
        Saving the data according to its identification number.

        Prameters
        ----------
        id: Unique identification number of the transmitted information
            0 = Approval Kitchen \n
            1 = Approval Counter \n
            2 = Glass Slot 
        data: Information that should get saved

        Returns
        ----------
        None
        """

        match id:
            case 0:
                self.approvalKitchen = data
                print(self.approvalKitchen)
            case 1: 
                self.approvalCounter = data
            case 2: 
                self.glassSlot = data
            case _:
                print("Invalid ID! Unable to set data")

    def getData(self, id : int) -> any:
        """
        Returning the data according to its identification number.

        Paramters
        ----------
        id: Unique identification number of the transmitted information 
            0 = Approval Kitchen \n
            1 = Approval Counter \n
            2 = Glass Slot

        Returns
        ----------
        any
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
