from SimulationEngine.ClassicDEVS.DEVSCoupledModel import DEVSCoupledModel
from modeling.simulation.atomic.player import Player


class SimulationModel(DEVSCoupledModel):

    def __init__(self, ID, playerALevel, playerBLevel):
        super().__init__(ID)
        
        playerA = Player('Player A', playerALevel)
        playerB = Player('Player B', playerBLevel)

        self.addModel(playerA)
        self.addModel(playerB)

        self.addInputPort('ball_to_player_A')
        self.addInputPort('ball_to_player_B')

        self.addOutputPort('ball_to_referee')

        self.addExternalInputCoupling('ball_to_player_A', playerA, 'ball_from_referee')
        self.addExternalInputCoupling('ball_to_player_B', playerB, 'ball_from_referee')

        self.addExternalOutputCoupling(playerA, 'ball_to_referee', 'ball_to_referee')
        self.addExternalOutputCoupling(playerB, 'ball_to_referee', 'ball_to_referee')

        self.addInternalCoupling(playerA, 'ball_to_opponent', playerB, 'ball_from_opponent')
        self.addInternalCoupling(playerB, 'ball_to_opponent', playerA, 'ball_from_opponent')