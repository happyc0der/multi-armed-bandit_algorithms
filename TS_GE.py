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
        
    # Thompson-Sampling Phase
    K = Arm.size()
    Arm_list = [Arms(i*0.1,1) for i in range(0,K)]
    priors = [[1,1] for i in range(0,K)]
    
    probability_of_change = 1-(1/Time_Horizon)**(1/(Time_Horizon**(1/2) - Time_Horizon**(2/5)))
    probability_of_change = random.uniform(probability_of_change,1)
                                                    
    Rewards_List = []
    Time_Step = []
    Regret_List = []
    p = 0
    Max_Episodes = math.sqrt(Time_Horizon)
    e = 0
    while e < Time_Horizon:
        # Thompson Sampling phase
        for t in range(0,Time_Horizon):
            pass 
        p +=1 
        # Broadcast Probing Phase
        # Build the estimate
        flag = False 
        # Checking if change is detected
        
        if (flag):
            # change is detected hence we go to group exploration phase
            pass
            
        


