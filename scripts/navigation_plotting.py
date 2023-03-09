import numpy as np
from parsing import *


def navplot(clean_df,spoofed_df, plot_name):

    c = 299792458 #m/s
    clean_time = clean_df['ORTseconds']+clean_df['ORT_fract_sec']
    spoofed_time = spoofed_df['ORTseconds']+spoofed_df['ORT_fract_sec']

    clean_x_mean = np.mean(clean_df['x_recv'][0:100])
    clean_y_mean = np.mean(clean_df['y_recv'][0:100])
    clean_z_mean = np.mean(clean_df['z_recv'][0:100])
    clean_b_mean = np.mean(clean_df['deltR'])

    # spoofed_x_mean = np.mean(spoofed_df['x_recv'])
    # spoofed_y_mean = np.mean(spoofed_df['y_recv'])
    # spoofed_z_mean = np.mean(spoofed_df['z_recv'])

    fig = plt.figure(dpi = 500, figsize =[10 ,4.5])
    plt.plot(clean_time, clean_df['x_recv'], label = 'clean', color = 'grey')
    # plt.plot(spoofed_time, spoofed_df['x_recv']-clean_x_mean, label = 'spoofed', color = 'k')
    plt.xlim(spoofed_time[0])
    # plt.ylim(-10,10)
    plt.grid()
    plt.xlabel('Time (seconds)')
    plt.ylabel('$\Delta x$ (m)')
    plt.legend()
    fig.savefig('figures/comparison/'+plot_name+'_nav_x.png')

    fig = plt.figure(dpi = 500, figsize =[10 ,4.5])
    plt.plot(clean_time, clean_df['y_recv'], label = 'clean', color = 'grey')
    # plt.plot(spoofed_time, spoofed_df['y_recv']-clean_y_mean, label = 'spoofed', color = 'k')
    plt.xlim(spoofed_time[0])
    # plt.ylim(-10,10)
    plt.grid()
    plt.xlabel('Time (seconds)')
    plt.ylabel('$\Delta y$ (m)')
    plt.legend()
    fig.savefig('figures/comparison/'+plot_name+'_nav_y.png')

    fig = plt.figure(dpi = 500, figsize =[10 ,4.5])
    plt.plot(clean_time, clean_df['z_recv'], label = 'clean', color = 'grey')
    # plt.plot(spoofed_time, spoofed_df['z_recv'] - clean_z_mean, label = 'spoofed', color = 'k')
    plt.xlim(spoofed_time[0])
    # plt.ylim(-10,10)
    plt.grid()
    plt.xlabel('Time (seconds)')
    plt.ylabel('$\Delta z$ (m)')
    plt.legend()
    fig.savefig('figures/comparison/'+plot_name+'_nav_z.png')


    fig = plt.figure(dpi = 500, figsize =[10 ,4.5])
    plt.plot(clean_time, clean_df['deltR']-clean_b_mean, label = 'clean', color = 'grey')
    # plt.plot(spoofed_time, spoofed_df['deltR']-clean_b_mean, label = 'spoofed', color = 'k')
    plt.xlim(spoofed_time[0])
    # plt.ylim(-10,10)
    plt.grid()
    plt.xlabel('Time (seconds)')
    plt.ylabel('$\Delta t$ (m)')
    plt.legend()
    fig.savefig('figures/comparison/'+plot_name+'clock_bias.png')


clean_df = navsol_parse('data/cleanStatic/navsol.mat')
ds2_df = navsol_parse('data/ds2/navsol.mat')
ds3_df = navsol_parse('data/ds3/navsol.mat')
ds7_df = navsol_parse('data/ds7/navsol.mat')


print(clean_df)
# print(ds2_df['sol_flag'].unique())

navplot(clean_df,ds2_df, 'clean_vs_ds2')
navplot(clean_df,ds3_df, 'clean_vs_ds3')
navplot(clean_df,ds7_df, 'clean_vs_ds7')

# 1 ----------- ORT week number. 

# 2 ----------- ORT whole seconds of week.

# 3 ----------- ORT fractional second. 

# 4,5,6 ------- X,Y,Z receiver antenna position expressed in meters the ECEF
#               reference frame.

# 7 ----------- deltR, the receiver clock error expressed in equivalent meters.
#               True GPS time (TGT) is related to deltR by TGT = ORT - deltR/c.