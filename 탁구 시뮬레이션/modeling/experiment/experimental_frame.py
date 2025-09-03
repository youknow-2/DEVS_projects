from SimulationEngine.ClassicDEVS.DEVSCoupledModel import DEVSCoupledModel
from modeling.experiment.atomic.referee import Referee


class ExperimentalFrame(DEVSCoupledModel):

    def __init__(self, ID):
        super().__init__(ID)
        
        referee = Referee('Referee')

        self.addModel(referee)

        self.addInputPort('ball_to_referee')

        self.addOutputPort('ball_to_player_A')
        self.addOutputPort('ball_to_player_B')

        self.addExternalInputCoupling('ball_to_referee', referee, 'ball_from_players')

        self.addExternalOutputCoupling(referee, 'ball_to_player_A', 'ball_to_player_A')
        self.addExternalOutputCoupling(referee, 'ball_to_player_B', 'ball_to_player_B')