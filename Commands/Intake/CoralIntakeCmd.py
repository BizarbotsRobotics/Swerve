import commands2
import commands2.cmd
import wpilib

from Subsystems.Coralina.Coralina import Coralina



class CoralIntakeCmd(commands2.Command):
    """A command that will run the coral intake. Ends when a coral is stored"""

    def __init__(self, coralina : Coralina) -> None:
        self.coralina = coralina
        super().__init__()
        self.addRequirements(self.coralina)

    def initialize(self):  
        pass

    def execute(self):

        self.coralina.setIntakePower(-1)

    def end(self, interrupted: bool):
        self.coralina.setIntakePower(-.02)
        pass

    def isFinished(self) -> bool:
        return self.coralina.getCoralinaStored()
