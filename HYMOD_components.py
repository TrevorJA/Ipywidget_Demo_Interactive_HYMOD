"""
Trevor Amestoy

Contains modular functions used in the HYMOD model.

"""

import numpy as np


def effective_rainfall(storage, c_max, b_exp, precip, PET):
    storage_previous = storage.copy()
    c_prev = c_max * (1 - (1 - ((b_exp + 1) * storage / c_max))**(1 / (b_exp + 1)))

    eff_R1 = max((precip - c_max + c_prev), 0.0)

    precip = precip - eff_R1

    dummy = min(((c_prev + precip) / c_max), 1)
    storage = (c_max / (b_exp + 1)) * (1 - (1 - dummy)**(b_exp + 1))

    eff_R2 = max(precip - (storage - storage_previous), 0.0)

    evap = (1 - (((c_max / (b_exp + 1)) - storage) / (c_max / (b_exp + 1)))) * PET
    storage = max(storage - evap, 0.0)

    return eff_R1, eff_R2, storage


def linear_reservoir(Storage, slow_inflow, Ks):
    Storage = (1 - Ks) * Storage + (1 - Ks) * slow_inflow
    outflow = (Ks / (1 - Ks)) * Storage
    return Storage, outflow


def cascading_reservoirs(Storage, quick_inflow, Kq, N_reservoirs):

    reservoir_out = np.zeros(N_reservoirs)

    # Cascade through 1 reservoir at a time
    for res in range(N_reservoirs):

        reservoir_out[res] = Kq * Storage[res]

        if res == 0:
            Storage[res] = Storage[res] - reservoir_out[res] + quick_inflow
        else:
            Storage[res] = Storage[res] - reservoir_out[res] + reservoir_out[res - 1]

    # Total quick reservoir outflow is equal to flow out of the last reservoir
    quick_outflow = reservoir_out[N_reservoirs - 1]
    return Storage, quick_outflow


def calculate_error_by_type(obs, sim, precip, error_type = 'RMSE'):
    if error_type == 'RMSE':
        return np.sqrt(np.nanmean( (sim - obs)**2 ))
    elif error_type == 'NSE':

        return (1 - np.nansum((obs - sim)**2) / (np.nansum((obs - np.nanmean(obs))**2)))
    elif error_type == 'ROCE':
        return abs((np.nanmean(sim) - np.nanmean(obs)) / np.nanmean(precip))
    else:
        print('Incorrect error type specification.')
        return


################################################################################
# The following two functions are not needed for the current HYMOD implementation,
# since evaporation data is provided.
# If using precipiration and temperature data as inputs, then these functions
# can be used to estimate evaporation.
################################################################################

def saturation_vapor_pressure(T):
    """"
    Parameters:
    -----------
    T: (int)
        Average monthly temperature (degree-C).

    Returns:
    --------
    e_sat: (int)
        Saturation vapor pressure
    """
    return (6.108 * exp((17.27 * T) / (T + 327.3)))

def hamon_pet(k, T, N = 12):
    """
    Parameters:
    ----------
    k: (int)
        Proportionality coefficient.
    N: (int)
        Daytime length (hours)
    T: (int)
        Average monthly temperature (degree-C).

    Returns:
    --------
    PET: (float)
        Potential evapotranspiration (mm/day)
    """

    e_sat = saturation_vapor_pressure(T)

    PET = k * 0.165 * 216.7 * N * (e_sat / (T + 273.3))
    return PET
