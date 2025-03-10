import commands2
import commands2.cmd
import wpilib

from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina
from constants import ElevatorConstants



class SetAlgaePivotCmd(commands2.Command):
    """A command that will set the algae pivot to a specified position"""

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
        if (self.position - 5) < self.gorgina.getAlgaePivotPosition() < (self.position + 5):
            return True
        return False
