import commands2
import commands2.cmd
import wpilib

from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.AlgaeOuttakeCmd import AlgaeOuttakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina


class ScoreProcessorCmd(commands2.SequentialCommandGroup):
    """A command that will release an algae into the processor"""

    def __init__(self, gorgina : Gorgina, elevator : Elevator) -> None:
        self.gorgina = gorgina
        self.elevator = elevator
        super().__init__()

        self.addRequirements(self.gorgina, self.elevator)
        self.addCommands(SetElevatorPositionCmd(self.elevator, 3), SetAlgaePivotCmd(self.gorgina, 70), commands2.WaitCommand(.5), AlgaeOuttakeCmd(self.gorgina))
    

