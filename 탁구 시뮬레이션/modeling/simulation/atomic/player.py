import random

from SimulationEngine.ClassicDEVS.DEVSAtomicModel import DEVSAtomicModel
from modeling.messages.ball import Ball


INF = float('inf')


class Player(DEVSAtomicModel):
    
    LEVEL_BEGINNER = 0
    LEVEL_INTERMEDIATE = 1
    LEVEL_EXPERT = 2

    def __init__(self, ID, level):
        super().__init__(ID)

        self.addStateVariable('state', 'WAIT')

        self.addInputPort('ball_from_referee')
        self.addInputPort('ball_from_opponent')

        self.addOutputPort('ball_to_referee')
        self.addOutputPort('ball_to_opponent')

        self.ball: Ball
        self.setPlayerCapability(level)
        
    def setPlayerCapability(self, level):
        if level == Player.LEVEL_BEGINNER:
            self.capabilityMin = 20
            self.capabilityMax = 80
            self.serveMissRate = 0.3
        elif level == Player.LEVEL_INTERMEDIATE:
            self.capabilityMin = 30
            self.capabilityMax = 90
            self.serveMissRate = 0.2
        elif level == Player.LEVEL_EXPERT:
            self.capabilityMin = 40
            self.capabilityMax = 100
            self.serveMissRate = 0.1

    def funcExternalTransition(self, strPort, event):
        state = self.getStateValue('state')
        if state == 'WAIT':
            self.ball = event
            if strPort == 'ball_from_referee':
                self.setStateValue('state', 'SERVE')
            elif strPort == 'ball_from_opponent':
                self.setStateValue('state', 'RECEIVE')
        elif state == 'SERVE':
            pass
        elif state == 'RECEIVE':
            pass

    def funcOutput(self):
        state = self.getStateValue('state')
        if state == 'WAIT':
            pass
        elif state == 'SERVE':
            if self.tryToServe():
                self.addOutputEvent('ball_to_opponent', self.ball)
            else:
                self.addOutputEvent('ball_to_referee', self.ball)
        elif state == 'RECEIVE':
            if self.tryToReceive():
                self.addOutputEvent('ball_to_opponent', self.ball)
            else:
                self.addOutputEvent('ball_to_referee', self.ball)
    
    def funcInternalTransition(self):
        state = self.getStateValue('state')
        if state == 'WAIT':
            pass
        elif state == 'SERVE':
            self.setStateValue('state', 'WAIT')
        elif state == 'RECEIVE':
            self.setStateValue('state', 'WAIT')

    def funcTimeAdvance(self):
        state = self.getStateValue('state')
        if state == 'WAIT':
            return INF
        elif state == 'SERVE':
            return 0
        elif state == 'RECEIVE':
            return 1

    def funcSelect(self):
        pass
    
    def tryToServe(self):
        if self.isSuccessfulServe():
            attackPower = self.getRandomAbility()
            self.ball.serve(self.ID, attackPower)
            return True
        else:
            self.ball.fail_to_serve(self.ID)
            return False
    
    def isSuccessfulServe(self):
        result = self.serveMissRate < random.random()
        return result

    def tryToReceive(self):
        ballAttackPower = self.ball.get_attack_power()
        playerDefensePower = self.getRandomAbility()
        if self.isSuccessfulReceive(ballAttackPower, playerDefensePower):
            playerAttackPower = self.getRandomAbility()
            self.ball.receive(self.ID, playerDefensePower, playerAttackPower)
            return True
        else:
            self.ball.fail_to_receive(self.ID, playerDefensePower)
            return False
    
    def isSuccessfulReceive(self, attackPower, DefensePower):
        if attackPower <= DefensePower:
            return True
        elif random.random() < 0.5:
            return True
        else:
            return False

    def getRandomAbility(self):
        ability = random.randint(self.capabilityMin, self.capabilityMax)
        return ability