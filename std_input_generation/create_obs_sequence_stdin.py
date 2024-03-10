# create a .txt file as the input of ./create_obs_sequence program
# Usage:
# python create_obs_sequence_stdin.py
# ./create_obs_sequence < ./create_obs_sequence_stdin.txt

import os
import numpy as np

def obs_grid_tmp(lon_grid_interval: int=5, lat_grid_interval: int=5):
    """observation grid for ps (surface pressure) and t (temperature)

    Args:
        lon_grid_interval (int, optional): longitude grid interval for observation. Defaults to 5.
        lat_grid_interval (int, optional): latitude grid interval for observation. Defaults to 5.

    Returns:
        tuple[list, list]: observation grid in longitude and latitude
    """
    # longitude grids
    TmpI = [  2.99999992,   8.99999976,  14.99999959,  20.99999943,
            26.99999927,  32.99999911,  38.99999894,  44.99999878,
            50.99999862,  56.99999846,  62.99999829,  68.99999813,
            74.99999797,  80.99999781,  86.99999764,  92.99999748,
            98.99999732, 104.99999716, 110.99999699, 116.99999683,
            122.99999667, 128.99999651, 134.99999634, 140.99999618,
            146.99999602, 152.99999586, 158.99999569, 164.99999553,
            170.99999537, 176.99999521, 182.99999504, 188.99999488,
            194.99999472, 200.99999456, 206.99999439, 212.99999423,
            218.99999407, 224.99999391, 230.99999374, 236.99999358,
            242.99999342, 248.99999326, 254.99999309, 260.99999293,
            266.99999277, 272.99999261, 278.99999245, 284.99999228,
            290.99999212, 296.99999196, 302.9999918 , 308.99999163,
            314.99999147, 320.99999131, 326.99999115, 332.99999098,
            338.99999082, 344.99999066, 350.9999905 , 356.99999033]
    
    # latitude grids
    TmpJ = [-86.99999764, -80.99999781, -74.99999797, -68.99999813,
            -62.99999829, -56.99999846, -50.99999862, -44.99999878,
            -38.99999894, -32.99999911, -26.99999927, -20.99999943,
            -14.99999959,  -8.99999976,  -2.99999992,   2.99999992,
            8.99999976,  14.99999959,  20.99999943,  26.99999927,
            32.99999911,  38.99999894,  44.99999878,  50.99999862,
            56.99999846,  62.99999829,  68.99999813,  74.99999797,
            80.99999781,  86.99999764]
    
    TmpI_obs = TmpI[::lon_grid_interval] # observations evenly distribute in space
    TmpJ_obs = TmpJ[::lat_grid_interval]
    
    # print(TmpI_obs)
    # print(TmpJ_obs)
    return TmpI_obs, TmpJ_obs

