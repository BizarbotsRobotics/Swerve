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

    def __init__(self, gorgina : Gorgina, elevator: Elevator, coralina: Coralina) -> None:
        self.gorgina = gorgina
        self.elevator = elevator
        self.coralina = coralina
        super().__init__()
        self.addRequirements(self.gorgina, self.elevator, self.coralina)
        self.addCommands(SetCoralPivotCmd(self.coralina, 186), SetAlgaePivotCmd(self.gorgina, 175), SetElevatorPositionCmd(self.elevator, 2.5), AlgaeIntakeCmd(self.gorgina), commands2.WaitCommand(1), SetAlgaePivotCmd(self.gorgina, 120), SetElevatorPositionCmd(self.elevator, 0))
