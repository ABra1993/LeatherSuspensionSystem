# Read data from .csv file into a pandas dataframe
# Sarah Brands & Amber Brands
# Created November 2022; Last edited May 2023

import numpy as np
import pandas as pd
import datetime as dt

def correct_jump(df, jump_day, jump_size, direction):
    """
    Correct for discontinuities due to reset of device.

    Input:
    - df [pandas dataframe]: dataframe with leather displacement data
    - jump_day [float]: moment on which jump occurs (days)
    - jump_size [float]: size of the jump (same units as displacement)
    - direction [str]: 'ver' for vertical or 'hor' for horizontal

    Output:
    - df (pandas dataframe): dataframe with leather displacement data

    """

    x_new = df.copy()[direction + '_rel'].values
    x_new[df['days_diff'].values > jump_day] = x_new[df['days_diff'].values
        > jump_day] + jump_size
    df[direction + '_rel'] = x_new

    return df

def data2df(do_correct=True, be_verbose=False):
    """
    Read comma delimited log file into dataframe & clean data.
    This function is tailored to the specific data file 'log_20220315.csv'

    Input:
    -   do_correct_shifts [bool].
        Set to True for data analysis (default), or to False for inspection
        of original data (not corrected for shifts due to reset of devices)
    -   be_verbose [bool]. If True, print irregularities in the data and/or
        checks if cleaning was carried out correctly (default = False)

    Output:
    - df [pandas dataframe]: dataframe with leather displacement data

    """

    # Data file, originally space delimited, converted to comma delimited.
    logfile = '../data/log_20220315.csv'
    data = np.genfromtxt(logfile, dtype='str').T
    ncols = len(data)
    nrows = len(data[0])

    # Correct notation for decimals
    datetime = []
    for i in range(nrows):
        datetime.append(data[0,i] + ' ' + data[1,i])
        for j in range(ncols-2):
            data[2+j,i].replace(",", ".")
    data = data[2:-1].astype(float)

    # Assign column names
    # RV = Relative Humidity (procent) (from Dutch: Relatieve Vochtigheid)
    # T = Temperature (Celcius):
    colnames = ['ver_rel', 'hor_rel',
            'T1', 'RV1', 'T2', 'RV2', 'T3', 'RV3', 'T4', 'RV4',
            'T5', 'RV5', 'T6', 'RV6', 'T7', 'RV7', 'T8', 'RV8']

    # Defines sensors hanging in front and behind the leather
    T_front = ['T1', 'T4', 'T7']
    RV_front = ['RV1', 'RV4', 'RV7']

    T_back = ['T2', 'T3', 'T5', 'T6', 'T7']
    RV_back = ['RV2', 'RV3', 'RV5', 'RV6', 'RV7']

    # Group all RV and T columns
    RVcollist = []
    Tcollist = []
    for acol in colnames:
        if 'RV' in acol:
            RVcollist.append(acol)
        if 'T' in acol:
            Tcollist.append(acol)

    # Group all RV and T columns separate for the sensors hanging in front
    # and behind the leather
    RVcollist_front = []
    RVcollist_back = []
    Tcollist_front = []
    Tcollist_back = []
    for acol in colnames:
        if acol in T_front:
            Tcollist_front.append(acol)
        elif acol in RV_front:
            RVcollist_front.append(acol)
        elif acol in T_back:
            Tcollist_back.append(acol)
        elif acol in RV_back:
            RVcollist_back.append(acol)

    # Create dataframe
    df = pd.DataFrame(data.T, columns=colnames)

    # Convert time units to 'days_diff' = number of days since
    # start of measurements
    df['datetime_raw'] = datetime
    df['datetime'] = pd.to_datetime(df['datetime_raw'],
        format='%Y-%m-%d %H:%M:%S')

    # Make list of indices that contain summer time values. Remove the last two
    # values (that are the duplicates, as the last two are winter time again)
    summer = (df['datetime']>pd.Timestamp(2021,3,28,2,30,0)) & \
        (df['datetime']<pd.Timestamp(2021,10,31,3,0,0))
    summer_idx = [i for i, x in enumerate(summer) if x]
    summer[summer_idx[-2]] = False
    summer[summer_idx[-1]] = False

    # Set all datatimes to winter time so that the time runs continously
    df['datetime'][summer] = df['datetime'][summer] - pd.Timedelta("1 hour")

    if be_verbose:
        print('=== Check summer time corrections === ')
        print(df[940:950])
        print(df[11405:11415])

    # Measure time in days and minutes from start of measurement
    first_day = df['datetime'].iloc[0]
    df['minutes_diff'] = (df['datetime'] - first_day).dt.total_seconds()/60.0
    df['days_diff'] = df['minutes_diff']/(24*60.0)

    # Convert relative shift to mm, take negative value so that expansion
    # corresponds with an increasing number
    df['ver_rel'] = -df['ver_rel']*10
    df['hor_rel'] = -df['hor_rel']*10

    # Take average RV and T over axis=1, that is, take the mean per row over
    # the columns in RVcollist and Tcollist
    df['RV_avg'] = df[RVcollist].mean(axis=1)
    df['RV_front'] = df[RVcollist_front].mean(axis=1)
    df['RV_back'] = df[RVcollist_back].mean(axis=1)

    df['T_avg'] = df[Tcollist].mean(axis=1)
    df['T_front'] = df[Tcollist_front].mean(axis=1)
    df['T_back'] = df[Tcollist_back].mean(axis=1)

    # Compute the shifts per sampling interval, essentially the derivative in
    # time. This is for correcting for the jumps created by device reset.
    vertical_strech_diff = df['ver_rel'].values[1:] - df['ver_rel'].values[:-1]
    horizontal_strech_diff = df['hor_rel'].values[1:] - df['hor_rel'].values[:-1]
    time_avg = 0.5*(df['days_diff'].values[1:] + df['days_diff'].values[:-1])

    vertical_strech_diff = np.concatenate((np.array([0.0]),
        vertical_strech_diff))
    horizontal_strech_diff = np.concatenate((np.array([0.0]),
        horizontal_strech_diff))

    df['dver_raw'] = vertical_strech_diff
    df['dhor_raw'] = horizontal_strech_diff

    diff_mins = df['minutes_diff'].values[1:] - df['minutes_diff'].values[:-1]
    df['interval_mins'] = np.concatenate((np.array([0]), diff_mins))

    # Correct for jumps due to device reset in the data
    if do_correct:
        if be_verbose:
            print('\n=== Jump corrections / Resets ===')
            print('Datetime'.ljust(20), 'Direction'.ljust(12),
                'Reset val (mm)'.ljust(18), 'Jump size (mm)')

        ver_cut = 0.25
        hor_cut = 0.15

        sh_ver = []
        sh_hor = []
        for i in range(len(df)):
            if (np.abs(df['dver_raw'].iloc[i]) > ver_cut and
                    np.abs(df['ver_rel'].iloc[i]) < ver_cut):
                sh_ver.append([df['days_diff'].iloc[i-1],
                    df['ver_rel'].iloc[i-1]])
                if be_verbose:
                    print(str(df['datetime'].iloc[i]).ljust(20),
                        'Vertical'.ljust(12),
                        str(round(df['ver_rel'].iloc[i],2)).ljust(18),
                        str(round(df['dver_raw'].iloc[i],2)))
        for i in range(len(df)):
            if (np.abs(df['dhor_raw'].iloc[i]) > hor_cut and
                    np.abs(df['hor_rel'].iloc[i]) < hor_cut):
                sh_hor.append([df['days_diff'].iloc[i-1],
                    df['hor_rel'].iloc[i-1]])
                if be_verbose:
                    print(str(df['datetime'].iloc[i]).ljust(20),
                        'Horizontal'.ljust(12),
                        str(round(df['hor_rel'].iloc[i],2)).ljust(18),
                        str(round(df['dhor_raw'].iloc[i],2)))

        for shiftinfo in sh_ver:
            df = correct_jump(df, shiftinfo[0], shiftinfo[1], 'ver')
        for shiftinfo in sh_hor:
            df = correct_jump(df, shiftinfo[0], shiftinfo[1], 'hor')

        if be_verbose:
            print("Correcting for jumps due to device reset")
            print('Number of ver jumps:', len(sh_ver))
            print('Number of hor jumps:', len(sh_hor))

    if do_correct:
        # Drop first 14 rows, where the time intervals are not regular
        ndrop = 14
        df = df.iloc[ndrop: , :]
        df['days_diff'] = df['days_diff'] - df['days_diff'].iloc[0]
        df['minutes_diff'] = df['minutes_diff'] - df['minutes_diff'].iloc[0]
        df['ver_rel'] = df['ver_rel'] - df['ver_rel'].iloc[0]
        df['hor_rel'] = df['hor_rel'] - df['hor_rel'].iloc[0]
        df.index = range(len(df))

        # Setting days_diff = 0 at the first time it is 00:00h (midnight)
        df['days_diff'] = df['days_diff'] - df['days_diff'].values[16]

    # Remove data points with very high values of RV. Before throwing them
    # out print them (if verbose)
    if be_verbose:
        print('\n=== Large RV instances ===')
        df_wrongRV = df.copy()[df['RV_avg'] > 100]
        print(df_wrongRV)

    # Only keep rows with RV values below 100%.
    df = df.copy()[df['RV_avg'] < 100]

    return df
