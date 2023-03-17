import numpy as np
from parsing import *


clean_power2MHz_df = power_parse('data/cleanStatic/cd1power2MHz.mat', norm = False)
ds2_power2MHz_df = power_parse('data/ds2/tb2power2MHz.mat',  norm = False)
ds3_power2MHz_df = power_parse('data/ds3/tb3power2MHz.mat',  norm = False)
ds7_power2MHz_df = power_parse('data/ds7/tb7power2MHz.mat',  norm = False)


# clean_power4MHz_df = power_parse('data/cleanStatic/cd1power4MHz.mat', norm = False)
# ds2_power4MHz_df = power_parse('data/ds2/tb2power4MHz.mat',  norm = False)
# ds3_power4MHz_df = power_parse('data/ds3/tb3power4MHz.mat',  norm = False)
# ds7_power4MHz_df = power_parse('data/ds7/tb7power4MHz.mat',  norm = False)


# clean_power8MHz_df = power_parse('data/cleanStatic/cd1power8MHz.mat', norm = False)
# ds2_power8MHz_df = power_parse('data/ds2/tb2power8MHz.mat',  norm = False)
# ds3_power8MHz_df = power_parse('data/ds3/tb3power8MHz.mat',  norm = False)
# ds7_power8MHz_df = power_parse('data/ds7/tb7power8MHz.mat',  norm = False)


def clean_dat_PL(df_power):
    #parameter learning via MLE
    #assuming the the signal power is a Gaussian distribution
    u = np.average(df_power['power'])
    var = np.sum([(df_power['power'].iloc[i]-u)**2 for i in range(len(df_power['power']))])/(len(df_power['power']))
    return u,var

def spoofed_PL(df_power, initial_t=0):
    t = 0; count = 1;
    moving_m = 0; moving_variance = 0;

    while df_power['time'].iloc[t]<= 60 + initial_t:
        moving_variance = ((count-1)/(count)) * (moving_variance+ ((moving_m-df_power['power'].iloc[t])**2/(count)))
        moving_m += (1/count)*(df_power['power'].iloc[t] - moving_m)
        t+=1
        count+=1

    return [moving_m, moving_variance]


def simple_H_test(df_power_test, mean, variance, m):

    h_val = np.zeros(len(df_power_test['time']))

    for i in range(len(h_val)):
        if np.abs(df_power_test['power'].iloc[i]) > mean + m*np.sqrt(variance) or np.abs(df_power_test['power'].iloc[i]) < mean - m*np.sqrt(variance):
            h_val[i] = 1

    return h_val


def power_check(clean_df, spoofed_df, parameters, plot_name, m=5, count=0):

    #data gathered thus far
    mean = parameters[0]
    variance = parameters[1]

    print(mean - m*np.sqrt(variance))
    print(mean + m*np.sqrt(variance))

    spoofed_h_test = simple_H_test(spoofed_df, mean, variance, m)

    first_one = spoofed_df['time'].iloc[np.argmax(spoofed_h_test)]
    print(f'First detection at {first_one}')

    fig = plt.figure(dpi = 500, figsize =[10 ,4.5])
    plt.plot(clean_df['time'], clean_df['power']- clean_df['power'].iloc[0] , label = 'clean', color = 'grey')
    plt.plot(spoofed_df['time'], spoofed_df['power'] - spoofed_df['power'].iloc[0] , label = 'spoofed', color = 'k')

    plt.plot(spoofed_df['time'], np.zeros(len(spoofed_df['time']))*mean + m*np.sqrt(variance), '--', color = 'tab:red', label = f'$\pm {m}\sigma$')
    plt.plot(spoofed_df['time'], np.zeros(len(spoofed_df['time']))*mean - m*np.sqrt(variance), '--', color = 'tab:red')

    plt.xlim(0,500)
    # plt.ylim(-0.3,0.2)
    plt.grid()
    plt.xlabel('RRT time (seconds)')
    plt.ylabel('Normalized Power (dB)')
    plt.legend()
    fig.savefig('figures/comparison/'+plot_name+'_power.png')

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(spoofed_df['time'], spoofed_df['power'] , label = 'Signal', color = 'k')
    axs[0].plot(spoofed_df['time'], np.ones(len(spoofed_df['time']))*mean + m*np.sqrt(variance), '--', color = 'tab:red', label = f'$\pm {m}\sigma$')
    axs[0].plot(spoofed_df['time'], np.ones(len(spoofed_df['time']))*mean - m*np.sqrt(variance), '--', color = 'tab:red')
    axs[0].set_xlim(0,500)
    axs[0].grid()
    axs[0].set_ylabel('P (dB)')
    # axs[0].legend()

    axs[1].plot(spoofed_df['time'],spoofed_h_test, '.-', markersize = 4, lw = 0.5)
    axs[1].set_xlim(0,500)
    axs[1].grid()
    axs[1].set_xlabel('RRT time (seconds)')
    axs[1].set_ylabel('Detection')
    axs[1].set_yticks(range(0,2))
    plt.show()
    fig.set_figheight(4)
    fig.set_figwidth(12)
    fig.tight_layout()
    fig.savefig('figures/comparison/'+plot_name+'_h_test.png')


