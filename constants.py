class SwerveConstants:
    SWERVE_GEAR_RATIO = 21.42857

    SWERVE_P = 2.4
    SWERVE_I = 0
    SWERVE_D = 0.1

    DRIVE_P = 2.4
    DRIVE_I = 0
    DRIVE_D = 0.1

    DRIVE_MAX_SPEED = 6.0

    ATTAINABLE_MAX_TRANSLATIONAL_SPEED_METERS_PER_SECOND = 0
    ATTAINABLE_MAX_ROTATIONAL_VELOCITY_RADIANS_PER_SECOND = 0

        # Coordinates of swer ve modules relative to the center of the robot
    FRONT_LEFT_CORDS = {'x':.381, 'y':.381}
    FRONT_RIGHT_CORDS = {'x':.381, 'y':-.381}
    BACK_LEFT_CORDS = {'x':-.381, 'y':.381}
    BACK_RIGHT_CORDS = {'x':-.381, 'y':-.381}

    # Absolute Encoder Ports for Swerve Module
    FRONT_RIGHT_ENCODER_PORT = 1
    FRONT_LEFT_ENCODER_PORT = 0
    BACK_RIGHT_ENCODER_PORT = 2
    BACK_LEFT_ENCODER_PORT = 3

    # Drive Motor IDs for Swerve Module
    FRONT_RIGHT_DRIVE = 7
    FRONT_LEFT_DRIVE = 5
    BACK_RIGHT_DRIVE = 4
    BACK_LEFT_DRIVE = 6

    # Swerve Motor IDs for Swerve Module
    FRONT_RIGHT_SWERVE = 9
    FRONT_LEFT_SWERVE = 3
    BACK_RIGHT_SWERVE = 8
    BACK_LEFT_SWERVE = 10

    FRONT_RIGHT_ENCODER_OFFSET = .9307
    FRONT_LEFT_ENCODER_OFFSET = .54
    BACK_RIGHT_ENCODER_OFFSET = .167
    BACK_LEFT_ENCODER_OFFSET = .815
