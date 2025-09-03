from SimulationEngine.ClassicDEVS.DEVSCoupledModel import DEVSCoupledModel
from SimulationEngine.Utility.Configurator import Configurator
from modeling.experiment.experimental_frame import ExperimentalFrame
from modeling.simulation.simulation_model import SimulationModel


class Outmost(DEVSCoupledModel):

    def __init__(self, ID, objConfiguration: Configurator):
        super().__init__(ID)

        self.objConfiguration = objConfiguration
        
        playerALevel = objConfiguration.getConfiguration('player_A_level')
        playerBLevel = objConfiguration.getConfiguration('player_B_level')

        EF = ExperimentalFrame('Experimental Frame')
        SM = SimulationModel('Simulation Model', playerALevel, playerBLevel)
        
        self.addModel(EF)
        self.addModel(SM)

        self.addInternalCoupling(EF, 'ball_to_player_A', SM, 'ball_to_player_A')
        self.addInternalCoupling(EF, 'ball_to_player_B', SM, 'ball_to_player_B')
        self.addInternalCoupling(SM, 'ball_to_referee', EF, 'ball_to_referee')