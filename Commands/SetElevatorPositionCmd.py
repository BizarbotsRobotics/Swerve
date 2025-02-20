import commands2
import commands2.cmd
import wpilib

from Subsystems.Elevator.Elevator import Elevator, lOneElevatorHeight
from constants import ElevatorConstants



class SetElevatorPositionCmd(commands2.Command):
    """A command that will align the robot to an April Tag. Not great for speed but last resort"""

    def __init__(self, elevator : Elevator, position) -> None:
        self.elevator = elevator
        self.position = position
        super().__init__()
        self.addRequirements(self.elevator)

    def initialize(self):  
        pass

    def execute(self):

        self.elevator.setElevatorPosition(self.position())

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
