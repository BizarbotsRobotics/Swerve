import math
import ntcore
from phoenix6 import StatusCode, hardware, controls, configs
from wpilib import AnalogEncoder
import wpimath
import wpimath.units
from constants import SwerveConstants
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition
from wpimath.geometry import Rotation2d

class SwerveModule:
    def __init__(self, driveMotorId:int,swerveMotorId:int, absoluteEncoderPort:int, encoderOffset:float, swerveInvert:bool=False, driveInvert:bool=False):
        """Constructor for the swervemodule class.

        Args:
            driveMotorId (int): CAN ID for kraken drive motor.
            swerveMotorId (int): CAN ID for kraken swerve motor.
            absoluteEncoderPort (int): Absolute Encoder port number for swerve.
            encoderOffset (float): Offset for absolute encoder.
        """

        inst = ntcore.NetworkTableInstance.getDefault()
        inst.startServer()
        self.sd = inst.getTable("SmartDashboard")

        self.debug_state = False
        self.telemetry = False

        self.swerveMotorId = swerveMotorId

        # Defining motor objects for swerve module
        self.driveMotor = hardware.TalonFX(driveMotorId)
        self.swerveMotor = hardware.TalonFX(swerveMotorId)

        # Define motor control objects 
        self.voltageControl = controls.DutyCycleOut(0)
        self.positionVoltage = controls.PositionVoltage(0).with_slot(0)
        self.brake = controls.NeutralOut()

        # Define absolute encoder object based off given port
        self.AbsoluteEncoder = AnalogEncoder(absoluteEncoderPort)

        # Create class variable of encoder offset
        self.encoderOffset = encoderOffset
        
        # Define configuration variables for swerve motor
        cfgSwerve = configs.TalonFXConfiguration()
        cfgSwerve.slot0.k_p = SwerveConstants.SWERVE_P
        cfgSwerve.slot0.k_i = SwerveConstants.SWERVE_I
        cfgSwerve.slot0.k_d = SwerveConstants.SWERVE_D

        #Try changing peak voltage
        cfgSwerve.voltage.peak_forward_voltage = 8
        cfgSwerve.voltage.peak_reverse_voltage = -8
        cfgSwerve.torque_current.peak_forward_torque_current = 120
        cfgSwerve.torque_current.peak_reverse_torque_current = -120
        cfgSwerve.motor_output.neutral_mode = configs.config_groups.NeutralModeValue.BRAKE
        cfgSwerve.closed_loop_general.continuous_wrap = True
        cfgSwerve.feedback.sensor_to_mechanism_ratio = SwerveConstants.SWERVE_GEAR_RATIO


        if swerveInvert:
            cfgSwerve.motor_output.inverted = configs.config_groups.InvertedValue.CLOCKWISE_POSITIVE
        else:
            cfgSwerve.motor_output.inverted = configs.config_groups.InvertedValue.COUNTER_CLOCKWISE_POSITIVE


        # Define configuration variables for drive motor
        cfgDrive = configs.TalonFXConfiguration()
        cfgDrive.slot0.k_p = SwerveConstants.DRIVE_P
        cfgDrive.slot0.k_i = SwerveConstants.DRIVE_I
        cfgDrive.slot0.k_d = SwerveConstants.DRIVE_D
        cfgDrive.voltage.peak_forward_voltage = 12
        cfgDrive.voltage.peak_reverse_voltage = -12
        cfgDrive.torque_current.peak_forward_torque_current = 120
        cfgDrive.torque_current.peak_reverse_torque_current = -120
        cfgDrive.feedback.sensor_to_mechanism_ratio = SwerveConstants.DRIVE_GEAR_RATIO


        cfgDrive.motor_output.neutral_mode = configs.config_groups.NeutralModeValue.BRAKE
        
        if driveInvert:
            cfgDrive.motor_output.inverted = configs.config_groups.InvertedValue.CLOCKWISE_POSITIVE
        else:
            cfgDrive.motor_output.inverted = configs.config_groups.InvertedValue.COUNTER_CLOCKWISE_POSITIVE


        # Save configuration settings to each motor controller
        self.setConfigs(self.swerveMotor, cfgSwerve)
        self.setConfigs(self.driveMotor, cfgDrive)

        # Syncs swerve motor encoder to absolute encoder
        self.seedSwerveMotorEncoderPosition()

        self.synchronizeEncoderQueued = True

        self.lastState = self.getState()

    def setConfigs(self, motor:hardware.TalonFX, config:configs.TalonFXConfiguration) -> None:
        motorStatus = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for i in range(5):
            motorStatus = motor.configurator.apply(config, 0.05)

            if motorStatus.is_ok() and i > 2:
                break

        if not motorStatus.is_ok() and self.debug_state:
            self.sd.putString("Could not configure device. Error: "+ str(motorStatus))

        
    
    def getAbsoluteEncoderRawValue(self) -> float:
        """Returns the absolute encoder position from 0-1.

        Returns:
            float: Absolute encoder position.
        """
        return self.AbsoluteEncoder.get()
    
    def getAbsoluteEncoderPosition(self) -> float:
        """Returns the absolute encoder position with the offset included from 0-1.

        Returns:
            float: absolute encoder value.
        """
        encoderVal = self.getAbsoluteEncoderRawValue() - self.encoderOffset
        if encoderVal < 0:
            return 1 + encoderVal
        return encoderVal
    
    def getAbsoluteEncoderDegrees(self) -> float:
        """Returns the absolute encoder position in degrees.

        Returns:
            float: absolute encoder postion in degrees.
        """
        return self.getAbsoluteEncoderPosition() * 360

    def getAbsoluteEncoderRadians(self) -> float:
        """Returns the absolute encoder position in radians.

        Returns:
            float: absolute encoder postion in radians.
        """
        return self.getAbsoluteEncoderPosition() * 2 * math.pi
    
    def getDriveMotorVelocity(self) -> float:
        return self.driveMotor.get_rotor_velocity().value
    
    def getSwerveMotorPosition(self) -> float:
        """Returns the swerve motor encoder position from 0-1.

        Returns:
            float: swerve motor encoder position.
        """
        return self.swerveMotor.get_position().value_as_double % 1
    
    def getDriveMotorPosition(self) -> float:
        """Returns the drive motor encoder position

        Returns:
            float: swerve motor encoder position.
        """
        return self.driveMotor.get_position().value_as_double
    
    def getSwervePositionDegrees(self) -> float:  
        return self.getSwerveMotorPosition() * 360
    
    def getSwervePositionRadians(self) -> float:  
        return self.getSwerveMotorPosition() * (2 * math.pi)
    
    def getDrivePositionRadians(self) -> float:  
        return self.getDriveMotorPosition() * (2 * math.pi)
    
    def getState(self) -> SwerveModuleState:
        """
        Returns the current state of the swerve module.

        Returns:
            SwerveModuleState: The state of the module.
        """
        velocity = self.getDriveMotorVelocity()
        angle = Rotation2d.fromDegrees(self.getSwervePositionDegrees())
        return SwerveModuleState(velocity, angle)
    
    def getSwerveModulePosition(self):

        position = self.getDriveMotorPosition() * (4 * math.pi)
        azimuth = self.getSwervePositionRadians()
        return SwerveModulePosition(position, Rotation2d(azimuth))

    
    def seedSwerveMotorEncoderPosition(self) -> None:
        """Syncs swerve motor encoder to absolute encoder
        """
        self.swerveMotor.set_position(self.getAbsoluteEncoderPosition())

    def setSwervePower(self, power:float) -> None:  
        """Sets the swerve motor's power to a value from 0-1 (0%-100%).

        Args:
            power (float): power value from 0-1.
        """
        self.swerveMotor.set_control(self.swerveControl.with_output(power))         

    def setDrivePower(self, power:float) -> None:  
        """Sets the drive motor's power to a value from 0-1 (0%-100%).

        Args:
            power (float): power value from 0-1.
        """
        self.driveMotor.set_control(self.voltageControl.with_output(power))    

    def setSwervePosition(self, position:float) -> None:
        """ Sets the swerve motor's position from 0-1 (0 deg - 360 deg).

        Args:
            position (float): a position value from 0-1.
        """
        self.swerveMotor.set_control(self.positionVoltage.with_position(position))

    def setSwervePositionDegrees(self, position:float) -> None:
        """Sets the swerve motor's position in degrees from 0-360.

        Args:
            position (float): position value from 0-360.
        """
        self.setSwervePosition((position % 360) / 360)

    def setSwervePositionRadians(self, position:float) -> None:
        """Sets the swerve motor's position in radians from 0-2pi.

        Args:
            position (float): position value from 0-2pi.
        """
        self.setSwervePosition((position % (2 * math.pi)) / (2 * math.pi))

    def setDesiredState(self, state:SwerveModuleState, openLoop:bool = True) -> None:
        SwerveModuleState.optimize(state, Rotation2d.fromDegrees(self.getSwervePositionDegrees()))
        self.seedSwerveMotorEncoderPosition()
        if (state.angle is self.lastState.angle) and self.synchronizeEncoderQueued:
            self.seedSwerveMotorEncoderPosition()
            self.synchronizeEncoderQueued = False   
        else:
            self.setSwervePositionDegrees(state.angle.degrees())

        if openLoop:
            percentOutput = state.speed / SwerveConstants.DRIVE_MAX_SPEED
            self.setDrivePower(percentOutput)
        else:
            if state.speed != self.lastState.speed:
                velocity = state.speed
                #self.driveMotor.setVelocity(velocity)

        self.lastState = state

    def debug(self):
        self.debug_state = True

        self.sd.putNumber("Absolute Motor Position "+ str(self.swerveMotorId), self.getAbsoluteEncoderRawValue())
        self.sd.putNumber("Motor Position "+ str(self.swerveMotorId), self.getSwerveMotorPosition())

    def telemetry(self) -> None:
        self.telemetry = True


        




                            




