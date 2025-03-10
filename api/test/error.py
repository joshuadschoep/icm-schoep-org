from malmuthharville import calculate as malmuthharville
from tysen import calculate2 as tysen2
from tysen import calculate as tysen
from matplotlib import pyplot
from scipy.optimize import curve_fit
import numpy as np

def calculate_average_error(arr1, arr2):
    """
    Calculates the average error between two arrays.

    Args:
        arr1 (numpy.ndarray): The first array.
        arr2 (numpy.ndarray): The second array.

    Returns:
        float: The average error between the two arrays.
    """
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must have the same length")

    absolute_errors = np.abs(np.subtract(arr1, arr2))
    average_error = np.mean(absolute_errors)
    return average_error

case_object = [{ 
    "size": case,
    "payouts": sorted([10 + 10 * item for item in range(case)]), 
    "players": sorted([10 + 10 * item for item in range(case)]), 
} for case in range(2, 10)]


def get_error_of_cases(cases):
    for case in cases:
        print(case)
        ty = list(tysen(case["payouts"], case["players"]))
        mh = list(tysen2(case["payouts"], case["players"]))
        err = calculate_average_error(mh, ty)
        print("Tysen\n", ty)
        print("Malmuth-Harville\n", mh, "\n\n")
        yield err


err = list(get_error_of_cases(case_object))

pyplot.plot(range(2, 10), err, 'ko')
pyplot.show()