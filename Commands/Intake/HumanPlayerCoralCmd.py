import commands2
import commands2.cmd
import wpilib

from Commands.Intake.CoralIntakeCmd import CoralIntakeCmd
from Commands.Intake.CoralOuttakeCmd import CoralOuttakeCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator



class HumanPlayerCoralCmd(commands2.SequentialCommandGroup):
    """A command that will prepare coral intake from the human player station"""

    def __init__(self, coralina : Coralina, elevator: Elevator) -> None:
        self.coralina = coralina
        self.elevator = elevator
        super().__init__()
        self.addRequirements(self.coralina, self.elevator)
        self.addCommands(SetCoralPivotCmd(self.coralina, 100), SetElevatorPositionCmd(self.elevator, 18.7), CoralIntakeCmd(self.coralina, 200), SetCoralPivotCmd(self.coralina, 40), SetElevatorPositionCmd(self.elevator,0))

    def isFinished(self) -> bool:
        return self.coralina.getCoralinaStored()
