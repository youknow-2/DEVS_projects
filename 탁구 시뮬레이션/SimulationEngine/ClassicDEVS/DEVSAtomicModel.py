from SimulationEngine.ClassicDEVS.DEVSModel import DEVSModel
from SimulationEngine.Utility.Event import Event
from SimulationEngine.Utility.Logger import Logger

class  DEVSAtomicModel(DEVSModel):

    def __init__(self,ID):
        super().__init__()
        self.blnContinue = False
        self.setModelID(ID)
        self.time = 0

    def receiveExternalEvent(self,port,event,currentTime):
        self.blnContinue = False
        self.funcExternalTransition(port,event)
        if self.blnContinue == False:
            self.time = currentTime
            self.execTimeAdvance()

    def addOutputEvent(self,varOutput,varMessage):
        self.engine.addEvent(Event(self,varOutput,varMessage))

    def performTimeAdvance(self,currentTime):
        self.time = currentTime
        if self.nextTime <= currentTime:
            self.funcOutput()
            self.funcInternalTransition()
            self.execTimeAdvance()

    def queryTimeAdvance(self):
        self.logger.log(Logger.TA,"Query MIN TA ("+self.getModelID()+") : " + str(self.nextTimeAdvance))
        return self.nextTimeAdvance

    def queryTime(self):
        self.logger.log(Logger.TA,"Query Time ("+self.getModelID()+") : " + str(self.nextTime))
        return self.nextTime

    def continueTimeAdvance(self):
        self.blnContinue = True

    def execTimeAdvance(self):
        self.nextTimeAdvance = self.funcTimeAdvance()
        self.nextTime = self.time + self.nextTimeAdvance

    def checkContinue(self):
        value = self.blnContinue
        self.blnContinue = False
        return value

    def funcOutput(self):
        pass

    def funcExternalTransition(self, strPort, event):
        pass

    def funcInternalTransition(self):
        pass

    def funcTimeAdvance(self):
        pass

    def funcSelect(self):
        pass

if __name__ == "__main__":
    pass