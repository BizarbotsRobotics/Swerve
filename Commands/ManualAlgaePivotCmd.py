import commands2
import commands2.cmd

from Subsystems.Gorgina.Gorgina import Gorgina

class ManualAlgaePivotCmd(commands2.Command):
    """A command that will toggle the algae intake."""

    def __init__(self, gorgina: Gorgina, power) -> None:
        self.gorgina = gorgina
        self.power = power
        super().__init__()
        self.addRequirements(self.gorgina)

    def initialize(self):
        pass

    def execute(self):
        self.gorgina.setPivotPower(self.power())
        
    def end(self, interrupted: bool):
       pass

    def isFinished(self) -> bool:
        # End when the controller is at the reference.
        return True