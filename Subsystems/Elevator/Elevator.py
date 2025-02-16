import commands2
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

        cfgElevatorOne = configs.TalonFXConfiguration()
        cfgElevatorTwo = configs.TalonFXConfiguration()

        cfgElevatorOne.motor_output.neutral_mode = configs.config_groups.NeutralModeValue.BRAKE
        cfgElevatorTwo.motor_output.neutral_mode = configs.config_groups.NeutralModeValue.BRAKE

        self.setConfigs(self.elevatorMotorOne, cfgElevatorOne)
        self.setConfigs(self.elevatorMotorTwo, cfgElevatorTwo)

        self.elevatorMotorTwo.set_control(controls.Follower(ElevatorConstants.ELEVATOR_MOTOR_ONE, False))

        self.voltageControl = controls.DutyCycleOut(0)

        self.absoluteEncoder = wpilib.Encoder(0,1,True)

        self.positionVoltage = controls.PositionVoltage(0).with_slot(0)
        self.trap = TrapezoidProfile.Constraints(500, 500)
        self.pid = ProfiledPIDController(ElevatorConstants.ELEVATOR_P, ElevatorConstants.ELEVATOR_I, ElevatorConstants.ELEVATOR_D, self.trap)

        self.absoluteEncoder.setDistancePerPulse(.0059)

        self.pid.reset(0)

        self.pid.setTolerance(1,1)
        
    def periodic(self):
        self.telemetry()

    def telemetry(self):
        """
        Sends subsystem info to console or smart dashboard
        """
        #print(self.absoluteEncoder.getDistance())
        pass

    def getElevatorRPM(self):
        return self.elevatorMotorOne.getBuiltInEncoderPosition()
    
    def setElevatorPower(self, power):
        self.elevatorMotorOne.set_control(self.voltageControl.with_output(power)) 

    def getElevatorEncoder(self):
        pass

    def setConfigs(self, motor:hardware.TalonFX, config:configs.TalonFXConfiguration) -> None:
        motorStatus = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for i in range(5):
            motorStatus = motor.configurator.apply(config, 0.05)

            if motorStatus.is_ok() and i > 2:
                break

        if not motorStatus.is_ok() and self.debug_state:
            self.sd.putString("Could not configure device. Error: "+ str(motorStatus))

    def setElevatorPosition(self, position:float) -> None:
        """ Sets the swerve motor's position from 0-1 (0 deg - 360 deg).

        Args:
            position (float): a position value from 0-1.
        """
        self.pid.setGoal(position)
        self.elevatorMotorOne.set_control(self.voltageControl.with_output(-self.pid.calculate(self.absoluteEncoder.getDistance())))

    def clamp(self,v, minval, maxval):
        return max(min(v, maxval), minval)