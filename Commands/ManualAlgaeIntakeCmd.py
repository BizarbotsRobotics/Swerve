import commands2
import commands2.cmd
import wpilib

from Subsystems.Gorgina.Gorgina import Gorgina






class ManualAlgaeIntakeCmd(commands2.Command):
    """A command that will align the robot to an April Tag. Not great for speed but last resort"""

    def __init__(self, gorgina : Gorgina, power) -> None:
        self.gorgina = gorgina
        self.power = power
        super().__init__()
        #self.addRequirements(self.gorgina)

    def initialize(self):  
        pass

    def execute(self):
        self.gorgina.setIntakePower(self.power)

    def end(self, interrupted: bool):
        self.gorgina.setIntakePower(.1)
        pass

    def isFinished(self) -> bool:
        return False
