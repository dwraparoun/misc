import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

GCONST = 6.67408e-11

class CelestialBody:
    def __init__(self, pos, vel, mass, name="Not given"):
        """
        Creates planets and stars objects to be animated by CelestialSystem
        """
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.name = name

    def __str__(self):
        return "Pos = {}; Vel = {}; Mass = {}".format(self.pos, self.vel,
                self.mass)

    def __repr__(self):
        return "CelestialBody(np.array({}), np.array({}), {})".format(
                self.pos, self.vel, self.mass)

    def __eq__(self, other):
        """
        Needed for CelestialSystem's solve() method to disregard
        a contribution of a planet to itself
        """
        return (np.all(self.pos == other.pos)
                and np.all(self.vel == other.vel)
                and np.all(self.mass == other.mass)
                and np.all(self.name == other.name))    

    def __ne__(self, other):
        return not self.__eq__(other)


class CelestialSysem:
    def __init__(self, step, endtime, *args, **kwargs):
        """
        Instances of CelestialBody are passed into args. The animation
        is customizable with kwargs; plot_colors and plot_sizes keywords
        are lists of the same size as args - they specify the color and
        glyph size of each CelestialBody instance in the order they were
        passed to this constructor.
        """
        self.step, self.endtime = step, endtime
        self.planets = args
        self.positions = self.solve()
        self.fig, self.ax = plt.subplots()
        self.sizes = kwargs.get("plot_sizes")
        self.colors = kwargs.get("plot_colors")
        self.scale = kwargs.get("plot_scale", 2)  # (default) x-y scale
        self.speed = kwargs.get("plot_speed", 5)  # frame delay
        self.anim = FuncAnimation(self.fig, self.update, interval=self.speed,
                init_func=self.setup_plot, blit=True)

    def solve(self):
        curr_time = 0.0
        curr_forces = np.zeros((len(self.planets), 2))
        curr_force = np.array([0.0, 0.0])
        while(curr_time < self.endtime):
            for index, planet in enumerate(self.planets):
                curr_force *= 0.0
                for other_planet in self.planets:
                    if planet != other_planet:
                        dist = other_planet.pos - planet.pos
                        norm = np.sqrt(np.dot(dist, dist))
                        unit = dist / norm
                        curr_force += (GCONST
                                * planet.mass
                                * other_planet.mass
                                * unit
                                / norm**2)
                curr_forces[index] = curr_force
            for index, planet in enumerate(self.planets):
                acc = curr_forces[index] / planet.mass
                planet.vel += acc * self.step
                planet.pos += planet.vel * self.step
            curr_forces *= 0.0
            positions = [planet.pos for planet in self.planets]
            curr_time += self.step
            yield positions

    def setup_plot(self):
        positions = next(self.positions)
        x = [position[0] for position in positions]
        y = [position[1] for position in positions]
        if self.colors and self.sizes:
            self.scat = self.ax.scatter(x, y, c=self.colors, s=self.sizes,
                    animated=True)
        else:
            self.scat = self.ax.scatter(x, y, animated=True)
        self.ax.grid(True)
        maxdist = self.scale * max([np.max(np.abs(planet.pos)) for planet in self.planets])
        self.ax.axis([-maxdist, maxdist, -maxdist, maxdist])
        return self.scat,

    def update(self, i):
        positions = next(self.positions)
        self.scat.set_offsets(positions)
        return self.scat,

    def show(self):
        plt.show()

if __name__ == "__main__":
    # Celestial bodies (data from wiki)
    sun = CelestialBody(np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1.9885e30)
    mercury = CelestialBody(0.387 * np.array([1.496e11, 0.0]), np.array([0.0, 47362.0]), 4.8675e24)
    venus = CelestialBody(0.723 * np.array([1.496e11, 0.0]), np.array([0.0, 35020.0]), 4.8675e24)
    earth = CelestialBody(np.array([1.496e11, 0.0]), np.array([0.0, 29780.0]), 5.97237e24)
    mars = CelestialBody(1.523 * np.array([1.496e11, 0.0]), np.array([0.0, 24007.0]), 6.4171e23)
    moon = CelestialBody(np.array([1.496e11+384399e3, 0.0]), np.array([0.0, 29780.0+1022.0]), 7.342e22) 

    # Create a system
    colors = ['y', 'orange', 'b', 'c', 'r', 'gray']
    sizes = [750, 50, 75, 150, 125, 30]
    sys = CelestialSysem(24 * 3600.0, np.inf, sun, mercury, venus, earth,
            mars, moon, plot_colors=colors, plot_sizes=sizes,
            plot_scale=2.0, plot_speed=3.5)
    sys.show()
