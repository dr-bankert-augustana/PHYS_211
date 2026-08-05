##=============================================================================================##
## Import Libraries:                                                                           ##
##=============================================================================================##

import numpy as np

##=============================================================================================##
## Establish Possible Outcomes:                                                                ##
##=============================================================================================##

outcome_right         = "Correct!"
outcome_close         = "Almost, check for rounding errors!"
outcome_neg           = "Incorrect, check minus signs!"
outcome_neg_close     = "Incorrect, check for rounding errors and minus signs!"
outcome_inv           = "Incorrect, check inverse!"
outcome_inv_close     = "Incorrect, check for rounding errors and inverse!"
outcome_neg_inv       = "Incorrect, check for inverse and minus signs!"
outcome_neg_inv_close = "Incorrect, check for rounding errors, inverse, and minus signs!"
outcome_wrong         = "Incorrect!"

# outcome_custom_1 = ""

##=============================================================================================##
## Establish Tolerances:                                                                       ##
##=============================================================================================##

right_tolerance = 0.01
close_tolerance = 0.1

##=============================================================================================##
## Set Problem Parameters:                                                                     ##
##=============================================================================================##

vi = 8
vf = 3
ti = 2
tf = 14

##=============================================================================================##
## Solve Problem:                                                                              ##
##=============================================================================================##

solution = (vf - vi) / (tf - ti)

##=============================================================================================##
## Get Absolute Percent Difference of Student Answer to Solution:                              ##
##=============================================================================================##

abs_percent_error = np.abs((solution - answer_1) / solution)

neg_percent_error = np.abs((solution - (-answer_1)) / solution)

inv_percent_error = np.abs((solution - (1/answer_1)) / (solution))

neg_inv_percent_error = np.abs((solution - (-1/answer_1)) / (solution))

##=============================================================================================##
## Compare Percent Error to Tolerances:                                                        ##
##=============================================================================================##

##---------------------------------------------------------------------------------------------##
## Check the Right Tolerance:                                                                  ##
##---------------------------------------------------------------------------------------------##

if (abs_percent_error <= right_tolerance): outcome = outcome_right

##---------------------------------------------------------------------------------------------##
## Check the Close Tolerance:                                                                  ##
##---------------------------------------------------------------------------------------------##

elif (abs_percent_error <= close_tolerance): outcome = outcome_close

##---------------------------------------------------------------------------------------------##
## Check the Answer Negative for Right Tolerance:                                              ##
##---------------------------------------------------------------------------------------------##

elif (neg_percent_error <= right_tolerance): outcome = outcome_neg

##---------------------------------------------------------------------------------------------##
## Check the Answer Negative for Close Tolerance:                                              ##
##---------------------------------------------------------------------------------------------##

elif (neg_percent_error <= close_tolerance): outcome = outcome_neg_close

##---------------------------------------------------------------------------------------------##
## Check the Answer Inverse for Right Tolerance:                                               ##
##---------------------------------------------------------------------------------------------##

elif (inv_percent_error <= right_tolerance): outcome = outcome_inv

##---------------------------------------------------------------------------------------------##
## Check the Answer Inverse for Close Tolerance:                                               ##
##---------------------------------------------------------------------------------------------##

elif (inv_percent_error <= close_tolerance): outcome = outcome_inv_close

##---------------------------------------------------------------------------------------------##
## Check the Answer Negative Inverse for Right Tolerance:                                      ##
##---------------------------------------------------------------------------------------------##

elif (neg_inv_percent_error <= right_tolerance): outcome = outcome_neg_inv

##---------------------------------------------------------------------------------------------##
## Check the Answer Negative Inverse for Close Tolerance:                                      ##
##---------------------------------------------------------------------------------------------##

elif (neg_inv_percent_error <= close_tolerance): outcome = outcome_neg_inv_close

##---------------------------------------------------------------------------------------------##
## Check for Likely Pitfall Answers:                                                           ##
##---------------------------------------------------------------------------------------------##

# Put Custom Outcomes Here

##---------------------------------------------------------------------------------------------##
## Catch-All Incorrect:                                                                        ##
##---------------------------------------------------------------------------------------------##

else: outcome = outcome_wrong

##=============================================================================================##
## Display the Outcome:                                                                        ##
##=============================================================================================##

print(outcome)

if (outcome != outcome_right): print("Try Again!")
