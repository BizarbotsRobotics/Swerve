
import commands2
import ntcore
import phoenix6
from constants import IntakeConstants
import rev

class Gorgina(commands2.Subsystem):
    
    def __init__(self):

        super().__init__()
        # Start smart dashboard
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startServer()
        self.sd = self.inst.getTable("SmartDashboard")


        self.algaeIntakeMotor = rev.SparkMax(IntakeConstants.ALGAE_INTAKE_MOTOR, rev.SparkLowLevel.MotorType.kBrushless)
        self.algaePivotMotor = rev.SparkMax(IntakeConstants.ALGAE_PIVOT_MOTOR, rev.SparkLowLevel.MotorType.kBrushless)

        
        config = rev.SparkBaseConfig()
        config.closedLoop.P(IntakeConstants.ALGAE_PIVOT_P)
        config.closedLoop.I(IntakeConstants.ALGAE_PIVOT_I)
        config.closedLoop.D(IntakeConstants.ALGAE_PIVOT_D)
        config.closedLoop.setFeedbackSensor(rev.ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder)
        config.setIdleMode(rev.SparkBaseConfig.IdleMode.kBrake)

        
        # config.encoder.positionConversionFactor = .2


        self.pivotPID = self.algaePivotMotor.getClosedLoopController()


        
        self.algaePivotMotor.configure(config, rev.SparkBase.ResetMode.kResetSafeParameters, rev.SparkBase.PersistMode.kPersistParameters)
        
        
    def periodic(self):
        pass

    def telemetry(self):
        """
        Sends subsystem info to console or smart dashboard
        """
        # self.sd.putBoolean("Algae Stored", self.getNoteStored())
        # self.sd.putNumber("ALgae Prox", self.prox)
        pass

    
    def setIntakePower(self, power):
        self.algaeIntakeMotor.set(power)

    def setPivotPower(self, power):
        if(power < .05 and power > -.05):
            self.algaePivotMotor.set(-.025)
        else:
            self.algaePivotMotor.set(power)

    def setPivotPosition(self, position):
        self.pivotPID.setReference(position, rev.SparkLowLevel.ControlType.kPosition)

    def setCoralPivotPosition(self, position):
        self.algaePivotMotor.set_position(position)


    # def getIntakeRPM(self):
    #     return self.intakeMotor.getBuiltInEncoderVelocity()

    # def getIntakePivotAngle(self):
    #     return self.algaePivotMotor.get_rotor_position().value_as_double

    # def setPivotPosition(self, degrees):
    #     self.algaePivotMotor.set_control(self.request.with_position(degrees))

    # def setPivotPower(self, power):
    #     self.algaePivotMotor.set_control(phoenix6.controls.DutyCycleOut(power))

    # def setPivotEncoderVal(self, value):
    #     print(self.algaePivotMotor.set_position(value))

    # def setProxVal(self):
    #     self.prox = self.gorginaProxSensor.getRange()
    #     pass

    # def getAlgaeStored(self):
    #     if self.prox < 200:
    #         return True
    #     return False
