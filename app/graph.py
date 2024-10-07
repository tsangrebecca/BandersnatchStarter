from altair import Chart, Tooltip
from pandas import DataFrame


def chart(df, x, y, target) -> Chart:
    """
    Create an Altair chart based on the provided DataFrame.
    
    Args:
        df (DataFrame): The pandas DataFrame containing monster data.
        x (str): The column to use for the x-axis.
        y (str): The column to use for the y-axis.
        target (str): The column to use for color encoding.
    
    Returns:
        Chart: An Altair chart object.
    """
    graph = Chart(
        df,
        title=f"{y} by {x} for {target}",
    ).mark_circle(size=100).encode(
        x=x,
        y=y,
        color=target,
        tooltip=Tooltip(df.columns.to_list())
    ).interactive()

    return graph
