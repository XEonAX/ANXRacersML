from math import fabs
from time import sleep
from rtgym import RealTimeGymInterface
import GymClient
import gym.spaces as spaces
import gym
import numpy as np


class ANXRacersInterface(RealTimeGymInterface, gym.Env):
    def __init__(self):
        self.client = None
        self.initialized = False
        pass

    def get_observation_space(self):
        SpaceshipPosX = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        SpaceshipPosY = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        SpaceshipRotationZ = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        SpaceshipRotationX = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        SpaceshipVelocityX = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        SpaceshipVelocityY = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        SpaceshipAngularVelocity = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        SpaceshipInputY = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        SpaceshipInputZ = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        CheckpointRelPosX = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        CheckpointRelPosY = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        CheckpointRotationZ = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        CheckpointRotationW = spaces.Box(low=-1.0, high=1.0, shape=(1,))

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
        return spaces.Tuple(
            (
                SpaceshipPosX,
                SpaceshipPosY,
                SpaceshipRotationZ,
                SpaceshipRotationX,
                SpaceshipVelocityX,
                SpaceshipVelocityY,
                SpaceshipAngularVelocity,
                SpaceshipInputY,
                SpaceshipInputZ,
                CheckpointRelPosX,
                CheckpointRelPosY,
                CheckpointRotationZ,
                CheckpointRotationW,
                # Sensors,
            )
        )

    def get_action_space(self):
        return spaces.Box(low=-1.0, high=1.0, shape=(2,))
        pass

    def get_default_action(self):
        return np.array([0.0, 0.0], dtype="float32")
        pass

    def send_control(self, control):
        print(control)
        self.client.set_inputs(control[0], control[1])
        pass

    def reset(self):
        if not self.initialized:
            self.client = GymClient.ANXRacersTelemetryClient()
            while self.client.AccessReceived == False:
                print("waiting for access")
            self.initialized = True
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
        ) = self.client.retrieve_data()
        return [
            np.array([SpaceshipState[0]], dtype="float32"),
            np.array([SpaceshipState[1]], dtype="float32"),
            np.array([SpaceshipState[2]], dtype="float32"),
            np.array([SpaceshipState[3]], dtype="float32"),
            np.array([SpaceshipState[4]], dtype="float32"),
            np.array([SpaceshipState[5]], dtype="float32"),
            np.array([SpaceshipState[6]], dtype="float32"),
            np.array([SpaceshipState[7]], dtype="float32"),
            np.array([SpaceshipState[8]], dtype="float32"),
            np.array([trackState[0]], dtype="float32"),
            np.array([trackState[1]], dtype="float32"),
            np.array([trackState[2]], dtype="float32"),
            np.array([trackState[3]], dtype="float32"),
        ], {}
        pass

    def get_obs_rew_terminated_info(self):
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
        ) = self.client.retrieve_data()

        obs = [
            np.array([SpaceshipState[0]], dtype="float32"),
            np.array([SpaceshipState[1]], dtype="float32"),
            np.array([SpaceshipState[2]], dtype="float32"),
            np.array([SpaceshipState[3]], dtype="float32"),
            np.array([SpaceshipState[4]], dtype="float32"),
            np.array([SpaceshipState[5]], dtype="float32"),
            np.array([SpaceshipState[6]], dtype="float32"),
            np.array([SpaceshipState[7]], dtype="float32"),
            np.array([SpaceshipState[8]], dtype="float32"),
            np.array([trackState[0]], dtype="float32"),
            np.array([trackState[1]], dtype="float32"),
            np.array([trackState[2]], dtype="float32"),
            np.array([trackState[3]], dtype="float32"),
        ]

        rew = -np.linalg.norm(
            np.array([trackState[0], trackState[1]], dtype=np.float32)
        )
        terminated = rew > -0.01 / 100000
        info = {}
        return obs, rew, terminated, info

    def wait(self):
        self.send_control(self.get_default_action())
