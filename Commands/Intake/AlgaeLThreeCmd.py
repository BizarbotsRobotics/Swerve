import commands2
import commands2.cmd

from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina



class AlgaeLThreeCmd(commands2.SequentialCommandGroup):
    """A command that will prepare coral intake from the human player station"""

    def __init__(self, gorgina : Gorgina, elevator: Elevator, coralina: Coralina) -> None:
        self.gorgina = gorgina
        self.elevator = elevator
        self.coralina = coralina
        super().__init__()
        self.addRequirements(self.gorgina, self.elevator, self.coralina)
        self.addCommands(SetCoralPivotCmd(self.coralina, 186),SetAlgaePivotCmd(self.gorgina, 175), SetElevatorPositionCmd(self.elevator, 3.8), AlgaeIntakeCmd(self.gorgina), commands2.WaitCommand(1), SetAlgaePivotCmd(self.gorgina, 120), SetElevatorPositionCmd(self.elevator, 0))
