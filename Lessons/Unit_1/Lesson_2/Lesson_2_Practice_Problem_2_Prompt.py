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

v_min = -20.0
v_max =  20.0
t_min =   0.0
t_max =  30.0
round =     2

vi = np.round(rd.uniform(v_min, v_max), round)
vf = np.round(rd.uniform(v_min, v_max), round)
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

problem_2_solution_value = (vf - vi) / (tf - ti)

problem_2_solution_units = ["m/s^2", "meters per second squared", "mpss"]

##================================================================================================##
## Create the Word Problem:                                                                       ##
##================================================================================================##

problem_prompt = f"""
A cart travels along the positive direction. At time {ti} s, its velocity is {vi} m/s. At {tf} s, 
the cart's velocity has changed to {vf} m/s. Calculate the average acceleration of the cart between 
these two measurements.
"""

print(problem_prompt)
