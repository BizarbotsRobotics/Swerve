
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
from Commands.CoralPivotCmd import CoralPivotCmd
from Commands.ManualAlgaeIntakeCmd import ManualAlgaeIntakeCmd
from Commands.ManualAlgaePivotCmd import ManualAlgaePivotCmd
from Commands.ManualCoralIntakeCmd import ManualCoralIntakeCmd
from Commands.ClimberCmd import ClimberCmd
from Commands.DriveCmd import DriveCmd
from Commands.ManualElevatorCmd import ManualElevatorCmd
from Commands.SetElevatorPositionCmd import SetElevatorPositionCmd
from Subsystems.Cimber.Climber import Climber
from Subsystems.Coralina.Coralina import Coralina
from Subsystems.Elevator.Elevator import Elevator
from Subsystems.Gorgina.Gorgina import Gorgina
from Subsystems.Swerve.SwerveDrive import SwerveDrive
import constants




class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """


    def __init__(self) -> None:
        self.swerveDrive = SwerveDrive()
        self.climber = Climber()
        self.elevator = Elevator()
        self.coralina = Coralina()
        self.gorgina = Gorgina()

        self.driverController = wpilib.XboxController(0)
        self.operatorController = wpilib.XboxController(1)

        self.swerveDrive.setDefaultCommand(DriveCmd(self.swerveDrive, self.driverController.getLeftY, self.driverController.getLeftX, self.driverController.getRightX))

        self.climber.setDefaultCommand(ClimberCmd(self.climber, self.operatorController.getRightTriggerAxis, self.operatorController.getLeftTriggerAxis))

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

        commands2.button.povbutton.POVButton(self.operatorController, wpilib.XboxController.POVDown).onTrue(
            SetElevatorPositionCmd(self.elevator, constants.ElevatorConstants.L_ONE_ELEVATOR_HEIGHT)
        )

        commands2.button.povbutton.POVButton(self.operatorController, wpilib.XboxController.POVLeft).onTrue(
            SetElevatorPositionCmd(self.elevator, constants.ElevatorConstants.L_TWO_ELEVATOR_HEIGHT)
        )
    
        commands2.button.povbutton.POVButton(self.operatorController, wpilib.XboxController.POVUp).onTrue(
            SetElevatorPositionCmd(self.elevator, constants.ElevatorConstants.L_THREE_ELEVATOR_HEIGHT)
        )

        commands2.button.povbutton.POVButton(self.operatorController, wpilib.XboxController.POVRight).onTrue(
            SetElevatorPositionCmd(self.elevator, constants.ElevatorConstants.L_FOUR_ELEVATOR_HEIGHT)
        )

        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kB).whileTrue(
            ManualAlgaeIntakeCmd(self.gorgina,  returnOne)
        )

        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kX).whileTrue(
            ManualAlgaeIntakeCmd(self.gorgina, returnOneN)
        )
        
        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kA).whileTrue(
            ManualCoralIntakeCmd(self.coralina,  returnOne)
        )

        commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kY).whileTrue(
            ManualCoralIntakeCmd(self.coralina, returnOneN)
        )

        # commands2.button.JoystickButton(self.operatorController, wpilib.XboxController.Button.kLeftBumper).whileTrue(
        #     AlgaePivotCmd(self.gorgina)
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