import numpy as np
import matplotlib.pyplot as plt

x, y, c, s = np.random.rand(4, 40)
s = s * 100 + 5

fig, ax = plt.subplots()
sc = ax.scatter(x, y, s=s, c=c)
fig.colorbar(sc)

ax.legend(*sc.legend_elements("sizes"), loc="upper left")

plt.show()