
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import commands2.button
import commands2.cmd
import wpilib

from Commands.AlgaePivotCmd import AlgaePivotCmd
from Commands.CoralIOuttakeCmd import CoralOuttakeCmd
from Commands.CoralIntakeCmd import CoralIntakeCmd
from Commands.CoralPivotCmd import CoralPivotCmd
from Commands.ManualAlgaeIntakeCmd import ManualAlgaeIntakeCmd
from Commands.ManualAlgaePivotCmd import ManualAlgaePivotCmd
from Commands.ManualCoralIntakeCmd import ManualCoralIntakeCmd
from Commands.ClimberCmd import ClimberCmd
from Commands.DriveCmd import DriveCmd
from Commands.ManualElevatorCmd import ManualElevatorCmd
from Commands.SetAlgaePivotCmd import SetAlgaePivotCmd
from Commands.SetCoralPivotCmd import SetCoralPivotCmd
from Commands.SetElevatorPositionCmd import SetElevatorPositionCmd
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
        # self.vision = Vision()
        # self.swerveDrive = SwerveDrive(self.vision)
        # self.climber = Climber()
        self.elevator = Elevator()
        self.coralina = Coralina()
        self.gorgina = Gorgina()

        self.driverController = wpilib.XboxController(0)
        self.operatorController = wpilib.XboxController(1)

        # self.swerveDrive.setDefaultCommand(DriveCmd(self.swerveDrive, self.driverController.getLeftY, self.driverController.getLeftX, self.driverController.getRightX))

        # self.climber.setDefaultCommand(ClimberCmd(self.climber, self.operatorController.getRightTriggerAxis, self.operatorController.getLeftTriggerAxis))

        self.elevator.setDefaultCommand(ManualElevatorCmd(self.elevator, self.operatorController.getLeftY))

        # self.coralina.setDefaultCommand(ManualCoralIntakeCmd(self.coralina, self.operatorController.getLeftY))
        self.coralina.setDefaultCommand(CoralPivotCmd(self.coralina, self.operatorController.getRightX))
    
        self.gorgina.setDefaultCommand(ManualAlgaePivotCmd(self.gorgina, self.operatorController.getRightY))
        

        self.configureButtonBindings()

        

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """


        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kLeftBumper).whileTrue(
            ManualAlgaeIntakeCmd(self.gorgina, -1)
        )

        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kRightBumper).whileTrue(
            ManualAlgaeIntakeCmd(self.gorgina, .5)
        )
        
        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kX).onTrue(
            SetElevatorPositionCmd(self.elevator, -12)
        )

        # commands2.button.povbutton.POVButton(self.operatorController, wpilib.XboxController.POVDown).onTrue(
        #     SetAlgaePivotCmd(self.gorgina, constants.IntakeConstants.REEF_ALGAE_ANGLE)
        # )

        # commands2.button.POVButton(self.operatorController, wpilib.XboxController.POVDown).onTrue(
        #     SetCoralPivotCmd(self.coralina, constants.IntakeConstants.MID_CORAL_ANGLE)
        # )
        
        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kX).onTrue(
        #     CoralIntakeCmd(self.coralina)
        # )

        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kA).onTrue(
            SetAlgaePivotCmd(self.gorgina, 45)
        )

        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kY).whileTrue(
            CoralOuttakeCmd(self.coralina)
        )

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