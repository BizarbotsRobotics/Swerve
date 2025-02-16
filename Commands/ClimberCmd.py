import commands2
import commands2.cmd
import wpilib

from Subsystems.Cimber.Climber import Climber


class ClimberCmd(commands2.Command):
    """A command that will align the robot to an April Tag. Not great for speed but last resort"""

    def __init__(self, climber : Climber, powerNeg, powerPos) -> None:
        self.climber = climber
        self.powerNeg = powerNeg
        self.powerPos = powerPos
        super().__init__()
        self.addRequirements(self.climber)

    def initialize(self):  
        pass

    def execute(self):
        self.climber.setPower(self.powerPos() + self.powerNeg())

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
