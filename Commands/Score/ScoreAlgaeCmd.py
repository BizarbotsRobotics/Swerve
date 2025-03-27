import commands2
import commands2.cmd

from Commands.Intake.AlgaeOuttakeCmd import AlgaeOuttakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina




class ScoreAlgaeCmd(commands2.SequentialCommandGroup):
    """A command that will remove an algae and score a coral on the reefs"""

    def __init__(self, gorgina : Gorgina, coralina : Coralina, elevator: Elevator) -> None:
        self.coralina = coralina
        self.elevator = elevator
        self.gorgina = gorgina
        super().__init__()
        self.addRequirements(self.gorgina, self.coralina, self.elevator)
        self.addCommands(AlgaeOuttakeCmd(self.gorgina), SetCoralPivotCmd(self.coralina, 186), SetAlgaePivotCmd(self.gorgina, 155), SetElevatorPositionCmd(self.elevator, 0))
