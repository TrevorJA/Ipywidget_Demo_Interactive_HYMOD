"""
Trevor Amestoy
Summer 2022

Contains an implementation of the HYMOD model, designed to be used
with an interactive ipywidget.

HYMOD parameters:
Cmax: Max soil moisture storage (mm) [10-2000]
B: Distribution of soil stores [0.0 - 7.0]
Alpha: Division between quick/slow routing [0.0 - 1.0]
Kq: Quick flow reservoir rate constant (day^-1) [0.15 - 1.0]
Ks: Slow flow reservoir rate constant. (day^-1) [0.0 - 0.15]

"""

import numpy as np


# Import
from HYMOD_components import cascading_reservoirs, linear_reservoir
from HYMOD_components import effective_rainfall

def run_HYMOD(precip, evap, N_reservoirs, C_max, B, Alpha, Kq, Ks, gw_initial, Xq_initial, Xs_initial):
    """
    Simulates runoff using the HYMOD conceptual rainfall runoff model.

    Parameters:
    ----------
    precip : array
        An array of observed precipitation data.
    evap : array
        An array of observed evaporation data.
    N_reservoirs : int
        The number of quick-flow reservoirs used in the abstraction of the system.
    C_max : float
        Max soil moisture storage (mm) [10-2000]
    B : float
        Distribution of soil stores [0.0 - 7.0]
    Alpha : float
        Division between quick/slow routing [0.0 - 1.0]
    Kq : float
        Quick flow reservoir rate constant (day^-1) [0.15 - 1.0]
    Ks : float
        Slow flow reservoir rate constant. (day^-1) [0.0 - 0.15]
    gw_initial : float
        Initial soil storage.
    Xq_initial : float
        Initial quick-flow reservoir storage.
    Xs_initial : float
        Initial slow-flow reservoir storage.

    Returns:
    --------
    discharge : array
        The simulated runoff given the provided data and model parameters.
    """

    # Set the simulation duration based on data
    duration = len(precip)

    # Initialize vectors to store values
    slow_storage = np.zeros(duration)
    quick_storage = np.zeros((N_reservoirs, duration))
    gw_storage = np.zeros(duration)
    slow_outflow = np.zeros(duration)
    quick_outflow = np.zeros(duration)
    discharge = np.zeros(duration)

    # Set initial values
    slow_storage[0] = Xs_initial
    quick_storage[:, 0] = Xq_initial
    gw_storage[0] = gw_initial

    # Begin simulation
    for t in range(duration - 1):

        # Calculate potential evapotranspiration using temperature
        #pet = hamon_pet(1, temp[t])
        pet = evap[t]

        # Calculate rainfall excess
        excess_rain1, excess_rain2, gw_storage[t+1] = effective_rainfall(gw_storage[t], C_max, B, precip[t], pet)
        rainfall_excess = excess_rain1 + excess_rain2

        # Calculate the quick flow component, using cascading reservoirs
        quick_inflow = Alpha * rainfall_excess
        quick_storage[:, t+1], quick_outflow[t+1] = cascading_reservoirs(quick_storage[:, t], quick_inflow, Kq, N_reservoirs)

        # Calculate the slow flow component, as one linear reservoir
        slow_inflow = (1 - Alpha) * rainfall_excess
        slow_storage[t+1], slow_outflow[t+1] = linear_reservoir(slow_storage[t], slow_inflow, Ks)

        # Total runoff/discharge is the combination of quick and slow reservoir outflows
        discharge[t+1] = slow_outflow[t+1] + quick_outflow[t+1]

    return discharge
