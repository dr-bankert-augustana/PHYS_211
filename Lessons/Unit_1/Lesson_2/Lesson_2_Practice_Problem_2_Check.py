##================================================================================================##
## Import Libraries:                                                                              ##
##================================================================================================##

import sys

import numpy as np

##================================================================================================##
## Establish Possible Outcomes:                                                                   ##
##================================================================================================##

outcome_right         = "Value is Correct!"
outcome_close         = "Value is close, check for rounding errors!"
outcome_neg           = "Value is Incorrect, check minus signs!"
outcome_neg_close     = "Value is Incorrect, check for rounding errors and minus signs!"
outcome_inv           = "Value is Incorrect, check inverse!"
outcome_inv_close     = "Value is Incorrect, check for rounding errors and inverse!"
outcome_neg_inv       = "Value is Incorrect, check for inverse and minus signs!"
outcome_neg_inv_close = "Value is Incorrect, check for rounding errors, inverse, and minus signs!"
outcome_wrong         = "Value is Incorrect!"
outcome_wrong_units   = "Units are Incorrect!"

# outcome_custom_1 = ""

##================================================================================================##
## Establish Tolerances:                                                                          ##
##================================================================================================##

right_tolerance = 0.01
close_tolerance = 0.1

##================================================================================================##
## Wrap Answer Check in a Function:                                                               ##
##================================================================================================##

def check_answer():

  ##==============================================================================================##
  ## Set Problem Solution:                                                                        ##
  ##==============================================================================================##

  if "problem_2_solution_value" not in globals():

    print("You must generate the problem before checking the answer.")

    return
  
  solution_value = problem_2_solution_value
  solution_units = problem_2_solution_units

  ##==============================================================================================##
  ## Set the Student's Answer:                                                                    ##
  ##==============================================================================================##

  if ("answer_2_value" not in globals()) or ("answer_2_units" not in globals()):

    print("You must fully answer the problem before checking the answer.")

    return

  given_value = answer_2_value 
  given_units = answer_2_units

  ##==============================================================================================##
  ## Check that Answer is a Number:                                                               ##
  ##==============================================================================================##

  if isinstance(given_value, str): 

    print("Your answer value must be a number only!")

    return

  ##==============================================================================================##
  ## Get Absolute Percent Difference of Student Answer to Solution:                               ##
  ##==============================================================================================##

  abs_percent_error = np.abs((solution_value - given_value) / solution_value)

  neg_percent_error = np.abs((solution_value - (-given_value)) / solution_value)

  inv_percent_error = np.abs((solution_value - (1 / given_value)) / (solution_value))

  neg_inv_percent_error = np.abs((solution_value - (-1 / given_value)) / (solution_value))

  ##==============================================================================================##
  ## Compare Percent Error to Tolerances:                                                         ##
  ##==============================================================================================##

  ##----------------------------------------------------------------------------------------------##
  ## Check the Right Tolerance:                                                                   ##
  ##----------------------------------------------------------------------------------------------##

  if (abs_percent_error <= right_tolerance): outcome = outcome_right

  ##----------------------------------------------------------------------------------------------##
  ## Check the Close Tolerance:                                                                   ##
  ##----------------------------------------------------------------------------------------------##

  elif (abs_percent_error <= close_tolerance): outcome = outcome_close

  ##----------------------------------------------------------------------------------------------##
  ## Check the Answer Negative for Right Tolerance:                                               ##
  ##----------------------------------------------------------------------------------------------##

  elif (neg_percent_error <= right_tolerance): outcome = outcome_neg

  ##----------------------------------------------------------------------------------------------##
  ## Check the Answer Negative for Close Tolerance:                                               ##
  ##----------------------------------------------------------------------------------------------##

  elif (neg_percent_error <= close_tolerance): outcome = outcome_neg_close

  ##----------------------------------------------------------------------------------------------##
  ## Check the Answer Inverse for Right Tolerance:                                                ##
  ##----------------------------------------------------------------------------------------------##

  elif (inv_percent_error <= right_tolerance): outcome = outcome_inv

  ##----------------------------------------------------------------------------------------------##
  ## Check the Answer Inverse for Close Tolerance:                                                ##
  ##----------------------------------------------------------------------------------------------##

  elif (inv_percent_error <= close_tolerance): outcome = outcome_inv_close

  ##----------------------------------------------------------------------------------------------##
  ## Check the Answer Negative Inverse for Right Tolerance:                                       ##
  ##----------------------------------------------------------------------------------------------##

  elif (neg_inv_percent_error <= right_tolerance): outcome = outcome_neg_inv

  ##----------------------------------------------------------------------------------------------##
  ## Check the Answer Negative Inverse for Close Tolerance:                                       ##
  ##----------------------------------------------------------------------------------------------##

  elif (neg_inv_percent_error <= close_tolerance): outcome = outcome_neg_inv_close

  ##----------------------------------------------------------------------------------------------##
  ## Check for Likely Pitfall Answers:                                                            ##
  ##----------------------------------------------------------------------------------------------##

  # Put Custom Outcomes Here

  ##----------------------------------------------------------------------------------------------##
  ## Catch-All Incorrect:                                                                         ##
  ##----------------------------------------------------------------------------------------------##

  else: outcome = outcome_wrong

  ##==============================================================================================##
  ## Display the Outcome:                                                                         ##
  ##==============================================================================================##

  print(outcome)

  ##==============================================================================================##
  ## Check the Student's Units:                                                                   ##
  ##==============================================================================================##

  if given_units not in solution_units: print ("Units are Incorrect!")

  else: print ("Units are Correct!")

  ##==============================================================================================##
  ## Encourage Student to try again:                                                              ##
  ##==============================================================================================##

  if (outcome != outcome_right) or (given_units not in solution_units): print("Try Again!")

check_answer()
