# Future python file for jod tier arm's implementation for stationary and non-stationary armed bandits
import random 
import numpy as np
class ARMS:
    arm_index = None
    arm_mean = None
    arm_std = None
    Time_Horizon = None

    # sampling obligations
    time_when_first_chosen = None
    time_when_last_chosen = 0

    # 0 if not chosen at t'th time step else 1
    number_of_times_chosen = None
    reward_List = []
    eviction_observed_mean_reward = None
    eviction_gap = None

    def tell_reward(self, time_step):
        # gives the reward for the arm by assuming a normal distribution
        return self.reward_List[time_step]

    def __init__(self, arm_index, arm_mean, arm_std, change,Time_Horizon):
        """
            Initialize the arm with the index, mean and std
        Args:
            arm_index (_type_): index of the arm
            arm_mean (_type_): average expected reward of the arm
            arm_std (_type_): standard deviation of the arm
            change (_type_): 0 if the arm is stationary else 1
            Time_Horizon (_type_): The time horizon for the problem
        """
        self.arm_index = arm_index
        self.arm_mean = arm_mean
        self.arm_std = arm_std
        self.Time_Horizon = Time_Horizon
        self.number_of_times_chosen = [0 for i in range(Time_Horizon+1)]
        # Adding code to make changes to arm_mean k number of times
        # a random number between 0 and time horizon
        # code to make changes to arm_mean k number any number of times.
        if (change == 1):
            # I will randomize the change happening itself, along with when it is happening
            number_of_changes = random.randint(0, 10)
        else:
            self.reward_List = np.random.normal(
                arm_mean, arm_std, Time_Horizon + 1)

    def __str__(self):
        string = "Arm Index: " + \
            str(self.arm_index) + " Arm Mean: " + \
            str(self.arm_mean)+" Arm Std: "+str(self.arm_std)
        return string

    def __repr__(self):
        return "Arm Index: "+str(self.arm_index)

    def update_chosen(self, time):
        if self.time_when_first_chosen is None:
            self.time_when_first_chosen = time
        self.number_of_times_chosen[time] += 1
        self.time_when_last_chosen = time

    def chosen_in_interval(self, start, end):
        return self.number_of_times_chosen[start:end + 1].count(1)

    def mean_rewards_observed(self, start, end):
        # function is inclusive it is simply the average of the observed values
        num = 0
        denom = 0
        flag = False
        for i in range(start, end + 1):
            # print(i)
            if self.number_of_times_chosen[i] == 1:
                flag = True
                num += self.reward_List[i]
                denom += 1
        if (flag == False):
            return 0
        return num / denom

