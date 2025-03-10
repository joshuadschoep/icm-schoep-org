from time import process_time
from malmuthharville import calculate as malmuthharville
from tysen import calculate as tysen
from matplotlib import pyplot
from scipy.optimize import curve_fit
import numpy as np

case_object = [{ 
    "size": case,
    "payouts": sorted([10 + 10 * item for item in range(case)]), 
    "players": sorted([10 + 10 * item for item in range(case)]), 
} for case in range(2, 11)]


def get_time_of_cases(cases):
    for case in cases:
        start = process_time()
        list(tysen(case["payouts"], case["players"]))
        end = process_time()
        print("Process took", end - start, "seconds.")
        yield end - start

res = list(get_time_of_cases(case_object))

# def func(x, a, b):
#     return a*x+b

# popt, pcov = curve_fit(func, range(2, 11), res, p0=(1, 1e-6, 1))

# regressx = np.linspace(0.9, 10.1, 6000)
# regressy = func(regressx, *popt)

# pyplot.plot(regressx, regressy)
pyplot.plot(range(2, 11), res, 'ko')
pyplot.show()