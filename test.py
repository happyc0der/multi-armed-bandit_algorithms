# import random

# probability = 0.6
# count = 0
# mean = 0
# for i in range(1000):
#     count = 0
#     for i in range(100):
#         if (random.random()<probability):
#             count+=1
#     mean += count/100

# print(mean/1000)\

# checking if object iteration is viable in python

# class obj:
#     x = None
#     y = None
#     def __init__(self,x,y):
#         self.x = x
#         self.y = y

#     def print(self):
#         print(self.x,self.y)

# obj_list = []
# for i in range(10):
#     obj1 = obj(i,i)
#     obj_list.append(obj1)
# print(obj_list)

# for i in obj_list:
#     i.print()
#     print(i.x)

from ctypes import sizeof


class obj:
    index = None
    change_to_detect = 0.5
    first_sampled = None
    number_of_samplings = None

    def __init__(self, index):
        self.index = index

    def return_obligations(self):
        return [self.change_to_detect, self.number_of_samplings, self.first_sampled]

    def __str__(self):
        return "I hate your mom " + str(self.index)
    def __repr__(self):
        return "I hate your dad" + str(self.index)

# god_dict = {}
# for k in range(0,5):
#     arm = obj(k)
#     god_dict[arm] = []
#     god_dict[arm].append(arm.return_obligations())
#     god_dict[arm].append(arm.return_obligations())

# print(god_dict)
# print(2**(-1))
# def check(lst):
#     for i in lst:
#         if (i%2==0):
#             lst.remove(i)

# lst1 = [i*i for i in range(10)]
# lst2 = [i for i in range(10)]
# for i in lst1+lst2:
#     print(i)


# for i in range(1,5):
#     print(i)
# lst = [obj(1)]

# print(lst)
# a = 2
# print(a**2)
# print(a)
# import random
# import numpy as np
# Upper = 100

# print(bin(10))
# # one hot encode

# K = 2
# while (~(K and ~(K & (K-1)))):
#     K += 1
# print(K)

# lst = [i+1 for i in range(1024)]
# for i in range(0,1024,32):
#     print(lst[i])
    
k = 2
number = 3
# detect whether number has 1 on it's kth place or not
if (number & (1<<k)):
    print(number, "has 1 on it's", k, "th place")
    print("Yes")
else :
    print("No")
import numpy as np
theta = np.random.beta(1,1)

print(theta)            
   