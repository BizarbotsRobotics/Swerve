import commands2
import commands2.cmd
import wpilib

from Subsystems.Cimber.Climber import Climber


class ClimbCmd(commands2.Command):
    """A command that will manually control the position of the climber"""

    def __init__(self, climber : Climber, power) -> None:
        self.climber = climber
        self.power = power

        super().__init__()
        self.addRequirements(self.climber)

    def initialize(self):  
        pass

    def execute(self):
        self.climber.setPower(self.power())

    def end(self, interrupted: bool):
        self.climber.setPower(0)

        pass

    def isFinished(self) -> bool:
        return False
