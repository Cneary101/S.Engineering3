class Delivery_Person():
    def __init__(self,driver_id,area,date,completed_delivery, docket,availability_publications):
        self.driver_id = driver_id
        self.area = area
        self.date = date
        self.completed_delivery = completed_delivery
        self.docket = docket
        self.availability_publications = availability_publications
    def verifyUniqueId(self):
        pass
    #
    #
    #returns true if valid, false otherwise
    def verifyDeliveryArea(self,currentArea):
        return currentArea==self.area
    #Verify that there are available publications in stock
    #
    #
    #return true if valid, false otherwise
    def verifyAvailabilityPublications(self):
        return self.availability_publications
    #Verify that the delivery was delivered correctly
    #
    #
    #return true if valid, false otherwise
    def verifyCompletedDelivery(self):
        return self.completed_delivery
    #Verify that the delivery date is correct
    #
    #return true if valid, false otherwise
    def verifyDeliveryDate(self,currentDate):
        return currentDate==self.date
    #Verify that the docket is the required one
    #
    #
    def verifyDocket(self, currentDocket):
        return currentDocket==self.docket
