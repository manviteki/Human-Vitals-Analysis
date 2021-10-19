# Human-Vitals-Analysis

## Introduction
The undertaking here is to create a graphical user interface of the vital signs of a dummy patient and its analysis.

## Flow of work
1) We get the data from our dummy patient with a selenium module for web automation and create a dataframe with pandas
2) We clean the data
3) We create a graph object with the visualisation package plotly
4) We make a graph by using the dash core component “Graph” to plot the figure. To do this we provide the graph object from the previous section as a variable for the figure.
5) A lot of calls during on-call shifts are concerned about the question of whether to isolate or not isolate a patient based on a specific temperature. If you unselect all vital signs on the right and only leave the temperature in the list you get more insight into the temperatures variation through time. It becomes easy to identify a subfebrile temperature (=37.5–38.4) on 4 February. 
6)  There is of course a lot more to do before it’s usable in a day-to-day work environment, but what I have done here is a basic run down of an intermediate application.
