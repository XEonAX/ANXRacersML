from math import fabs
import mmap
import struct
from threading import Lock, Thread
from time import sleep

from anxracersgym.envs.gamestate import GameState


    # <MMAP>
    # 0-100 (Unicode) MemoryMapName = "ANXRacersGymInterface"
    # 100-200 (Object) Level
    #     100-116 (Guid) LevelId
    #     116-120 (int) Number of Checkpoints
    #     120-124 (int) Laps
    #     124-128 (float) Difficulty
    #     128- (Unicode) LevelName
    # 200-300 (Object) Spaceship Physics
    #     200-216 (Guid) LevelId
    #     216-220 (float) Mass         
    #     220-224 (float) LDrag        
    #     224-228 (float) ADrag        
    #     228-232 (float) SurgeForward 
    #     232-236 (float) SurgeBackward
    #     236-240 (float) Strafe       
    #     240-244 (float) Torque       
    #     244-248 (float) Radius       
    #     248-252 (float) Friction     
    #     252-256 (float) Bounce  
    #     256- (Unicode) ShipName     
    # 300-400 (Object) Player
    #     300-316 (Guid) UserId
    #     316- (Unicode) DisplayName
    # 400-404 (int) GameState
    # 404-410 Empty
    # 410-418 (Vector2) Spaceship Inputs
    #     410-414 (float) Y Surge +1.0 -1.0
    #     414-418 (float) Z Turn +1.0 -1.0
    # 418-422 (int) Reset Input    
    # 422-426 (int) Giveup Input    
    # 426-512 Empty
    # 512-516 (int) UpdateNumber
    # 520-556 (Object) Spaceship State Live
    #     520-528 (Vector2) Spaceship Position
    #         520-524 (float) X Position
    #         524-528 (float) Y Position
    #     528-536 (Vector2) Spaceship Rotation
    #         528-532 (float) Z Rotation
    #         532-536 (float) W Rotation
    #     536-544 (Vector3) Spaceship Rigidbody
    #         536-540 (float) X Velocity
    #         540-544 (float) Y Velocity
    #         544-548 (float) Z Angular Velocity
    #     548-556 (Vector3) Spaceship Inputs
    #         548-552 (float) Y Surge +1.0 -1.0
    #         552-556 (float) Z Turn +1.0 -1.0
    # 556-560 Empty    
    # 560-580 (Object) Track State Live
    #     560-568 (Vector2) Rel Position
    #         560-564 (float) X Position
    #         564-568 (float) Y Position
    #     568-576 (Vector2) Rotation
    #         568-572 (float) Z Rotation
    #         572-576 (float) W Rotation
    #     576-580 (int) Checkpoint Index
    # 600 (Array * 24 * 5) Sensor Info Live (24 Sensors returning 5 Detections each)
    #     0 (bool) Hit
    #     1 (bool) IsObstacle
    #     2 (bool) IsProp
    #     3 (bool) IsTrack
    #     4-8 (int) ObjType
    #     8-12 (float) Distance
    #     12-20 (Vector2) Rotation
    #         12-16 (float) Z Rotation
    #         16-20 (float) W Rotation
    # </MMAP>

class ANXRacersMemoryMapClient:
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
                self.__lock.acquire()
                mm.seek(0)
                data = mm.read(100)
                tagNameFromMmap = data.decode("UTF-8").rstrip("\x00")
                if(tagNameFromMmap==self.tagname):
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
                    if(self.AccessReceived==False):
                        self.ResetCount = memResetCount
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
                    self.AccessReceived=True
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
    ANXRacersMemoryMapClient()
