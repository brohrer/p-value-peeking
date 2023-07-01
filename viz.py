import matplotlib.pyplot as plt


def create_violations_axes(N_STEPS, name):
    # Layout the axes within the figure
    fig_height = 8  # inches
    fig_width = 10  # inches

    x_spacing = 1.6  # inches
    y_spacing = 1.2  # inches

    x_min = x_spacing / fig_width
    x_max = 1 - x_min
    dx_ax = x_max - x_min

    y_border = y_spacing / fig_height
    dy_ax = 1 - 2 * y_border
    fig = plt.figure(f"{name}_violations", figsize=(fig_width, fig_height))

    y_min = y_border
    violations_ax = fig.add_axes((x_min, y_min, dx_ax, dy_ax))

    # Format the axes
    violations_ax.set_xlim(0, N_STEPS / 1e3)

    # Set the style for the lines in the plots
    fontsize = 16
    labelsize = 12

    violations_ax.set_ylabel(
        f"{name} fraction of runs violating p < 0.05 threshold",
        fontsize=fontsize,
    )
    violations_ax.set_xlabel(
        "Thousands of samples collected from each group",
        fontsize=fontsize,
    )
    violations_ax.tick_params(axis="x", labelsize=labelsize)
    violations_ax.tick_params(axis="y", labelsize=labelsize)

    # Add lines showing actual values
    dashed_line_color = "darkblue"
    dashed_linewidth = 1
    violations_ax.plot(
        [0, N_STEPS / 1e3],
        [0.05, 0.05],
        color=dashed_line_color,
        linestyle="dashed",
        linewidth=dashed_linewidth,
        zorder=2,
    )

    return fig, violations_ax
