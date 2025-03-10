import commands2
import commands2.cmd
import wpilib

from Subsystems.Coralina.Coralina import Coralina



class ManualCoralPivotCmd(commands2.Command):
    """A command that will run manual controls for the coral pivot"""

    def __init__(self, coralina : Coralina, power) -> None:
        self.coralina = coralina
        self.power = power
        super().__init__()
        self.addRequirements(self.coralina)

    def initialize(self):  
        pass

    def execute(self):

        self.coralina.setPivotPower(self.power())

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
