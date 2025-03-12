import commands2
import commands2.cmd
import wpilib

from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina






class GroundPickupCmd(commands2.SequentialCommandGroup):
    """A command that will run algae ground intake"""

    def __init__(self, gorgina : Gorgina, elevator : Elevator) -> None:
        self.gorgina = gorgina
        self.elevator = elevator
        super().__init__()

        self.addRequirements(self.gorgina, self.elevator)
        self.addCommands(SetElevatorPositionCmd(self.elevator, 2), SetAlgaePivotCmd(self.gorgina, 110), AlgaeIntakeCmd(self.gorgina))


    def isFinished(self) -> bool:
        return self.gorgina.getAlgaeStored()
