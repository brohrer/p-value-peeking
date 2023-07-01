import numpy as np

N_OBSERVATIONS = 100_000
N_RUNS = 1_000

# Create two identical distributions to compare.
MEAN_A = 0
VAR_A = 1
MEAN_B = 0
VAR_B = 1
EPSILON = 1e-12


def main():
    estimate = np.zeros((N_RUNS, N_OBSERVATIONS))
    var_pooled = np.ones((N_RUNS, N_OBSERVATIONS))

    for i_run in range(N_RUNS):
        print(f"Starting run {i_run}", end="\r")
        sum_a = 0
        sum_b = 0
        sum_sq_a = 0
        sum_sq_b = 0

        for i_observation in range(N_OBSERVATIONS):
            new_a = draw_from_A()
            new_b = draw_from_B()

            # Update sums with each new observation.
            sum_a += np.sum(new_a)
            sum_b += np.sum(new_b)
            sum_sq_a += np.sum(new_a**2)
            sum_sq_b += np.sum(new_b**2)

            # Use running sums to efficiently calculate
            # sample and comparison statistics.
            mean_a = sum_a / (i_observation + EPSILON)
            mean_b = sum_b / (i_observation + EPSILON)
            estimate[i_run, i_observation] = mean_b - mean_a

            var_a = (
                (sum_sq_a - i_observation * mean_a**2)
                / (i_observation + EPSILON)
            )
            var_b = (
                (sum_sq_b - i_observation * mean_b**2)
                / (i_observation + EPSILON)
            )
            var_pooled[i_run, i_observation] = (var_a + var_b) / 2

    print("                                             ")

    # Save point estimate and standard error for analysis
    np.save("estimate.npy", estimate)
    np.save("var_pooled.npy", var_pooled)


def draw_from_A():
    return np.random.normal(loc=MEAN_A, scale=np.sqrt(VAR_A))


def draw_from_B():
    return np.random.normal(loc=MEAN_B, scale=np.sqrt(VAR_B))


main()
