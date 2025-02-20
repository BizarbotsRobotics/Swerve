import commands2
import commands2.cmd
import wpilib

from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from constants import ElevatorConstants, CoralConstants



class SetCoralPivotCmd(commands2.Command):
    """A command that will align the robot to an April Tag. Not great for speed but last resort"""

    def __init__(self, coralina : Coralina, position) -> None:
        self.coralina = coralina
        self.position = position
        super().__init__()
        self.addRequirements(self.coralina)

    def initialize(self):  
        pass

    def execute(self):

        self.coralina.setCoralPivotPosition(self.position())

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
