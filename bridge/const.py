"""
Определение необходимых констант
"""

from enum import Enum


class Color(Enum):
    """Класс с цветами"""

    ALL = 0
    BLUE = 1
    YELLOW = 2


##################################################
# GAME SETTING CONSTS
DIV = "B"
COLOR = Color.BLUE
POLARITY = 1  # -1 если ворота синих на +x; 1 если ворота синих на -x

IS_SIMULATOR_USED = True
IS_DRIBBLER_USED = True  # dribler and upper_kick
SELF_PLAY = False

GK = 5
PENALTY_KICKER = 0
ENEMY_GK = 5

CAMERAS_COUNT: int = 4
MAX_BALLS_IN_CAMERA: int = 64
MAX_BALLS_IN_FIELD: int = CAMERAS_COUNT * MAX_BALLS_IN_CAMERA
BALL_PACKET_SIZE: int = 2

ROBOTS_MAX_COUNT: int = 32
TEAM_ROBOTS_MAX_COUNT: int = ROBOTS_MAX_COUNT // 2
SINGLE_ROBOT_PACKET_SIZE = 5
ROBOT_TEAM_PACKET_SIZE: int = SINGLE_ROBOT_PACKET_SIZE * TEAM_ROBOTS_MAX_COUNT

GEOMETRY_PACKET_SIZE: int = 2

CONTROL_MAPPING: dict[int, int] = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
}
REVERSED_KICK: list[int] = []

for i in range(TEAM_ROBOTS_MAX_COUNT):
    try:
        CONTROL_MAPPING[i]
    except KeyError:
        CONTROL_MAPPING[i] = -1

TOPIC_SINK = "control-sink"
FIELD_TOPIC = "field-topic"
IMAGE_TOPIC = "image-topic"
##################################################

##################################################
# CONTROL CONSTS
Ts = 0.05  # s

# ROBOT SETTING CONSTS
# MAX_SPEED = 100
# MAX_SPEED_R = 50
# ACCELERATION = 3
# BASE_KICKER_VOLTAGE = 7.0
MAX_SPEED = 3000
MAX_SPEED_R = 30
SOFT_MAX_SPEED = 1500
SOFT_MAX_SPEED_R = 16
ACCELERATION = 3
BASE_KICKER_VOLTAGE = 7.0

R_KP = 7
R_KD = 0
KP = 0.1

INTERCEPT_SPEED = 50
GK_PEN_KICKOUT_SPEED = 500
##################################################
# GEOMETRY CONSTS

BALL_R = 22
ROBOT_R = 100
GRAVEYARD_POS_X = -10000


GOAL_DX = 4500
GOAL_DY = 1000
GOAL_PEN_DX = 1000
GOAL_PEN_DY = 2000
if DIV == "C":
    GOAL_DX = 2250
    GOAL_DY = 800
    GOAL_PEN_DX = 500
    GOAL_PEN_DY = 1350

GK_FORW = 200 + ROBOT_R
KICK_ALIGN_DIST = 150
GRAB_ALIGN_DIST = 130
KICK_ALIGN_DIST_MULT = 1.5
KICK_ALIGN_ANGLE = 0.07
KICK_ALIGN_OFFSET = 20
BALL_GRABBED_DIST = 115
BALL_GRABBED_ANGLE = 0.8

# ROUTE CONSTS
KEEP_BALL_DIST = 500 + ROBOT_R

# SOME STRATEGY TRASH
MIN_GOOD_ANGLE = 90
ROBOT_SPEED = 1.5
FULL_DELAY = 0.16


# VOLTAGES
VOLTAGE_PASS = 10
VOLTAGE_SHOOT = 15
VOLTAGE_UP = 10
VOLTAGE_ZERO = min(VOLTAGE_PASS, VOLTAGE_SHOOT, VOLTAGE_UP)
