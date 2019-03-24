import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

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


def basic_pre_proc(df):
    df.columns = ['ms', 'H', 'A']
    # df['seconds'] = df['ms'] / 1000
    df['heat thresh'] = np.where(df['H'] < HEAT_TRIGGER, 1, 0)
    df['heat diff'] = df['heat thresh'].diff()
    df['heat positive edges'] = np.where(df['heat diff'] > 0, 1, 0)
    df['appl thresh'] = np.where(df['A'] > APPLIANCE_TRIGGER, 1, 0)
    df['appl diff'] = df['appl thresh'].diff()
    df['appl positive edges'] = np.where(df['appl diff'] > 0, 1, 0)
    return df

def time_stretch(df, start_date_time, end_date_time):
    start_ms = df['ms'][0]
    end_ms = df['ms'].iloc[-1]
    measured_milliseconds = (end_ms-start_ms)
    actual_seconds = (end_date_time-start_date_time).total_seconds()
    scale_factor = actual_seconds/measured_milliseconds
    df['corrected_seconds'] = df['ms']*scale_factor
    df['corrected_hours'] = df['corrected_seconds'] / 3600
    return df

def calc_heating(df):
    selected_heat_pulses = pd.DataFrame(data=df, columns=['corrected_seconds', 'corrected_hours', 'heat positive edges'])
    selected_heat_pulses.drop(selected_heat_pulses.index[selected_heat_pulses['heat positive edges'] == 0],
                              inplace=True)
    selected_heat_pulses.reset_index(drop=True, inplace=True)
    selected_heat_pulses['delta seconds'] = selected_heat_pulses['corrected_seconds'].diff()
    selected_heat_pulses['power'] = HEAT_ENERGY_BETWEEN_PULSES / selected_heat_pulses['delta seconds']
    selected_heat_pulses['time delta for average power'] = selected_heat_pulses['corrected_seconds'].diff(
        periods=HEATING_AVERAGING_WINDOW_WIDTH)
    selected_heat_pulses['average power'] = (HEAT_ENERGY_BETWEEN_PULSES * HEATING_AVERAGING_WINDOW_WIDTH) / \
                                            selected_heat_pulses['time delta for average power']
    return selected_heat_pulses

def calc_appl(df):
    selected_appl_pulses = pd.DataFrame(data=df, columns=['corrected_seconds', 'corrected_hours', 'appl positive edges'])
    selected_appl_pulses.drop(selected_appl_pulses.index[selected_appl_pulses['appl positive edges'] == 0],
                              inplace=True)
    selected_appl_pulses.reset_index(drop=True, inplace=True)
    selected_appl_pulses['delta seconds'] = selected_appl_pulses['corrected_seconds'].diff()
    selected_appl_pulses['power'] = APPLIANCE_ENERGY_BETWEEN_PULSES / selected_appl_pulses['delta seconds']
    selected_appl_pulses['time delta for average power'] = selected_appl_pulses['corrected_seconds'].diff(
        periods=APPLIANCE_AVERAGING_WINDOW_WIDTH)
    selected_appl_pulses['average power'] = (APPLIANCE_ENERGY_BETWEEN_PULSES * APPLIANCE_AVERAGING_WINDOW_WIDTH) / \
                                            selected_appl_pulses['time delta for average power']
    return selected_appl_pulses

def preprocess(df, start_date_time, end_date_time, start_ht, start_nt, start_appl, end_ht, end_nt, end_appl):
    df = basic_pre_proc(df)
    df = time_stretch(df, start_date_time, end_date_time)
    selected_heat_pulses = calc_heating(df)
    selected_appl_pulses = calc_appl(df)
    heat_total = df['heat positive edges'][START:FINISH].sum() / HEAT_PULSES_2_KWH
    appl_total = df['appl positive edges'][START:FINISH].sum() / APPLIANCE_PULSES_2_KWH

    print(heat_total)
    print(appl_total)

    return df, selected_heat_pulses, selected_appl_pulses