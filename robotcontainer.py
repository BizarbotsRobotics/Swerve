
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import commands2.button
import commands2.cmd
import wpilib

from Commands.Climber.ClimbCmd import ClimbCmd
from Commands.Intake.AlgaeLThreeCmd import AlgaeLThreeCmd
from Commands.Intake.AlgaeLTwoCmd import AlgaeLTwoCmd
from Commands.Intake.CoralIntakeCmd import CoralIntakeCmd
from Commands.Intake.CoralOuttakeCmd import CoralOuttakeCmd
from Commands.Intake.ManualCoralPivotCmd import ManualCoralPivotCmd
from Commands.Intake.GroundPickupCmd import GroundPickupCmd
from Commands.Intake.HumanPlayerCoralCmd import HumanPlayerCoralCmd
from Commands.Intake.ManualAlgaeIntakeCmd import ManualAlgaeIntakeCmd
from Commands.Intake.ManualAlgaePivotCmd import ManualAlgaePivotCmd
from Commands.Intake.ManualCoralIntakeCmd import ManualCoralIntakeCmd
from Commands.Drive.DriveCmd import DriveCmd
from Commands.Elevator.ManualElevatorCmd import ManualElevatorCmd
from Commands.Score.BargeScoreCmd import BargeScoreCmd
from Commands.Score.ReefScoreLFourCmd import ReefScoreLFourCmd
from Commands.Score.ReefScoreLThreeCmd import ReefScoreLThreeCmd
from Commands.Score.ReefScoreLTwoCmd import ReefScoreLTwoCmd
from Commands.Score.ScoreProcessorCmd import ScoreProcessorCmd
from Commands.Intake.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.Intake.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.Elevator.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Cimber.Climber import Climber
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina
from Subsystems.Swerve.SwerveDrive import SwerveDrive
from Subsystems.Vision.Vision import Vision
import constants




class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """


    def __init__(self) -> None:
        self.vision = Vision()
        self.swerveDrive = SwerveDrive(self.vision)
        self.climber = Climber()
        self.elevator = Elevator()
        self.coralina = Coralina()
        self.gorgina = Gorgina()

        self.driverController = wpilib.XboxController(0)
        self.operatorController = wpilib.XboxController(1)

        # Driver Controller - Swerve Drive
        self.swerveDrive.setDefaultCommand(DriveCmd(self.swerveDrive, self.driverController.getLeftY, self.driverController.getLeftX, self.driverController.getRightX))

        # Operator Controller - Manual Elevator
        self.elevator.setDefaultCommand(ManualElevatorCmd(self.elevator, self.operatorController.getLeftY))
        #self.climber.setDefaultCommand(ClimbCmd(self.climber, self.operatorController.getRightY))
        self.gorgina.setDefaultCommand(ManualAlgaeIntakeCmd(self.gorgina, self.operatorController.getRightY))
        #self.coralina.setDefaultCommand(ManualCoralIntakeCmd(self.coralina, self.operatorController.getRightX))
        

        self.configureButtonBindings()

        

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        # Manual Intake and Outtake for Coral - Triggers Operator
        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.leftTrigger).whileTrue(
        #     ManualCoralIntakeCmd(self.coralina, -1)
        # )

        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.rightTrigger).whileTrue(
        #     ManualCoralIntakeCmd(self.coralina, .5)
        # )

        # Manual Intake and Outtake for Algae - Bumpers Operator
        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kLeftBumper).whileTrue(
        #     ManualAlgaeIntakeCmd(self.gorgina, -1)
        # )

        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kRightBumper).whileTrue(
        #     ManualAlgaeIntakeCmd(self.gorgina, .5)
        # )

        # # Score Barge - Left Stick Button Operator
        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kLeftStick).whileTrue(
        #     BargeScoreCmd(self.gorgina, self.elevator)
        # )

        # # Algae removal on L3 & L2 - Up & Down D Pad Operator
        # commands2.button.povbutton(self.operatorController, wpilib.XboxController.POVUp).onTrue(
        #     AlgaeLThreeCmd(self.gorgina)
        # )
        # commands2.button.povbutton(self.operatorController, wpilib.XboxController.POVDown).onTrue(
        #     AlgaeLTwoCmd(self.gorgina)
        # )

        # # Hang - Xbox Button Operator
        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kStart).onTrue(
        #     ClimbCmd(self.climber)
        # )

        # # Human Player Station - Right Trigger Driver
        # commands2.button.JoystickButton(self.driverController, wpilib.XboxController.rightTrigger).onTrue(
        #     HumanPlayerCoralCmd(self.coralina, self.elevator)
        # )

        # Align to coral column - Left & Right d pad Operator
        # commands2.button.povbutton(self.operatorController, wpilib.XboxController.POVLeft).onTrue(
        #     DriveReefCmd(self.vision)
        # )

        # commands2.button.povbutton(self.operatorController, wpilib.XboxController.POVRight).onTrue(
        #     DriveReefCmd(self.vision)
        # )








        # Ready for comp cmds

        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kX).onTrue(
        #     ReefScoreLTwoCmd(self.coralina, self.elevator)
        # )

        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kY).onTrue(
        #     ReefScoreLThreeCmd(self.coralina, self.elevator)
        # )

        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kB).onTrue(
        #     ReefScoreLFourCmd(self.coralina, self.elevator)
        # )

        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kStart).onTrue(
        #     GroundPickupCmd(self.gorgina, self.elevator)
        # )

        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kA).onTrue(
        #     ScoreProcessorCmd(self.gorgina, self.elevator)
        # )


        
        

    def disablePIDSubsystems(self) -> None:
        """Disables all ProfiledPIDSubsystem and PIDSubsystem instances.
        This should be called on robot disable to prevent integral windup."""


    def getAutonomousCommand(self) -> commands2.Command:
        """Use this to pass the autonomous command to the main {@link Robot} class.

        :returns: the command to run in autonomous
        """
        return commands2.cmd.none()

def returnOne():
    return 1

def returnOneN():
    return -1