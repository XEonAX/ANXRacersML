from stable_baselines3 import SAC

import anxracersgym

model = SAC(
    "MlpPolicy",
    "anxracersgym/ANXRacers-v0",
    verbose=1,
    tensorboard_log="./sac_anxracers_tensorboard/",
)
model.learn(total_timesteps=10000, log_interval=4)
model.save("sac_racers")
