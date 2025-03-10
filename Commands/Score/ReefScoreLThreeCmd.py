import commands2
import commands2.cmd
import wpilib

from Commands.Intake.CoralIntakeCmd import CoralIntakeCmd
from Commands.Intake.CoralOuttakeCmd import CoralOuttakeCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator



class ReefScoreLThreeCmd(commands2.SequentialCommandGroup):
    """A command that will score coral on level three"""

    def __init__(self, coralina : Coralina, elevator: Elevator) -> None:
        self.coralina = coralina
        self.elevator = elevator
        super().__init__()
        self.addRequirements(self.coralina, self.elevator)
        self.addCommands(SetCoralPivotCmd(self.coralina, 100), SetElevatorPositionCmd(self.elevator, 11.7), SetCoralPivotCmd(self.coralina, 200), CoralOuttakeCmd(self.coralina))

    def isFinished(self) -> bool:
        return not self.coralina.getCoralinaStored()
