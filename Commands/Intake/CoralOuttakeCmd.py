import commands2
import commands2.cmd
import wpilib

from Subsystems.Coralina.Coralina import Coralina



class CoralOuttakeCmd(commands2.Command):
    """A command that will run the coral outtake. Ends when there is no coral stored"""

    def __init__(self, coralina : Coralina) -> None:
        self.coralina = coralina
        super().__init__()
        self.addRequirements(self.coralina)

    def initialize(self):  
        pass

    def execute(self):

        self.coralina.setIntakePower(.7)

    def end(self, interrupted: bool):
        self.coralina.setIntakePower(0)
        pass

    def isFinished(self) -> bool:
        return not self.coralina.getCoralinaStored()
