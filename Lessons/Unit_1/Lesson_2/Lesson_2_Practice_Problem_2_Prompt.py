##================================================================================================##
## Import Libraries:                                                                              ##
##================================================================================================##

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import random as rd

##================================================================================================##
## Set the Seed:                                                                                  ##
##================================================================================================##

try: seed

except NameError: seed = -1

if (seed == -1): rd.seed(time.time())

else: rd.seed(int(seed))

##================================================================================================##
## Function:  plot_data                                                                           ##
##                                                                                                ##
## Purpose:   Create a scatterplot with optional model overlays and error bands                   ##
##                                                                                                ##
## Input(s):  data          - List of data points [x_data, y_data]                                ##
##            title         - Graph title                                                         ##
##            axis_labels   - Override axis labels [x_label, y_label] (optional)                  ##
##            model_list    - List of model predictions to overlay (optional)                     ##
##            color_list    - Colors for each model line (optional)                               ##
##            label_list    - Labels for each model line (optional)                               ##
##            error_display - Show +/- error band around first model (default is False)           ##
##            error         - Error value for shaded band                                         ##
##                                                                                                ##
## Output(s): graph       - Matplotlib axes object, can be used for overplotting                  ##
##================================================================================================##

def plot_data(data, title, axis_labels = [], model_list = [], color_list = [], label_list = [],
              error_display = False, error = 0):

  # Create the Matplotlib figure:

  figure = plt.figure(figsize = (12, 9))

  # Add a graph to the figure:

  graph = figure.add_subplot()

  # Set the graph background Color:

  graph.set_facecolor('lightcyan')

  # Create a scatterplot of the data:

  #sns.scatterplot(x = data[0], y = data[1], ax = graph)
  sns.lineplot(x = data[0], y = data[1], ax = graph)

  # Overlay model predictions:

  for i in range(0, len(model_list)):

    graph.plot(data[0], model_list[i], color = color_list[i], label = label_list[i])

  # Set the graph title:

  graph.set_title(title, fontsize = 20)

  # Set the x_label and y_label:

  if (axis_labels != []):

    graph.set_xlabel(axis_labels[0], fontsize = 14)

    graph.set_ylabel(axis_labels[1], fontsize = 14)

  # Apply a grid to the graph:

  graph.grid(which = 'both')

  # Adjust the x-axis scale of the graph:

  graph.autoscale(enable = True, axis = 'x', tight = False)

  # Adjust the y-axis scale of the graph:

  graph.autoscale(enable = True, axis = 'y', tight = False)

  # If requested, show the +/- error bounds:

  if ((error_display == True) and model_list != []):

    model_plus_error  = model_list[0] + error
    model_minus_error = model_list[0] - error

    error_df = pd.DataFrame({
        'X-Data': data[0],
        'Model+Error': model_plus_error,
        'Model-Error': model_minus_error
    }).sort_values(by="X-Data")

    graph.fill_between(error_df['X-Data'], error_df['Model+Error'], error_df['Model-Error'],
                       alpha = 0.5, color = (0.6, 0.6, 0.6), label = "Error Bounds")

  # Add the graph legend

  if (label_list != []): graph.legend()

  # Return the graph object

  return graph

##================================================================================================##
## Setup the Simulation:                                                                          ##
##================================================================================================##

##------------------------------------------------------------------------------------------------##
## Set the Number of Data Points:                                                                 ##
##------------------------------------------------------------------------------------------------##

n_steps = 100

##------------------------------------------------------------------------------------------------##
## Set the Time Step:                                                                             ##
##------------------------------------------------------------------------------------------------##

dt = 0.1

##------------------------------------------------------------------------------------------------##
## Set the Object's Initital Velocity:                                                            ##
##------------------------------------------------------------------------------------------------##

x_min = -20.0
x_max =  20.0

v_min = -10.0
v_max =  10.0

position = np.array([rd.uniform(x_min, x_max), 0])

##------------------------------------------------------------------------------------------------##
## Set the Object's Acceleration:                                                                 ##
##------------------------------------------------------------------------------------------------##

velocity = np.array([rd.uniform(v_min, v_max), 0.0])

problem_2_solution_value = velocity

##------------------------------------------------------------------------------------------------##
## Create a List to Store the Time History:                                                       ##
##------------------------------------------------------------------------------------------------##

time_history = []

time_history.append(0)

##------------------------------------------------------------------------------------------------##
## Create a List to Store the Object's Velocity History:                                          ##
##------------------------------------------------------------------------------------------------##

position_history = []

position_history.append([position[0], position[1]])

##================================================================================================##
## Run the Simulation and Populate the Position History:                                          ##
##================================================================================================##

for i in range(n_steps):

  ##----------------------------------------------------------------------------------------------##
  ## Set the velocity for each time:                                                              ##
  ##----------------------------------------------------------------------------------------------##

  position = position + velocity * dt

  position_history.append(position)

  ##----------------------------------------------------------------------------------------------##
  ## Store the Time in the History:                                                               ##
  ##----------------------------------------------------------------------------------------------##
  
  time_history.append(time_history[-1] + dt)

##================================================================================================##
## Load the History into a DataFrame:                                                             ##
##================================================================================================##

history_df = pd.DataFrame(
    {
        "Time (s)": time_history,
        "Position X (m)": [x[0] for x in position_history],
        "Position Y (m)": [x[1] for x in position_history],
    }
)

##================================================================================================##
## Clean the Data and Separate Features and Targets:                                              ##
##================================================================================================##

# Remove any rows missing data:

cleaned_data = history_df.dropna()

# Identify the feature data:

X = cleaned_data["Time (s)"]

# Identify the target data:

y = cleaned_data["Position X (m)"]

##================================================================================================##
## Create a Plot of the Data:                                                                     ##
##================================================================================================##

# Set the title of the plot:

title = "Position vs Time"

# Set the x-axis and y-axis labels:

x_label = "Time (s)"
y_label = "Position (m)"

# Create a scatterplot of the feature data vs the target data:

graph_1 = plot_data([X.values, y.values], title, [x_label, y_label])

acceleration = rd.random()
