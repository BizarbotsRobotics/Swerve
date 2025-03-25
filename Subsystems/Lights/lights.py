
import commands2
import ntcore
import phoenix6
import wpilib
from constants import IntakeConstants
import rev

class Gorgina(commands2.Subsystem):
    
    def __init__(self):

        super().__init__()
        # Start smart dashboard
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startServer()
        self.sd = self.inst.getTable("SmartDashboard")

        self.i2c = wpilib.I2C(wpilib.I2C.Port.kOnboard)


        
    def periodic(self):
        pass


    def linedUp(self, linedUp=True):
        if linedUp:
            command = "linedUp"
        else: 
            command = "null"
        data = command.encode()
        self.i2c.transaction(data, len(data), None, 0)

