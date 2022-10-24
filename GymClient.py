from math import fabs
import mmap
import struct
from threading import Lock, Thread
from time import sleep
from uuid import uuid4
import uuid

from GameState import GameState


class ANXRacersTelemetryClient:
    def __init__(self, tagname="ANXRacersGymInterface"):
        self.tagname = tagname

        self.ResetCount = 0
        self.GiveupCount = 0
        self.Inputs = (0, 0)
        self.AccessReceived = False
        # Threading attributes:
        self.__lock = Lock()
        self.__data = None
        self.__t_client = Thread(
            target=self.__client_thread, args=(), kwargs={}, daemon=True
        )
        self.__t_client.start()

    def __client_thread(self):
        # -1=AnonFile,10000=Size,tagName=mmapName
        with mmap.mmap(-1, 10000, self.tagname, access=mmap.ACCESS_WRITE) as mm:
            while True:
                self.AccessReceived=True
                self.__lock.acquire()
                mm.seek(0)
                data = mm.read(100)
                tagName = data.decode("UTF-8")
                # print(tagName)  # prints tagname
                mm.seek(100)
                levelbytes = mm.read(100)
                # levelId = uuid.UUID(bytes=struct.unpack("16c", levelbytes[0:16]))
                # print(levelId)
                self.level = (NoOfCheckpoints, Laps, Difficulty) = struct.unpack(
                    "iif", levelbytes[16:28]
                )
                self.LevelName = levelbytes[28:].decode("UTF-8")
                # print(self.level, self.LevelName)  # prints updatenumber

                mm.seek(200)
                spaceshipPhysicsBytes = mm.read(100)
                self.SpaceshipPhysics = (
                    Mass,
                    LDrag,
                    ADrag,
                    SurgeForward,
                    SurgeBackward,
                    Strafe,
                    Torque,
                    Radius,
                    Friction,
                    Bounce,
                ) = struct.unpack("10f", spaceshipPhysicsBytes[16:56])
                self.ShipName = spaceshipPhysicsBytes[56:].decode("UTF-8")
                # print(self.SpaceshipPhysics, self.ShipName)

                mm.seek(300)
                userBytes = mm.read(100)
                # userId = uuid.UUID(bytes=struct.unpack("16c", userBytes[0:16]))
                # print(userId)
                self.UserDisplayName = userBytes[16:].decode("UTF-8")
                # print(self.UserDisplayName)

                mm.seek(400)
                self.gameState = GameState(struct.unpack("i", mm.read(4))[0])

                mm.seek(512)
                self.UpdateNumber = struct.unpack("i", mm.read(4))[0]
                # print(self.UpdateNumber)

                mm.seek(520)

                spaceshipStateBytes = mm.read(36)
                self.SpaceshipState = (
                    PosX,
                    PosY,
                    RotationZ,
                    RotationX,
                    VelocityX,
                    VelocityY,
                    AngularVelocity,
                    InputY,
                    InputZ,
                ) = struct.unpack("9f", spaceshipStateBytes)
                # print(self.SpaceshipState)

                mm.seek(560)
                trackStateBytes = mm.read(20)
                self.trackState = (
                    RelPosX,
                    RelPosY,
                    CheckpointRotationZ,
                    CheckpointRotationW,
                    CheckpointIndex,
                ) = struct.unpack("ffffi", trackStateBytes)
                # print(self.trackState)

                mm.seek(600)
                self.Rayhits = []
                for x in range(24 * 5):
                    RayhitBytes = mm.read(20)
                    RayHit = (
                        Hit,
                        IsObstacle,
                        IsProp,
                        IsTrack,
                        ObjType,
                        Distance,
                        RotationZ,
                        RotationX,
                    ) = struct.unpack("????ifff", RayhitBytes)
                    self.Rayhits.append(RayHit)
                    # print(self.RayHit)
                self.__lock.release()

                mm.seek(418)
                memResetCount, memGiveupCount = struct.unpack("ii", mm.read(8))
                if self.ResetCount == 0:
                    self.ResetCount = memResetCount
                if self.GiveupCount == 0:
                    self.GiveupCount = memGiveupCount
                mm.seek(410)
                mm.write(
                    struct.pack(
                        "ffii",
                        self.Inputs[0],
                        self.Inputs[1],
                        self.ResetCount,
                        self.GiveupCount,
                    )
                )
                sleep(0.01)
                # print("=====================================")

    def retrieve_data(self):
        return (
            self.level,
            self.LevelName,
            self.SpaceshipPhysics,
            self.ShipName,
            self.UserDisplayName,
            self.gameState,
            self.UpdateNumber,
            self.SpaceshipState,
            self.trackState,
            self.Rayhits,
        )

    def set_inputs(self, x: float, y: float):
        self.Inputs = (x, y)

    def send_reset(self):
        self.ResetCount += 1
    def send_giveup(self):
        self.GiveupCount += 1
        # """
        # Thread of the client.
        # This listens for incoming data until the object is destroyed
        # TODO: handle disconnection
        # """
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.connect((self._host, self._port))
        #     data_raw = b""
        #     while True:  # main loop
        #         while len(data_raw) < self._nb_bytes:
        #             data_raw += s.recv(1024)
        #         div = len(data_raw) // self._nb_bytes
        #         data_used = data_raw[(div - 1) * self._nb_bytes : div * self._nb_bytes]
        #         data_raw = data_raw[div * self._nb_bytes :]
        #         self.__lock.acquire()
        #         self.__data = data_used
        #         self.__lock.release()


if __name__ == "__main__":
    ANXRacersTelemetryClient()
