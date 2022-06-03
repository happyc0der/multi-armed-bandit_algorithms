import numpy as np
import math
import matplotlib.pyplot as plt
import random
import sys
# The implementation fails for large values of Time_Horizon due to memory constraints, in such a case,
# resort to simply running the algorithm for small Time_Horizon multiple times and average the results.
# Possible solutions to this in the future
# Better implementations of the arms themselves is needed, for stationary and non-stationary experiments
"""
1. Make the functions for start new episode and next time step iterative instead of recursive
"""
# I HAVE TAKEN BASE 10 LOGARITHM EVERYWHERE KEEP THIS IN MIND IF IT HAS TO BE CHANGED IN FUTURE
Time_Horizon = 1000
Arm_List = []
debug = 0 # Set to 1 if you want to debug
graph = 1 # Set to 1 if you want to see the graph in the end

class ARMS:
    arm_index = None
    arm_mean = None
    arm_std = None

    # sampling obligations
    time_when_first_chosen = None
    time_when_last_chosen = 0

    # 0 if not chosen at t'th time step else 1
    number_of_times_chosen = [0 for i in range(Time_Horizon +1)]
    reward_List = []
    eviction_observed_mean_reward = None
    eviction_gap = None

    def tell_reward(self, time_step):
        # gives the reward for the arm by assuming a normal distribution
        return self.reward_List[time_step]

    def __init__(self, arm_index, arm_mean, arm_std,change):
        self.arm_index = arm_index
        self.arm_mean = arm_mean
        self.arm_std = arm_std
        self.number_of_times_chosen = [0 for i in range(Time_Horizon+1)]
        # Adding code to make changes to arm_mean k number of times
        # a random number between 0 and time horizon
        # code to make changes to arm_mean k number any number of times.
        if (change==0):
            # I will randomize the change happening itself, along with when it is happening
            number_of_changes = random.randint(0, 10)
        else:
            self.reward_List = np.random.normal(
                arm_mean, arm_std, Time_Horizon + 1)
        
        

    def __str__(self):
        string = "Arm Index: " + str(self.arm_index) +" Arm Mean: "+str(self.arm_mean)+" Arm Std: "+str(self.arm_std)
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


K = 10  # number of arms
for i in range(0, K):
    mean = 1*i
    std = 1
    index = i  # 0 based indexing for the arms
    arm = ARMS(index, mean, std,1)
    Arm_List.append(arm)


def Check_Bad_Arms(Bad_Arms_Current_Time_Step, Sampling_Obligations_Current_Time_Step, Current_Episode, Time_Step):
    for arms in Bad_Arms_Current_Time_Step:
        i = 1
        change_to_detect = 2 ** (-i)
        Sampling_Obligations_Current_Time_Step[arms] = []
        delta = arms.eviction_gap / 16
        while change_to_detect >= delta:
            probability = change_to_detect * \
                math.sqrt(Current_Episode /
                          (K * Time_Horizon * math.log(Time_Horizon,10)))
            if random.random() < probability:
                Sampling_Obligations_Current_Time_Step[arms].append(
                    [change_to_detect, math.ceil((2 ** (2 * i + 1)) * math.log(Time_Horizon,10)), Time_Step])
            i += 1
            change_to_detect = 2 ** (-i)


def Check_Changes_Of_Good_Arms(Start_Of_Current_Episode, Time_Step, Good_Arms_Current_Time_Step):
    for arm in Good_Arms_Current_Time_Step:
        for s in range(Start_Of_Current_Episode, Time_Step + 1):
            for s1 in range(Start_Of_Current_Episode, Time_Step + 1):
                for s2 in range(s1, Time_Step + 1):
                    # put checks for zeros i.e if we divide by zero then the answer is infinite so it can never be the case so we just continue
                    if (arm.chosen_in_interval(s, Time_Step) == 0 or arm.chosen_in_interval(s1, s2) == 0):
                        continue
                    x = abs(arm.mean_rewards_observed(s, s1) -
                            arm.mean_rewards_observed(s1, s2))
                    y = math.sqrt(2 * math.log(Time_Horizon,10) / arm.chosen_in_interval(s1, s2)) + math.sqrt(
                        2 * math.log(Time_Horizon,10) / arm.chosen_in_interval(s, Time_Step))
                    if x > y:
                        return True  # This condition holds so we must start a new episode
    return False


