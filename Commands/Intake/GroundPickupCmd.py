import commands2
import commands2.cmd
import wpilib

from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina



class GroundPickupCmd(commands2.SequentialCommandGroup):
    """A command that will run algae ground intake"""

    def __init__(self, coralina: Coralina, gorgina : Gorgina, elevator : Elevator) -> None:
        self.coralina = coralina
        self.gorgina = gorgina
        self.elevator = elevator
        super().__init__()

        self.addRequirements(self.gorgina, self.elevator)
        self.addCommands(SetCoralPivotCmd(self.coralina, 100), SetElevatorPositionCmd(self.elevator, .5), SetAlgaePivotCmd(self.gorgina, 70), AlgaeIntakeCmd(self.gorgina), SetAlgaePivotCmd(self.gorgina, 100))
