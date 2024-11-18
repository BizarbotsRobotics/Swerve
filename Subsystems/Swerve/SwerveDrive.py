from commands2 import Subsystem
from Subsystems.Swerve.SwerveModule import SwerveModule
from constants import SwerveConstants
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from wpimath.geometry import Translation2d, Pose2d, Rotation2d


class SwerveDrive(Subsystem):
    def __init__(self):
        self.initializeModules()

        self.kinematics = self.getSwerveDriveKinematics()

    def periodic(self):
        self.debug()

    def initializeModules(self):
        try:
            self.frontLeft = SwerveModule(SwerveConstants.FRONT_LEFT_DRIVE, SwerveConstants.FRONT_LEFT_SWERVE,
                                        SwerveConstants.FRONT_LEFT_ENCODER_PORT, SwerveConstants.FRONT_LEFT_ENCODER_OFFSET, swerveInvert=True)
            self.frontRight = SwerveModule(SwerveConstants.FRONT_RIGHT_DRIVE, SwerveConstants.FRONT_RIGHT_SWERVE,
                                        SwerveConstants.FRONT_RIGHT_ENCODER_PORT, SwerveConstants.FRONT_RIGHT_ENCODER_OFFSET, swerveInvert=True, driveInvert=False)
            self.backLeft = SwerveModule(SwerveConstants.BACK_LEFT_DRIVE, SwerveConstants.BACK_LEFT_SWERVE,
                                        SwerveConstants.BACK_LEFT_ENCODER_PORT, SwerveConstants.BACK_LEFT_ENCODER_OFFSET, swerveInvert=True
                                        )
            self.backRight = SwerveModule(SwerveConstants.BACK_RIGHT_DRIVE, SwerveConstants.BACK_RIGHT_SWERVE,
                                        SwerveConstants.BACK_RIGHT_ENCODER_PORT, SwerveConstants.BACK_RIGHT_ENCODER_OFFSET, swerveInvert=True)
            self.swerveModules = [self.frontLeft, self.frontRight, self.backLeft, self.backRight]

        except Exception as e:
            raise Exception("Check ports in constants file or check for Incorrect can IDs")
        

    def getSwerveDriveKinematics(self) -> SwerveDrive4Kinematics:
        """
        Return the Kinematics object for the current swerve drive using the values in our constants file.

        Raises:
            Exception: Constants are not set or not set correctly.

        Returns:
            kinematics.SwerveDrive4Kinematics : Swerve Drive Kinematics Object
        """
        try:
            m_frontLeftLocation = Translation2d(SwerveConstants.FRONT_LEFT_CORDS['x'], SwerveConstants.FRONT_LEFT_CORDS['y'])
            m_frontRightLocation = Translation2d(SwerveConstants.FRONT_RIGHT_CORDS['x'], SwerveConstants.FRONT_RIGHT_CORDS['y'])
            m_backLeftLocation = Translation2d(SwerveConstants.BACK_LEFT_CORDS['x'], SwerveConstants.BACK_LEFT_CORDS['y'])
            m_backRightLocation = Translation2d(SwerveConstants.BACK_RIGHT_CORDS['x'], SwerveConstants.BACK_RIGHT_CORDS['y'])
            return SwerveDrive4Kinematics(m_frontLeftLocation, m_frontRightLocation, m_backLeftLocation, m_backRightLocation)
        except Exception as e:
            raise Exception("Check your constants folder")
        
    def getStates(self):
        states = []
        counter = 0
        for swerve in self.swerveModules:
            states.insert(counter, swerve.getState())
            counter+=1
        return states
    
    def getRobotVelocity(self) -> ChassisSpeeds:
        return self.kinematics.toChassisSpeeds(self.getStates())
        
    def setRawModuleStates(self, states:tuple, isOpenLoop:bool) -> None:
        SwerveDrive4Kinematics.desaturateWheelSpeeds(states, self.getRobotVelocity(),
                                                  SwerveConstants.DRIVE_MAX_SPEED,
                                                  SwerveConstants.ATTAINABLE_MAX_TRANSLATIONAL_SPEED_METERS_PER_SECOND,
                                                  SwerveConstants.ATTAINABLE_MAX_ROTATIONAL_VELOCITY_RADIANS_PER_SECOND)
        counter = 0
        for swerve in self.swerveModules:
            swerve.setDesiredState(states[counter], isOpenLoop)
            counter+=1


    def drive(self, velocity, isOpenLoop, centerOfRotationMeters):
        swerveModuleStates = self.kinematics.toSwerveModuleStates(velocity)

        self.setRawModuleStates(swerveModuleStates, isOpenLoop)

    def driveNormal(self, dx, dy, theta):
        velocity = ChassisSpeeds(dx, dy, theta)
        self.drive(velocity, True, None)

    def debug(self):
        for module in self.swerveModules:
            module.debug()

   
