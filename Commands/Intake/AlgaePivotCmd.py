import commands2
import commands2.cmd

from Subsystems.Gorgina.Gorgina import Gorgina

class AlgaePivotCmd(commands2.Command):
    """A command that will toggle the algae pivot."""

    def __init__(self, gorgina: Gorgina) -> None:
        self.gorgina = gorgina
        super().__init__()
        self.addRequirements(self.gorgina)

    def initialize(self):
        pass

    def execute(self):
        self.gorgina.setPivotPosition(.188)
        
    def end(self, interrupted: bool):
       pass

    def isFinished(self) -> bool:
        # End when the controller is at the reference.
        return True