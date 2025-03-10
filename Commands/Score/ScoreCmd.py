import commands2
import commands2.cmd
import wpilib

from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.CoralIntakeCmd import CoralIntakeCmd
from Commands.Score.ReefScoreLThreeCmd import ReefScoreLThreeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
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
        self.addCommands(SetElevatorPositionCmd(self.elevator, 4), SetAlgaePivotCmd(self.gorgina, 90), AlgaeIntakeCmd(self.gorgina),SetAlgaePivotCmd(self.gorgina,120), ReefScoreLThreeCmd(self.coralina, self.elevator))

    def isFinished(self) -> bool:
        return not self.coralina.getCoralinaStored()
        pass
