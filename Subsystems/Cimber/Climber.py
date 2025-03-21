import commands2
import ntcore
from phoenix5 import ControlMode
import wpilib
from constants import ClimberConstants
from phoenix6.hardware import TalonFX
import phoenix6
import rev
from phoenix6 import StatusCode, hardware, controls, configs

class Climber(commands2.Subsystem):
    
    def __init__(self):

        super().__init__()
        # Start smart dashboard
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startServer()
        self.sd = self.inst.getTable("SmartDashboard")



        self.climberMotor = hardware.TalonFX(ClimberConstants.CLIMBER_MOTOR_ONE)
        

        self.voltageControl = controls.DutyCycleOut(0)


        


        
    def periodic(self):
        pass

    def telemetry(self):
        """
        Sends subsystem info to console or smart dashboard
        """
        pass

    def setPower(self, power):
        self.climberMotor.set_control(self.voltageControl.with_output(power))    
