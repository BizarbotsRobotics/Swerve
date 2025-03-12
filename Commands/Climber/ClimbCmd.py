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
        if self.power > .1 or self.power < -.1:
            self.climber.setPower(self.power())
        else:
            self.climber.setPower(0)

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
