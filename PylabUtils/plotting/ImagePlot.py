from pylab import *

ARRANGEMENT = 111

class ImagePlot (object):

    """

    Shows the z value when you hover over with mouse, and prints the (x,y,z) value on mouse click

    """

    def __init__ (self, data):
        self.data = data
        self.numrows, self.numcols = self.data.shape

    def _getColRow (self, x, y):
        col = int (x+0.5)
        row = int (y+0.5)
        return (col, row)

    def _getZ (self, col, row):
        z = None
        if col>=0 and col<self.numcols and row>=0 and row<self.numrows:
            z = self.data[row, col]
        return z

    def _getString (self, x, y, z):
        if z is not None:
            return 'x = %d\t\ty = %d\t\tz = %1.1f' % (x, y, z)
        else:
            return 'x = %d\t\ty = %d' % (x, y)

    def _onMouseClick (self, event):
        x = event.xdata
        y = event.ydata
        if not x and not y:
            return
        col, row = self._getColRow (x, y)
        z = self._getZ (col, row)

        str = self._getString (x, y, z)
        print str

    def _formatCoord (self, x, y):
        col, row = x, y
        z = self._getZ (col, row)
        str = self._getString (x, y, z)
        return str
        
    def newAx (self):
        fig = figure ()
        ax = fig.add_subplot (ARRANGEMENT)
        ax.format_coord = self._formatCoord
        fig.canvas.mpl_connect ('button_press_event', self._onMouseClick)
        return ax
