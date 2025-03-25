import commands2
import commands2.cmd
import wpilib

from Subsystems.Coralina.Coralina import Coralina



class SetCoralPivotCmd(commands2.Command):
    """A command that will set the pivot for the coral intake to a specified position"""

    def __init__(self, coralina : Coralina, position) -> None:
        self.coralina = coralina
        self.position = position
        super().__init__()
        self.addRequirements(self.coralina)

    def initialize(self):  
        pass

    def execute(self):

        self.coralina.setCoralPivotPosition(self.position)
        print("pibot")

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        if (self.position - 5) < self.coralina.getCoralPivotPosition() < (self.position + 5):
            return True
        return False
