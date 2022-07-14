# The upper bound for the reward is going to be max of reward mean of all current arms + 1 and then we divide to get the success rate probability

import numpy as np
import matplotlib.pyplot as plt
import random
import math
import Arms

    
def TS_GE(Arm,Time_Horizon,Delta): # K,T,delta
    """
    Arms : List of arms
    Time_Horizon : Time horizon for which we want to run the algorithm
    Delta : Maximum error allowed in the mean reward of the arms beyond which it gives an error
    """
    
    def super_arms(Arms,n):
        s = {}
        K = len(Arms)
        for k in range(1,n):
            for i in range(1,K+1):
                pass
        
    K = Arm.size()
    # check if K is a power of two or not
    Arm_list = [Arms(i*0.1, 1) for i in range(0, K)]
    priors = [[1,1] for i in range(0,K)] # alpha, beta
    while (~(K and ~(K & (K-1)))):
        K +=1
        Arm_list.append(Arms(-(2<<31), 1))
        priors.append([1,1])
        
    
    upper_bound = 100 # to normalize
    
    
    probability_of_change = 1-(1/Time_Horizon)**(1/(Time_Horizon**(1/2) - Time_Horizon**(2/5)))
    probability_of_change = random.uniform(probability_of_change,1)
                                                    
    Rewards_List = []
    Time_Step = []
    Regret_List = []
    t = 0 # 
    # Max_Episodes = math.sqrt(Time_Horizon)  => Number of episodes
    
        
    
    # Initializing explore then commit phase
    n_etc = 1/(2*Delta**2)*math.log(Time_Horizon) # pl is of the order of ln(T)
    n_etc = (int)(n_etc)
    estimates = [0 for i in range(0,K)]
    count_arms = [0 for i in range(0,K)]
    for i in range(0,K):
        sum = 0;
        temp = Arm[i]
        mean = temp.arm_mean
        for j in range(0,n_etc):
            mean+=np.random.normal(mean,1,1)
        estimate = mean/n_etc    
        estimates.append(estimate)
    
    Length_Episode = (int)(math.sqrt(Time_Horizon))
    # Algo begins
    
    for e in range(0,Time_Horizon,Length_Episode):
        # Thompson Sampling phase
        Length_TS = (int)(Length_Episode - Time_Horizon**(2/5))
        for t_ts in range(0,Length_TS):
            max_index = np.argmax(np.random.beta(priors[i][0],priors[i][1]) for i in range(0,K))
            t+=1
            reward = np.random.normal(Arm_list[max_index].arm_mean,1,1)
            Rewards_List.append(reward)
            Time_Step.append(t)
            best_expected_reward = max([i.arm_mean for i in Arm_list])
            Regret_List.append(best_expected_reward - reward)
            success_event_probablity = reward/upper_bound
            
            R_value = np.bernoulli(success_event_probablity)
            priors[max_index][0] += 1-R_value
            priors[max_index][1] += R_value
            count_arms[max_index] +=1
            
         
        # Broadcast Probing Phase
        # Build the estimate
        flag = False 
        # Checking if change is detected
        
        if (flag):
            # change is detected hence we go to group exploration phase
            pass
            
        


