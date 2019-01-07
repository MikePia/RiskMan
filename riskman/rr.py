'''
Show the amount of shares to buy give a set risk value
@author: Mike Petersen
@creation_data: 5/1/19
'''
from typing import List
# pylint: disable = C0103
DEFAULT_VALUE = 50.00
STOPS = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1., 1.25, 1.50]

class RiskMan(object):
    '''
    Risk management via risking a specific dollar amount.
    '''

    def __init__(self, stops = None):
        self.stops = List[float]
        if stops:
            self.setStopLimits(stops)
        else:
            self.stops = STOPS

    def runCmdline(self):
        '''
        When run from commandline, request a risk amount and print a set list of
        Shares to purchase for given stop loss based on the risk amount
        '''
        while True:
            try:
                risk = input("Please input the max risk for the day:     ")
                risk = float(risk)
                break
            except ValueError:
                print("Please enter a valid monetary amount")

        print("\nIn order to risk ${0:.2f} dollars per trade:".format(risk))
        for s in self.stops:

            print("Buy {0:-4.0f} shares for a ${1:.2f} {2:6} stop loss"
                .format(risk/s, s, "cent" if s < 1 else "dollar"))


    def getrisk(self, riskAmount):
        '''
        :params riskAmount: A float, the intended dollar risk amount for a trade.
        :return: A string displaying the number of shares to purchase in order to risk
                riskAmount for the given stoplosses.
        '''
        if not isinstance(riskAmount, float):
            try:
                riskAmount = float(riskAmount)
            except ValueError:
                print('Risk amount was misformatted. Setting it to default value.')
                riskAmount = DEFAULT_VALUE
        retMsg = "In order to risk ${0:.02f} dollars".format(riskAmount)

        for s in self.stops:
            newLine = "Buy {0:-4.0f} shares for a ${1:.2f} {2:6} stop loss".format(
                riskAmount/s, s, "cent" if s < 1 else "dollar")
            retMsg = retMsg + '\n' + newLine
        return retMsg


    def setStopLimits(self, listOfStops):
        '''
        :params listOfStops: A string list of amounts, seperated by comma,  that represent
                the |Value| of the diffence between the entry and a stop loss.
        '''
        listOfStrings = listOfStops.split(',')
        errorMessage = []
        listOfFloats = []
        for stop in listOfStrings:
            stop = stop.strip()
            try:
                stop = float(stop)
                listOfFloats.append(stop)
            except ValueError:
                errorMessage.append(f"Failed to convert {stop} to a float")
        self.stops.clear()
        self.stops = listOfFloats.copy()
        self.stops.sort()
        return errorMessage if errorMessage else None

    def addStopLimit(self, stop):
        '''
        Add a single entry to self.stops
        '''
        assert isinstance(stop, float)
        if stop not in self.stops:
            self.stops.append(stop)
            self.stops.sort()


    def removeStopLimit(self, stop):
        '''
        :params stop: Remove the given amont from the list of stop losses to display
        '''
        if stop in self.stops:
            self.stops.remove(stop)

    def getStops(self):
        '''
        :return: A string formatted list of stops. 
            If the float list is needed, retrieve self.stops
        '''
        theList = str(self.stops)[1:-1]
        return theList


if __name__ == '__main__':
    rm = RiskMan()
    rm.runCmdline()
    # print(rm.getrisk(250.50))
