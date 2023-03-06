import sys
from scipy.io import loadmat
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def power_parse(inputfilename, norm = True):
    """ Function to parse the power data
    Args:
        inputfilename (string): path to mat file

    Returns:
        DataFrame: parsed dataframe
    """
    power_dict = loadmat(inputfilename)
    time = power_dict['t'][0]
    data = power_dict['power'][0]

    colmn_names = ['time', 'power']
    type_specs = ['float', 'float']
    
    typ = dict(zip(colmn_names, type_specs))
    df = pd.DataFrame({'time':time, 'power':data})
    df = df.astype(typ)

    data_set = inputfilename.split('/')[1]
    power_type = inputfilename.split('/')[-1][0:9]

    if data_set == 'ds2':
        df = df[df['time']>=2.99691752].reset_index(drop=True)
        df['time'] = df['time']+df['time'][0]
    if data_set == 'ds3':
        df = df[df['time']>=2.20332084].reset_index(drop=True)
        df['time'] = df['time']+df['time'][0]

    if norm:
        df['power'] = df['power']-np.average(df['power'][0:10])

    fig = plt.figure(dpi = 500, figsize =[10 ,7])
    plt.plot(df['time'],df['power'])
    plt.xlim(0)
    plt.grid()
    plt.xlabel('RRT time (seconds)')
    plt.ylabel('$Power$ (dB)')
    # plt.ylim(-0.3,0.2)
    fig.savefig('figures/'+data_set+'/'+power_type+'_power.png')

    return df

def channel_parse(inputfilename):
    """
    ============================ channeldef.txt =================================
    This file defines the columns of data in the channel.log file produced by the
    GRID software receiver. Two types of measurement time stamps are given in
    channel.log, both corresponding to the same event, namely, the observables
    measurement event:

    (1) Raw Receiver Time (RRT): This time stamp is linked directly to the
        receiver's sampling clock.  It starts at zero when the receiver is
        initialized and is never interrupted or adjusted by the code.  RRT is
        guaranteed to be non-decreasing.  The increment between subsequent RRT
        values is only approximately uniform; it may vary by up to a few
        milliseconds as GRID adjusts its internal updates to keep all channels
        at approximately the same receiver time.

    (2) Offset Receiver Time (ORT): This time stamp is equal to RRT plus an
        offset that brings the result close (within a few ms) to true GPS
        time:

        ORT = RRT + tOffset

       GRID automatically adjusts tOffset every so often to bring ORT within a
       few ms of true GPS time.  When tOffset is adjusted, a small jump in ORT
       is introduced and concomitant shifts occur in the pseudorange and
       carrier phase data.  For maximum resolution, ORT is given in separate
       columns for week, whole second, and fractional seconds.

    =============================================================================

    Args:
        inputfilename (string): path to mat file

    Returns:
        DataFrame: parsed dataframe
    """

    channel_dict = loadmat(inputfilename)
    data = channel_dict['channel']

    colmn_names = ['RRTweek', 'RRTseconds', 'ORTweek', 
                    'ORTseconds','ORT_fract_sec', 'Doppler_f',
                    'Beat_carrier_phi', 'Pseudo_m', 'CN0',
                    'valid', 'err_id', 'status', 'type', 'TXID']

    type_specs = ['int', 'float', 'int', 'int', 'float', 'float', 'float', 'float',
            'float', 'int', 'int', 'int', 'int', 'int']
    
    typ = dict(zip(colmn_names, type_specs))

    df = pd.DataFrame(data.T, columns = colmn_names)
    df = df.astype(typ)

    data_set = inputfilename.split('/')[1]

    if data_set == 'ds2':
        df = df[df['RRTseconds']>=2.99691752].reset_index(drop=True)
        df['RRTseconds'] = df['RRTseconds']+df['RRTseconds'][0]
    if data_set == 'ds3':
        df = df[df['RRTseconds']>=2.20332084].reset_index(drop=True)
        df['RRTseconds'] = df['RRTseconds']+df['RRTseconds'][0]

    #need to take out invalid offset receiver time
    df = df[df['ORTweek']<9999].reset_index(drop=True)

    fig = plt.figure(dpi = 500, figsize =[10 ,7])
    for prn in df['TXID'].unique():
        if prn<=32:
            plt.plot(df[df['TXID'] == prn]['RRTseconds'],df[df['TXID'] == prn]['CN0'], label = f'PRN:{prn}')
    plt.legend()
    plt.grid()
    plt.xlim(0)
    plt.xlabel('RRT time (seconds)')
    plt.ylabel('$C/N_0$ (dB-Hz)')
    fig.savefig('figures/'+data_set+'/CN0.png')

    fig = plt.figure(dpi = 500, figsize =[10 ,7])
    for prn in df['TXID'].unique():
        if prn<=32:
            plt.plot(df[df['TXID'] == prn]['RRTseconds'],df[df['TXID'] == prn]['Pseudo_m'], label = f'PRN:{prn}')
    plt.legend()
    plt.grid()
    plt.xlim(0)
    plt.xlabel('RRT time (seconds)')
    plt.ylabel('Pseudorange (m)')
    fig.savefig('figures/'+data_set+'/rho_m.png')

    fig = plt.figure(dpi = 500, figsize =[10 ,7])
    for prn in df['TXID'].unique():
        if prn<=32:
            plt.plot(df[df['TXID'] == prn]['RRTseconds'],df[df['TXID'] == prn]['Doppler_f'], label = f'PRN:{prn}')
    plt.legend()
    plt.grid()
    plt.xlim(0)
    plt.xlabel('RRT time (seconds)')
    plt.ylabel('Doppler Frequency (Hz)')
    fig.savefig('figures/'+data_set+'/dopp_f.png')

    fig = plt.figure(dpi = 500, figsize =[10 ,7])
    for prn in df['TXID'].unique():
        if prn<=32:
            plt.plot(df[df['TXID'] == prn]['RRTseconds'],df[df['TXID'] == prn]['Beat_carrier_phi'], label = f'PRN:{prn}')
    plt.legend()
    plt.grid()
    plt.xlim(0)
    plt.xlabel('RRT time (seconds)')
    plt.ylabel('Carrier Phase (cycles)')
    fig.savefig('figures/'+data_set+'/phi_cycles.png')

    
    return df

