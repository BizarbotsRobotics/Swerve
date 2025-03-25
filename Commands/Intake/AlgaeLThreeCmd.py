import commands2
import commands2.cmd

from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina



class AlgaeLThreeCmd(commands2.SequentialCommandGroup):
    """A command that will prepare coral intake from the human player station"""

    def __init__(self, gorgina : Gorgina, elevator: Elevator) -> None:
        self.gorgina = gorgina
        self.elevator = elevator
        super().__init__()
        self.addRequirements(self.gorgina, self.elevator)
        self.addCommands(SetAlgaePivotCmd(self.gorgina, 100), SetElevatorPositionCmd(self.elevator, 18.7), AlgaeIntakeCmd(self.gorgina))
