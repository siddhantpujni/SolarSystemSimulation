from Beeman.planet import Planet

class PlanetEuler(Planet):
    """
    PlanetEuler class
    """
    def updatePos(self, G, dt):
        # keep old position to check for year
        self.r_old = self.r

        # update position using Euler method
        self.r = self.r + self.v * dt

    def updateVel(self, G, dt, p):
        # update velocity using Euler method
        a_new = self.updateAcc(G, p)
        self.v = self.v + self.a * dt

        # now update acc ready for next iteration
        self.a_old = self.a
        self.a = a_new
 