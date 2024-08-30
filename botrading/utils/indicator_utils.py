import numpy as np


def calculate_trend(values):
    if len(values) == 0:
        return 0, 0

    x = np.arange(1, len(values) + 1, 1)
    y = np.array(values)

    #  Handle nan values
    x_new = x[~np.isnan(y)]
    y_new = y[~np.isnan(y)]

    m, c = np.polyfit(x_new, y_new, 1)
    return m, c
