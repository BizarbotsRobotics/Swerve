
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
from Commands.Drive.DriveReefCmd import DriveReefCmd
from Commands.Intake.AlgaeIntakeCmd import AlgaeIntakeCmd
from Commands.Intake.AlgaeLThreeCmd import AlgaeLThreeCmd
from Commands.Intake.AlgaeLTwoCmd import AlgaeLTwoCmd
from Commands.Intake.AlgaeOuttakeCmd import AlgaeOuttakeCmd
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
from Commands.Score.ScoreAlgaeCmd import ScoreAlgaeCmd
from Commands.Score.ScoreCmd import ScoreCmd
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

        self.driverController = commands2.button.CommandXboxController(0)
        self.operatorController = commands2.button.CommandXboxController(1)

        # Driver Controller - Swerve Drive
        self.swerveDrive.setDefaultCommand(DriveCmd(self.swerveDrive, self.driverController.getLeftY, self.driverController.getLeftX, self.driverController.getRightX))

        # Operator Controller - Manual Elevator
        # self.elevator.setDefaultCommand(ManualElevatorCmd(self.elevator, self.operatorController.getLeftY))


        # self.gorgina.setDefaultCommand(ManualAlgaePivotCmd(self.gorgina, self.operatorController.getRightY))
        # self.coralina.setDefaultCommand(ManualCoralPivotCmd(self.coralina, self.operatorController.getRightX))
        
        # Comp Ready Cmds

        # Hang - Xbox Button Operator
        self.climber.setDefaultCommand(ClimbCmd(self.climber, self.operatorController.getRightY))

        self.configureButtonBindings()

        

    def configureButtonBindings(self) -> None:

        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        self.chooser = wpilib.SendableChooser()
        self.chooser.addOption("Drive Forward", DriveCmd(self.swerveDrive, 0, 0.5, 0).withTimeout(3))

        
        algaePivotTrigger = commands2.button.Trigger(lambda: self.gorgina.getAlgaePivotPosition > 110)

        self.operatorController.leftBumper().whileTrue(
            ManualAlgaeIntakeCmd(self.gorgina, lambda: -1)
        )

        self.operatorController.rightBumper().whileTrue(
            ManualAlgaeIntakeCmd(self.gorgina, lambda: .5)
        )

        self.operatorController.axisGreaterThan(2, 0.1).whileTrue(
            ManualCoralIntakeCmd(self.coralina, lambda: -.5)
        )

        self.operatorController.axisGreaterThan(3, 0.1).whileTrue(
            ManualCoralIntakeCmd(self.coralina, lambda: .5)
        )

        self.operatorController.a().onTrue(
            ScoreCmd(self.gorgina, self.coralina, self.elevator)
        )

        self.operatorController.povUp().onTrue(
            ScoreAlgaeCmd(self.gorgina, self.coralina, self.elevator)
        )

        self.operatorController.start().onTrue(
            HumanPlayerCoralCmd(self.coralina, self.elevator, self.gorgina)
        )

        algaePivotTrigger.onTrue(SetCoralPivotCmd(self.coralina, 90))

        self.operatorController.x().onTrue(
            ReefScoreLTwoCmd(self.coralina, self.elevator, self.gorgina)
        )

        self.operatorController.y().onTrue(
            ReefScoreLThreeCmd(self.coralina, self.elevator, self.gorgina)
        )

        self.operatorController.b().onTrue(
            ReefScoreLFourCmd(self.coralina, self.elevator, self.gorgina)
        )

        self.operatorController.povLeft().onTrue(
            GroundPickupCmd(self.coralina, self.gorgina, self.elevator)
        )

        self.operatorController.povRight().onTrue(
            ScoreProcessorCmd(self.gorgina, self.elevator)
        )

        self.operatorController.axisMagnitudeGreaterThan(1,.05).onTrue(
            ManualElevatorCmd(self.elevator, self.operatorController.getLeftY)
        )

        self.operatorController.axisMagnitudeGreaterThan(4 ,.2).onTrue(
            ManualCoralPivotCmd(self.coralina, lambda: (self.operatorController.getRightX())*.7)
        )

        self.operatorController.axisMagnitudeGreaterThan(5, .2).onTrue(
            ManualAlgaePivotCmd(self.gorgina, lambda: (self.operatorController.getRightY() )*.7)
        )









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
        """Use this to pass the autonomous command to the main {Robot} class.

        :returns: the command to run in autonomous
        """
        return self.chooser.getSelected()

def returnOne():
    return 1

def returnOneN():
    return -1