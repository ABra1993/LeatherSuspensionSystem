# Generate figure 7
# Sarah Brands & Amber Brands
# Created November 2022; Last edited May 2023

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import read_data

global plotdir
plotdir = '../plots/'

color_ver = 'red'
color_hor = 'dodgerblue'
color_RH = '#ffb300'

def main():

    # import data
    df = read_data.data2df(do_correct=True, be_verbose=False)

    df['ver_perc'] = df['ver_rel']/3000*100
    df['hor_perc'] = df['hor_rel']/2400*100

    df['ver_perc'] = df['ver_perc'] - np.min(df['ver_perc'])
    df['hor_perc'] = df['hor_perc'] - np.min(df['hor_perc'])

    """ 2 panels: overplot temperature/humidity and
    horizontal/vertical expansion"""
    overplot_temp_hum_stretch(df, savefig=True)

def overplot_temp_hum_stretch(df, savefig, figname=''):

    # Initiate figure
    fig = plt.figure(figsize=(8, 6))
    gs = fig.add_gridspec(9, 10)
    ax = dict()

    # Create subplots
    axs1 = fig.add_subplot(gs[0:4, 0:10])
    axs22 = fig.add_subplot(gs[6:10, 0:4])
    axs21 = fig.add_subplot(gs[6:10, 6:10])

    ax = plt.gca()
    ms = 0.5
    alpha = 0.1

    ax12 =  axs1.twinx()
    axs1.plot(df['days_diff'], df['RV_avg'], marker='o', ms=ms, lw=0,
        color=color_RH, label='Relative Humidity')
    ax12.plot(df['days_diff'], df['ver_rel'], marker='o', ms=ms, lw=0,
        color=color_ver, label='Vertical replacement')
    ax12.plot(df['days_diff'], df['hor_rel'], marker='o', ms=ms, lw=0,
        color=color_hor, label='Horizontal replacement')
    ax12.set_ylabel('Displacement (mm)')
    axs1.set_ylabel('Relative Humidity (%)')

    han1, lab1 = axs1.get_legend_handles_labels()
    han2, lab2 = ax12.get_legend_handles_labels()
    lgnd1 = axs1.legend(han1+han2, lab1+lab2, loc='lower center')

    df['only_dates'] = pd.to_datetime(df['datetime']).dt.date

    df_datetime = df.datetime
    month_start = pd.DatetimeIndex(df_datetime).is_month_start

    date_labels = []
    date_labels_str = []
    for rowi in range(len(month_start)):
        if month_start[rowi]:
            date_labels.append(df['days_diff'].iloc[rowi])
            date_labels_str.append(df['datetime'].iloc[rowi].strftime('%-d %b %Y'))
    date_labels_str, unique_args = np.unique(date_labels_str, return_index=True)
    date_labels_unique = []
    for iarg in unique_args:
        date_labels_unique.append(date_labels[iarg])

    index = np.where(month_start)
    start_indices = [0, index[0][0]]
    for i in range(1, len(index[0])):
        if int(index[0][i] - 1) != int(index[0][i-1]):
            start_indices.append(index[0][i])
    start_indices.append(len(df)-1)

    axs1.set_xticks(date_labels_unique)
    axs1.set_xticklabels(date_labels_str, rotation=45, ha='right')

    colors = ['grey', 'lightgrey']
    for i in range(len(start_indices)-1):
        if i % 2 == 0:
            axs1.axvspan(df.loc[start_indices[i], 'days_diff'],
                df.loc[start_indices[i+1], 'days_diff'],
                color=colors[0], alpha=alpha)
        else:
            axs1.axvspan(df.loc[start_indices[i], 'days_diff'],
                df.loc[start_indices[i+1], 'days_diff'],
                color=colors[1], alpha=alpha)

    axs1.set_xlim(np.min(df['days_diff']), np.max(df['days_diff']))

    # Change the marker size manually for both lines
    for i in range(len(lgnd1.legendHandles)):
        lgnd1.legendHandles[i]._legmarker.set_markersize(3)

    start = 4020
    end = 4200
    ms = 2.5

    ax212 = axs21.twinx()
    axs21.plot(df['days_diff'][start:end], df['RV_avg'][start:end],
        marker='o', ms=ms, lw=0, color=color_RH, label='Relative Humidity')
    ax212.plot(df['days_diff'][start:end], df['ver_rel'][start:end],
        marker='o', ms=ms, lw=0, color=color_ver, label='Vertical replacement')
    ax212.plot(df['days_diff'][start:end], df['hor_rel'][start:end],
        marker='o', ms=ms, lw=0, color=color_hor, label='Horizontal replacement')
    ax212.set_ylabel('Displacement (mm)')
    axs21.set_ylabel('Relative Humidity (%)')

    ax.set_xlim(83.4, 84.2)
    df_ticks_ax21 = df.copy().iloc[[4024, 4032, 4040, 4048, 4056]]


    axs21.set_xticks(df_ticks_ax21['days_diff'])
    axs21.set_xticklabels(df_ticks_ax21['datetime'].dt.strftime('%-d %b %H:%M'),
        rotation=45, ha='right')

    start = 4020
    end = 4200
    ms = 1.5

    ax222 = axs22.twinx()
    axs22.plot(df['days_diff'][start:end], df['RV_avg'][start:end],
        marker='o', ms=ms, lw=0, color=color_RH, label='Relative Humidity')
    ax222.plot(df['days_diff'][start:end], df['ver_rel'][start:end],
        marker='o', ms=ms, lw=0, color=color_ver, label='Vertical replacement')
    ax222.plot(df['days_diff'][start:end], df['hor_rel'][start:end],
        marker='o', ms=ms, lw=0, color=color_hor, label='Horizontal replacement')
    ax222.set_ylabel('Displacement (mm)')#, fontsize=8)
    axs22.set_ylabel('Relative Humidity (%)')#, fontsize=8)

    df_ticks_ax22 = df.copy().iloc[[4048, 4096,4144, 4192]]
    axs22.set_xticks(df_ticks_ax22['days_diff'])
    axs22.set_xticklabels(df_ticks_ax22['datetime'].dt.strftime('%-d %b'),
        rotation=45, ha='right')

    ylimdiff_hum_main = axs1.get_ylim()[1] - axs1.get_ylim()[0]
    ylimdiff_dis_main = ax12.get_ylim()[1] - ax12.get_ylim()[0]
    ratio_ylim_main = ylimdiff_hum_main / ylimdiff_dis_main
    zeropoint = axs1.get_ylim()[0]/ratio_ylim_main

    axs1.text(0.015,0.95,'a)', transform=axs1.transAxes,
        ha='left', va='top', size=13)
    axs22.text(0.03,0.95,'b)', transform=axs22.transAxes,
        ha='left', va='top', size=13)
    axs21.text(0.03,0.95,'c)', transform=axs21.transAxes,
        ha='left', va='top', size=13)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15, top=0.98, left=0.10, right=0.90)

    if savefig:
        if figname == '':
            figname = 'fig7_mm.png'
        plt.savefig(plotdir + figname, dpi=300)

    plt.show()

if __name__ == '__main__':
    main()
