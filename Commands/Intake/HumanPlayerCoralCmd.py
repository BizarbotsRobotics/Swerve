import commands2
import commands2.cmd
import wpilib

from Commands.Intake.CoralIntakeCmd import CoralIntakeCmd
from Commands.Intake.CoralOuttakeCmd import CoralOuttakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina



class HumanPlayerCoralCmd(commands2.SequentialCommandGroup):
    """A command that will prepare coral intake from the human player station"""

    def __init__(self, coralina : Coralina, elevator: Elevator, gorgina: Gorgina) -> None:
        self.coralina = coralina
        self.elevator = elevator
        self.gorgina = gorgina
        super().__init__()
        self.addRequirements(self.coralina, self.elevator, self.gorgina)
        self.addCommands(SetCoralPivotCmd(self.coralina, 124), SetAlgaePivotCmd(self.gorgina, 100), SetElevatorPositionCmd(self.elevator, 4.3), SetCoralPivotCmd(self.coralina, 80), CoralIntakeCmd(self.coralina).withTimeout(2), SetCoralPivotCmd(self.coralina, 124), SetElevatorPositionCmd(self.elevator,0))
