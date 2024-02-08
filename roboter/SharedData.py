class SharedData():
    def __init__(self):
        self.approvalKitchen = None
        self.approvalCounter = None
        self.glassSlot = None
    
    def setData(self, id, data):
        """
        Saving the data according to its identification number
        ID: 0 = Approval Kitchen
            1 = Approval Counter
            2 = Glass Slot
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
        ID: 0 = Approval Kitchen
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