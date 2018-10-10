from bokeh.plotting import figure


def bar_1(x, y):
    """
    Returns the plot for a bar graph.
    Arguments:
    x: a list of values or factors for the x axis.
    y: a list of values corresponding to each x axis point.
    """

    TOOLTIPS = [
                ("Month", "@x"),
                ("Number of Wins", "@top{0.0 a}"),
                ]

    p = figure(x_range=x, title="Wins by Month",
               x_axis_label='Month',
               y_axis_label='Number of Wins',
               plot_width=500, plot_height=400,
               tooltips=TOOLTIPS,
               sizing_mode='scale_width')

    p.vbar(x=x, top=y, width=0.5, alpha=0.5, color='rgb(25, 162, 183)')
    p.background_fill_alpha = 0.5
    p.border_fill_alpha = 0.7
    p.xgrid.visible = False
    p.toolbar.logo = None

    return p
