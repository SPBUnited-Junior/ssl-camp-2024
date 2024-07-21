"""Верхнеуровневый код стратегии"""

# pylint: disable=redefined-outer-name

# @package Strategy
# Расчет требуемых положений роботов исходя из ситуации на поле


# !v DEBUG ONLY
from enum import Enum
from time import time

import bridge.router.waypoint as wp
from bridge import const
from bridge.auxiliary import fld
from bridge.processors.referee_state_processor import Color as ActiveTeam
from bridge.processors.referee_state_processor import State as GameStates
from bridge.strategy import ref_states, easy_strategy


class States(Enum):
    """Класс с глобальными состояниями игры"""

    DEBUG = 0
    DEFENSE = 1
    ATTACK = 2


class Strategy:
    """Основной класс с кодом стратегии"""

    def __init__(
        self,
        dbg_game_status: GameStates = GameStates.RUN,
        dbg_state: States = States.ATTACK,
    ) -> None:

        self.game_status = dbg_game_status
        self.active_team: ActiveTeam = ActiveTeam.ALL
        self.we_active = False
        self.state = dbg_state
        self.timer = time()

    def change_game_state(
        self, new_state: GameStates, upd_active_team: ActiveTeam
    ) -> None:
        """Изменение состояния игры и цвета команды"""
        self.game_status = new_state
        self.active_team = upd_active_team

    def process(self, field: fld.Field) -> list[wp.Waypoint]:
        """
        Рассчитать конечные точки для каждого робота
        """
        if self.game_status not in [GameStates.KICKOFF, GameStates.PENALTY]:
            if (
                self.active_team == ActiveTeam.ALL
                or field.ally_color == self.active_team
            ):
                self.we_active = True
            else:
                self.we_active = False

        waypoints: list[wp.Waypoint] = []
        for i in range(const.TEAM_ROBOTS_MAX_COUNT):
            waypoints.append(
                wp.Waypoint(
                    field.allies[i].get_pos(),
                    field.allies[i].get_angle(),
                    wp.WType.S_STOP,
                )
            )

        if field.ally_color == const.COLOR:
            print("-" * 32)
            print(self.game_status, "\twe_active:", self.we_active)

        match self.game_status:
            case GameStates.RUN:
                easy_strategy.run(field, waypoints)
            case GameStates.TIMEOUT:
                ref_states.timeout(field, waypoints)
            case GameStates.HALT:
                pass
                # self.halt(field, waypoints)
            case GameStates.PREPARE_PENALTY:
                ref_states.prepare_penalty(field, waypoints, self.we_active)
            case GameStates.PENALTY:
                if self.we_active:
                    easy_strategy.attacker(field, waypoints, const.PENALTY_KICKER)
                else:
                    easy_strategy.goalkeeper(field, waypoints)
            case GameStates.PREPARE_KICKOFF:
                ref_states.prepare_kickoff(field, waypoints, self.we_active)
            case GameStates.KICKOFF:
                ref_states.kickoff(field, waypoints, self.we_active)
            case GameStates.FREE_KICK:
                easy_strategy.run(field, waypoints)
            case GameStates.STOP:
                easy_strategy.run(field, waypoints)

        # self.debug(field, waypoints)  # NOTE

        return waypoints
