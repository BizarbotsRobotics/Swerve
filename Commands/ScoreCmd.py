import commands2
import commands2.cmd
import wpilib

from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina
from constants import ElevatorConstants, CoralConstants



class ScoreCmd(commands2.Command):
    """A command that will align the robot to an April Tag. Not great for speed but last resort"""

    def __init__(self, gorgina: Gorgina, coralina : Coralina, elevator: Elevator, apa, cpa, position) -> None:
        self.gorgina = gorgina
        self.coralina = coralina
        self.elevator = elevator

        self.apa = apa
        self.cpa = cpa
        self.position = position

        
        super().__init__()
        self.addRequirements(self.coralina, self.gorgina, self.elevator)

    def initialize(self):  
        pass

    def execute(self):
        self.elevator.setElevatorPosition(self.position())

        if self.elevator.getElevatorPosition() == self.position:
            self.gorgina.setAlgaePivotPosition(self.apa())
            
            if self.gorgina.getAlgaePivotPosition() == self.apa:
                self.coralina.setCoralPivotPosition(self.cpa())
                    


    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
