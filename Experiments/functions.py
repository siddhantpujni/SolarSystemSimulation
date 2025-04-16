from Beeman.solar import Solar
from Beeman.planet import Planet
from Euler.solareuler import SolarEuler
from Euler.planeteuler import PlanetEuler

import matplotlib.pyplot as plt
import pandas as pd
import math as m

"""
This file contains the functions that are used for the energy comparsion graph and to check 
for planetary alignment.

add code to plot individual simulation energies
"""

# Define a function to parse the lines in the file
def parse_line(line):
    parts = line.split()
    time = float(parts[2])
    energy = float(parts[8])
    return time, energy

# Define a function to read in the data and plot the energies for both integration techniques
def plot_energies(filename_beeman, filename_euler):
    # Read the data from the Beeman simulation file
    with open(filename_beeman, 'r') as f:
        lines = f.readlines()
    
    # Parse the lines into a DataFrame
    data_beeman = pd.DataFrame([parse_line(line) for line in lines], columns=['Time', 'Energy'])

    # Read the data from the Euler simulation file
    with open(filename_euler, 'r') as f:
        lines = f.readlines()
    
    # Parse the lines into a DataFrame
    data_euler = pd.DataFrame([parse_line(line) for line in lines], columns=['Time', 'Energy'])

    # Plot the data
    plt.figure()
    plt.plot(data_beeman['Time'], data_beeman['Energy'], label='Beeman')
    plt.plot(data_euler['Time'], data_euler['Energy'], label='Euler')
    plt.xlabel('Time (earth years)')
    plt.ylabel('Total energy (J)')
    plt.title('Total energy vs time')
    plt.legend()
    plt.show()

# Define a function to plot the energies for a single simulation
def plot_energy(filename):
    # Read the data from the Beeman simulation file
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Parse the lines into a DataFrame
    data = pd.DataFrame([parse_line(line) for line in lines], columns=['Time', 'Energy'])
    
    plt.figure()
    plt.plot(data['Time'], data['Energy'])
    plt.xlabel('Time (earth years)')
    plt.ylabel('Total energy (J)')
    plt.title('Total energy vs time')
    plt.show()




            