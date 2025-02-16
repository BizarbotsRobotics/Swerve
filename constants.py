class SwerveConstants:
    SWERVE_GEAR_RATIO = 21.42857

    SWERVE_P = 24
    SWERVE_I = 0
    SWERVE_D = 0.1

    DRIVE_P = 2.4
    DRIVE_I = 0
    DRIVE_D = 0.1

    DRIVE_MAX_SPEED = 6.0

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
    ALGAE_PIVOT_MOTOR = 25

    CORAL_INTAKE_MOTOR = 15
    CORAL_PIVOT_MOTOR = 14

class ElevatorConstants:
    ELEVATOR_MOTOR_ONE = 1
    ELEVATOR_MOTOR_TWO = 2

    ELEVATOR_P =.15
    ELEVATOR_I = 0
    ELEVATOR_D = 0



    

class ClimberConstants:
    CLIMBER_MOTOR_ONE = 15
    CLIMBER_MOTOR_TWO = 20


