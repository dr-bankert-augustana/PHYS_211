import numpy as np

vi = 8
vf = 3
ti = 2
tf = 14
answer_1 = (vf - vi) / (tf - ti)

answer_1 = np.round(answer_1, 3)
if (acceleration == answer_1):

  print("Correct!")

else:

  print("Incorrect!")
