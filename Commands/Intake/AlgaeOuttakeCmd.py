import commands2
import commands2.cmd
import wpilib

from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Gorgina.Gorgina import Gorgina



class AlgaeOuttakeCmd(commands2.Command):
    """A command that will run the coral intake. Ends when a coral is stored"""

    def __init__(self, gorgina : Gorgina) -> None:
        self.gorgina = gorgina
        super().__init__()
        self.addRequirements(self.gorgina)

    def initialize(self):  
        pass

    def execute(self):

        self.gorgina.setIntakePower(.5)

    def end(self, interrupted: bool):
        self.gorgina.setIntakePower(0)
        pass

    def isFinished(self) -> bool:
        return not self.gorgina.getAlgaeStored()
