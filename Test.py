import gym
from Config import my_config
env = gym.make("real-time-gym-v0", config=my_config)
terminated, truncated = False, False
obs, info = env.reset()
while not (terminated or truncated):
    act = env.action_space.sample()
    obs, rew, terminated, truncated, info =  env.step(act)
    print(f"rew:{rew}\nterminated:{terminated}\ttruncated:{truncated}")