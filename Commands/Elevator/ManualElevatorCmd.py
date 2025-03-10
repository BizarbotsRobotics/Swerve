import commands2
import commands2.cmd
import wpilib

from Subsystems.Elevator.Elevator import Elevator
from constants import SwerveConstants


class ManualElevatorCmd(commands2.Command):
    """A command that will run manual controls for the elevator height"""

    def __init__(self, elevator : Elevator, power) -> None:
        self.elevator = elevator
        self.power = power
        super().__init__()
        self.addRequirements(self.elevator)

    def initialize(self):  
        pass

    def execute(self):

        self.elevator.setElevatorPower(self.power())

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
