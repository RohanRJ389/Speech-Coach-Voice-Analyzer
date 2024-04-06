import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import numpy as np

# Generate sample data
x = np.linspace(0, 10, 100)
ideal_curve = np.sin(x)  # Ideal curve
master_score = np.sin(x) + np.random.normal(0, 0.1, size=len(x))  # Master score curve (with noise)

# Define initial weights
weight = 0.5

# Plot the curves
fig, ax = plt.subplots()
l1, = ax.plot(x, ideal_curve, label='Ideal Curve')
l2, = ax.plot(x, master_score, label='Master Score')
plt.legend()
plt.xlabel('X')
plt.ylabel('Score')
plt.title('Master Score vs Ideal Curve')
plt.grid(True)

# Add slider for weight adjustment
ax_weight = plt.axes([0.1, 0.01, 0.8, 0.03])
slider_weight = Slider(ax_weight, 'Weight', 0, 1, valinit=weight)


def update(val):
    global weight
    weight = slider_weight.val
    l2.set_ydata(np.sin(x) * weight + np.random.normal(0, 0.1, size=len(x)))  # Adjusted master score curve
    fig.canvas.draw_idle()


slider_weight.on_changed(update)
plt.show()
