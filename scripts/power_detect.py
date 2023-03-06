import numpy as np
from parsing import *


clean_power2MHz_df = power_parse('data/cleanStatic/cd1power2MHz.mat', norm = False)
ds2_power2MHz_df = power_parse('data/ds2/tb2power2MHz.mat',  norm = False)
ds3_power2MHz_df = power_parse('data/ds3/tb3power2MHz.mat',  norm = False)
ds7_power2MHz_df = power_parse('data/ds7/tb7power2MHz.mat',  norm = False)


def clean_dat_PL(df_power):
    #parameter learning via MLE
    u = np.average(df_power['power'])
    var = np.sum([(df_power['power'].iloc[i]-u)**2 for i in range(len(df_power['power']))])/(len(df_power['power']))

    return [u,var]



print(clean_dat_PL(clean_power2MHz_df))
print(np.var(clean_power2MHz_df['power']))

# fig = plt.figure(dpi = 500, figsize =[10 ,7])
# plt.plot(clean_power2MHz_df['time'], clean_power2MHz_df['power'], label = 'clean')
# plt.plot(ds2_power2MHz_df['time'],ds2_power2MHz_df['power'], label = 'ds2')
# plt.plot(ds3_power2MHz_df['time'],ds3_power2MHz_df['power'], label = 'ds3')
# plt.plot(ds7_power2MHz_df['time'],ds7_power2MHz_df['power'], label = 'ds7')
# # plt.xlim(0,100)
# # plt.ylim(8,9)
# plt.grid()
# plt.xlabel('RRT time (seconds)')
# plt.ylabel('Power (dB)')
# plt.legend()
# fig.savefig('figures/comparison/power.png')