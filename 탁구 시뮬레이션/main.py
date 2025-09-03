from SimulationEngine.SimulationEngine import SimulationEngine
from SimulationEngine.Utility.Configurator import Configurator
from modeling.outmost import Outmost
from modeling.simulation.atomic.player import Player


INF = float('inf')

objConfiguration = Configurator()
objConfiguration.addConfiguration('player_A_level', Player.LEVEL_BEGINNER)
objConfiguration.addConfiguration('player_B_level', Player.LEVEL_BEGINNER)

outmost = Outmost('Outmost', objConfiguration)

engine = SimulationEngine()
engine.setOutmostModel(outmost)
engine.run(
    maxTime=INF,
    ta=-1,
    visualizer=False,
    logFileName='log.txt',
    logGeneral=False,
    logActivateState=False,
    logActivateMessage=False,
    logActivateTA=False,
    logStructure=False,
)