import commands2
import wpilib
from wpimath.controller import PIDController
from wpimath.geometry import Rotation2d, Translation2d

from Subsystems.Swerve.SwerveDrive import SwerveDrive
from constants import AutoAimConstants, AutoFollowConstants, SwerveConstants
# from wpilib. import SmartDashboard


class AlignCommand(commands2.command):
    def __init__(self, l_LimelightSubsystem: LimelightSubsystem, x: float, z: float, ry: float, swerveDrive: SwerveDrive):
        super().__init__()
        self.TX = lambda: l_LimelightSubsystem.getTargetPos(0)
        self.TZ = lambda: l_LimelightSubsystem.getTargetPos(2)
        self.RY = lambda: l_LimelightSubsystem.getTargetPos(4)
        self.tv = lambda: l_LimelightSubsystem.IsTargetAvailable()
        self.swerveDrive = swerveDrive()
        self.l_LimelightSubsystem = l_LimelightSubsystem

        self.x = x
        self.z = z
        self.ry = ry

        # Add subsystems to the command
        self.addRequirements(swerveDrive)
        self.addRequirements(l_LimelightSubsystem)

        # Initialize the PID controllers
        self.TranslatePID = PIDController(
            AutoFollowConstants.kP,
            AutoFollowConstants.kI,
            AutoFollowConstants.kD
        )

        self.RotatePID = PIDController(
            AutoAimConstants.kP,
            AutoAimConstants.kI,
            AutoAimConstants.kD
        )

        self.StrafePID = PIDController(
            AutoFollowConstants.kP,
            AutoFollowConstants.kI,
            AutoFollowConstants.kD
        )

    def initialize(self):
        # Set robotCentric to False when command is initialized
        RobotContainer.robotCentric = False

    def execute(self):
        # Set the setpoints for each PID controller
        self.TranslatePID.setSetpoint(self.x)
        self.TranslatePID.setTolerance(0.01)
        self.StrafePID.setSetpoint(self.z)
        self.StrafePID.setTolerance(0.01)
        self.RotatePID.setSetpoint(self.ry)
        self.RotatePID.setTolerance(1)

        # Calculate PID output for translation
        x = self.l_LimelightSubsystem.getTargetPos(0)
        target = self.l_LimelightSubsystem.IsTargetAvailable()
        value = self.TranslatePID.calculate(x)
        translate = value if target and not self.TranslatePID.atSetpoint() else 0
        translate = max(min(translate, 0.87), -0.87)

        # Update SmartDashboard for debugging
        wpilib.SmartDashboard.putNumber("TPID", value)
        wpilib.SmartDashboard.putNumber("TTX", x)

        # Calculate PID output for strafing
        z = self.l_LimelightSubsystem.getTargetPos(2)
        value1 = self.StrafePID.calculate(z)
        strafe = value1 if target and not self.StrafePID.atSetpoint() else 0
        strafe = max(min(strafe, 0.87), -0.87)

        # Update SmartDashboard for debugging
        wpilib.SmartDashboard.putNumber("SPID", value1)
        wpilib.SmartDashboard.putNumber("STZ", z)

        # Calculate PID output for rotation
        a = self.l_LimelightSubsystem.getTargetPos(4)
        value2 = self.RotatePID.calculate(a)
        rotate = value2 if target and not self.RotatePID.atSetpoint() else 0
        rotate = max(min(rotate, 0.57), -0.57)

        # Update SmartDashboard for debugging
        wpilib.SmartDashboard.putNumber("RRY", a)
        wpilib.SmartDashboard.putNumber("RPID", rotate)

        # Drive the robot with calculated translation, strafe, and rotation
        self.s_Swerve.drive(
            Translation2d(-strafe, translate).times(SwerveConstants.DRIVE_MAX_SPEED),
            rotate * Constants.Swerve.MAX_ANGULAR_VELOCITY,
            False,  # This boolean flag is equivalent to "robotCentric"
            True
        )

    def end(self, interrupted: bool):
        # Reset robotCentric when the command ends
        RobotContainer.robotCentric = False

    def isFinished(self) -> bool:
        # Command finishes when all PID controllers are at setpoints
        return self.RotatePID.atSetpoint() and self.TranslatePID.atSetpoint() and self.StrafePID.atSetpoint()
