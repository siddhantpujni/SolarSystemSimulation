import math as m
import numpy as np
from numpy.linalg import norm

class Planet():
    """
    Planet class
    """

    def __init__(self, name, mass, orbit, colour):
        self.name = name
        # mass in kg
        self.m = mass
        # orbital radius in m
        self.orbit = orbit
        # colour - need to strip trailing line return!
        self.c = colour.strip()
        # set year to zero
        self.year = 0 

    def initialise(self, G, p):
        # p is a planet object (instance)
        # inital position, initial coords = (orbit radius, 0)
        self.r = np.array([self.orbit, 0])
        # inital velocity, tangential to position
        # speed = sqrt(G*marsmass/r)
        if self.orbit == 0.0:
            self.v = np.array([0, 0])
        else:
            vel = m.sqrt(G*p.m/self.orbit)
            self.v = np.array([0, vel])
        # intial accelatation, using gravitational force law
        if self.orbit == 0.0:
            self.a = np.array([0, 0])
        else:
            self.a = self.updateAcc(G, p)
        # set acc_old = acc to start Beeman
        self.a_old = self.a

    def updatePos(self, G, dt):
        # keep old position to check for year
        self.r_old = self.r
        
        # update position first: Beeman
        self.r = self.r + self.v*dt + (4*self.a - self.a_old)*dt*dt/6.0

    def updateVel(self, G, dt, p):
        # update velocity second: Beeman
        a_new = self.updateAcc(G, p)
        self.v = self.v + + (2*a_new + 5*self.a - self.a_old)*dt/6.0
        # now update acc ready for next iteration
        self.a_old = self.a
        self.a = a_new

    def updateAcc(self, G, p):
        # update acc (gravitational force law)
        pos = self.r - p.r
        a = -G*p.m*pos/m.pow(norm(pos),3)
        return a

    def newYear(self):
    # update the year when the planet passes the positive x-axis
        if self.r_old[1] < 0.0 and self.r[1] >= 0.0:
            self.year +=1
            return True
        else:
            return False

    def kineticEnergy(self):
        # determine kinetic energy in Joules
        ke = (np.dot(self.v, self.v))*self.m/2
        return ke 
    
    def planetAngle(self):
        # The x-axis vector as unit vectot
        x_axis_vector = np.array([1, 0])
        # Calculate the dot product of the two vectors
        dot_product = np.dot(self.r, x_axis_vector)
        # Calculate the magnitude (norm) of each vector
        magnitude1 = np.linalg.norm(self.r)
        magnitude2 = np.linalg.norm(x_axis_vector)
        # Check if the magnitudes are zero
        if magnitude1 == 0 or magnitude2 == 0:
            raise ValueError("One or both of the vectors are zero vectors")
        # Calculate the angle using the arccosine formula
        angle = np.arccos(dot_product / (magnitude1 * magnitude2))
        # Adjust the angle based on the sign of the y-coordinate
        if self.r[1] < 0:
            angle = -angle
        angle = np.degrees(angle)
        return angle
