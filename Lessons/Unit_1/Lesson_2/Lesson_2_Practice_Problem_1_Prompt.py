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
## Set Question List:                                                                             ##
##================================================================================================##

question_list = [
  {"prompt"   : """Which statement best describes average acceleration?""", 
   "solution" : "The rate at which an object's velocity changes over a time interval.", 
   "choices"  : ["The total distance traveled divided by the total time.", 
                  "The rate at which an object's position changes.", 
                  "The rate at which an object's velocity changes over a time interval.", 
                  "The force acting on an object divided by its mass."
                ]
   },
                 
  {"prompt"   : """Which of the following situations corresponds to an object having zero average acceleration 
  during a time interval?""",
   "solution" : "The object moves in a straight line at a constant velocity.",
   "choices"  : ["The object moves in a straight line at a constant velocity.", 
                 "The object speeds up while moving in a straight line.",
                 "The object slows down while moving in a straight line.",
                 "The object changes direction while maintaining a constant speed."]
   },
  
  {"prompt"   : """An object's speed remains constant, but its direction changes. Which statement is most true?""",
   "solution" : "The object has experienced a change in velocity and therefore has a nonzero average acceleration.",
   "choices"  : ["The object's average acceleration must be zero.", 
                 "The object has experienced a change in velocity and therefore has a nonzero average acceleration.",
                 "The object cannot be accelerating because its speed is constant.",
                 "The object's average acceleration depends only on the distance traveled."]
   },
  
  {"prompt"   : """Which of the following changes would produce a negative average acceleration in the positive direction?""",
   "solution" : "The object's velocity changes from +10 m/s to +4 m/s.",
   "choices"  : ["The object's velocity changes from +5 m/s to +10 m/s.", 
                 "The object's velocity changes from -8 m/s to -2 m/s.",
                 "The object's velocity changes from +10 m/s to +4 m/s.",
                 "The object's velocity changes from -4 m/s to +4 m/s."]
   },
  {"prompt"   : """Which statement about average acceleration is always true?""",
   "solution" : "It is determined by the change in velocity and the elapsed time.",
   "choices"  : ["It points in the same direction as the object's velocity.", 
                 "It depends only on the initial velocity.",
                 "It is determined by the change in velocity and the elapsed time.",
                 "It is zero whenever the object's speed is constant."]
   },
]

##================================================================================================##
## Choose Random Question:                                                                        ##
##================================================================================================##

question = rd.choice(question_list)

##================================================================================================##
## Set the Parameters:                                                                            ##
##================================================================================================##

prompt = question["prompt"]

solution = question["solution"]

choices = rd.sample(question["choices"], len(question["choices"]))

choice_headers = ["A.", "B.", "C.", "D."]

problem_1_solution = choice_headers[choices.index(solution)][:-1]

##================================================================================================##
## Print the Prompt and Choices:                                                                  ##
##================================================================================================##

print(prompt)
print()

for choice in choices:

  print(choice_headers[choices.index(choice)], choice)

print()
print("The correct answer is", problem_1_solution)
