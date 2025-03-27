import commands2
import commands2.cmd
import wpilib

from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.AlgaeOuttakeCmd import AlgaeOuttakeCmd
from Commands.Intake.CoralIntakeCmd import CoralIntakeCmd
from Commands.Intake.CoralOuttakeCmd import CoralOuttakeCmd
from Commands.Score.ReefScoreLThreeCmd import ReefScoreLThreeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Commands.Score.ScoreProcessorCmd import ScoreProcessorCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina




class ScoreCmd(commands2.SequentialCommandGroup):
    """A command that will remove an algae and score a coral on the reefs"""

    def __init__(self, gorgina : Gorgina, coralina : Coralina, elevator: Elevator) -> None:
        self.coralina = coralina
        self.elevator = elevator
        self.gorgina = gorgina
        super().__init__()
        self.addRequirements(self.gorgina, self.coralina, self.elevator)

        self.addCommands(CoralOuttakeCmd(self.coralina), SetCoralPivotCmd(self.coralina, 186), SetAlgaePivotCmd(self.gorgina, 90), SetElevatorPositionCmd(self.elevator, 0))
