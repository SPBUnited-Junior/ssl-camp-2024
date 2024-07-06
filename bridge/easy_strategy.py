import math
import bridge.processors.field as fld
import bridge.processors.waypoint as wp


def easy_run(field: fld.Field, waypoints: list[wp.Waypoint]) -> None:
    robot = field.allies[0]
    ball_pos = field.ball.get_pos()

    print("dist:", (robot.get_pos() - ball_pos).mag())


# длина вектора - point.mag()
# аргумент вектора - point.arg()
# акртангенс - math.atan2(y, x)
