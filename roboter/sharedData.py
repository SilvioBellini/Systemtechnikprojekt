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
        Saving the data according to its identification number. Checking for correct types and values.

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
                if(isinstance(data, bool)):
                    self.approvalKitchen = data
                else:
                    print("Invalid type of data! \nIs: {} \nShould be: bool \n".format(type(data)))

            case 1:
                if(isinstance(data, bool)):
                    self.approvalCounter = data
                else:
                    print("Invalid type of data! \nIs: {} \nShould be: bool \n".format(type(data)))

            case 2:
                if(isinstance(data, int)):
                    if(data >= 1 and data <= 5):
                        self.glassSlot = data
                    else:
                        print("Invalid value of data! \nIs: {} \nShould be: 1-5 \n".format(data))
                else:
                    print("Invalid type of data! \nIs: {} \nShould be: int \n".format(type(data)))
                    
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