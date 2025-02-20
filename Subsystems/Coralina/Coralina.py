import commands2
import ntcore
import wpilib
from constants import IntakeConstants
from phoenix6.hardware import TalonFX
import phoenix6
import rev

class Coralina(commands2.Subsystem):
    
    def __init__(self):

        super().__init__()
        # Start smart dashboard
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startServer()
        self.sd = self.inst.getTable("SmartDashboard")
        
        # self.coralinaProxSensor = lasercan.laserCAN(1)
        self.pivotAbsoluteEncoder = wpilib.DutyCycleEncoder(8)

        self.coralIntakeMotor = rev.SparkMax(IntakeConstants.CORAL_INTAKE_MOTOR, rev.SparkLowLevel.MotorType.kBrushless)
        self.coralPivotMotor = rev.SparkMax(IntakeConstants.CORAL_PIVOT_MOTOR, rev.SparkLowLevel.MotorType.kBrushless)

        config = rev.SparkBaseConfig()
        config.closedLoop.P(IntakeConstants.CORAL_PIVOT_P)
        config.closedLoop.I(IntakeConstants.CORAL_PIVOT_I)
        config.closedLoop.D(IntakeConstants.CORAL_PIVOT_D)
        config.closedLoop.setFeedbackSensor(rev.ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder)
        config.setIdleMode(rev.SparkBaseConfig.IdleMode.kBrake)

        
        # config.encoder.positionConversionFactor = .2


        self.pivotPID = self.coralPivotMotor.getClosedLoopController()


        
        self.coralPivotMotor.configure(config, rev.SparkBase.ResetMode.kResetSafeParameters, rev.SparkBase.PersistMode.kPersistParameters)



        
    def periodic(self):
        # self.setCoralinaProxVal()
        pass

    def telemetry(self):
        """
        Sends subsystem info to console or smart dashboard
        """
        # self.sd.putBoolean("Coral Stored", self.getCoralStored())
        # self.sd.putNumber("Coral Prox 1", self.coralinaProx)
        pass

    def getcoralIntakeRPM(self):
        return self.coralIntakeMotor.getBuiltInEncoderPosition()
    
    def setIntakePower(self, power):
        self.coralIntakeMotor.set(power)

    def setPivotPower(self, power):
        self.coralPivotMotor.set(power)
    
    def setCoralPivotPosition(self, position):
        self.coralPivotMotor.set_position(position)


    # def setCoralinaProxVal(self):
    #     self.coralinaProx = self.coralinaProxSensor.getRange()
    #     pass

    # def getCoralinaStored(self):
    #     if self.coralinaProx < 200:
    #         return True
    #     return False