def navsol_parse(inputfilename):
    """
    ============================ navsoldef.txt ==================================
    This file defines the columns of data in the navsol.log files produced by the
    GRID software receiver. Each navsol.log file contains time-stamped navigation
    solutions that represent the receiver's best estimate of position, velocity,
    receiver clock error, and receiver clock error rate as calculated from data
    provided by all participating receiver banks.  See channeldef.txt for a
    definition of ORT.  ORT time stamps indicate the time at which the navigation
    solution applies.
    =============================================================================

    Args:
        inputfilename (string): path to mat file

    Returns:
        DataFrame: parsed dataframe
    """
    nav_dict = loadmat(inputfilename)
    data = nav_dict['navsol']

    colmn_names = ['ORTweek', 'ORTseconds','ORT_fract_sec', 'x_recv', 'y_recv', 'z_recv',
                    'deltR', 'xdot_recv', 'ydot_recv', 'zdot_recv', 'deltRdot',
                    'sol_flag']

    type_specs = ['int', 'int', 'float', 'float', 'float', 'float', 'float',
            'float', 'float', 'float', 'float', 'int']
    
    typ = dict(zip(colmn_names, type_specs))

    df = pd.DataFrame(data.T, columns = colmn_names)
    df = df.astype(typ)

    return df

def iq_parse(inputfilename):
    """
    =============================== iqdef.txt ===================================
    This file defines the columns of data in the iq.log files produced by the GRID
    software receiver.  The iq.log files contain high-rate in-phase and quadrature
    symaccumulation and beat carrier phase data.  A symaccumulation is a coherent
    accumulation that is time-aligned with data modulation (if any) and of length
    equal to the minimum of the symbol interval and the standard accumulation
    interval.  See channeldef.txt for definitions of RRT and ORT.  Time stamps in
    RRT and ORT correspond to the end of the interval over which each in-phase and
    quadrature accumulation was computed.
    =============================================================================

    Args:
        inputfilename (string): path to mat file

    Returns:
        DataFrame: parsed dataframe
    """
    iq_dict = loadmat(inputfilename)
    data = iq_dict['iq']

    colmn_names = ['RRTweek', 'RRTseconds', 'ORTweek', 
                    'ORTseconds','ORT_fract_sec', 'Beat_carrier_phi', 
                    'in_phase_acc', 'quad_acc',
                    'data_symbol', 'type', 'TXID']

    type_specs = ['int', 'float', 'int', 'int', 'float', 'float', 
                  'float', 'float', 'int', 'int', 'int']
    
    typ = dict(zip(colmn_names, type_specs))

    df = pd.DataFrame(data.T, columns = colmn_names)
    df = df.astype(typ)

    return df

