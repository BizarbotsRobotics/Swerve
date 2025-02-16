from math import pi
from commands2 import Subsystem
from Subsystems.Swerve.SwerveModule import SwerveModule
from constants import SwerveConstants
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from wpimath.geometry import Translation2d, Pose2d, Rotation2d
from phoenix6 import hardware
import ntcore
from wpimath import estimator
from pathplannerlib import config, controller
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPHolonomicDriveController
from pathplannerlib.config import RobotConfig, PIDConstants
from wpilib import DriverStation

class SwerveDrive(Subsystem):
    def __init__(self):
        inst = ntcore.NetworkTableInstance.getDefault()
        inst.startServer()
        self.sd = inst.getTable("SmartDashboard")
    
        self.initializeIMU()
        self.initializeModules()

        self.kinematics = self.getSwerveDriveKinematics()

        # self.swervePoseEstimator = estimator.SwerveDrive4PoseEstimator(self.kinematics,
        #     self.getYaw(),
        #     self.getModulePositions(),
        #     Pose2d(),
        #     (0.4,0,0.0),
        #     (0.4, 0.0, 0.1)
        #     #TODO Optimize these standard deviations later
        #    )
        
        # AutoBuilder.configureHolonomic(
        #     self.getPose, # Robot pose supplier
        #     self.resetOdometry, # Method to reset odometry (will be called if your auto has a starting pose)
        #     self.getRobotVelocity, # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
        #     self.setChassisSpeeds, # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds
        #     config.HolonomicPathFollowerConfig( # HolonomicPathFollowerConfig, this should likely live in your Constants class
        #         controller.PIDConstants(.1, 0.0, 0.05), # Translation PID constants
        #         controller.PIDConstants(.7, 0.0, .1), # Rotation PID constants
        #         4.5, # Max module speed, in m/s
        #         0.4, # Drive base radius in meters. Distance from robot center to furthest module.
        #         config.ReplanningConfig() # Default path replanning config. See the API for the options here
        #     ),
        #     False, self
        # )

        config = RobotConfig.fromGUISettings()

        # # Configure the AutoBuilder last
        # AutoBuilder.configureHolonomic(
        #     self.getPose, # Robot pose supplier
        #     self.resetOdometry, # Method to reset odometry (will be called if your auto has a starting pose)
        #     self.getRobotVelocity, # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
        #     self.setChasisSpeeds, # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds. Also outputs individual module feedforwards
        #     PPHolonomicDriveController( # PPHolonomicController is the built in path following controller for holonomic drive trains
        #         PIDConstants(5.0, 0.0, 0.0), # Translation PID constants
        #         PIDConstants(5.0, 0.0, 0.0) # Rotation PID constants
        #     ),
        #     config, # The robot configuration
        #     False, # Supplier to control path flipping based on alliance color
        #     self # Reference to this subsystem to set requirements
        # )

    def periodic(self):
        self.debug()
        # self.updateOdometry()

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
        # print(self.getPose())
        for module in self.swerveModules:
            module.debug()
            self.sd.putNumber("IMU: ", self.imu.get_yaw().value)


    def initializeIMU(self):
        self.imu = hardware.Pigeon2(SwerveConstants.PIGEON_PORT)
        self.imu.set_yaw(0)

    def getYaw(self):
        if self.imu != None:
            return self.degreesToRad(Rotation2d(self.imu.get_yaw().value_as_double))
        else:
            return Rotation2d()
        
    def degreesToRad(self, val):
        return (val / 360) * (2 * pi)
    
    
    def getModulePositions(self, invertOdometry=False) -> tuple:
        """
        Returns the module position as a tuple.

        Args:
            invertOdometry (bool, optional): Inverts the odometry. Defaults to False.

        Returns:
            tuple: Position of the module.
        """
        counter = 0
        positions = []
        for swerve in self.swerveModules:
            positions.insert(counter, swerve.getSwerveModulePosition())
            if invertOdometry:
                positions[counter].distance *= -1
            counter+=1
        return tuple(positions)
    
    def getPose(self):
        poseEstimation = self.swervePoseEstimator.getEstimatedPosition()
        return poseEstimation

    def resetOdometry(self, pose):
        self.swervePoseEstimator.resetPosition(self.getYaw(), self.getModulePositions(), pose)
        self.kinematics.toSwerveModuleStates(ChassisSpeeds.fromFieldRelativeSpeeds(0, 0, 0, pose.rotation()))

    def updateOdometry(self):
        try:
            self.swervePoseEstimator.update(self.getYaw(), self.getModulePositions())
            self.currentHeading = self.swervePoseEstimator.getEstimatedPosition().rotation().degrees().real            
        except Exception as e:
            raise e
        return None



   
