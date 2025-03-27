import math


class SwerveConstants:
    SWERVE_GEAR_RATIO = 21.42857

    SWERVE_P = 24
    SWERVE_I = 0
    SWERVE_D = 0.1

    DRIVE_GEAR_RATIO = 6.12

    DRIVE_P = 2.4
    DRIVE_I = 0
    DRIVE_D = 0.1

    DRIVE_MAX_SPEED = 6.0
    DRIVE_MAX_ROTATION = 1

    ATTAINABLE_MAX_TRANSLATIONAL_SPEED_METERS_PER_SECOND = 0
    ATTAINABLE_MAX_ROTATIONAL_VELOCITY_RADIANS_PER_SECOND = 0

        # Coordinates of swerve modules relative to the center of the robot
    FRONT_LEFT_CORDS = {'x':.381, 'y':.381}
    FRONT_RIGHT_CORDS = {'x':.381, 'y':-.381}
    BACK_LEFT_CORDS = {'x':-.381, 'y':.381}
    BACK_RIGHT_CORDS = {'x':-.381, 'y':-.381}

    # Absolute Encoder Ports for Swerve Module
    FRONT_LEFT_ENCODER_PORT = 0
    FRONT_RIGHT_ENCODER_PORT = 1
    BACK_LEFT_ENCODER_PORT = 2
    BACK_RIGHT_ENCODER_PORT = 3
    

    # Drive Motor IDs for Swerve Module
    FRONT_LEFT_DRIVE = 7
    FRONT_RIGHT_DRIVE = 11
    BACK_LEFT_DRIVE = 6
    BACK_RIGHT_DRIVE = 4
   

    # Swerve Motor IDs for Swerve Module
    FRONT_LEFT_SWERVE = 9
    FRONT_RIGHT_SWERVE = 3
    BACK_LEFT_SWERVE = 10
    BACK_RIGHT_SWERVE = 8
    
    FRONT_LEFT_ENCODER_OFFSET = .801
    FRONT_RIGHT_ENCODER_OFFSET = .678
    BACK_LEFT_ENCODER_OFFSET = .195
    BACK_RIGHT_ENCODER_OFFSET = .824
    

    # IMU ID
    PIGEON_PORT = 3

class IntakeConstants:
    ALGAE_INTAKE_MOTOR = 3
    ALGAE_PIVOT_MOTOR = 24

    ALGAE_PIVOT_P = 0.01
    ALGAE_PIVOT_I = 0
    ALGAE_PIVOT_D = 0

    ZERO_ALGAE_ANGLE = 0
    REEF_ALGAE_ANGLE = 0
    BARGE_ALGAE_ANGLE = 0
    FLOOR_ALGAE_ANGLE = 0



    CORAL_INTAKE_MOTOR = 15
    CORAL_PIVOT_MOTOR = 14

    CORAL_PIVOT_P = 0.01
    CORAL_PIVOT_I = 0
    CORAL_PIVOT_D = 0

    ZERO_CORAL_ANGLE = 0
    L_ONE_CORAL_ANGLE = 0
    MID_CORAL_ANGLE = 0
    L_FOUR_CORAL_ANGLE = 0
    HP_CORAL_ANGLE = 0


class ElevatorConstants:
    ELEVATOR_MOTOR_ONE = 1
    ELEVATOR_MOTOR_TWO = 2

    ELEVATOR_P = 100
    ELEVATOR_I = 0
    ELEVATOR_D = 0

    L_ONE_ELEVATOR_HEIGHT = 40
    L_TWO_ELEVATOR_HEIGHT = 0
    L_THREE_ELEVATOR_HEIGHT = 0
    L_FOUR_ELEVATOR_HEIGHT = 0

    HP_ELEVATOR_HEIGHT = 0
        
    ZERO_ELEVATOR_HEIGHT = 0
    BARGE_ELEVATOR_HEIGHT = 0
    PROCESSOR_ELEVATOR_HEIGHT = 0
    



    

class ClimberConstants:
    CLIMBER_MOTOR_ONE = 15

class AutoAimConstants:
    kP = 0.004537
    kI = 0.0000
    kD = 0.000
    AutoAimPIDTolerance = 1.0
        # // public static final double DeflectorPosInValue = 0.0
        # // public static final double DeflectorPosOutValue = 0.0


class AutoFollowConstants:
        kP = 0.271
        kI = 0
        kD = 0.0

       

        AutoFollowPIDTolerance = 1.0
        # // public static final double DeflectorPosInValue = 0.0
        # // public static final double DeflectorPosOutValue = 0.0

    

class AutoRotateConstants:
    kP = 0.002037
    kI = 0.0000665
    kD = 0.0003333

    Tolerance = 6.0
        # // public static final double DeflectorPosInValue = 0.0
        # // public static final double DeflectorPosOutValue = 0.0

    

class AutoTranslateConstants: 
    kP = 0.05471
    kI = 0.000665
    kD = 0.001333

       

    Tolerance = 0.3
    Setpoint = 1.2


class AutoStrafeConstants:
    kP = 0.05471
    kI = 0.000665
    kD = 0.001333

       

    Tolerance = 1
        



class AutoConstants:
    kHeadingOffset = 90
    kMaxSpeedMetersPerSecond = 7.5
    kMaxAccelerationMetersPerSecondSquared = 5.2
    kMaxAngularSpeedRadiansPerSecond = 3 * math.pi
    kMaxAngularSpeedRadiansPerSecondSquared = 4* math.pi

    kPXController = 1
    kPYController = 1
    kPThetaController = 1



