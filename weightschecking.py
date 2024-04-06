import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Generate sample data
x = np.linspace(0, 10, 100)
ideal_curve = np.sin(x)  # Ideal curve
component1_weight = 0.25
component2_weight = 0.25
component3_weight = 0.25
component4_weight = 0.25

# Function to calculate the master score
def calculate_master_score(component1_weight, component2_weight, component3_weight, component4_weight):
    component1 = np.sin(x) * component1_weight
    component2 = np.cos(x) * component2_weight
    component3 = np.sin(x) * np.cos(x) * component3_weight
    component4 = np.sin(x)**2 * component4_weight
    return component1 + component2 + component3 + component4 + np.random.normal(0, 0.1, size=len(x))

master_score = calculate_master_score(component1_weight, component2_weight, component3_weight, component4_weight)

# Plot the curves
fig, ax = plt.subplots()
l1, = ax.plot(x, ideal_curve, label='Ideal Curve')
l2, = ax.plot(x, master_score, label='Master Score')
plt.legend()
plt.xlabel('X')
plt.ylabel('Score')
plt.title('Master Score vs Ideal Curve')
plt.grid(True)

# Add sliders for weight adjustment
ax_component1 = plt.axes([0.1, 0.1, 0.8, 0.03])
slider_component1 = Slider(ax_component1, 'Component 1 Weight', 0, 1, valinit=component1_weight)

ax_component2 = plt.axes([0.1, 0.05, 0.8, 0.03])
slider_component2 = Slider(ax_component2, 'Component 2 Weight', 0, 1, valinit=component2_weight)

ax_component3 = plt.axes([0.1, 0.15, 0.8, 0.03])
slider_component3 = Slider(ax_component3, 'Component 3 Weight', 0, 1, valinit=component3_weight)

ax_component4 = plt.axes([0.1, 0.2, 0.8, 0.03])
slider_component4 = Slider(ax_component4, 'Component 4 Weight', 0, 1, valinit=component4_weight)

def update(val):
    global component1_weight, component2_weight, component3_weight, component4_weight
    component1_weight = slider_component1.val
    component2_weight = slider_component2.val
    component3_weight = slider_component3.val
    component4_weight = slider_component4.val
    master_score = calculate_master_score(component1_weight, component2_weight, component3_weight, component4_weight)
    l2.set_ydata(master_score)
    fig.canvas.draw_idle()

slider_component1.on_changed(update)
slider_component2.on_changed(update)
slider_component3.on_changed(update)
slider_component4.on_changed(update)

plt.show()
