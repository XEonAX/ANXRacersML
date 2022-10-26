import gym
import anxracersgym
env =  gym.make("anxracersgym/ANXRacers-v0")
terminated, truncated = False, False
# obs,info = env.reset() #uncomment for env checker
obs = env.reset() 
# from gym.utils.env_checker import check_env
# check_env(env.unwrapped) # commented since this will reset the game few times
while not (terminated or truncated):
    act = env.action_space.sample()
    # obs, rew, terminated, truncated, info =  env.step(act) #uncomment for env checker
    obs, rew, terminated, info =  env.step(act)
    print(f"rew:{rew}\tterminated:{terminated}", end="\r")
