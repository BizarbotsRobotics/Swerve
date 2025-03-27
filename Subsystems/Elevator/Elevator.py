import commands2
import libgrapplefrc
from wpimath.controller import ProfiledPIDController
from wpimath.trajectory import TrapezoidProfile
import ntcore
import wpilib
from constants import ElevatorConstants
from phoenix6.hardware import TalonFX
from phoenix6 import StatusCode, controls, configs, hardware
import rev
from wpimath.controller import PIDController

class Elevator(commands2.Subsystem):
    
    def __init__(self):

        super().__init__()
        # Start smart dashboard
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startServer()
        self.sd = self.inst.getTable("SmartDashboard")

        self.elevatorMotorOne = TalonFX(ElevatorConstants.ELEVATOR_MOTOR_ONE)
        self.elevatorMotorTwo = TalonFX(ElevatorConstants.ELEVATOR_MOTOR_TWO)

        self.elevatorProxSensor = libgrapplefrc.LaserCAN(2)
        self.positionSet = False
        self.positionHold = 0

        # currentElevatorPosition = self.getElevatorPosition()

        cfgElevatorOne = configs.TalonFXConfiguration()
        cfgElevatorTwo = configs.TalonFXConfiguration()

        cfgElevatorOne.motor_output.neutral_mode = configs.config_groups.NeutralModeValue.BRAKE
        cfgElevatorTwo.motor_output.neutral_mode = configs.config_groups.NeutralModeValue.BRAKE

        self.elevatorMotorTwo.set_control(controls.Follower(ElevatorConstants.ELEVATOR_MOTOR_ONE, False))
        self.elevatorAbsoluteEncoder = wpilib.Encoder(6,7)
        self.elevatorAbsoluteEncoder.setDistancePerPulse(.0004882813)
        self.elevatorAbsoluteEncoder.setReverseDirection(True)

        


        cfgElevatorOne = configs.TalonFXConfiguration()
        cfgElevatorOne.slot0.k_p = ElevatorConstants.ELEVATOR_P
        cfgElevatorOne.slot0.k_i = ElevatorConstants.ELEVATOR_I
        cfgElevatorOne.slot0.k_d = ElevatorConstants.ELEVATOR_D
        cfgElevatorOne.slot0.closed_loop_error = 0.02
        cfgElevatorOne.voltage.peak_forward_voltage = 12
        cfgElevatorOne.voltage.peak_reverse_voltage = -12
        cfgElevatorOne.motor_output.inverted = configs.config_groups.InvertedValue.CLOCKWISE_POSITIVE
        cfgElevatorOne.torque_current.peak_forward_torque_current = 120
        cfgElevatorOne.torque_current.peak_reverse_torque_current = -120
        cfgElevatorOne.feedback.sensor_to_mechanism_ratio= 6.88


        motion_magic_configs = cfgElevatorOne.motion_magic
        
        motion_magic_configs.motion_magic_cruise_velocity = 80 # Target cruise velocity of 80 rps
        motion_magic_configs.motion_magic_acceleration = 20  # Target acceleration of 160 rps/s (0.5 seconds)
        motion_magic_configs.motion_magic_jerk = 100


        self.goal = 0

        self.setConfigs(self.elevatorMotorOne, cfgElevatorOne)
        self.setConfigs(self.elevatorMotorTwo, cfgElevatorTwo)
        self.seedElevator()

        self.voltageControl = controls.DutyCycleOut(0)

        self.positionVoltage = controls.MotionMagicVoltage(0)

        
        #self.elevatorMotorOne.setDistancePerPulse(.0059)

        #self.pid.reset(0)

        #self.pid.setTolerance(1,1)

        
        # self.synchronizeEncoderQueued = True
        
    def periodic(self):
        self.telemetry()
        if self.elevatorAbsoluteEncoder.getRate() < .05 and self.elevatorAbsoluteEncoder.getDistance() < .3:
            self.elevatorMotorOne.set_position(self.elevatorAbsoluteEncoder.getDistance())

    def telemetry(self):
        """
        Sends subsystem info to console or smart dashboard
        """
        self.sd.putNumber("Elevator position", self.elevatorAbsoluteEncoder.getDistance())
        self.sd.putNumber("Elevator position motor", self.getElevatorPosition())
        self.sd.putNumber("Elevator Prox ", self.getElevatorDistanceTOF())
        pass

    def getElevatorDistanceTOF(self):
        try:
            return self.elevatorProxSensor.get_measurement().distance_mm / 25.4
        except: 
            return 10000000

        

    def getElevatorRPM(self):
        return self.elevatorMotorOne.getBuiltInEncoderPosition()
    
    def setElevatorPower(self, power):
        self.elevatorMotorOne.set_control(self.voltageControl.with_output(power)) 
        # if -.05 < power < .05 and not self.positionSet:
        #     self.positionSet = True
        #     self.positionHold = self.getElevatorPosition()
        # elif -.05 < power < .05 and self.positionSet:    
        #     self.setElevatorPosition(self.positionHold)
        # else:
        #     if power < 0:
        #         power = power * .4
        #     self.elevatorMotorOne.set_control(self.voltageControl.with_output(power)) 
        #     self.positionSet = False

        

    def getElevatorEncoder(self):
        pass

    def setConfigs(self, motor:hardware.TalonFX, config:configs.TalonFXConfiguration) -> None:
        motorStatus = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for i in range(5):
            try:
                motorStatus = motor.configurator.apply(config, 0.05)

                if motorStatus.is_ok() and i > 2:
                    break
            except:
                pass

        if not motorStatus.is_ok() and self.debug_state:
            self.sd.putString("Could not configure device. Error: "+ str(motorStatus))

    def setElevatorPosition(self, position:float) -> None:
        """ Sets the swerve motor's position from 0-1 (0 deg - 360 deg).

        Args:
            position (float): a position value from 0-1.
        """
        self.elevatorMotorOne.set_control(self.positionVoltage.with_position(position))
        #self.elevatorMotorOne.set_position(position)


    def getElevatorPosition(self):
        return self.elevatorMotorOne.get_position().value

    def clamp(self,v, minval, maxval):
        return max(min(v, maxval), minval)
    
    def getElevatorMotorPosition(self) -> float:
        """Returns the swerve motor encoder position from 0-1.

        Returns:
            float: swerve motor encoder position.
        """
        return self.elevatorMotorOne.get_position().value % 1
    
    def seedElevator(self):
        if self.getElevatorDistanceTOF() is not None:
            self.elevatorMotorOne.set_position(0)
    