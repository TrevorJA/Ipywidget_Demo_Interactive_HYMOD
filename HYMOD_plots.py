"""
Trevor Amestoy
Summer 2022

Contains a script used to run a HYMOD model, calculate the error, and
plot the results.

"""
import numpy as np
import matplotlib.pyplot as plt
from HYMOD_model import run_HYMOD
from HYMOD_components import calculate_error_by_type


def plot_HYMOD_results(C_max, B, Alpha, Ks, Kq, N_reservoirs, plot_observed,
                        data_length = 365,
                        S_initial = 0.0, Sq_initial = 0.0, Ss_initial = 0.0,
                        show_error = True, error_type = 'RMSE'):

    # Load a test dataset
    data = np.loadtxt('./LeafCatch.dat', unpack = True)[:, 0:365]

    # Separate the data from the dataset
    precip = data[0, :]
    evap = data[1, :]
    Q_observed = data[2, :]

    # Run the simulation
    Q_model = run_HYMOD(precip, evap, N_reservoirs, C_max, B, Alpha, Kq, Ks, S_initial, Sq_initial, Ss_initial)

    # Calculate the error between observed and modeled dishcharge
    error = calculate_error_by_type(Q_observed, Q_model, precip, error_type)

    # Set up plot
    time = range(len(Q_model))
    plot_title = 'Modeled runoff'

    # Plot modeled flow
    plt.plot(time, Q_model, label = 'Simulated Runoff', color = 'darkorange', zorder = 1)

    # Plot observed flow
    if plot_observed:
        plt.plot(time, Q_observed, label = 'Observed Runoff', color = 'cornflowerblue', zorder = 2)
        plot_title = 'Modeled and observed runoff'

    # Include a text label with the error value
    if show_error:
        text_x_coord = 0.75 * data_length
        text_y_coord = 0.75 * max(Q_observed)
        plt.text(text_x_coord, text_y_coord, str(f'{error_type}: {error:.2f}'))

    plt.legend()
    plt.ylim((0, 1.2*max(Q_observed)))
    plt.title(plot_title)
    plt.ylabel('Streamflow (mm)')
    plt.xlabel('Time (days)')

    return
