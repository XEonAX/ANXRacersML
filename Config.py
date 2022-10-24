from rtgym import DEFAULT_CONFIG_DICT

from ANXRacersInterface import ANXRacersInterface

my_config = DEFAULT_CONFIG_DICT
my_config["interface"] = ANXRacersInterface

my_config["time_step_duration"] = 0.05
my_config["start_obs_capture"] = 0.05
my_config["time_step_timeout_factor"] = 1.0
my_config["ep_max_length"] = 100
my_config["act_buf_len"] = 4
my_config["reset_act_buf"] = False