# clean_mean, clean_variance = clean_dat_PL(clean_power2MHz_df)
from statistics import NormalDist
prob = 2*(NormalDist(mu =0, sigma = np.sqrt(1)).cdf(0+5*(np.sqrt(1))) - 0.5)

print(f'Interval of confidence  = {prob}')
print(f'Probability of false detection  = {1-prob}') #not the same as false positive rate


power_check(clean_power2MHz_df, ds2_power2MHz_df, spoofed_PL(ds2_power2MHz_df), '2MHz_clean_vs_ds2')
power_check(clean_power2MHz_df, ds3_power2MHz_df, spoofed_PL(ds3_power2MHz_df), '2MHz_clean_vs_ds3')
power_check(clean_power2MHz_df, ds7_power2MHz_df, spoofed_PL(ds7_power2MHz_df), '2MHz_clean_vs_ds7')

# power_check(clean_power4MHz_df, ds7_power4MHz_df, spoofed_PL(ds7_power4MHz_df), '4MHz_clean_vs_ds7')
# power_check(clean_power4MHz_df, ds2_power4MHz_df, spoofed_PL(ds2_power4MHz_df), '4MHz_clean_vs_ds2')
# power_check(clean_power4MHz_df, ds3_power4MHz_df, spoofed_PL(ds3_power4MHz_df), '4MHz_clean_vs_ds3')


# power_check(clean_power8MHz_df, ds7_power8MHz_df, spoofed_PL(ds7_power8MHz_df), '8MHz_clean_vs_ds7')
# power_check(clean_power8MHz_df, ds2_power8MHz_df, spoofed_PL(ds2_power8MHz_df), '8MHz_clean_vs_ds2')
# power_check(clean_power8MHz_df, ds3_power8MHz_df, spoofed_PL(ds3_power8MHz_df), '8MHz_clean_vs_ds3')


# get the mean and the variance from the first minute of each data set
#learn the average and variance assuming unspoofed

fig = plt.figure(dpi = 500, figsize =[10 ,5])
plt.plot(clean_power2MHz_df['time'], clean_power2MHz_df['power'] - clean_power2MHz_df['power'].iloc[0], label = 'Clean', color = 'grey')
plt.plot(ds2_power2MHz_df['time'], ds2_power2MHz_df['power'] - ds2_power2MHz_df['power'].iloc[0], label = 'Overpowered', color = 'tab:blue')
plt.plot(ds3_power2MHz_df['time'], ds3_power2MHz_df['power'] - ds3_power2MHz_df['power'].iloc[0] , label = 'Matched', color = 'tab:orange')
plt.plot(ds7_power2MHz_df['time'], ds7_power2MHz_df['power'] - ds7_power2MHz_df['power'].iloc[0] , label = 'Sophisticated', color = 'tab:green')

# plt.plot(spoofed_df['time'], np.zeros(len(spoofed_df['time']))*mean + m*np.sqrt(variance), '--', color = 'tab:red', label = f'$\pm {m}\sigma$')
# plt.plot(spoofed_df['time'], np.zeros(len(spoofed_df['time']))*mean - m*np.sqrt(variance), '--', color = 'tab:red')

