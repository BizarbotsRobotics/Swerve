

import math
import commands2
import ntcore
import limelight
import limelightresults
import json
from wpimath.geometry import Translation2d, Pose2d, Rotation2d
import time
from limelight import Limelight

class FiducialResult:
    def __init__(self, fiducial_data):
        self.fiducial_id = fiducial_data["fID"]
        self.family = fiducial_data["fam"]
        self.points = fiducial_data["pts"]
        self.skew = fiducial_data["skew"]
        self.camera_pose_target_space = fiducial_data["t6c_ts"]
        self.robot_pose_field_space = fiducial_data["t6r_fs"]
        self.robot_pose_target_space = fiducial_data["t6r_ts"]
        self.target_pose_camera_space = fiducial_data["t6t_cs"]
        self.target_pose_robot_space = fiducial_data["t6t_rs"]
        self.target_area = fiducial_data["ta"]
        self.target_x_degrees = fiducial_data["tx"]
        self.target_x_pixels = fiducial_data["txp"]
        self.target_y_degrees = fiducial_data["ty"]
        self.target_y_pixels = fiducial_data["typ"]

class Vision(commands2.Subsystem):
    
    def __init__(self):

        super().__init__()
        # Start smart dashboard
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startServer()
        self.sd = self.inst.getTable("SmartDashboard")
        
        self.staticLimelight = Limelight("10.54.94.11")
        results = self.staticLimelight.get_results()
        status = self.staticLimelight.get_status()

        self.staticLimelight.enable_websocket()

        self.botPose = {"red": None, "blue": None}



    def update_megatag2_robot_orientation(self, degrees):
        self.staticLimelight.update_robot_orientation([degrees,0,0,0,0,0])

        
    def periodic(self):
        pass
        
#          LimelightHelpers.SetRobotOrientation("limelight", m_poseEstimator.getEstimatedPosition().getRotation().getDegrees(), 0, 0, 0, 0, 0);
#   LimelightHelpers.PoseEstimate mt2 = LimelightHelpers.getBotPoseEstimate_wpiBlue_MegaTag2("limelight");
   
#   // if our angular velocity is greater than 360 degrees per second, ignore vision updates
#   if(Math.abs(m_gyro.getRate()) > 360)
#   {
#     doRejectUpdate = true;
#   }
#   if(mt2.tagCount == 0)
#   {
#     doRejectUpdate = true;
#   }
#   if(!doRejectUpdate)
#   {
#     m_poseEstimator.setVisionMeasurementStdDevs(VecBuilder.fill(.7,.7,9999999));
#     m_poseEstimator.addVisionMeasurement(
#         mt2.pose,
#         mt2.timestampSeconds);
#   }
            



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
        try:
            if parsedResults is not None:
                bluePose = parsedResults.botpose_wpiblue
                if len(parsedResults.fiducialResults) >= 1:
                    return [bluePose, parsedResults.timestamp]
        except:
            return None
        return None
        
    def getTX(self):
        results = self.staticLimelight.get_latest_results()
        parsedResults = limelightresults.parse_results(results)
        try:
            if parsedResults is not None:
                if len(parsedResults.fiducialResults) >= 1:
                    return parsedResults.fiducialResults[0].target_x_degrees
        except:
            return None
        return None
        
    def getTY(self):
        results = self.staticLimelight.get_latest_results()
        parsedResults = limelightresults.parse_results(results)
        try:
            if parsedResults is not None:
                if len(parsedResults.fiducialResults) >= 1:
                    return parsedResults.fiducialResults[0].target_y_degrees
        except:
            return None
        return None
    
    def isAlign(self):
        if abs(self.getTX()) < 0.2 and abs(self.getTY()) < 3:
            return True
        return False 


