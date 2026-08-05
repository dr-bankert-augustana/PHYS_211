vi = 8
vf = 3
ti = 2
tf = 14
acceleration = (vf - vi) / (tf - ti)

acceleration = np.round(acceleration, 3)
if (acceleration == answer_1):

  print("Correct!")

elif (np.abs(acceleration - answer_1) / acceleration

else:

  print("Incorrect!")
