from matplotlib import pyplot as plt
from tysen import calculate as tysen
from tysen import calculate as mh


def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

test_case = {
    "payouts": [50, 30, 20],
    "stacks": [10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000]
}

res1 = list(mh(test_case["payouts"], test_case["stacks"]))
res2 = list(tysen(test_case["payouts"], test_case["stacks"]))

plt.bar(range(len(res1)), res1, 0.4, label="Malmuth-Harville")
plt.bar([0.4 + i for i in range(len(res2))], res2, 0.4, label="Tysen")
addlabels(range(len(res1)), [round(bar, 2) for bar in res1])
addlabels([0.4 + i for i in range(len(res2))], [round(bar, 2) for bar in res2])
plt.legend()
plt.show()