def obs_grid_vel(lon_grid_interval: int=5, lat_grid_interval: int=5):
    """observation grid for velocity u and v

    Args:
        lon_grid_interval (int, optional): longitude grid interval for observation. Defaults to 5.
        lat_grid_interval (int, optional): latitude grid interval for observation. Defaults to 5.

    Returns:
        tuple[list, list]: observation grid in longitude and latitude
    """
    # longitude grids
    VelI = [  5.99999984,  11.99999968,  17.99999951,  23.99999935,
            29.99999919,  35.99999903,  41.99999886,  47.9999987 ,
            53.99999854,  59.99999838,  65.99999821,  71.99999805,
            77.99999789,  83.99999773,  89.99999756,  95.9999974 ,
            101.99999724, 107.99999708, 113.99999691, 119.99999675,
            125.99999659, 131.99999643, 137.99999626, 143.9999961 ,
            149.99999594, 155.99999578, 161.99999561, 167.99999545,
            173.99999529, 179.99999513, 185.99999496, 191.9999948 ,
            197.99999464, 203.99999448, 209.99999431, 215.99999415,
            221.99999399, 227.99999383, 233.99999366, 239.9999935 ,
            245.99999334, 251.99999318, 257.99999301, 263.99999285,
            269.99999269, 275.99999253, 281.99999236, 287.9999922 ,
            293.99999204, 299.99999188, 305.99999171, 311.99999155,
            317.99999139, 323.99999123, 329.99999106, 335.9999909 ,
            341.99999074, 347.99999058, 353.99999041, 359.99999025]
    
    # latitude grids
    VelJ = [-83.99999773, -77.99999789, -71.99999805, -65.99999821,
            -59.99999838, -53.99999854, -47.9999987 , -41.99999886,
            -35.99999903, -29.99999919, -23.99999935, -17.99999951,
            -11.99999968,  -5.99999984,   0.        ,   5.99999984,
            11.99999968,  17.99999951,  23.99999935,  29.99999919,
            35.99999903,  41.99999886,  47.9999987 ,  53.99999854,
            59.99999838,  65.99999821,  71.99999805,  77.99999789,
            83.99999773]
    
    VelI_obs = VelI[::lon_grid_interval] # observations evenly distribute in space
    VelJ_obs = VelJ[::lat_grid_interval]
    
    # print(VelI_obs)
    # print(VelJ_obs)
    return VelI_obs, VelJ_obs


def dump_obs_config(lons, lats, obs_variable, obs_variance):
    """ dump observation configurations

    Args:
        lons (list[int]): longitude grids
        lats (list[int]): latitude grids
        obs_variable (str): type of observation variable, 'ps', 't', 'u' or 'v'
        obs_variance (float): observation error variance
    """
    
    obs_variable_to_id = {
        'u': 1, 'v': 2, 'ps': 4, 't': 5,
    }
    
    for lon in lons:
        for lat in lats:
            for lev in range(5):
                # input a -1 if there are no more obs
                f.write('0\n')
                # Input the name of the observation types from table below
                # OR input (-1 * state variable index) for identity observations:
                #             1 RADIOSONDE_U_WIND_COMPONENT
                #             2 RADIOSONDE_V_WIND_COMPONENT
                #             4 RADIOSONDE_SURFACE_PRESSURE
                #             5 RADIOSONDE_TEMPERATURE
                f.write(f'{obs_variable_to_id[obs_variable]}\n')
                #  Vertical coordinate options
                #     -2  --> vertical coordinate undefined
                #     -1  --> surface
                #     1  --> model level
                #     2  --> pressure
                #     3  --> height
                #     4  --> scale height
                f.write('1\n')
                # Vertical coordinate model level
                f.write(f'{lev}\n')
                # Input longitude: value 0 to 360.0 or a negative number for 
                # Uniformly distributed random location in the horizontal
                f.write(f'{lon}\n')
                # Input latitude: value -90.0 to 90.0
                f.write(f'{lat}\n')
                # input time in days and seconds (as integers)
                f.write(f'0 0\n')
                # Input the error variance for this observation definition
                f.write(f'{obs_variance}\n')
    

if __name__ == '__main__':
    obs_var = 1.0
    number_of_obs = 6 * 12 * 4 * 10

    with open('create_obs_sequence_stdin.txt', 'w') as f:
        # Input upper bound on number of observations in sequence
        f.write(f'{number_of_obs}\n')
        # Input number of copies of data (0 for just a definition)
        f.write('0\n')
        # Input number of quality control values per field (0 or greater)
        f.write('0\n')
        
        # ps
        lons, lats = obs_grid_tmp(1, 1)
        dump_obs_config(lons, lats, 'ps', obs_var)
        dump_obs_config(lons, lats, 't', obs_var)
        vlons, vlats = obs_grid_vel(1, 1)
        dump_obs_config(vlons, vlats, 'u', obs_var)
        dump_obs_config(vlons, vlats, 'v', obs_var)
        
                
        f.write('-1\n')
        f.write('set_def.out\n')
        
        