import commands2
import commands2.cmd
import wpilib

from Subsystems.Swerve.SwerveDrive import SwerveDrive


class DriveCmd(commands2.Command):
    """A command that will align the robot to an April Tag. Not great for speed but last resort"""

    def __init__(self, swerveDrive : SwerveDrive, x, y, rot) -> None:
        self.swerve = swerveDrive
        self.x = x
        self.y = y
        self.rot = rot
        super().__init__()
        self.addRequirements(self.swerve)

    def initialize(self):  
        pass

    def execute(self):
        self.swerve.driveNormal(-self.x(), -self.y(), -self.rot())
        #self.swerve.driveFO(self.x(),self.y(),self.rot())

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        return False
