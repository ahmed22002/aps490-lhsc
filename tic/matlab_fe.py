import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk

def animate_actuators(start1, end1, start2, end2):
    """
    Animate the movement of two actuators from given start to end positions in an oscillating motion.
    """
    Ax, Ay, Az = start1
    Bx, By, Bz = end1
    Cx, Cy, Cz = start2
    Dx, Dy, Dz = end2

    stepsize = 0.01
    max_step = 1
    increments = np.concatenate((np.linspace(0, max_step, int(max_step / stepsize)), np.linspace(max_step, 0, int(max_step / stepsize))))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(min(Ax, Bx, Cx, Dx) - 1, max(Ax, Bx, Cx, Dx) + 1)
    ax.set_ylim(min(Ay, By, Cy, Dy) - 1, max(Ay, By, Cy, Dy) + 1)
    ax.set_zlim(min(Az, Bz, Cz, Dz) - 1, max(Az, Bz, Cz, Dz) + 1)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    actuator1, = ax.plot([], [], [], 'ro', markersize=8)
    actuator2, = ax.plot([], [], [], 'bo', markersize=8)
    
    # Plot the dotted lines showing the actuator paths
    ax.plot([Ax, Bx], [Ay, By], [Az, Bz], 'r--', alpha=0.5)
    ax.plot([Cx, Dx], [Cy, Dy], [Cz, Dz], 'b--', alpha=0.5)
    
    def update(frame):
        t = increments[frame]
        T1x = Ax + (Bx - Ax) * t
        T1y = Ay + (By - Ay) * t
        T1z = Az + (Bz - Az) * t
        T2x = Cx + (Dx - Cx) * t
        T2y = Cy + (Dy - Cy) * t
        T2z = Cz + (Dz - Cz) * t
        actuator1.set_data([T1x], [T1y])
        actuator1.set_3d_properties(T1z)
        actuator2.set_data([T2x], [T2y])
        actuator2.set_3d_properties(T2z)
        return actuator1, actuator2
    
    ani = animation.FuncAnimation(fig, update, frames=len(increments), interval=10, blit=False)
    plt.show()

def start_animation():
    try:
        start1 = (float(x1_entry.get()), float(y1_entry.get()), float(z1_entry.get()))
        end1 = (float(x2_entry.get()), float(y2_entry.get()), float(z2_entry.get()))
        start2 = (float(x3_entry.get()), float(y3_entry.get()), float(z3_entry.get()))
        end2 = (float(x4_entry.get()), float(y4_entry.get()), float(z4_entry.get()))
        animate_actuators(start1, end1, start2, end2)
    except ValueError:
        print("Invalid input. Please enter numeric values.")

# Create GUI with Tkinter
root = tk.Tk()
root.title("Actuator Movement Visualization")
frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0)

labels = ["Start Actuator 1 (x, y, z)", "End Actuator 1 (x, y, z)", "Start Actuator 2 (x, y, z)", "End Actuator 2 (x, y, z)"]
entries = []

for i, label in enumerate(labels):
    ttk.Label(frame, text=label).grid(row=i, column=0, pady=5)
    entry_x = ttk.Entry(frame, width=5)
    entry_y = ttk.Entry(frame, width=5)
    entry_z = ttk.Entry(frame, width=5)
    entry_x.grid(row=i, column=1)
    entry_y.grid(row=i, column=2)
    entry_z.grid(row=i, column=3)
    entries.extend([entry_x, entry_y, entry_z])

x1_entry, y1_entry, z1_entry, x2_entry, y2_entry, z2_entry, x3_entry, y3_entry, z3_entry, x4_entry, y4_entry, z4_entry = entries

button = ttk.Button(frame, text="Show Actuator Movement", command=start_animation)
button.grid(row=4, column=0, columnspan=4, pady=10)

root.mainloop()
