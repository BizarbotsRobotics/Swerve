import commands2
import commands2.cmd
import wpilib

from Commands.Intake.CoralIntakeCmd import CoralIntakeCmd
from Commands.Intake.CoralOuttakeCmd import CoralOuttakeCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator



class ReefScoreLTwoCmd(commands2.SequentialCommandGroup):
    """A command that will score a coral on level two"""

    def __init__(self, coralina : Coralina, elevator: Elevator) -> None:
        self.coralina = coralina
        self.elevator = elevator
        super().__init__()
        self.addRequirements(self.coralina, self.elevator)
        self.addCommands(SetCoralPivotCmd(self.coralina, 90), SetElevatorPositionCmd(self.elevator, 6), SetCoralPivotCmd(self.coralina, 190), CoralOuttakeCmd(self.coralina), SetCoralPivotCmd(90), SetElevatorPositionCmd(0))

    def isFinished(self) -> bool:
        return not self.coralina.getCoralinaStored()
