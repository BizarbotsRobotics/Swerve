import math
from phoenix6 import hardware, controls, configs
from wpilib import AnalogEncoder

class SwerveModule:
    def __init__(self, driveMotorId:int,swerveMotorId:int, absoluteEncoderPort:int, encoderOffset:float):
        """Constructor for the swervemodule class.

        Args:
            driveMotorId (int): CAN ID for kraken drive motor.
            swerveMotorId (int): CAN ID for kraken swerve motor.
            absoluteEncoderPort (int): Absolute Encoder port number for swerve.
            encoderOffset (float): Offset for absolute encoder.
        """
        self.driveMotor = hardware.TalonFX(driveMotorId)
        self.swerveMotor = hardware.TalonFX(swerveMotorId)

        self.swerveControl = controls.DutyCycleOut(0)
        self.driveControl = controls.DutyCycleOut(0)

        self.AbsoluteEncoder = AnalogEncoder(absoluteEncoderPort)
        self.encoderOffset = encoderOffset
        

         # Start at position 0, use slot 0
        self.position_voltage = controls.PositionVoltage(0).with_slot(0)
        # Keep a brake request so we can disable the motor
        self.brake = controls.NeutralOut()


        cfg = configs.TalonFXConfiguration()
        cfg.slot0.k_p = 2.4; # An error of 1 rotation results in 2.4 V output
        cfg.slot0.k_i = 0; # No output for integrated error
        cfg.slot0.k_d = 0.1; # A velocity of 1 rps results in 0.1 V output
        # Peak output of 8 V
        cfg.voltage.peak_forward_voltage = 8
        cfg.voltage.peak_reverse_voltage = -8
        # Peak output of 120 A
        cfg.torque_current.peak_forward_torque_current = 120
        cfg.torque_current.peak_reverse_torque_current = -120

        self.swerveMotor.configurator.apply(cfg)
        self.seedSwerveMotorEncoderPosition()
    

        


    def getAbsoluteEncoderRawValue(self) -> float:
        """Returns the absolute encoder position from 0-1.

        Returns:
            float: Absolute encoder position.
        """
        return 1 - self.AbsoluteEncoder.getAbsolutePosition()
    
    def getAbsoluteEncoderPosition(self) -> float:
        encoderVal = self.getAbsoluteEncoderRawValue() - self.encoderOffset
        if encoderVal < 0:
            return 1 + encoderVal
        return encoderVal
    
    def getAbsoluteEncoderDegrees(self) -> float:
        return self.getAbsoluteEncoderPosition() * 360

    def getAbsoluteEncoderRadians(self) -> float:
        return self.getAbsoluteEncoderPosition() * 2 * math.pi
    
    def getSwerveMotorPosition(self) -> float:
        return abs(self.swerveMotor.get_rotor_position().value / 21.42857) % 1
    
    def seedSwerveMotorEncoderPosition(self):
        self.swerveMotor.set_position(self.getAbsoluteEncoderPosition() * 21.42857)

    def setSwervePower(self, power) -> None:  
        self.swerveMotor.set_control(self.swerveControl.with_output(power))         

    def setDrivePower(self, power) -> None:  
        self.driveMotor.set_control(self.driveControl.with_output(power))    

    def setSwervePosition(self, position):
        self.swerveMotor.set_control(self.position_voltage.with_position(position * 21.42857))

                            




