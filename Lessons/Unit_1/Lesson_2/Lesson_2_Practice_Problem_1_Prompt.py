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

x_min = -10.0
x_max =  40.0
t_min =   0.0
t_max =  20.0
round =     2

xi = np.round(rd.uniform(x_min, x_max), round)
xf = np.round(rd.uniform(x_min, x_max), round)
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

problem_1_solution_value = (xf - xi) / (tf - ti)

problem_1_solution_units = ["m/s", "meters per second", "mps"]

##================================================================================================##
## Create the Word Problem:                                                                       ##
##================================================================================================##

problem_prompt = f"""
An object moves in the positive direction. At time {ti} s, the object's position is {xi} m. At {tf} s, 
the object's position has changed to {xf} m. Calculate the average velocity of the object between 
these two measurements.
"""

print(problem_prompt)
