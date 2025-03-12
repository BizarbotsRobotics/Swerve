import commands2
import libgrapplefrc.libgrapplefrc
import ntcore
import wpilib
from constants import IntakeConstants
from phoenix6.hardware import TalonFX
import phoenix6
import rev
import libgrapplefrc

class Coralina(commands2.Subsystem):
    
    def __init__(self):

        super().__init__()
        # Start smart dashboard
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startServer()
        self.sd = self.inst.getTable("SmartDashboard")
        
        self.coralinaProxSensor = libgrapplefrc.LaserCAN(1)
        

        self.coralIntakeMotor = rev.SparkMax(IntakeConstants.CORAL_INTAKE_MOTOR, rev.SparkLowLevel.MotorType.kBrushless)
        self.coralPivotMotor = rev.SparkMax(IntakeConstants.CORAL_PIVOT_MOTOR, rev.SparkLowLevel.MotorType.kBrushless)
        self.pivotAbsoluteEncoder = self.coralPivotMotor.getAbsoluteEncoder()

        config = rev.SparkBaseConfig()
        config.closedLoop.P(IntakeConstants.CORAL_PIVOT_P)
        config.closedLoop.I(IntakeConstants.CORAL_PIVOT_I)
        config.closedLoop.D(IntakeConstants.CORAL_PIVOT_D)
        config.closedLoop.setFeedbackSensor(rev.ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder)
        config.setIdleMode(rev.SparkBaseConfig.IdleMode.kBrake)
        config.absoluteEncoder.positionConversionFactor(360)
        config.absoluteEncoder.velocityConversionFactor(360)
        config.absoluteEncoder.zeroOffset((0.845))
        config.closedLoop.maxMotion.maxVelocity(600000)
        config.closedLoop.maxMotion.maxAcceleration(50000)
        config.closedLoop.maxMotion.allowedClosedLoopError(1)
        #config.closedLoop.maxMotion.positionMode(rev.MAXMotionConfig.MAXMotionPositionMode.kMAXMotionTrapezoidal)

        config.closedLoop.positionWrappingEnabled(True)

        self.pivotPID = self.coralPivotMotor.getClosedLoopController()

        
        self.coralPivotMotor.configure(config, rev.SparkBase.ResetMode.kResetSafeParameters, rev.SparkBase.PersistMode.kPersistParameters)



        
    def periodic(self):
        #self.setCoralinaProxVal()
        self.telemetry()
        pass

    def telemetry(self):
        """
        Sends subsystem info to console or smart dashboard
        """
        # self.sd.putBoolean("Coral Stored", self.getCoralinaStored())
        # self.sd.putNumber("Coral Prox ", self.coralinaProxSensor.get_measurement().distance_mm)
        self.sd.putNumber("Coral pivot ", self.getPivotPositionDegrees())
        pass

    def getcoralIntakeRPM(self):
        return self.coralIntakeMotor.getBuiltInEncoderPosition()
    
    def setIntakePower(self, power):
        self.coralIntakeMotor.set(power)

    def setPivotPower(self, power):
        self.coralPivotMotor.set(power)
    
    def setCoralPivotPosition(self, cpa):
        self.pivotPID.setReference(cpa, rev.SparkLowLevel.ControlType.kMAXMotionPositionControl)

    def getCoralPivotPosition(self):
        return self.coralPivotMotor.getAbsoluteEncoder().getPosition()



    # def setCoralinaProxVal(self):
    #     self.coralinaProx = self.coralinaProxSensor.getRange()
    #     pass

    # def getCoralinaStored(self):
    #     if self.coralinaProxSensor.get_measurement().distance_mm < 10:
    #         return True
    #     return False
    
    def getPivotPositionDegrees(self):
        return self.pivotAbsoluteEncoder.getPosition()
