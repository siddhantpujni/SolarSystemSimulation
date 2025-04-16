import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy.linalg import norm

from Beeman.planet import Planet

class Solar():

    """
    Class to run the orbital simulation
    """

    def __init__(self, filename):
        
        self.bodies = []
        self.alignment_instances = []
        
        with open(filename, "r") as file:
            lines = [line for line in file if not line.strip().startswith("#")]
            self.niter = int(lines[0])
            self.dt = float(lines[1])
            self.G = float(lines[2])
            i = 3
            while i < len(lines):
                name = lines[i].strip()
                mass = float(lines[i+1])
                orbit = float(lines[i+2])
                colour = lines[i+3].strip()
                self.bodies.append(Planet(name, mass, orbit, colour))
                i += 4
            
        for body in self.bodies:
            body.initialise(self.G, self.bodies[0])
    
        self.new_year_start_times = [None for _ in self.bodies]
        self.orbital_periods = [None for _ in self.bodies]

    def init(self):
        # initialiser for animator
        return self.patches

    def animate(self, i, check_alignment = False, tolerance = 5):
        # keep track of time in earth years, (i + 1) to account for indexing
        self.time = (i+1)*self.dt

        # update positions
        for j in range(0, len(self.bodies)):
            self.bodies[j].updatePos(self.G, self.dt)
            self.patches[j].center = self.bodies[j].r
            
        # then update velocities
        for j in range(0, len(self.bodies)):
            for k in range(0, len(self.bodies)):
                if j != k:
                    self.bodies[j].updateVel(self.G, self.dt, self.bodies[k])

        if check_alignment:
            self.alignmentCheck(tolerance = tolerance)

        # check year and print year if new year for any planet
        for j in range(0, len(self.bodies)):
            if self.bodies[j].newYear():
                # If this is the first new year for this planet, store the start time
                if self.new_year_start_times[j] is None:
                    self.new_year_start_times[j] = self.time
                # If this is not the first new year for this planet, calculate the orbital period
                else:
                    orbital_period = self.time - self.new_year_start_times[j]
                    self.orbital_periods[j] = orbital_period
                    self.new_year_start_times[j] = self.time

                # if new year is earth year, also print total energy
                if self.bodies[j].name.strip() == "earth":
                    # need to convert from earth masses AU^2 yr^-2 to kg m^2 s-2 (J)
                    c =(5.97219e+24*1.496e+11*1.496e+11)/(3.154e+7*3.154e+7)
                    energy = self.energy()*c
                    # Open the file in append mode
                    with open(self.filename, 'a') as f:
                        # Write the data to the file
                        f.write(f"Time = {self.time} earth years. Total energy = {energy} J.\n")
                    print(f"Time = {self.time:.3f} earth years. "
                          f"Total energy = {energy:.3e} J.")
        
        return self.patches

    def energy(self):
        ke = 0.0
        pe = 0.0
        for j in range(0, len(self.bodies)):
            ke += self.bodies[j].kineticEnergy()
            for k in range(0, len(self.bodies)):
                if k != j:
                    r = norm(self.bodies[k].r - self.bodies[j].r)
                    pe -= self.G*self.bodies[j].m*self.bodies[k].m / r
        # divide pe by two to avoid double counting
        pe = pe / 2
        totEnergy = ke + pe
        return totEnergy

    def run(self, title, check_alignment = False, tolerance = 5):
        self.filename = f'{title}_energy_output.txt'
        with open(self.filename, 'w') as f:
            pass

        # set up the plot components        
        fig = plt.figure()
        ax = plt.axes()

        # create an array for patches (planet)
        self.patches = []

        # get orbital radius of outermost body (including satellite) to set size of
        # orbiting bodies and of plot
        maxOrb = max(math.sqrt(np.dot(body.r, body.r)) for body in self.bodies)

        # add the planet and moons to the Axes and patches
        for i in range(0, len(self.bodies)):
            if i == 0:
                self.patches.append(
                    ax.add_patch(plt.Circle(self.bodies[i].r, 0.05*maxOrb,
                                            color=self.bodies[i].c, animated=True)))
            else:
                self.patches.append(
                    ax.add_patch(plt.Circle(self.bodies[i].r, 0.02*maxOrb,
                                            color=self.bodies[i].c, animated=True)))

        # set up the axes
        # scale axes so circle looks like a circle and set limits
        # with border b for prettier plot
        b = 1.2
        lim = maxOrb*b
        ax.set_facecolor('black')  # set a space-like background
        for body, patch in zip(self.bodies, self.patches):
            patch.set_facecolor(body.c)  # set the color of the patch
            patch.set_label(body.name.strip())
        ax.legend()
        ax.axis("scaled")
        ax.set_title(title)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)

        anim = FuncAnimation(
            fig, self.animate, init_func=self.init,
            frames=self.niter, repeat=False, interval=1, blit=True, fargs=(check_alignment, tolerance))
        plt.show()

    def alignmentCheck(self, tolerance):
        """
        Method to check for planetary alignment.
        
        The angle between the x-axis and the line from the sun to the planet is calculated for each planet.
        If all planets are within a certain tolerance of the mean angle, a statement is printed.
        """
        # Calculate the angles and convert them to degrees
        theta_list = [np.degrees(body.planetAngle()) for body in self.bodies[1:]]  # Exclude the sun

        # Calculate the mean angle
        mean_angle = np.mean(theta_list)
    
        # Check if all angles are within the tolerance of the mean angle
        alignment = all(abs(theta - mean_angle) <= tolerance for theta in theta_list)
        if alignment:
            print(f'Planetary alignment at time {self.time} Earth years')
            self.alignment_instances.append((self.time))
    

