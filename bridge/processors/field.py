"""
Модуль описания структуры Field для хранения информации об объектах на поле (роботы и мяч)
"""

import bridge.processors.auxiliary as aux
import bridge.processors.const as const
import bridge.processors.entity as entity
import bridge.processors.robot as robot

from math import cos


class Goal:
    """
    Структура, описывающая ключевые точки ворот
    """

    def __init__(self, goal_dx: float, goal_dy: float, pen_dx: float, pen_dy: float) -> None:

        # Абсолютный центр
        self.center = aux.Point(goal_dx, 0)

        # Относительные вектора
        self.eye_forw = aux.Point(-aux.sign(goal_dx), 0)
        self.eye_up = aux.Point(0, aux.sign(goal_dy))

        self.vec_up = aux.Point(0, goal_dy / 2)
        self.vec_pen = aux.Point(-pen_dx, 0)
        self.vec_pen_up = aux.Point(0, goal_dy / 2)

        # Абсолютные вектора
        self.up = self.center + self.vec_up
        self.down = self.center - self.vec_up
        self.frw = self.center + self.vec_pen
        self.frw_up = self.frw + self.vec_pen_up
        self.frw_down = self.frw - self.vec_pen_up

        # Оболочка штрафной зоны
        self.hull = [
            self.center + self.vec_pen_up,
            self.frw_up,
            self.frw_down,
            self.center - self.vec_pen_up,
            aux.FIELD_INF * self.eye_forw.x,
        ]

        # Попуск
        self.popusk_positions = [
            aux.Point(0, 2000),
            aux.Point(0, -2000),
            aux.Point(0, 0),
            aux.Point(aux.sign(goal_dx) * 2000, 2000),
            aux.Point(aux.sign(goal_dx) * 2000, -2000),
        ]


class Field:
    """
    Класс, хранящий информацию о всех объектах на поле и ключевых точках
    """

    def __init__(self, ctrl_mapping: dict[int, int], ally_color: str) -> None:
        """
        Конструктор
        Инициализирует все нулями

        TODO Сделать инициализацию реальными параметрами для корректного
        определения скоростей и ускорений в первые секунды
        """
        self.ally_with_ball = None

        self.ally_color = ally_color
        if self.ally_color == "b":
            self.polarity = const.POLARITY * -1
        else:
            self.polarity = const.POLARITY
        self.ball = entity.Entity(aux.GRAVEYARD_POS, 0, const.BALL_R, 0.2)
        self.b_team = [
            robot.Robot(aux.GRAVEYARD_POS, 0, const.ROBOT_R, "b", i, ctrl_mapping[i])
            for i in range(const.TEAM_ROBOTS_MAX_COUNT)
        ]
        self.y_team = [
            robot.Robot(aux.GRAVEYARD_POS, 0, const.ROBOT_R, "y", i, ctrl_mapping[i])
            for i in range(const.TEAM_ROBOTS_MAX_COUNT)
        ]
        self.all_bots = [*self.b_team, *self.y_team]
        self.ally_goal = Goal(
            const.GOAL_DX * self.polarity,
            const.GOAL_DY * self.polarity,
            const.GOAL_PEN_DX * self.polarity,
            const.GOAL_PEN_DY * self.polarity,
        )
        self.enemy_goal = Goal(
            -const.GOAL_DX * self.polarity,
            -const.GOAL_DY * self.polarity,
            -const.GOAL_PEN_DX * self.polarity,
            -const.GOAL_PEN_DY * self.polarity,
        )

        if const.SELF_PLAY:
            self.enemy_goal = self.ally_goal

        if self.ally_color == "b":
            self.allies = [*self.b_team]
            self.enemies = [*self.y_team]
        elif self.ally_color == "y":
            self.allies = [*self.y_team]
            self.enemies = [*self.b_team]

    def update_ball(self, pos: aux.Point, t: float) -> None:
        """
        Обновить положение мяча
        !!! Вызывать один раз за итерацию с постоянной частотой !!!
        """
        self.ball.update(pos, 0, t)

        self.ally_with_ball = None
        for r in self.allies:
            if self._is_ball_in(r):
                self.ally_with_ball = r


    def _is_ball_in(self, robo: robot.Robot) -> bool:
        """
        Определить, находится ли мяч внутри дриблера
        """
        return (robo.get_pos() - self.ball.get_pos()).mag() < const.BALL_GRABBED_DIST and abs(
            aux.wind_down_angle((self.ball.get_pos() - robo.get_pos()).arg() - robo.get_angle())
        ) < const.BALL_GRABBED_ANGLE

    def is_ball_in(self, robo: robot.Robot) -> bool:
        """
        Определить, находится ли мяч внутри дриблера
        """
        print(self.ally_with_ball)
        return robo == self.ally_with_ball

    def update_blu_robot(self, idx: int, pos: aux.Point, angle: float, t: float) -> None:
        """
        Обновить положение робота синей команды
        !!! Вызывать один раз за итерацию с постоянной частотой !!!
        """
        self.b_team[idx].update(pos, angle, t)

    def update_yel_robot(self, idx: int, pos: aux.Point, angle: float, t: float) -> None:
        """
        Обновить положение робота желтой команды
        !!! Вызывать один раз за итерацию с постоянной частотой !!!
        """
        self.y_team[idx].update(pos, angle, t)

    def get_ball(self) -> entity.Entity:
        """
        Получить объект мяча

        @return Объект entity.Entity
        """
        return self.ball

    def get_blu_team(self) -> list[robot.Robot]:
        """
        Получить массив роботов синей команды

        @return Массив entity.Entity[]
        """
        return self.b_team

    def get_yel_team(self) -> list[robot.Robot]:
        """
        Получить массив роботов желтой команды

        @return Массив entity.Entity[]
        """
        return self.y_team

    def is_ball_stop_near_goal(self) -> bool:
        """
        Определить, находится ли мяч в штрафной зоне
        """
        return aux.is_point_inside_poly(self.ball.get_pos(), self.ally_goal.hull) and not self.is_ball_moves_to_goal()

    def is_ball_moves(self) -> bool:
        """
        Определить, движется ли мяч
        """
        return self.ball.get_vel().mag() > const.INTERCEPT_SPEED

    def is_ball_moves_to_point(self, point: aux.Point) -> bool:
        """
        Определить, движется ли мяч в сторону точки
        """
        vec_to_point = point - self.ball.get_pos()
        # print( self.ball.get_vel().mag() * (sin(vec_to_point.arg() - self.ball.get_vel().mag()) ** 2) , const.INTERCEPT_SPEED)
        return self.ball.get_vel().mag() * (cos(vec_to_point.arg() - self.ball.get_vel().arg()) ** 2) > const.INTERCEPT_SPEED * 2

    def is_ball_moves_to_goal(self) -> bool:
        """
        Определить, движется ли мяч в сторону ворот
        """
        return self.is_ball_moves_to_point(self.ally_goal.center)
