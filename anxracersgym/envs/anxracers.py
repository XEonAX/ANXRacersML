from math import fabs
import math
from time import sleep
import gym.spaces as spaces
import gym
import numpy as np
from anxracersgym.envs.gameconnector import ANXRacersMemoryMapClient
from anxracersgym.envs.gamestate import GameState


def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))


class ANXRacersEnv(gym.Env):
    def __init__(self, reactionTime=0.01):
        super(ANXRacersEnv, self).__init__()
        self.reactionTime = reactionTime
        self.connector = None
        self.initialized = False
        self.observation_space = self._get_observation_space()
        self.action_space = self._get_action_space()
        self.stuckForHowManyTicks = 0
        pass

    def _get_observation_space(self):
        # SpaceshipPosX = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # SpaceshipPosY = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # SpaceshipRotationZ = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # SpaceshipRotationX = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # SpaceshipVelocityX = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # SpaceshipVelocityY = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # SpaceshipAngularVelocity = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # SpaceshipInputY = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # SpaceshipInputZ = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # CheckpointRelPosX = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # CheckpointRelPosY = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # CheckpointRotationZ = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        # CheckpointRotationW = spaces.Box(low=-1.0, high=1.0, shape=(1,))

        # Sensor = spaces.Tuple(
        #     (
        #         spaces.Discrete(2),  # Hit,
        #         spaces.Discrete(2),  # IsObstacle,
        #         spaces.Discrete(2),  # IsProp,
        #         spaces.Discrete(2),  # IsTrack,
        #         spaces.Discrete(100),  # ObjType,
        #         spaces.Box(low=-1.0, high=1.0, shape=(1,)),  # Distance,
        #         spaces.Box(low=-1.0, high=1.0, shape=(1,)),  # RotationZ,
        #         spaces.Box(low=-1.0, high=1.0, shape=(1,)),  # RotationX,
        #     )
        # )

        # Sensors = spaces.Tuple(
        #     (
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #         Sensor,
        #     )
        # )
        # return spaces.Tuple(spaces=
        #     (
        #         SpaceshipPosX,
        #         SpaceshipPosY,
        #         SpaceshipRotationZ,
        #         SpaceshipRotationX,
        #         SpaceshipVelocityX,
        #         SpaceshipVelocityY,
        #         SpaceshipAngularVelocity,
        #         SpaceshipInputY,
        #         SpaceshipInputZ,
        #         CheckpointRelPosX,
        #         CheckpointRelPosY,
        #         CheckpointRotationZ,
        #         CheckpointRotationW,
        #         # Sensors,
        #     )
        # )
        return spaces.Box(low=-1.0, high=1.0, shape=(13,))

    def _get_action_space(self):
        return spaces.Box(low=-1.0, high=1.0, shape=(2,))
        pass

    def _get_default_action(self):
        return np.array([0.0, 0.0], dtype="float32")
        pass

    def _send_control(self, action):
        self.connector.set_inputs(action[0], action[1])
        pass

    def _get_obs_rew_terminated_info(self):
        (
            level,
            LevelName,
            SpaceshipPhysics,
            ShipName,
            UserDisplayName,
            gameState,
            UpdateNumber,
            SpaceshipState,
            trackState,
            Rayhits,
        ) = self.connector.retrieve_data()

        # obs = (
        #     np.array([SpaceshipState[0]], dtype="float32"),
        #     np.array([SpaceshipState[1]], dtype="float32"),
        #     np.array([SpaceshipState[2]], dtype="float32"),
        #     np.array([SpaceshipState[3]], dtype="float32"),
        #     np.array([SpaceshipState[4]], dtype="float32"),
        #     np.array([SpaceshipState[5]], dtype="float32"),
        #     np.array([SpaceshipState[6]], dtype="float32"),
        #     np.array([SpaceshipState[7]], dtype="float32"),
        #     np.array([SpaceshipState[8]], dtype="float32"),
        #     np.array([trackState[0]], dtype="float32"),
        #     np.array([trackState[1]], dtype="float32"),
        #     np.array([trackState[2]], dtype="float32"),
        #     np.array([trackState[3]], dtype="float32"),
        # )
        obs = [
            SpaceshipState[0],  # SpaceshipPosX,
            SpaceshipState[1],  # SpaceshipPosY,
            SpaceshipState[2],  # SpaceshipRotationZ,
            SpaceshipState[3],  # SpaceshipRotationX,
            SpaceshipState[4],  # SpaceshipVelocityX,
            SpaceshipState[5],  # SpaceshipVelocityY,
            SpaceshipState[6],  # SpaceshipAngularVelocity,
            SpaceshipState[7],  # SpaceshipInputY,
            SpaceshipState[8],  # SpaceshipInputZ,
            trackState[0],  # CheckpointRelPosX,
            trackState[1],  # CheckpointRelPosY,
            trackState[2],  # CheckpointRotationZ,
            trackState[3],  # CheckpointRotationW,
        ]
        obs = np.array(obs, dtype="float32")
        rew = -5
        rew += -np.linalg.norm(
            np.array([trackState[0], trackState[1]], dtype=np.float32)
        )  # distance to next checkpoint
        rew += trackState[4] / level[0]  # checkpoints completed/total checkpoints
        terminated = trackState[4] / level[0] > 0.9
        truncated = False
        if (
            magnitude([SpaceshipState[4], SpaceshipState[5], SpaceshipState[6]])
            == 0  # stuck somewhere
            and not magnitude([SpaceshipState[0], SpaceshipState[1]])
            == 0  # not at origin
        ):
            rew = -10
            terminated = True
            truncated = True
        info = {}
        # print(rew,"\r")
        # return obs, rew, terminated, truncated, info #uncomment for envchecker
        return obs, rew, terminated, info

    def _wait(self):
        self._send_control(self._get_default_action())

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if not self.initialized:
            self.connector = ANXRacersMemoryMapClient()
            while self.connector.AccessReceived == False:
                print("Waiting to connect to ANXRacers", end="\r")
                sleep(0.1)
            self.initialized = True
        self.connector.send_reset()
        sleep(0.2)
        while self.connector.gameState != GameState.Racing:
            print("Waiting for Race to start",end="\r")
            sleep(0.2)
        (
            level,
            LevelName,
            SpaceshipPhysics,
            ShipName,
            UserDisplayName,
            gameState,
            UpdateNumber,
            SpaceshipState,
            trackState,
            Rayhits,
        ) = self.connector.retrieve_data()
        # return (
        #     np.array([SpaceshipState[0]], dtype="float32"),
        #     np.array([SpaceshipState[1]], dtype="float32"),
        #     np.array([SpaceshipState[2]], dtype="float32"),
        #     np.array([SpaceshipState[3]], dtype="float32"),
        #     np.array([SpaceshipState[4]], dtype="float32"),
        #     np.array([SpaceshipState[5]], dtype="float32"),
        #     np.array([SpaceshipState[6]], dtype="float32"),
        #     np.array([SpaceshipState[7]], dtype="float32"),
        #     np.array([SpaceshipState[8]], dtype="float32"),
        #     np.array([trackState[0]], dtype="float32"),
        #     np.array([trackState[1]], dtype="float32"),
        #     np.array([trackState[2]], dtype="float32"),
        #     np.array([trackState[3]], dtype="float32"),
        # ), {}
        return (
            np.array(
                [
                    SpaceshipState[0],
                    SpaceshipState[1],
                    SpaceshipState[2],
                    SpaceshipState[3],
                    SpaceshipState[4],
                    SpaceshipState[5],
                    SpaceshipState[6],
                    SpaceshipState[7],
                    SpaceshipState[8],
                    trackState[0],
                    trackState[1],
                    trackState[2],
                    trackState[3],
                ],
                dtype="float32",
            ) #,{}, Uncomment for envchecker
        )
        pass

    def step(self, action):
        self._send_control(action)
        sleep(self.reactionTime)
        return self._get_obs_rew_terminated_info()

    def render(self):
        pass

    def close(self):
        print("Trying to close anxracers env. Not Implemented")
        pass
