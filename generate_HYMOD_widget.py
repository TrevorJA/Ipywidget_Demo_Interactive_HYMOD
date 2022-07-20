"""
Trevor Amestoy
Summer 2022

This script generates a Ipywidget interactive plot for the HYMOD model.

Widget features include:
- Sliders to manipulate model parameters.
- Drop-down selection of error metric to be shown.
- Toggle button to turn observed data On/off

"""

import numpy as np
import matplotlib.pyplot as plt

import ipywidgets as widgets
from ipywidgets import interact, interactive, interactive_output
from ipywidgets import HBox, VBox, Label, Layout, fixed

from HYMOD_model import run_HYMOD
from HYMOD_components import calculate_error_by_type
from HYMOD_plots import plot_HYMOD_results


plt.style.use('ggplot')


def make_HYMOD_widget():

    param_labs = ['Kq : Quick flow reservoir rate constant (1/day)',
                'Ks : Slow flow reservoir rate constant (1/day)',
                'C_max : Maximum soil moisture storage (mm)',
                'B : Distribution of soil stores',
                'Alpha : Division between quick/slow routing',
                'N : Number of quick-flow reservoirs']

    # Define sliders for later use
    Cmax_slider = widgets.FloatSlider(value = 100, min = 10, max = 2000, step = 1.0, disabled = False, continuous_update = False, readout = True, readout_format = '0.2f')
    B_slider = widgets.FloatSlider(value = 2.0, min = 0.0, max = 7.0, step = 0.1, disabled = False, continuous_update = False, readout = True, readout_format = '0.2f')
    Alpha_slider = widgets.FloatSlider(value = 0.30, min = 0.00, max = 1.00, step = 0.01, disabled = False, continuous_update = False, readout = True, readout_format = '0.2f')
    Kq_slider = widgets.FloatSlider(value = 0.33, min = 0.15, max = 1.00, step = 0.01, disabled = False, continuous_update = False, readout = True, readout_format = '0.2f')
    Ks_slider = widgets.FloatSlider(value = 0.07, min = 0.00, max = 0.15, step = 0.01, disabled = False, continuous_update = False, readout = True, readout_format = '0.2f')
    N_slider = widgets.IntSlider(value = 3, min = 2, max = 7, disabled = False, continuous_update = False, readout = True)

    # Let the user select from different error metrics
    drop_down = widgets.Dropdown(options=['RMSE','NSE','ROCE'],
                                    description='',
                                    value = 'RMSE',
                                    disabled = False)


    # Create a button to toggle the showing of observed data
    plot_button = widgets.ToggleButton(value = False, description = 'Toggle', disabled=False,
    button_style='', tooltip='Description')

    # Generate the plot as an interactive_output, specifying sliders and inputs
    result_comparison_plot = interactive_output(plot_HYMOD_results, {'C_max' : Cmax_slider, 'B': B_slider, 'Alpha':Alpha_slider, 'Ks':Ks_slider, 'Kq':Kq_slider,'N_reservoirs':N_slider, 'plot_observed' : plot_button,'error_type': drop_down})

    # Layout secifications for the widgets: center and wrap
    box_layout = widgets.Layout(display='flex', flex_flow = 'row', align_items ='center', justify_content = 'center')

    # Create the rows of the widets
    title_row = Label('Select parameter values for the HYMOD model:')
    slider_row = HBox([VBox([Label(i) for i in param_labs]), VBox([Cmax_slider, B_slider, Alpha_slider, Ks_slider, Kq_slider, N_slider])], layout = box_layout)
    error_menu_row = HBox([Label('Choose error metric:'), drop_down], layout = box_layout)
    observed_toggle_row = HBox([Label('Click to show observed flow'), plot_button], layout = box_layout)
    plot_row = HBox([result_comparison_plot], layout = box_layout)

    # Combine label and slider box (row_one) with plot for the final widget
    HYMOD_widget = VBox([title_row, slider_row, plot_row, error_menu_row, observed_toggle_row])

    return HYMOD_widget
