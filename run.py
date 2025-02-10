from Beeman.solar import Solar
from Euler.solareuler import SolarEuler
from Experiments.functions import plot_energy, plot_energies

import pandas as pd

if __name__ == "__main__":
    while True:
        print("Which of the following would you like to do:\n"
            "1. Run Beeman Simulation\n"
            "2. Show Orbital Periods of the Planets (must run for at least 24 Earth years)\n"
            "3. Run Euler Simulation\n"
            "4. Compare Evolution of Energy between Beeman and Euler Methods\n"
            "5. Check for Planetary Alignment\n")
        
        choice = int(input("Please enter your choice here (1-5): "))

        if choice == 1:
            # Run the Beeman simulation and plot its energy simulation
            solar_beeman = Solar("parameters-solar.txt")
            solar_beeman.run("Beeman Simulation", check_alignment = False)
            plot_energy('Beeman Simulation_energy_output.txt')
            break

        elif choice == 2:
            # Run the simulation
            solar_beeman = Solar("parameters-solar.txt")
            solar_beeman.run("Beeman Simulation", check_alignment = False)

            # Create and print the DataFrame of orbtial periods
            df = pd.DataFrame({
                'Planet': [body.name.strip() for body in solar_beeman.bodies],
                'Orbital Period (Earth years)': solar_beeman.orbital_periods})
            print(df)
            break

        elif choice == 3:
            # Run the Euler simulation and plot its energy simulation
            solar_euler = SolarEuler("parameters-solar.txt")
            solar_euler.run("Euler Simulation", check_alignment = False)
            plot_energy('Euler Simulation_energy_output.txt')
            break

        elif choice == 4:
            # run both simulations to generate and store energy data 
            solar_beeman = Solar("parameters-solar.txt")
            solar_beeman.run("Beeman Simulation")
            solar_euler = SolarEuler("parameters-solar.txt")
            solar_euler.run("Direct Euler Simulation")
            # calling function to plot the energy data
            plot_energies('Beeman Simulation_energy_output.txt', 'Direct Euler Simulation_energy_output.txt')
            break

        elif choice == 5:
            # Check for planetary alignment
            tolerance = float(input("Please enter the tolerance for planetary alignment (in degrees [-180, 180]): "))
            solar_beeman = Solar("parameters-solar.txt")
            solar_beeman.run("Beeman Simulation", check_alignment=True, tolerance=tolerance)
        
            df = pd.DataFrame(solar_beeman.alignment_instances, columns=['Instances of Planetary Alignment (Earth Years)'])
            print(df)
            break

        else:
            print("Invalid choice, please try again.")

            