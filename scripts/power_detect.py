import numpy as np
from parsing import *


clean_power2MHz_df = power_parse('data/cleanStatic/cd1power2MHz.mat', norm = False)
ds2_power2MHz_df = power_parse('data/ds2/tb2power2MHz.mat',  norm = False)
ds3_power2MHz_df = power_parse('data/ds3/tb3power2MHz.mat',  norm = False)
ds7_power2MHz_df = power_parse('data/ds7/tb7power2MHz.mat',  norm = False)


def clean_dat_PL(df_power):
    #parameter learning via MLE
    #assuming the the signal power is a Gaussian distribution
    u = np.average(df_power['power'])
    var = np.sum([(df_power['power'].iloc[i]-u)**2 for i in range(len(df_power['power']))])/(len(df_power['power']))
    return u,var

def spoofed_mean(df_power):
    u = np.average(df_power['power'][0:400])
    return u

def simple_H_test(df_power_test, v_t):

    h_val = np.zeros(len(df_power_test['time']))

    for i in range(len(h_val)):
        if np.abs(df_power_test['power'].iloc[i]) > v_t:
            h_val[i] = 1

    return h_val


def power_check_plots(clean_df, spoofed_df, mean, variance, plot_name):

    spoofed_h_test = simple_H_test(spoofed_df, mean + 4*np.sqrt(variance))
    first_one = spoofed_df['time'].iloc[np.argmax(spoofed_h_test)]
    print(f'First detection at {first_one}')

    fig = plt.figure(dpi = 500, figsize =[10 ,4.5])
    plt.plot(clean_df['time'], clean_df['power']- clean_df['power'][0] , label = 'clean', color = 'grey')
    plt.plot(spoofed_df['time'], spoofed_df['power'] - spoofed_df['power'][0] , label = 'spoofed', color = 'k')

    plt.plot(clean_df['time'], np.zeros(len(clean_df['time']))*mean + 4*np.sqrt(variance), '--', color = 'tab:red', label = '$\pm 4\sigma$')
    plt.plot(clean_df['time'], np.zeros(len(clean_df['time']))*mean - 4*np.sqrt(variance), '--', color = 'tab:red')

    plt.xlim(0,500)
    # plt.ylim(-0.3,0.2)
    plt.grid()
    plt.xlabel('RRT time (seconds)')
    plt.ylabel('Normalized Power (dB)')
    plt.legend()
    fig.savefig('figures/comparison/'+plot_name+'_power.png')

    fig, axs = plt.subplots(2, 1)

    axs[0].plot(spoofed_df['time'], spoofed_df['power'] , label = 'ds7', color = 'k')
    axs[0].plot(clean_df['time'], np.ones(len(clean_df['time']))*mean + 4*np.sqrt(variance), '--', color = 'tab:red', label = '$\pm 4\sigma$')
    axs[0].plot(clean_df['time'], np.ones(len(clean_df['time']))*mean - 4*np.sqrt(variance), '--', color = 'tab:red')
    axs[0].set_xlim(0,500)
    axs[0].grid()
    axs[0].set_ylabel('P (dB)')
    axs[0].legend()

    axs[1].plot(spoofed_df['time'],spoofed_h_test, '.-', markersize = 4, lw = 0.5)
    axs[1].set_xlim(0,500)
    axs[1].grid()
    axs[1].set_xlabel('RRT time (seconds)')
    axs[1].set_ylabel('Detection')
    axs[1].set_yticks(range(0,2))
    fig.set_figheight(6)
    fig.set_figwidth(10)
    fig.tight_layout()
    fig.savefig('figures/comparison/'+plot_name+'_h_test.png')


clean_mean, clean_variance = clean_dat_PL(clean_power2MHz_df)
from statistics import NormalDist
prob = 2*(NormalDist(mu =clean_mean, sigma = np.sqrt(clean_variance)).cdf(clean_mean+4*(np.sqrt(clean_variance))) - 0.5)
print(f'Interval of confidence  = {prob}')
print(f'Probability of false detection  = {1-prob}') #not the same as false positive rate


power_check_plots(clean_power2MHz_df, ds7_power2MHz_df, clean_mean, clean_variance, 'clean_vs_ds7')
power_check_plots(clean_power2MHz_df, ds2_power2MHz_df, spoofed_mean(ds2_power2MHz_df), clean_variance, 'clean_vs_ds2')
power_check_plots(clean_power2MHz_df, ds3_power2MHz_df, spoofed_mean(ds3_power2MHz_df), clean_variance, 'clean_vs_ds3')

# power_check_plots(clean_power2MHz_df, ds7_power2MHz_df, clean_mean, clean_variance, 'clean_vs_ds7')