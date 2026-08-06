##================================================================================================##
## Import Libraries:                                                                              ##
##================================================================================================##
import time

import numpy as np
import random as rd

##================================================================================================##
## Set the Seed:                                                                                  ##
##================================================================================================##

try: seed

except NameError: seed = -1

if (seed == -1): rd.seed(time.time())

else: rd.seed(int(seed))

##================================================================================================##
## Set Problem Parameters:                                                                        ##
##================================================================================================##

a_min = -10.0
a_max =  10.0
v_min = -20.0
v_max =  20.0
t_min =   0.0
t_max =  30.0
round =     2

a  = np.round(rd.uniform(a_min, a_max), round)
vi = np.round(rd.uniform(v_min, v_max), round)
ti = np.round(rd.uniform(t_min, t_max), round)
tf = np.round(rd.uniform(t_min, t_max), round)

##------------------------------------------------------------------------------------------------##
## Ensure that the Final Time is Greater than the Initial Time:                                   ##
##------------------------------------------------------------------------------------------------##

swap = 0.0

if (ti > tf): 
  
  swap = tf
  tf   = ti
  ti   = swap

##================================================================================================##
## Solve Problem:                                                                                 ##
##================================================================================================##

problem_3_solution_value = vi + a * (tf - ti)

problem_3_solution_units = ["m/s", "meters per second", "mps"]

##================================================================================================##
## Create the Word Problem:                                                                       ##
##================================================================================================##

problem_prompt = f"""
A car travels along the positive direction. At time {ti} s, its velocity is {vi} m/s. The car is 
moving at a constant rate of acceleration {a} m/s^2 in the positive direction. Calculate the velocity
of the car at {tf} s.
"""

print(problem_prompt)
