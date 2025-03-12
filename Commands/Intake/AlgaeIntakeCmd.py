import commands2
import commands2.cmd
import wpilib

from Subsystems.Gorgina.Gorgina import Gorgina



class AlgaeIntakeCmd(commands2.Command):
    """A command that will run the algae intake. Ends when an algae is stored"""

    def __init__(self, gorgina : Gorgina) -> None:
        self.gorgina = gorgina
        super().__init__()
        self.addRequirements(self.gorgina)

    def initialize(self):  
        pass

    def execute(self):

        self.gorgina.setIntakePower(.35)

    def end(self, interrupted: bool):
        self.gorgina.setIntakePower(.1)
        pass

    def isFinished(self) -> bool:
        return self.gorgina.getAlgaeStored()