plt.xlim(0,500)
# plt.ylim(-0.3,1)
plt.grid()
plt.xlabel('RRT time (seconds)')
plt.ylabel('Normalized Power (dB)')
plt.legend()
fig.savefig('figures/comparison/2Mhz_all_at_once_power.png')

# fig, axs = plt.subplots(1, 3)
# axs[0].plot(clean_power2MHz_df['time'], clean_power2MHz_df['power']- clean_power2MHz_df['power'].iloc[0] , label = 'Clean', color = 'grey')
# axs[0].plot(ds2_power2MHz_df['time'], ds2_power2MHz_df['power'] - ds2_power2MHz_df['power'].iloc[0] , label = 'Overpowered', color = 'tab:blue')
# axs[0].plot(ds3_power2MHz_df['time'], ds3_power2MHz_df['power'] - ds3_power2MHz_df['power'].iloc[0] , label = 'Matched', color = 'tab:orange')
# axs[0].plot(ds7_power2MHz_df['time'], ds7_power2MHz_df['power'] - ds7_power2MHz_df['power'].iloc[0] , label = 'FL Matched', color = 'tab:green')
# axs[0].set_xlim(0,500)
# axs[0].grid()
# axs[0].set_xlabel('RRT time (seconds)')
# axs[0].set_ylabel('Normalized Power (dB)')
# # axs[0].legend()


# axs[1].plot(clean_power4MHz_df['time'], clean_power4MHz_df['power']- clean_power4MHz_df['power'].iloc[0] , label = 'Clean', color = 'grey')
# axs[1].plot(ds2_power4MHz_df['time'], ds2_power4MHz_df['power'] - ds2_power4MHz_df['power'].iloc[0] , label = 'Overpowered', color = 'tab:blue')
# axs[1].plot(ds3_power4MHz_df['time'], ds3_power4MHz_df['power'] - ds3_power4MHz_df['power'].iloc[0] , label = 'Matched', color = 'tab:orange')
# axs[1].plot(ds7_power4MHz_df['time'], ds7_power4MHz_df['power'] - ds7_power4MHz_df['power'].iloc[0] , label = 'FL Matched', color = 'tab:green')
# axs[1].set_xlim(0,500)
# axs[1].grid()
# axs[1].set_xlabel('RRT time (seconds)')
# # axs[1].set_ylabel('Normalized Power (dB)')
# # axs[1].legend()

# axs[2].plot(clean_power8MHz_df['time'], clean_power8MHz_df['power']- clean_power8MHz_df['power'].iloc[0] , label = 'Clean', color = 'grey')
# axs[2].plot(ds2_power8MHz_df['time'], ds2_power8MHz_df['power'] - ds2_power8MHz_df['power'].iloc[0] , label = 'Overpowered', color = 'tab:blue')
# axs[2].plot(ds3_power8MHz_df['time'], ds3_power8MHz_df['power'] - ds3_power8MHz_df['power'].iloc[0] , label = 'Matched', color = 'tab:orange')
# axs[2].plot(ds7_power8MHz_df['time'], ds7_power8MHz_df['power'] - ds7_power8MHz_df['power'].iloc[0] , label = 'FL Matched', color = 'tab:green')
# axs[2].set_xlim(0,500)
# axs[2].grid()
# axs[2].set_xlabel('RRT time (seconds)')
# # axs[2].set_ylabel('Normalized Power (dB)')
# axs[2].legend(loc='right')


# fig.set_figheight(3)
# fig.set_figwidth(15)
# fig.tight_layout()
# fig.savefig('figures/comparison/all_at_once_power.png')

# # print(ds2_power2MHz_df['power'].iloc[0])
# print(ds2_power2MHz_df['power'].iloc[0])

# print(clean_power2MHz_df['power'].iloc[15])

# print(10*(np.log10((10**((ds2_power2MHz_df['power'].iloc[0]-30)/10))/0.373))+30)
# # # print()

# print(clean_power2MHz_df['time'].iloc[15])
# print(ds2_power2MHz_df['time'].iloc[0])