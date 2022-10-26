
from gym.envs.registration import register
from gym import version
print("using gym = " + version.VERSION)
register(
    id="anxracersgym/ANXRacers-v0",
    entry_point="anxracersgym.envs:ANXRacersEnv"
)
