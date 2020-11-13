from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from scipy.ndimage.filters import gaussian_filter1d

from tkinter import *
from tkinter.ttk import *

import math

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


# ---- Main Code ----

plt.style.use('fivethirtyeight')

index = count()
RANGE = 120
R = 3
T = 10
time = 3 * T
slow_motion_factor = 1
fps = 50
interval = 1 / fps

root = Tk()
root.title('Blood Pressure Monitor')
# root.geometry('1024x768')

style = Style()
style.configure("SBP.Label", foreground="red")
style.configure("DBP.Label", foreground="blue")
style.configure("ABP.Label", foreground="orange")
style.configure("Root.BG", background="black")
style.configure("Value.Live", background="black", foreground="white", width=100)

sbp = Label(root, text="SBP :", font=("Arial Bold", 24), style="SBP.Label").grid(column=0, row=1)
dbp = Label(root, text="DBP :", font=("Arial Bold", 24), style="DBP.Label").grid(column=0, row=2)
abp = Label(root, text="ABP :", font=("Arial Bold", 24), style="ABP.Label").grid(column=0, row=3)


def animate(i):
    data = pd.read_csv('result.csv')
    index = data['index']
    sbp = data['SBP']
    dbp = data['DBP']
    abp = data['ABP']

    plt.cla()

    sbp_smooth = gaussian_filter1d(sbp, sigma=1)
    dbp_smooth = gaussian_filter1d(dbp, sigma=1)
    abp_smooth = gaussian_filter1d(abp, sigma=1.5)

    # x_new = np.linspace(index.min(), index.max(), len(index) * 3)

    # sbp_smooth = spline(index, sbp, x_new)

    # sbp_spl = make_interp_spline(index, sbp, k=3)  # type: BSpline
    # sbp_smooth = sbp_spl(x_new)

    plt.plot(index, sbp_smooth, label='SBP', color='red', linewidth=1)
    plt.plot(index, dbp_smooth, label='DBP', color='blue', linewidth=1)
    plt.plot(index, abp_smooth, label='Actual Bloop Pressure', color='orange', linewidth=1)
    plt.xticks([])

    plt.legend(loc='upper left')
    plt.tight_layout()

    last_element = len(index)
    min_x = last_element - RANGE

    sbp_val = Label(root, text=truncate(dbp[last_element - 1], 3), font=("Arial", 24)).grid(column=1, row=1)
    dbp_val = Label(root, text=truncate(sbp[last_element - 1], 3), font=("Arial", 24)).grid(column=1, row=2)
    abp_val = Label(root, text=truncate(abp[last_element - 1], 3), font=("Arial", 24)).grid(column=1, row=3)

    plt.xlim([min_x, last_element])
    plt.ylim([30, 180])


# label = Tk.Label(root, text="SHM Simulation").grid(column=0, row=0)

fig = plt.gcf()
# fig.set_size_inches(9, 6)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0, row=0)

ani = FuncAnimation(fig, animate,
                    interval=25)

root.mainloop()
