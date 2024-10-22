# importing 2 classes from the Altair visualization library
#   Chart to create and config visualization
#   Tooltip for pop-up text boxes when hover over data points
from altair import Chart, Tooltip
from pandas import DataFrame

def chart(df, x, y, target) -> Chart:
    """
    A method that creates an Altair Chart based on the provided DataFrame.
    
    Args:
        df (DataFrame): The pandas DataFrame containing monster data.
        x (str): The column name to use for the x-axis.
        y (str): The column name to use for the y-axis.
        target (str): The column name that will determine 
            the color of the data points (used for color encoding)
    
    Returns:
        Chart: An Altair Chart object.
    """

    # Create new Chart object using Altair library & assigns it to the variable "graph"
    graph = Chart(
        df,
        title=f"{y} by {x} for {target}",
    ).mark_circle(size=100).encode( # chart uses circles to rep each data point
        x=x, # use .encode() method to map columns
        y=y,
        color=target, # use color encoding, diff values in target have diff colors
        tooltip=Tooltip(df.columns.to_list()) # Tooltip class specifies what info shows when hovering over data points
        # df.columns.to_list() converts the column names to a list and uses them in tooltip
        # so when a user hovers over a point, entire row's data (all the specs of a monster) will be displayed
    ).interactive() # adds interactivity to the chart with zooming and panning features

    return graph # as an Altair Chart object
