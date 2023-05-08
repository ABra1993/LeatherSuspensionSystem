# Generate figure 8
# Sarah Brands & Amber Brands
# Created November 2022; Last edited May 2023

import numpy as np
import pandas as pd
import read_data
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def main():
    # import data
    df = read_data.data2df(do_correct=True, be_verbose=False)

    # Convert to percentages
    # Horizontal size of leather: 2400 mm
    # Vertical size of leather: 3000 mm

    hor_totsize = 2400
    ver_totsize = 3000
    df['ver_perc'] = df['ver_rel']/ver_totsize*100
    df['hor_perc'] = df['hor_rel']/hor_totsize*100

    df['ver_perc'] = df['ver_perc'] - np.min(df['ver_perc'])
    df['hor_perc'] = df['hor_perc'] - np.min(df['hor_perc'])


    # Compute the percentual change at a difference of 40% Relative Humidity

    minRV = 39
    maxRV = 80

    diffRV = maxRV - minRV
    deltaRV = 1.0
    nsteps = int(diffRV/deltaRV)
    linRV = np.linspace(minRV, maxRV-deltaRV, nsteps) + deltaRV
    nsig = 2

    hor_avg = []
    hor_std = []
    ver_avg = []
    ver_std = []
    for the_min in linRV:
        df_tmp = df.copy()[(df['RV_avg'] > the_min - 0.5*deltaRV) & (df['RV_avg'] < the_min + 0.5*deltaRV)]
        hor_avg.append(np.mean(df_tmp['hor_perc']))
        hor_std.append(np.std(df_tmp['hor_perc'])*nsig)
        ver_avg.append(np.mean(df_tmp['ver_perc']))
        ver_std.append(np.std(df_tmp['ver_perc'])*nsig)
    mean_std_hor = np.mean(hor_std)
    mean_std_ver = np.mean(ver_std)

    print('mean_std_hor', mean_std_hor)
    print('mean_std_ver', mean_std_ver)

    hor_avg_40 = hor_avg[0]
    hor_avg_80 = hor_avg[-1]
    ver_avg_40 = ver_avg[0]
    ver_avg_80 = ver_avg[-1]

    disp_hor = hor_avg_80 - hor_avg_40
    disp_ver = ver_avg_80 - ver_avg_40

    print('Horizontal displacement at 40% difference', round(disp_hor,2), '+/-', round(np.sqrt(mean_std_hor**2+ mean_std_hor**2),2))
    print('Vertical   displacement at 40% difference', round(disp_ver,2), '+/-', round(np.sqrt(mean_std_ver**2+ mean_std_ver**2),2))

    df['hor_perc_roll_month'] = df['hor_perc'].rolling(48*30).mean()
    df['hor_perc_roll_6h'] = df['hor_perc'].rolling(12).mean()
    df['ver_perc_roll_month'] = df['ver_perc'].rolling(48*30).mean()
    df['ver_perc_roll_6h'] = df['ver_perc'].rolling(12).mean()

    df['delta_roll_hor_month'] = df['hor_perc'] - df['hor_perc_roll_month']
    df['delta_roll_ver_month'] = df['ver_perc'] - df['ver_perc_roll_month']
    df['delta_roll_hor_6h'] = df['hor_perc'] - df['hor_perc_roll_6h']
    df['delta_roll_ver_6h'] = df['ver_perc'] - df['ver_perc_roll_6h']

    # Define custom color map
    colors= ['#011947', 'darkblue', '#3561e6', 'lightblue', 'pink', 'red', 'darkred']
    my_cm = LinearSegmentedColormap.from_list(
            "Custom", colors, N=100)

    # Create scatter plots
    fig, ax = plt.subplots(2,2, figsize=(7.5,6.5), sharey='row', sharex='row')
    savescat = []
    for i in (0,1):
        if i == 0:
            thes = 3
            the_col_ver = df['delta_roll_hor_month']
            the_col_hor = df['delta_roll_ver_month']
            the_vmin = -0.08
            the_vmax = 0.08
            the_cmap = 'viridis'
        elif i == 1:
            thes = 10
            the_col_ver = df['delta_roll_hor_6h']
            the_col_hor = df['delta_roll_ver_6h']
            the_vmin = -0.01
            the_vmax = 0.01
            the_cmap = my_cm

        ax[i,0].scatter(df['RV_avg'], df['hor_perc'], s=thes, c=the_col_hor,
            vmin=the_vmin, vmax=the_vmax,
            alpha=1.0, label='Single\nobservation', cmap=the_cmap)

        scat0 = ax[i,1].scatter(df['RV_avg'], df['ver_perc'], s=thes, c=the_col_ver,
            vmin=the_vmin, vmax=the_vmax,
            alpha=1.0, label='Single\nobservation', cmap=the_cmap)

        savescat.append(scat0)

        ax[i,0].set_xlabel('Relative Humidity (%)')
        ax[i,1].set_xlabel('Relative Humidity (%)')
        ax[i,0].set_ylabel('Displacement (%)')

    # Add color bars

    cbax = fig.add_axes([0.87, 0.55, 0.022, 0.35])
    cbar = plt.colorbar(savescat[0], cax = cbax, orientation='vertical',
        ticks=[-0.08, -0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, 0.08])
    cbar.ax.set_yticklabels([r'$\leq$ -0.08', -0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, r'$\geq$ 0.08'])
    cbar.ax.set_title(r'$\Delta$' +' RH\n(30 days)', fontsize=10.5)
    cbar.ax.text(-1.5,0.55,r'$\rightarrow$ Adsorption',
        transform=cbar.ax.transAxes,rotation=90, size=11)
    cbar.ax.text(-1.5,0.45,r' Desorption $\leftarrow$',
        va='top', transform=cbar.ax.transAxes,rotation=90, size=11)

    cbax = fig.add_axes([0.87, 0.08, 0.022, 0.35])
    cbar = plt.colorbar(savescat[1], cax = cbax, orientation='vertical',
        ticks=[-0.010, -0.005, 0.0, 0.005, 0.010])
    cbar.ax.set_yticklabels([r'$\leq$ -0.01', -0.005, 0.0, 0.005, r'$\geq$ 0.01'])
    cbar.ax.set_title(r'$\Delta$' +' RH\n(6 hours)', fontsize=10.5)
    cbar.ax.text(-1.5,0.55,r'$\rightarrow$ Adsorption',
        transform=cbar.ax.transAxes,rotation=90, size=11)
    cbar.ax.text(-1.5,0.45,r' Desorption $\leftarrow$',
        va='top', transform=cbar.ax.transAxes,rotation=90, size=11)

    # Set axis limits, title and panel names

    ax[1,0].set_xlim(59.5,68.9)
    ax[1,0].set_ylim(0.25,0.37)
    ax[1,1].set_xlim(59.5,68.9)
    ax[1,1].set_ylim(0.25,0.37)

    ax[0,0].set_title('Horizontal', size=11)
    ax[0,1].set_title('Vertical', size=11)

    ax[0,0].text(0.025, 0.975, 'a)', transform=ax[0,0].transAxes, ha='left', va='top')
    ax[0,1].text(0.025, 0.975, 'b)', transform=ax[0,1].transAxes, ha='left', va='top')
    ax[1,0].text(0.025, 0.975, 'c)', transform=ax[1,0].transAxes, ha='left', va='top')
    ax[1,1].text(0.025, 0.975, 'd)', transform=ax[1,1].transAxes, ha='left', va='top')
    plt.tight_layout()
    plt.subplots_adjust(right=0.78)

    # Add bars that indicate the size in mm for each plot.

    the_mm_color = '#454545'

    mm_ind_len_hor = 2.0 # mm
    mm_ind_len_ver = 2.0 # mm
    errorbar_hor = mm_ind_len_hor/hor_totsize*100/2.0
    errorbar_ver = mm_ind_len_ver/ver_totsize*100/2.0

    ax[0,0].errorbar([65], [0.10], [errorbar_hor],
        capsize=5, elinewidth=1, fmt='o', ms=0, color=the_mm_color)
    ax[0,0].text(65, 0.10, '  ' + str(mm_ind_len_hor) + ' mm',
        ha='left', va='center', color=the_mm_color)
    ax[0,1].errorbar([65], [0.10], [errorbar_ver],
        capsize=5, elinewidth=1, fmt='o', ms=0, color=the_mm_color)
    ax[0,1].text(65, 0.10, '  ' + str(mm_ind_len_ver) + ' mm',
        ha='left', va='center', color=the_mm_color)

    mm_ind_len_hor = 0.5 # mm
    mm_ind_len_ver = 0.5 # mm
    errorbar_hor = mm_ind_len_hor/hor_totsize*100/2.0
    errorbar_ver = mm_ind_len_ver/ver_totsize*100/2.0

    ax[1,0].errorbar([66.4], [0.27], [errorbar_hor],
        capsize=5, elinewidth=1, fmt='o', ms=0, color=the_mm_color)
    ax[1,0].text(66.4, 0.27, '  ' + str(mm_ind_len_hor) + ' mm',
        ha='left', va='center', color=the_mm_color)
    ax[1,1].errorbar([66.3], [0.27], [errorbar_ver],
        capsize=5, elinewidth=1, fmt='o', ms=0, color=the_mm_color)
    ax[1,1].text(66.3, 0.27, '  ' + str(mm_ind_len_ver) + ' mm',
        ha='left', va='center', color=the_mm_color)

    plt.savefig('../plots/fig8_perc_mm.png', dpi=300)

    plt.show()

if __name__ == '__main__':
    main()