def Check_Changes_Of_Bad_Arms(Start_Of_Current_Episode, Time_Step, Bad_Arms_Current_Time_Step):
    for arm in Bad_Arms_Current_Time_Step:
        for s in range(Start_Of_Current_Episode, Time_Step + 1):
            x = abs(arm.mean_rewards_observed(s, Time_Step) -   
                    arm.eviction_observed_mean_reward)
            if arm.chosen_in_interval(s, Time_Step) == 0:
                continue
            y = arm.eviction_gap / 4 + \
                math.sqrt(2 * math.log(Time_Horizon,10) /
                          arm.chosen_in_interval(s, Time_Step))
            if x > y:
                return True
    return False


# possible fixes may be to map the timestamp with the type of arms, keep track of what is being removed and where it is being added.
# This can also help in debugging as we can see the categories during each time step separately

def ADSWITCH():
    # declare the functions inside the class to turn this into a module
    global debug,graph
    sys.setrecursionlimit(Time_Horizon + 10000)
    Cumulative_Regret = 0  # sum of regret at each step
    Net_Reward = 0
    Opt_Reward = 0
    # This constant can be found by running the algorithm again and again to see how we achive optimum regret
    Constant_C1 = 0.1

    Current_Episode = 0  # l
    Time_Step = 0  # t
    # t of l
    Good_Arms_Current_Time_Step = []
    Bad_Arms_Current_Time_Step = []
    Good_Arms_Next_Time_Step = []
    Bad_Arms_Next_Time_Step = []
    Sampling_Obligations_Current_Time_Step = {}
    Sampling_Obligations_Next_Time_Step = {}

    # To plot the regret with time horizon
    Reward_List = []
    Regret_List = []
    Opt_List = []
    Time_Steps = []

    def Start_New_Episode():
        nonlocal Current_Episode, Time_Step, Good_Arms_Current_Time_Step, Bad_Arms_Current_Time_Step, Good_Arms_Next_Time_Step, Bad_Arms_Next_Time_Step, Sampling_Obligations_Current_Time_Step, Sampling_Obligations_Next_Time_Step, Reward_List, Regret_List, Opt_List, Time_Steps
        nonlocal Cumulative_Regret, Net_Reward, Constant_C1,Opt_Reward
        global debug,graph 
        if Time_Step > Time_Horizon:
            return
        Current_Episode += 1
        Start_Of_Current_Episode = Time_Step + 1
       
        # index, change, n , s(time when sampling began # need to check whether this will be updated or not)
        Good_Arms_Current_Time_Step = []
        Bad_Arms_Current_Time_Step = []
        Good_Arms_Next_Time_Step = []
        Bad_Arms_Next_Time_Step = []
        Sampling_Obligations_Current_Time_Step = {}
        Sampling_Obligations_Next_Time_Step = {}

        for k in Arm_List:
            k.eviction_gap = None
            k.eviction_observed_mean_reward = None
            Good_Arms_Current_Time_Step.append(k)
        Start_Of_Current_Episode = Time_Step + 1

        def nextTimeStep():
            nonlocal Time_Step, Good_Arms_Current_Time_Step, Bad_Arms_Current_Time_Step, Good_Arms_Next_Time_Step, Bad_Arms_Next_Time_Step, Sampling_Obligations_Current_Time_Step, Sampling_Obligations_Next_Time_Step, Current_Episode, Reward_List, Regret_List, Opt_List, Time_Steps
            nonlocal Cumulative_Regret, Net_Reward, Constant_C1,Opt_Reward
            global debug,graph
            Time_Step += 1
            
            if Time_Step > Time_Horizon:
                return
             # update bad arms
            for k in Bad_Arms_Current_Time_Step:
                Bad_Arms_Next_Time_Step.append(k)
                Sampling_Obligations_Next_Time_Step[k] = []
            
            # bad arm check
            Check_Bad_Arms(Bad_Arms_Current_Time_Step, Sampling_Obligations_Current_Time_Step, Current_Episode,
                           Time_Step)

            # select an arm
            Time = 10000000000000000000000000000000000000000000000000000000
            Reward_local = 0
            Chosen_Arm = None
            # select least recently selected arm
            Temp_List = Bad_Arms_Current_Time_Step + Good_Arms_Current_Time_Step
            for arm in Temp_List:

                if arm in Bad_Arms_Current_Time_Step and Sampling_Obligations_Current_Time_Step[arm] == []:
                    continue

                if arm.time_when_last_chosen < Time:
                    Time = arm.time_when_last_chosen
                    Chosen_Arm = arm
                
            Reward_local = Chosen_Arm.tell_reward(Time_Step)
            # uhuhuhu = str(Chosen_Arm)
            # print(uhuhuhu,"chosen at time step",Time_Step)
            Chosen_Arm.update_chosen(Time_Step)
            Net_Reward += Reward_local
            if (graph):
                Reward_List.append(Reward_local)

            # finding regret
            max_reward = -11111111111111111111111111111111111111111111111
            for k in Arm_List:
                max_reward = max(max_reward, k.arm_mean)
            if (graph):
                Regret_List.append(max_reward - Reward_local)
                Opt_List.append(max_reward)
                Time_Steps.append(Time_Step)
            
            Opt_Reward += max_reward 
            Cumulative_Regret += max_reward - Reward_local

            # check for changes of good arm
            if Check_Changes_Of_Good_Arms(Start_Of_Current_Episode, Time_Step, Good_Arms_Current_Time_Step):
                return Start_New_Episode()

            # check for changes of bad arm
            if Check_Changes_Of_Bad_Arms(Start_Of_Current_Episode, Time_Step, Bad_Arms_Current_Time_Step):
                return Start_New_Episode()
            for i in Sampling_Obligations_Current_Time_Step:  # only bad arms can have sampling obligations
                # check which arm has the same arm index first
                values = Sampling_Obligations_Current_Time_Step[i]
                for k in values:
                    n = k[1]
                    s = k[2]
                    # there is something wrong with this line need to fix it asap, then move to other more important things(damn I love this)
                    if i.chosen_in_interval(s, Time_Step) < n:
                        Bad_Arms_Next_Time_Step.append(i)
                        Sampling_Obligations_Next_Time_Step[i].append(
                            k.copy())

            # evict arms from good
            for i in range(0, K):
                random_small_value = -100000000000000000000000000000000000000000
                arms_to_compare = []  # a' and a
                values_to_store = []  # left and s
                for a_prime in Good_Arms_Current_Time_Step:
                    for a in Good_Arms_Current_Time_Step:
                        for s in range(Start_Of_Current_Episode, Time_Step + 1):
                            if a.chosen_in_interval(s, Time_Step) < 2:
                                continue
                            left = a_prime.mean_rewards_observed(
                                s, Time_Step) - a.mean_rewards_observed(s, Time_Step)
                            right = math.sqrt(
                                Constant_C1 * math.log(Time_Horizon,10) / (a.chosen_in_interval(s, Time_Step) - 1))
                            if left > right:
                                if left - right > random_small_value:
                                    random_small_value = left - right
                                    arms_to_compare = [a_prime, a]
                                    values_to_store = [left, s]
                if arms_to_compare != []:
                    a = arms_to_compare[1]
                    Good_Arms_Current_Time_Step.remove(a)
                    Bad_Arms_Next_Time_Step.append(a)
                    a.eviction_observed_mean_reward = a.mean_rewards_observed(
                        values_to_store[1], Time_Step)
                    a.eviction_gap = values_to_store[0]
                    Sampling_Obligations_Next_Time_Step[a] = []

            for a in Bad_Arms_Current_Time_Step:
                if a not in Bad_Arms_Next_Time_Step:
                    Bad_Arms_Next_Time_Step.append(a)

            Good_Arms_Next_Time_Step = list(
                set(Arm_List) - set(Bad_Arms_Next_Time_Step))
           
            if (debug==1):
                # debugging statements
                print("Good arms: ", Good_Arms_Current_Time_Step)
                print("Bad arms: ", Bad_Arms_Current_Time_Step)
                # print the sampling for current and next
                print("Sampling obligations for current time step: ",Sampling_Obligations_Current_Time_Step)
                print("Sampling obligations for next time step: ",Sampling_Obligations_Next_Time_Step)
                
            
            # swap the arm lists so that next becomes current and next becomes empty
            Good_Arms_Current_Time_Step = Good_Arms_Next_Time_Step.copy()
            Good_Arms_Next_Time_Step = []
            Bad_Arms_Current_Time_Step = Bad_Arms_Next_Time_Step.copy()
            Bad_Arms_Next_Time_Step = []
            Sampling_Obligations_Current_Time_Step = Sampling_Obligations_Next_Time_Step.copy()
            Sampling_Obligations_Next_Time_Step = {}

            return nextTimeStep()

        return nextTimeStep()

    Start_New_Episode()
    # result of the simulation :)
    print("Net Regret(sum of regret at each step) : ", Cumulative_Regret)
    print("Net Reward : ", Net_Reward)
    print("Best Possible Reward", Opt_Reward)
    if (graph):
        plt.scatter(Time_Steps, Regret_List, color='red')
        plt.scatter(Time_Steps, Reward_List, color='blue')
        plt.scatter(Time_Steps, Opt_List, color='green')
        plt.show()


ADSWITCH()
if (debug):
    for arms in Arm_List:
        print(arms.mean_rewards_observed(0, Time_Horizon),arms.arm_mean)
        print(arms.chosen_in_interval(0, Time_Horizon))
        print(arms.number_of_times_chosen)
