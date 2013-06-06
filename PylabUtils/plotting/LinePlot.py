from pylab import *

ARRANGEMENT = 111

# Shows the z value when you hover over with mouse, and prints the (x,y,z) value on mouse click
class LinePlot (object):
    
    def __init__ (self, xData, yData):
        self.xData = xData
        self.yData = yData
        self.numelems = len (self.xData)

    def _getIndex (self, x):
        ind = searchsorted (self.xData, x)
        return ind

    def _getY (self, ind):
        y = None
        
        if ind>=0 and ind<self.numelems:
            y = self.yData[ind]
        return y

    def _getString (self, x, y):
        if y is not None:
            return 'x = %1.2f\t\ty = %1.2f' % (x, y)
        else:
            return 'x = %1.2f' % (x)

    def _onMouseClick (self, event):
        x = event.xdata
        if not x:
            return
        ind = self._getIndex (x)
        y = self._getY (ind)

        str = self._getString (x, y)
        print str

    def _formatCoord (self, x, y):
        ind = self._getIndex (x)
        y = self._getY (ind)
        str = self._getString (x, y)
        return str
        
    def newAx (self):
        fig = figure ()
        ax = fig.add_subplot (ARRANGEMENT)
        ax.format_coord = self._formatCoord
        fig.canvas.mpl_connect ('button_press_event', self._onMouseClick)
        return ax
