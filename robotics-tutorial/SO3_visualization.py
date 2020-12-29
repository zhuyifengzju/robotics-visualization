from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('auto')
# Make data
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 1 * np.outer(np.cos(u), np.sin(v))
y = 1 * np.outer(np.sin(u), np.sin(v))
z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))

# Plot the surface
ax.plot_surface(x, y, z, rstride=4, cstride=4, color='b', alpha=0.1)
ax.plot(np.sin(u),np.cos(u),0,color='k', linestyle = 'dashed')
ax.plot(np.sin(v),np.cos(v),0,color='k', linestyle = 'solid')

ax.plot([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], color='r')
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
plt.show()
