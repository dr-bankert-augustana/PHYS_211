##================================================================================================##
##                                                                                                ##
## Physics Problem Solvers:                                                                       ##
##                                                                                                ##
##================================================================================================##

##================================================================================================##
## I) Problem Solver Functions:                                                                   ##
##================================================================================================##

##================================================================================================##
## Function:    solve_1d_average_velocity                                                         ##
##                                                                                                ##
## Description: Solve 1D average velocity problems.                                               ##
##================================================================================================##

def solve_1d_average_velocity(values):

    ##--------------------------------------------------------------------------------------------##
    ## Check for Required Variables for this Solver:                                              ##
    ##--------------------------------------------------------------------------------------------##

    required = ("ti", "tf", "xi", "xf")

    missing = [name for name in required if name not in values]

    if missing: raise ValueError(f"Missing values required for this problem type: {missing}")

    ##--------------------------------------------------------------------------------------------##
    ## Ensure Divide By Zero is Avoided:                                                          ##
    ##--------------------------------------------------------------------------------------------##

    delta_t = values["tf"] - values["ti"]

    if abs(delta_t) < 1e-12:
      
      raise ValueError("Time interval is zero; cannot calculate average velocity.")

    ##--------------------------------------------------------------------------------------------##
    ## Set the Solution:                                                                          ##
    ##--------------------------------------------------------------------------------------------##

    solution_value = (values["xf"] - values["xi"]) / delta_t

    solution_units = ["m/s", "meters per second", "mps"]

    ##--------------------------------------------------------------------------------------------##
    ## Return the Solution Value and Units:                                                       ##
    ##--------------------------------------------------------------------------------------------##

    return solution_value, solution_units

##================================================================================================##
## Function:    solve_1d_average_acceleration                                                    ##
##                                                                                                ##
## Description: Solve 1D average acceleration problems.                                           ##
##================================================================================================##

def solve_1d_average_acceleration(values):

    ##--------------------------------------------------------------------------------------------##
    ## Check for Required Variables for this Solver:                                              ##
    ##--------------------------------------------------------------------------------------------##

    required = ("ti", "tf", "vi", "vf")

    missing = [name for name in required if name not in values]

    if missing: raise ValueError(f"Missing values required for this problem type: {missing}")

    ##--------------------------------------------------------------------------------------------##
    ## Ensure Divide By Zero is Avoided:                                                          ##
    ##--------------------------------------------------------------------------------------------##

    delta_t = values["tf"] - values["ti"]

    if abs(delta_t) < 1e-12:
      
      raise ValueError("Time interval is zero; cannot calculate average acceleration.")

    ##--------------------------------------------------------------------------------------------##
    ## Set the Solution:                                                                          ##
    ##--------------------------------------------------------------------------------------------##

    solution_value = (values["vf"] - values["vi"]) / delta_t

    solution_units = ["m/s^2", "meters per second squared", "mps2", "mpss"]

    ##--------------------------------------------------------------------------------------------##
    ## Return the Solution Value and Units:                                                       ##
    ##--------------------------------------------------------------------------------------------##

    return solution_value, solution_units

##================================================================================================##
## Function:    solve_1d_motion_with_constant_velocity_v1                                         ##
##                                                                                                ##
## Description: Solve 1D average velocity problems (for final position).                          ##
##================================================================================================##

def solve_1d_motion_with_constant_velocity_v1(values):

    ##--------------------------------------------------------------------------------------------##
    ## Check for Required Variables for this Solver:                                              ##
    ##--------------------------------------------------------------------------------------------##

    required = ("ti", "tf", "xi", "v")

    missing = [name for name in required if name not in values]

    if missing: raise ValueError(f"Missing values required for this problem type: {missing}")

    ##--------------------------------------------------------------------------------------------##
    ## Set the Solution:                                                                          ##
    ##--------------------------------------------------------------------------------------------##

    delta_t = values["tf"] - values["ti"]

    solution_value = values["v"] * delta_t + values["xi"]

    solution_units = ["m", "meters"]

    ##--------------------------------------------------------------------------------------------##
    ## Return the Solution Value and Units:                                                       ##
    ##--------------------------------------------------------------------------------------------##

    return solution_value, solution_units

