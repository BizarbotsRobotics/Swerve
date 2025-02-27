import commands2
import commands2.cmd
import wpilib

from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina
from constants import ElevatorConstants



class SetAlgaePivotCmd(commands2.Command):
    """A command that will align the robot to an April Tag. Not great for speed but last resort"""

    def __init__(self, gorgina : Gorgina, position) -> None:
        self.gorgina = gorgina
        self.position = position
        super().__init__()
        self.addRequirements(self.gorgina)

    def initialize(self):  
        pass

    def execute(self):
        self.gorgina.setAlgaePivotPosition(self.position)

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
