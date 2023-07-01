import os
import numpy as np
import matplotlib.pyplot as plt
from viz import create_violations_axes

# For 95% stat significance
z_threshold = 1.960
phi = 1.618  # Golden Ratio

# For 99% stat significance
# z_threshold = 2.576
# phi = 1.396  # np.e**(1/3)

# For 90% stat significance
# z_threshold = 1.645
# phi = 1.772  # np.sqrt(np.pi)

# For 80% stat significance
# z_threshold = 1.282
# phi = 2.044  # 45 / 22

epsilon = 1e-12


def main():
    estimate = np.load("estimate.npy")
    var_pooled = np.load("var_pooled.npy")
    N_RUNS, N_OBSERVATIONS = estimate.shape
    i_observations = np.cumsum(np.ones(estimate.shape), axis=1)

    # Avoid numerically problematic variances at very low N
    var_pooled[:, :10] = 1
    stderr = phi * np.sqrt(2 * var_pooled / (i_observations + epsilon))
    upper_bound = estimate + stderr * z_threshold
    lower_bound = estimate - stderr * z_threshold
    upper_violations = upper_bound <= 0
    lower_violations = lower_bound >= 0

    # Ignore the first 100 observations because they can be wildly noisy.
    upper_violations[:, :100] = False
    lower_violations[:, :100] = False

    # Find the fraction of experiments that show false significance
    # at each point in the course of collecting observations.
    running_violations = upper_violations + lower_violations
    running_v_history = np.minimum(running_violations, 1)
    running_v_by_observation = np.sum(running_v_history, axis=0)
    fraction_running_v = running_v_by_observation / float(N_RUNS)

    # Find the fraction of experiments that have shown
    # false significance *at any time* previous to each point
    # in the course of collecting observations.
    cumulative_uv = np.cumsum(upper_violations, axis=1)
    cumulative_lv = np.cumsum(lower_violations, axis=1)
    cumulative_violations = cumulative_uv + cumulative_lv
    cumulative_v_history = np.minimum(cumulative_violations, 1)
    cumulative_v_by_observation = np.sum(cumulative_v_history, axis=0)
    fraction_cumulative_v = cumulative_v_by_observation / float(N_RUNS)

    fig, running_ax = create_violations_axes(N_OBSERVATIONS, "Running")
    N_thousand = np.arange(N_OBSERVATIONS) / 1e3
    running_ax.plot(N_thousand, fraction_running_v)
    running_ax.set_ylim(0, np.max(fraction_running_v) * 1.05)

    fig, cumulative_ax = create_violations_axes(N_OBSERVATIONS, "Cumulative")
    cumulative_ax.plot(N_thousand, fraction_cumulative_v)
    cumulative_ax.set_ylim(0, np.max(fraction_cumulative_v) * 1.05)

    plt.show()


main()