##================================================================================================##
## Function:    solve_1d_motion_with_constant_velocity_v2                                         ##
##                                                                                                ##
## Description: Solve 1D average velocity problems (for final time).                              ##
##================================================================================================##

def solve_1d_motion_with_constant_velocity_v2(values):

    ##--------------------------------------------------------------------------------------------##
    ## Check for Required Variables for this Solver:                                              ##
    ##--------------------------------------------------------------------------------------------##

    required = ("ti", "xi", "xf", "v")

    missing = [name for name in required if name not in values]

    if missing: raise ValueError(f"Missing values required for this problem type: {missing}")

    ##--------------------------------------------------------------------------------------------##
    ## Set the Solution:                                                                          ##
    ##--------------------------------------------------------------------------------------------##

    delta_x = values["xf"] - values["xi"]

    solution_value = delta_x / values["v"] + values["ti"]

    solution_units = ["s", "seconds"]

    ##--------------------------------------------------------------------------------------------##
    ## Return the Solution Value and Units:                                                       ##
    ##--------------------------------------------------------------------------------------------##

    return solution_value, solution_units

##================================================================================================##
## II) Registry of Solvers by Normalized Topic Name:                                              ##
##================================================================================================##

SOLVERS = {
    
    "1d average velocity": solve_1d_average_velocity,
    "1d motion with constant velocity v1": solve_1d_motion_with_constant_velocity_v1,
    "1d motion with constant velocity v2": solve_1d_motion_with_constant_velocity_v2,
    "1d average acceleration": solve_1d_average_acceleration,
    #"1d motion with constant acceleration": solve_1d_motion_with_constant_acceleration_v1,
}

##================================================================================================##
## III) Registry of Variables by Normalized Topic Name:                                           ##
##================================================================================================##

VAR_DICT = {
    
    "1d average velocity": [
        {
          "name": "ti",
          "description": "initial time (in seconds)",
          "example": 2.5,
        },
        {
          "name": "tf",
          "description": "final time (in seconds)",
          "example": 20.8,
        },
        {
          "name": "xi",
          "description": "initial position (in meters)",
          "example": 15.3,
        },
        {
          "name": "xf",
          "description": "final position (in meters)",
          "example": 1063.7,
        },
    ],

    "1d motion with constant velocity v1" : [
        {
          "name": "ti",
          "description": "initial time (in seconds)",
          "example": 2.5,
        },
        {
          "name": "tf",
          "description": "final time (in seconds)",
          "example": 20.8,
        },
        {
          "name": "xi",
          "description": "initial position (in meters)",
          "example": 15.3,
        },
        {
          "name": "v",
          "description": "velocity (in meters per second)",
          "example": 10.7,
        },
    ],

    "1d motion with constant velocity v2" : [
        {
          "name": "ti",
          "description": "initial time (in seconds)",
          "example": 2.5,
        },
        {
          "name": "xi",
          "description": "initial position (in meters)",
          "example": 15.3,
        },
        {
          "name": "xf",
          "description": "final position (in meters)",
          "example": 1063.7,
        },
        {
          "name": "v",
          "description": "velocity (in meters per second)",
          "example": 10.7,
        },
    ],

    "1d average acceleration": [
        {
          "name": "ti",
          "description": "initial time (in seconds)",
          "example": 2.5,
        },
        {
          "name": "tf",
          "description": "final time (in seconds)",
          "example": 20.8,
        },
        {
          "name": "vi",
          "description": "initial velocity (in meters per second)",
          "example": 5.3,
        },
        {
          "name": "vf",
          "description": "final velocity (in meters per second)",
          "example": 63.7,
        },
    ],
}

##================================================================================================##
## III) Registry of Targets by Normalized Topic Name:                                             ##
##================================================================================================##

TAR_DICT = {
    
    "1d average velocity": {
        "name": "v",
        "description": "average velocity (in meters per second)",
        "example": 7.3,
      },

    "1d motion with constant velocity v1" : {
        "name": "xf",
        "description": "final position (in meters)",
        "example": 1063.7,
      },

    "1d motion with constant velocity v2" : {
        "name": "tf",
        "description": "final time (in seconds)",
        "example": 22.5,
      },

    "1d average acceleration" : {
        "name": "a",
        "description": "average acceleration (in meters per second squared)",
        "example": 4.5,
      },
}
