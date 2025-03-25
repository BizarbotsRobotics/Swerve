import commands2
import commands2.cmd
from Subsystems.Swerve.SwerveDrive import SwerveDrive
from Subsystems.Vision.Vision import Vision


class AlignTargetCmd(commands2.Command):
    """A command that will align the robot to the April Tag on the human player station. """

    def __init__(self, swerveDrive : SwerveDrive, vision: Vision, x, y, rot) -> None:
        self.swerve = swerveDrive
        self.vision = vision
        self.x = x
        self.y = y
        self.rot = rot
        super().__init__()
        self.addRequirements(self.swerve, self.vision)
        rotationSpeed = self.swerve.limelightAimProportional()
        xSpeed = self.swerve.limelightRangeProportional()

    def initialize(self):  
        self.steerAdjust = 0


    def execute(self):
        self.rotationSpeed = self.swerve.limelightAimProportional()
        self.xSpeed = self.swerve.limelightRangeProportional()
        if self.xSpeed is not None and self.rotationSpeed is not None:
            self.swerve.driveNormal(self.xSpeed, self.y(), self.rotationSpeed)

    def end(self, interrupted: bool):
        pass

    def isFinished(self) -> bool:
        # rotationSpeed value might be wrong
        if abs(self.xSpeed) < 0.5 and abs(self.rotationSpeed) < 5:
            return True
        return False
    