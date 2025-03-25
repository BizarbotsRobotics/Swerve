import commands2
import commands2.cmd
import wpilib


from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Commands.Intake.AlgaeOuttakeCmd import AlgaeOuttakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina



class BargeScoreCmd(commands2.SequentialCommandGroup):
    """A command that will release an algae into the barge"""

    def __init__(self, gorgina : Gorgina, elevator: Elevator) -> None:
        self.gorgina = gorgina
        self.elevator = elevator
        super().__init__()
        self.addRequirements(self.gorgina, self.elevator)
        self.addCommands(SetAlgaePivotCmd(self.gorgina, 100), SetElevatorPositionCmd(self.elevator, 18.7), AlgaeOuttakeCmd(self.gorgina), SetAlgaePivotCmd(90), SetElevatorPositionCmd(0))
