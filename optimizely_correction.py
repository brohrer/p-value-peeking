import os
import numpy as np
import matplotlib.pyplot as plt
from viz import create_violations_axes

p_target = 0.05
tau = .1


def main():
    estimate = np.load("estimate.npy")
    var_pooled = np.load("var_pooled.npy")
    N_RUNS, N_OBSERVATIONS = estimate.shape
    N = np.cumsum(np.ones(estimate.shape), axis=1)

    # Avoid numerically problematic variances at very low N
    var_pooled[:, :100] = 1
    estimate[:, :100] = 0

    p_val = optimizely_p_value(N, estimate, var_pooled)
    running_violations = p_val < p_target

    # Ignore the first 100 because they can be wildly noisy.
    N_drop = np.where(N <= 100)
    running_violations[:, N_drop] = False

    running_v_by_observation = np.sum(running_violations, axis=0)
    fraction_running_v = running_v_by_observation / float(N_RUNS)

    cumulative_violations = np.cumsum(running_violations, axis=1)
    cumulative_v_history = np.minimum(cumulative_violations, 1)
    cumulative_v_by_observation = np.sum(cumulative_v_history, axis=0)
    fraction_cumulative_v = cumulative_v_by_observation / float(N_RUNS)

    fig, running_ax = create_violations_axes(np.max(N), "Running")
    running_ax.plot(N[0, :] / 1e3, fraction_running_v)
    running_ax.set_ylim(0, np.max(fraction_running_v) * 1.05)

    fig, cumulative_ax = create_violations_axes(np.max(N), "Cumulative")
    cumulative_ax.plot(N[0, :] / 1e3, fraction_cumulative_v)
    cumulative_ax.set_ylim(0, np.max(fraction_cumulative_v) * 1.05)

    plt.show()


def optimizely_p_value(n, estimate, var_p):
    # A small non-zero amount to keep everything non-zero and prevent overflow
    epsilon = 1e-6

    # Equation 11 from the original paper
    # http://library.usc.edu.ph/ACM/KKD%202017/pdfs/p1517.pdf
    Lambda = np.sqrt((2 * var_p) / (2 * var_p + n * tau**2)) * np.exp(
        (n**2 * tau**2 * (estimate) ** 2)
        / (4 * var_p * (2 * var_p + n * tau**2) + epsilon)
    )
    p_value = 1 / Lambda

    return p_value


main()
