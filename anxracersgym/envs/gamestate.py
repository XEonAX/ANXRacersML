from enum import Enum


class GameState(Enum):
    InMenu = 0
    InTracklist = 1
    InShipyard = 2
    RaceCountdown = 3
    Racing = 4
    RaceFinished = 5
