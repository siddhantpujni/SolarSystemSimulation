from Beeman.solar import Solar
from Euler.planeteuler import PlanetEuler

class SolarEuler(Solar):
    """
    SolarEuler class
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.bodies = []
        with open(filename, "r") as file:
            lines = [line for line in file if not line.strip().startswith("#")]
            i = 3
            while i < len(lines):
                name = lines[i].strip()
                mass = float(lines[i+1])
                orbit = float(lines[i+2])
                colour = lines[i+3].strip()
                self.bodies.append(PlanetEuler(name, mass, orbit, colour))
                i += 4
        for body in self.bodies:
            body.initialise(self.G, self.bodies[0])