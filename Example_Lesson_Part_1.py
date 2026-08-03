#@title This cell prepares the program details for us. You do not need to understand it, just run it.

##=============================================================================================##
## Import Python Libraries:                                                                    ##
##=============================================================================================##

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from IPython.display import HTML, display_html
from matplotlib.animation import FuncAnimation

##=============================================================================================##
## Function:  plot_data                                                                        ##
##                                                                                             ##
## Purpose:   Create a scatterplot with optional model overlays and error bands                ##
##                                                                                             ##
## Input(s):  data          - List of data points [x_data, y_data]                             ##
##            title         - Graph title                                                      ##
##            axis_labels   - Override axis labels [x_label, y_label] (optional)               ##
##            model_list    - List of model predictions to overlay (optional)                  ##
##            color_list    - Colors for each model line (optional)                            ##
##            label_list    - Labels for each model line (optional)                            ##
##            error_display - Show +/- error band around first model (default is False)        ##
##            error         - Error value for shaded band                                      ##
##                                                                                             ##
## Output(s): graph       - Matplotlib axes object, can be used for overplotting               ##
##=============================================================================================##

def plot_data(data, title, axis_labels = [], model_list = [], color_list = [], label_list = [],
              error_display = False, error = 0):

  # Create the Matplotlib figure:

  figure = plt.figure(figsize = (12, 9))

  # Add a graph to the figure:

  graph = figure.add_subplot()

  # Set the graph background Color:

  graph.set_facecolor('lightcyan')

  # Create a scatterplot of the data:

  sns.scatterplot(x = data[0], y = data[1], ax = graph)

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

##=============================================================================================##
## Define Parameters:                                                                          ##
##=============================================================================================##

# Set the value of the local acceleration due to gravity near Earth's surface in m/s^2:

local_g = 9.81

# Set the total number of data points:

n_points = 300

# Set the end time in seconds:

t_end = 2.0

##=============================================================================================##
## Generate Time Values Between 0 and 2 seconds:                                               ##
##=============================================================================================##

# Generate a uniformly distributed list of time values:

time_values = np.arange(0.0, t_end, t_end / n_points)

##=============================================================================================##
## Compute Position Data Values:                                                               ##
##=============================================================================================##

# Position = -0.5 * g * t^2:

position_values = -0.5 * local_g * time_values**2

##=============================================================================================##
## Compute Speed Data Values:                                                                  ##
##=============================================================================================##

# Speed = -g * t

speed_values = -local_g * time_values

##=============================================================================================##
## Organize Time And Speed Data In A DataFrame:                                                ##
##=============================================================================================##

# Round the values to make them easier to use:

time_values = np.round(time_values, 4)

speed_values = np.round(speed_values, 4)

# Create a DataFrame that stores the data:

data_df = pd.DataFrame({'Time (s)': time_values, 'Position (m)': position_values})

##=============================================================================================##
## Create A Plot Of The Data:                                                                  ##
##=============================================================================================##

# Set the title of the plot:

title = "Position vs Time"

# Set the x-axis and y-axis labels:

x_label = "Time (s)"
y_label = "Position (m)"

# Select the x_data and y_data:

x_data = data_df['Time (s)'].values

y_data = data_df['Position (m)'].values

# Create a scatterplot of the x_data vs the y_data:

plot_data([x_data, y_data], title, [x_label, y_label])
