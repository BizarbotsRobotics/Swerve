

import commands2
import ntcore
import limelight
import limelightresults
import json
import time
from limelight import Limelight


class Vision(commands2.Subsystem):
       
    def __init__(self):

        super().__init__()
        # Start smart dashboard
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startServer()
        self.sd = self.inst.getTable("SmartDashboard")

        self.staticLimelight = Limelight("10.54.94.3")

        self.botPose = {"red": None, "blue": None}





        
    def periodic(self):

        pass
            



        # if (limelightMeasurement.tagCount >= 2)
        #     m_poseEstimator.setVisionMeasurementStdDevs(VecBuilder.fill(0.7, 0.7, 9999999))
        #     m_poseEstimator.addVisionMeasurement(
        #         limelightMeasurement.pose,
        #         limelightMeasurement.timestampSeconds)



    def telemetry(self):
        """
        Sends subsystem info to console or smart dashboard
        """
        pass

    def getPose(self):
        #TODO implement megatag 2
        results = self.staticLimelight.get_latest_results()
        parsedResults = limelightresults.parse_results(results)

        if parsedResults is not None:
            bluePose = parsedResults.botpose_wpiblue
            redPose = parsedResults.botpose_wpired

        #TODO Fix for both red alliance as well
            if len(parsedResults.fiducialResults) >= 2:
                return [bluePose, parsedResults.timestamp]