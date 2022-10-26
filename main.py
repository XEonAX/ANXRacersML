import gym
import anxracersgym
env =  gym.make("anxracersgym/ANXRacers-v0")
terminated, truncated = False, False
obs = env.reset()
from gym.utils.env_checker import check_env
check_env(env.unwrapped)
while not (terminated or truncated):
    act = env.action_space.sample()
    obs, rew, terminated, info =  env.step(act)
    print(f"rew:{rew}\nterminated:{terminated}\ttruncated:{truncated}")
