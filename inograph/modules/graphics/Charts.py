import numpy as np
from matplotlib import pyplot as plt


def DrawFunction(f, xPoints):
    """
    Outputs an image of a function
    :param f: the function to draw (y-axis)
    :param xPoints: points along the x-axis
    """
    x_new = np.linspace(xPoints[0], xPoints[-1], 100)
    plt.plot(x_new, f(x_new), 'b-')
    plt.show()
