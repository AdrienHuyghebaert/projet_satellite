from mpl_toolkits.mplot3d.art3d import Line3D


class Orbite:

    def __init__(self, positions_satellites):
        self.positions_satellites = positions_satellites
        self.line = None

    def tracer_orbites(self, ax):
        for i in range(len(self.positions_satellites)):
            self.line = Line3D(self.positions_satellites[i, 0], self.positions_satellites[i, 1],
                               self.positions_satellites[i, 2], color='b', label='Orbite')
            ax.add_line(self.line)
        return self.line
