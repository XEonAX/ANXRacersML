
from gym.envs.registration import register

register(
    id="anxracersgym/ANXRacers-v0",
    entry_point="anxracersgym.envs:ANXRacersEnv"
)
