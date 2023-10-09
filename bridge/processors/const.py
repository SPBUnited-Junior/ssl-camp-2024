import bridge.processors.auxiliary as aux

##################################################
# GAME SETTING CONSTS
GK = 1
PENALTY_KICKER = 2
ENEMY_GK = 5
IS_SIMULATOR_USED = True
CAMERAS_COUNT: int = 4
MAX_BALLS_IN_CAMERA: int = 64
MAX_BALLS_IN_FIELD: int = CAMERAS_COUNT * MAX_BALLS_IN_CAMERA
BALL_PACKET_SIZE: int = 3

KEEP_BALL_DIST = 600

ROBOTS_MAX_COUNT: int = 32
TEAM_ROBOTS_MAX_COUNT: int = ROBOTS_MAX_COUNT // 2
SINGLE_ROBOT_PACKET_SIZE = 5
ROBOT_TEAM_PACKET_SIZE: int = SINGLE_ROBOT_PACKET_SIZE * TEAM_ROBOTS_MAX_COUNT

GEOMETRY_PACKET_SIZE: int = 2

DEBUG_ID = 1
DEBUG_CTRL = 9
CONTROL_MAPPING = \
{
    # DEBUG_ID: DEBUG_CTRL
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5
}

for i in range(TEAM_ROBOTS_MAX_COUNT):
    try:
        CONTROL_MAPPING[i]
    except:
        CONTROL_MAPPING[i] = None

TOPIC_SINK = "control-sink"
##################################################

##################################################
# CONTROL CONSTS
<<<<<<< HEAD
Ts = 0.03 # s
=======
Ts = 0.02 # s
>>>>>>> 9e1cc12 (.)

# ROBOT SETTING CONSTS
# MAX_SPEED = 100
# MAX_SPEED_R = 50
# ACCELERATION = 3
# BASE_KICKER_VOLTAGE = 7.0
MAX_SPEED = 700
MAX_SPEED_R = 4
ACCELERATION = 3
BASE_KICKER_VOLTAGE = 7.0

R_KP = 7
R_KD = 0
KP = 0.1

GK_INTERCEPT_SPEED = 300
GK_PEN_KICKOUT_SPEED = 500
##################################################
# GEOMETRY CONSTS

BALL_R = 0.05
ROBOT_R = 0.2
GRAVEYARD_POS = aux.Point(-10000, 0)
<<<<<<< HEAD
GOAL_DX = 4500
GOAL_DY = 1000
GOAL_PEN = 1000
=======
GOAL_DX = -1250
GOAL_DY = 800
GOAL_PEN = -800
>>>>>>> 9e1cc12 (.)
GOAL_BOUND_OFFSET = 100
GOAL_WALLLINE_OFFSET = 1800
GOAL_WALL_ROBOT_SEPARATION = 150

GK_FORW = 800
KICK_ALIGN_DIST = 200
KICK_ALIGN_DIST_MULT = 1.5
KICK_ALIGN_ANGLE = 0.1
KICK_ALIGN_OFFSET = 20
BALL_GRABBED_DIST = 150
BALL_GRABBED_ANGLE = 0.3

# ROUTE CONSTS

VANISH_DIST = 200
