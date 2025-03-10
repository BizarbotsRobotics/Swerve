import commands2
import commands2.cmd

from Subsystems.Swerve.SwerveDrive import SwerveDrive
from Subsystems.Vision.Vision import Vision


class DriveReefCmd(commands2.Command):
    """A command that will align the robot to an April Tag. Not great for speed but last resort"""

    def __init__(self, swerveDrive : SwerveDrive, vision: Vision, x, y, rot) -> None:
        self.swerve = swerveDrive
        self.vision = vision
        self.x = x
        self.y = y
        self.rot = rot
        super().__init__()
        self.addRequirements(self.swerve, self.vision)

    def initialize(self):  
        self.steerAdjust = 0


    def execute(self):
        self.steerAdjust = self.swerve.headingPID.calculate(self.vision.getReefCoords()[0], 0)
       
        self.swerve.drive(self.x(),self.y(),self.steerAdjust, False)

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False