def iq_taps_parse(inputfilename):
    """
    ============================= iqtapsdef.txt =================================
    This file defines the columns of data in the iqtaps.log files produced by the
    GRID software receiver.  The iqtaps.log files contain symaccumulation-length
    in-phase and quadrature symaccumulation data. A symaccumulation is a coherent
    accumulation that is time-aligned with data modulation (if any) and of length
    equal to the minimum of the symbol interval and the standard accumulation
    interval. See channeldef.txt for a definition of RRT.  Time stamps in RRT
    correspond to the end of the interval over which each in-phase and quadrature
    symaccumulation was computed.
    =============================================================================

    Args:
        inputfilename (string): path to mat file

    Returns:
        DataFrame: parsed dataframe
    """
    iq_dict = loadmat(inputfilename)
    data = iq_dict['iqtaps']

    phase_taps = [f'phase_tap_{i}' for i in range(int((data.shape[0]-4)/2))]
    quad_taps = [f'quad_tap_{i}' for i in range(int((data.shape[0]-4)/2))]

    colmn_names = ['RRTweek', 'RRTseconds', 'type', 'TXID']+phase_taps+quad_taps

    # type_specs = ['int', 'float', 'int', 'int', ]
    
    # typ = dict(zip(colmn_names, type_specs))

    df = pd.DataFrame(data.T, columns = colmn_names)

    # df = df.astype(typ)

    return df

def txinfo_parse(inputfilename):
    """
    ============================ txinfodef.txt ==================================
    This file defines the columns of data in the txinfo.log files produced by the
    GRID software receiver.  Each txinfo.log file contains time-stamped
    transmitter information in the form of azimuth angle, elevation angle, and
    health status for tracked transmitters. See channeldef.txt for a definition of
    ORT.  ORT time stamps indicate the time at which the transmitter information
    applies.
    =============================================================================

    Args:
        inputfilename (string): path to mat file

    Returns:
        DataFrame: parsed dataframe
    """
    txinfo_dict = loadmat(inputfilename)
    data = txinfo_dict['txinfo']

    colmn_names = ['ORTweek', 'ORTseconds','ORT_fract_sec', 'azimuth', 
                    'elevation', 'health',
                    'sys','TXID']

    type_specs = ['int', 'int', 'float', 'float', 
                  'float', 'int', 'int', 'int']
    
    typ = dict(zip(colmn_names, type_specs))

    df = pd.DataFrame(data.T, columns = colmn_names)
    df = df.astype(typ)

    return df


def main():
    if len(sys.argv) != 2:
        raise Exception("usage: python parse.py <folder with data>")

    #parse arguments provided
    inputfolder = sys.argv[1]

    ###have no clue what's inside the symmdiff

    for filename in os.listdir(inputfolder):
        f = os.path.join(inputfolder, filename)

        if f.split('/')[-1] == 'txinfo.mat':
            txinfo_df = txinfo_parse(f)
            prn_list = txinfo_df[txinfo_df['sys'] == 0]['TXID'].unique()
        
        # elif f.split('/')[-1] == 'navsol.mat':
        #     navsol_df = navsol_parse(f)
        
        elif f.split('/')[-1] == 'channel.mat':
            channel_df = channel_parse(f)

        # elif f.split('/')[-1] == 'iq.mat':
        #     iq_df = iq_parse(f)

        # elif f.split('/')[-1] == 'iqtaps.mat':
        #     iq_taps_df = iq_taps_parse(f)

        elif f.split('/')[-1][-len('power2MHz.mat'):] == 'power2MHz.mat':
            power2MHz_df = power_parse(f)

        elif f.split('/')[-1][-len('power4MHz.mat'):] == 'power4MHz.mat':
            power4MHz_df = power_parse(f)

        elif f.split('/')[-1][-len('power8MHz.mat'):] == 'power8MHz.mat':
            power8MHz_df = power_parse(f)

        else:
            print(f'Cannot parse {f}')


    # The overall power of the clean static scenario was also found to be 8.6 dB 
    # higher than the pre-spoofing part of the spoofed scenarios. 
    # An amplitude correction factor was found empirically to be 0.373. 
    # Multiplication of the clean static scenario by this factor will scale the 
    # raw signal and noise power in the sampled data to match that recorded in the spoofing scenario files. 
    # Scenarios seven, eight, and the clean static sce- nario should be multiplied by this correction factor 
    # to eliminate the increased signal and noise power relative to Scenarios 1-4.


if __name__ == '__main__':

    main()
