# THIS FILE IS TO BE USED UNTIL GUI IS AVAILABLE
# INSERT 'DUMP.TXT' FILE INTO THIS PYTHON FOLDER
# OR CHANGE THE FILENAME IN LINE 86
# NOTE THAT 1 WEEK DATA CAN BE PREOCESSED BUT 2 WEEK DATA NEEDS TO BE SPLIT DUE TO MEMORY LIMITS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# These two classes are copied form https://matplotlib.org/gallery/misc/cursor_demo_sgskip.html
class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()

class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):

        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        indx = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('time=%1.1f, power=%1.0f' % (x, y))
        # print('time=%1.1f, power=%1.0f' % (x, y))
        plt.draw()



HEAT_TRIGGER = 820
APPLIANCE_TRIGGER = 10

HEAT_PULSES_2_KWH = 75
APPLIANCE_PULSES_2_KWH = 1000

HEAT_ENERGY_BETWEEN_PULSES = 1000 * 3600 / HEAT_PULSES_2_KWH
APPLIANCE_ENERGY_BETWEEN_PULSES = 1000 * 3600 / APPLIANCE_PULSES_2_KWH

HEATING_AVERAGING_WINDOW_WIDTH = 100
APPLIANCE_AVERAGING_WINDOW_WIDTH = 100

START = 0
FINISH = -1

a = pd.to_datetime('now')
b = pd.Timestamp(datetime.datetime(1970, 1, 1, 0, 0, 0))
c = 3600 + (a-b).total_seconds()

offset = pd.Timestamp(datetime.datetime(2019, 2, 16, 9, 31, 0))
endtime = pd.Timestamp(datetime.datetime(2019, 3, 2, 8, 41, 0))
true_elapsed_time_seconds = (endtime-offset).total_seconds()


df = pd.read_csv('dump.txt')
df.columns = ['ms', 'H', 'A']

measured_elapsed_milliseconds = df['ms'].iloc[-1] - df['ms'].iloc[0]
scale_factor = true_elapsed_time_seconds*1000/measured_elapsed_milliseconds
print("Time Correction Scale Factor: ", scale_factor)
df['ms'] = df['ms']*scale_factor


df['heat thresh'] = np.where(df['H'] < HEAT_TRIGGER, 1, 0)
df['heat diff'] = df['heat thresh'].diff()
df['heat positive edges'] = np.where(df['heat diff'] > 0, 1, 0)

df['appl thresh'] = np.where(df['A'] > APPLIANCE_TRIGGER, 1, 0)
df['appl diff'] = df['appl thresh'].diff()
df['appl positive edges'] = np.where(df['appl diff'] > 0, 1, 0)

# REMOVE UNNECESSARY COLUMNS AND ROWS
df = df.drop(columns=['H', 'A', 'heat thresh', 'heat diff', 'appl thresh', 'appl diff'])

df['seconds'] = df['ms'] / 1000
df['Hours'] = df['seconds'] / 3600


# REMOVE UNNECESSARY COLUMNS AND ROWS
# df = df.drop(columns=['ms', 'H', 'A', 'heat thresh', 'heat diff', 'appl thresh', 'appl diff'])
df = df.drop(columns=['ms'])
df['select'] = df['heat positive edges'] + df['appl positive edges']
df = df[df['select'] !=0]
df = df.drop(columns=['select'])
df['actual datetime'] = offset + pd.to_timedelta(df['seconds'], 's')


selected_heat_pulses = pd.DataFrame(data=df, columns=['seconds', 'Hours', 'actual datetime', 'heat positive edges'])
selected_heat_pulses.drop(selected_heat_pulses.index[selected_heat_pulses['heat positive edges'] == 0], inplace=True)
selected_heat_pulses.reset_index(drop=True, inplace=True)
selected_heat_pulses['delta seconds'] = selected_heat_pulses['seconds'].diff()
selected_heat_pulses['power'] = HEAT_ENERGY_BETWEEN_PULSES / selected_heat_pulses['delta seconds']
selected_heat_pulses['time delta for average power'] = selected_heat_pulses['seconds'].diff(
    periods=HEATING_AVERAGING_WINDOW_WIDTH)
selected_heat_pulses['average power'] = (HEAT_ENERGY_BETWEEN_PULSES * HEATING_AVERAGING_WINDOW_WIDTH) / \
                                        selected_heat_pulses['time delta for average power']


selected_appl_pulses = pd.DataFrame(data=df, columns=['seconds', 'Hours', 'actual datetime', 'appl positive edges'])
selected_appl_pulses.drop(selected_appl_pulses.index[selected_appl_pulses['appl positive edges'] == 0], inplace=True)
selected_appl_pulses.reset_index(drop=True, inplace=True)
selected_appl_pulses['delta seconds'] = selected_appl_pulses['seconds'].diff()
selected_appl_pulses['power'] = APPLIANCE_ENERGY_BETWEEN_PULSES / selected_appl_pulses['delta seconds']
selected_appl_pulses['time delta for average power'] = selected_appl_pulses['seconds'].diff(
    periods=APPLIANCE_AVERAGING_WINDOW_WIDTH)
selected_appl_pulses['average power'] = (APPLIANCE_ENERGY_BETWEEN_PULSES * APPLIANCE_AVERAGING_WINDOW_WIDTH) / \
                                        selected_appl_pulses['time delta for average power']
# selected_appl_pulses['datetime'] = pd.to_datetime(3600+c+df['seconds'], unit='s')





heat_total = df['heat positive edges'][START:FINISH].sum() / HEAT_PULSES_2_KWH
appl_total = df['appl positive edges'][START:FINISH].sum() / APPLIANCE_PULSES_2_KWH
print("Total number of heating kWh: {0:.2f}".format(heat_total))
print("Total number of appliance kWh: {0:.2f}".format(appl_total))

fig, axs = plt.subplots(2, 1)
fig.subplots_adjust(hspace=0.7)
# axs[0].plot(selected_heat_pulses['Hours'], selected_heat_pulses['power'])
# axs[0].plot(selected_heat_pulses['Hours'], selected_heat_pulses['average power'])
axs[0].plot(selected_heat_pulses['actual datetime'], selected_heat_pulses['power'])
axs[0].plot(selected_heat_pulses['actual datetime'], selected_heat_pulses['average power'])
axs[0].set_title('Heating')
axs[0].set_xlabel('Date Time')
axs[0].set_ylabel('Power (Watts)')
axs[0].legend(loc='upper left')

axs[1].set_title('Appliance')
axs[1].set_xlabel('Date Time')
axs[1].set_ylabel('Power (Watts)')
# axs[1].plot(selected_appl_pulses['Hours'], selected_appl_pulses['power'])
# axs[1].plot(selected_appl_pulses['Hours'], selected_appl_pulses['average power'])
axs[1].plot(selected_appl_pulses['actual datetime'], selected_appl_pulses['power'])
axs[1].plot(selected_appl_pulses['actual datetime'], selected_appl_pulses['average power'])
axs[1].legend(loc='upper left')

# Uncomment for interactive cursor
# cursor = SnaptoCursor(axs[0], selected_heat_pulses['Hours'], selected_heat_pulses['power'])
# cid =  plt.connect('motion_notify_event', cursor.mouse_move)

plt.show()


df = df.drop(columns=['Hours'])
save_filename = str(endtime) + "---" + str(offset) + ".csv"
save_filename = save_filename.replace(":", "_")
df.to_csv(save_filename)
print("File saved with filename: ", save_filename)