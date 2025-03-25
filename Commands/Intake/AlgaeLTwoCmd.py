import commands2
import commands2.cmd
import wpilib

from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.CoralIntakeCmd import CoralIntakeCmd
from Commands.Intake.CoralOuttakeCmd import CoralOuttakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina



class AlgaeLTwoCmd(commands2.SequentialCommandGroup):
    """A command that will set algae intake position for level Two"""

    def __init__(self, gorgina : Gorgina, elevator: Elevator) -> None:
        self.gorgina = gorgina
        self.elevator = elevator
        super().__init__()
        self.addRequirements(self.gorgina, self.elevator)
        self.addCommands(SetAlgaePivotCmd(self.gorgina, 100), SetElevatorPositionCmd(self.elevator, 18.7), AlgaeIntakeCmd(self.gorgina))
