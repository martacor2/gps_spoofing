import sys
from scipy.io import loadmat
import pandas as pd

def channel_parse(inputfilename):

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

    return df

def navsol_parse(inputfilename):

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

# def symmdiff(inputfilename):

#     symmdiff_dict = loadmat(inputfilename)
#     data = symmdiff_dict['symmdiff']

#     pass

#     # colmn_names = ['RRTweek', 'RRTseconds', 'ORTweek', 
#     #                 'ORTseconds','ORT_fract_sec', 'Beat_carrier_phi', 
#     #                 'in_phase_acc', 'quad_acc',
#     #                 'data_symbol', 'type', 'TXID']

#     # type_specs = ['int', 'float', 'int', 'int', 'float', 'float', 
#     #               'float', 'float', 'int', 'int', 'int']
    
#     # typ = dict(zip(colmn_names, type_specs))

#     # df = pd.DataFrame(data.T, columns = colmn_names)
#     # df = df.astype(typ)

#     # return df

def txinfo_parse(inputfilename):
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
        raise Exception("usage: python parse.py <infile>.mat")

    #parse arguments provided
    inputfilename = sys.argv[1]


    # channel_dict = channel_parse(inputfilename)

    print(iq_parse(inputfilename))

    # if inputfilename == 'data/medium.csv':
    #     df_out = medium_learning(inputfilename)
    #     policy_file(df_out,outputfilename)

    # if inputfilename == 'data/large.csv':
    #     df_out = large_learning(inputfilename)
    #     # policy_file(df_out,outputfilename)

if __name__ == '__main__':
    main()
