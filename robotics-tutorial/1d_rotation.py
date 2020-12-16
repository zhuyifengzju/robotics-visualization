from celluloid import Camera
import matplotlib.pyplot as plt
import numpy as np

def plot_vector_field(camera, ax, omega, T=0):
    skew_matrix = np.array([[0, -omega], [omega, 0]])

    x, y = np.meshgrid(np.arange(-2, 2, 0.5),
                       np.arange(-2, 2, 0.5))

    u = skew_matrix[0][0] * x + skew_matrix[0][1] * y
    v = skew_matrix[1][0] * x + skew_matrix[1][1] * y

    q = ax.quiver(x, y, u, v, width=0.022,
                  scale=1 / 0.1, units='x')

    if T > 0:
        x0 = 1.0
        y0 = 0.6

        x_traj = [x0]
        y_traj = [y0]
        dt = 0.05
        t = 0
        while t < T:
            t += dt
            dx = skew_matrix[0][0] * x_traj[-1] + skew_matrix[0][1] * y_traj[-1]
            dy = skew_matrix[1][0] * x_traj[-1] + skew_matrix[1][1] * y_traj[-1]
            x_traj.append(x_traj[-1] + dx * dt)
            y_traj.append(y_traj[-1] + dy * dt)

        ax.plot(x_traj, y_traj, 'b')
        
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    if T == 0:
        ax.text(0.5, 1.01, f'omega: {round(omega, 2)} (rad / s)', transform=ax.transAxes)
    else:
        ax.text(0.5, 1.01, f't: {round(T, 2)} s, omega: {round(omega, 2)} (rad / s)', transform=ax.transAxes)
    camera.snap()
    
fig, ax = plt.subplots(1)
camera = Camera(fig)

for omega in np.linspace(0, 1.0, 80):
    plot_vector_field(camera, ax, omega)

for t in np.linspace(0, 3.14, 80):
    plot_vector_field(camera, ax, 1,  t)

    
animation = camera.animate()
animation.save('1d_rotation.mp4')
