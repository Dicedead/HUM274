from util import *

"""
The number of levels a  quarter note gives us its relative probability, probability which we increase more and more 
during the iterations.
"""

# simulating brownian motion from t=0 to t=TIME_HORIZON
TIME_HORIZON = 700.0
# number of sample points for the simulation
TIMESTEPS = 1000


def brownian_motion(dimensions=1, start_value=0, time_horizon=TIME_HORIZON, timesteps=TIMESTEPS):
    """
    function to simulate brownian motion

    :param dimensions: number of dimensions in which we simulate
    :param start_value: value at which the brownian motion starts
    :param time_horizon: time until which we simulate
    :param timesteps: number of sample points with which to simulate
    :return: a tuple of the different time points at which we simulate, the actual brownian
        motion values at these time points as well as the difference between any 2 points in
        the brownian motion values (as it is more practical to work with)
    """

    # partitioning the space into timesteps number of points
    times = np.linspace(0.0, time_horizon, timesteps)
    step_length = times[1] - times[0]

    # as brownian motion at time t1 - brownian motion at time t0 ~ Normal(mean = 0, variance = t1-t0)
    # scale is the standard deviation, so we take the square root of the step_length
    diff_b = np.random.normal(size=(timesteps - 1, dimensions), scale=np.sqrt(step_length))

    brownian_motion = np.zeros(shape=(timesteps, dimensions))

    # we start each brownian motion dimension with the given start value
    brownian_motion[0, :] = np.full((1, dimensions), start_value)

    # the rest of the values of brownian motion are the cumulative sum of normal values
    brownian_motion[1:, :] = np.cumsum(diff_b, axis=0) + start_value

    return times, brownian_motion, diff_b


if __name__ == "__main__":
    times, brownian_motion_arr, diff_brownian_motion = brownian_motion(dimensions=5)
    plt.plot(times, brownian_motion_arr)
    plt.show()
