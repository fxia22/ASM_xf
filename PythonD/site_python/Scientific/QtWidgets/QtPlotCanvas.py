# This module defines a plot widget for Qt user interfaces.
# It supports only elementary line plots at the moment.
# See the example at the end for documentation...
#
# Written by Konrad Hinsen <hinsen@cnrs-orleans.fr>
# Last revision: 2002-12-10
#

from qt import *
import string, Numeric, os

"""This module provides a plot widget for Qt user interfaces.
A plot widget acts like a canvas for special graphics objects
that represent curves shown by lines or markers.

Note that this module is not meant to replace a full-featured
plot program. It was designed to permit the simple integration of
plots into Qt-based user interfaces.
"""

# This must be 0 on the Zaurus
colors_by_name = not os.environ.has_key('QPEDIR')


class PolyPoints:

    def __init__(self, points, attr):
        self.points = Numeric.array(points)
        self.scaled = self.points
        self.attributes = {}
        for name, value in self._attributes.items():
            try:
                value = attr[name]
            except KeyError: pass
            self.attributes[name] = value

    def boundingBox(self):
        return Numeric.minimum.reduce(self.points), \
               Numeric.maximum.reduce(self.points)

    def scaleAndShift(self, scale=1, shift=0):
        self.scaled = scale*self.points+shift

    def writeToFile(self, file, separator):
        if self.points:
            for p in self.points:
                file.write(`p[0]` + ' ' + `p[1]` + '\n')
            return 1
        else:
            return 0

class PolyLine(PolyPoints):

    """Multiple connected lines

    Constructor: PolyLine(|points|, **|attr|)

    Arguments:

    |points| -- any sequence of (x, y) number pairs

    |attr| -- line attributes specified by keyword arguments:

      * 'width': the line width (default: 1)
      * 'color': a string whose value is one of the color names defined by
                 X-Windows (default: "black")
      * 'style': a Qt pen style object (default: Qt.SolidLine)
    """

    def __init__(self, points, **attr):
        PolyPoints.__init__(self, points, attr)

    _attributes = {'color': 'black',
                   'width': 1,
                   'style': Qt.SolidLine}

    def draw(self, painter, bbox):
        if len(self.points) > 1:
            color = self.attributes['color']
            width = self.attributes['width']
            style = self.attributes['style']
            points = QPointArray(len(self.points))
            for i in range(len(self.points)):
                x, y = self.scaled[i]
                points.setPoint(i, x, y)
            if colors_by_name:
                painter.setPen(QPen(QColor(color), width, style))
            else:
                painter.setPen(QPen(getattr(Qt, color), width, style))
            painter.drawPolyline(points)

class VerticalLine(PolyLine):

    """A vertical line

    Constructor: VerticalLine(|xpos|, **|attr|)

    Arguments:

    |xpos| -- the x coordinate of the line

    |attr| -- line attributes specified by keyword arguments:

      * 'width': the line width (default: 1)
      * 'color': a string whose value is one of the color names defined by
                 X-Windows (default: "black")
      * 'style': a Qt pen style object (default: Qt.SolidLine)
    """

    def __init__(self, xpos, **attr):
        apply(PolyLine.__init__, (self, 2*[(xpos, 0.)]), attr)

    def draw(self, canvas, bbox):
        self.scaled[0, 1] = bbox[0][1]
        self.scaled[1, 1] = bbox[1][1]
        PolyLine.draw(self, canvas, bbox)

    def writeToFile(self, file, separator):
        return 0

class HorizontalLine(PolyLine):

    """A horizontal line

    Constructor: HorizontalLine(|ypos|, **|attr|)

    Arguments:

    |ypos| -- the y coordinate of the line

    |attr| -- line attributes specified by keyword arguments:

      * 'width': the line width (default: 1)
      * 'color': a string whose value is one of the color names defined by
                 X-Windows (default: "black")
      * 'style': a Qt pen style object (default: Qt.SolidLine)
    """

    def __init__(self, ypos, **attr):
        print ypos
        apply(PolyLine.__init__, (self, 2*[(0., ypos)]), attr)

    def draw(self, canvas, bbox):
        self.scaled[0, 0] = bbox[0][0]
        self.scaled[1, 0] = bbox[1][0]
        PolyLine.draw(self, canvas, bbox)

    def writeToFile(self, file, separator):
        return 0

class PolyMarker(PolyPoints):

    """Series of markers

    Constructor: PolyPoints(|points|, **|attr|)

    Arguments:

    |points| -- any sequence of (x, y) number pairs

    |attr| marker attributes specified by keyword arguments:

    * 'width': the line width for drawing the marker (default: 1)
    * 'color': a string whose value is one of the color names defined by
               X-Windows, defines the color of the line forming the marker
               (default: black)
    * 'fillcolor': a string whose value is one of the color names defined
                   by X-Windows, defines the color of the interior of the
                   marker (default: black)
    * 'fillstyle': a Qt BrushStyle object (default: Qt.SolidPattern)
    * 'marker': one of 'circle' (default), 'dot', 'square', 'triangle',
                'triangle_down', 'cross', 'plus'
    """

    def __init__(self, points, **attr):

        PolyPoints.__init__(self, points, attr)

    _attributes = {'color': 'black',
                   'width': 1,
                   'fillcolor': 'black',
                   'size': 2,
                   'fillstyle': Qt.SolidPattern,
                   'marker': 'circle'}

    def draw(self, painter, bbox):
        color = self.attributes['color']
        size = self.attributes['size']
        fillcolor = self.attributes['fillcolor']
        marker = self.attributes['marker']
        fillstyle = self.attributes['fillstyle']
        if colors_by_name:
            painter.setPen(QPen(QColor(color), 1, Qt.SolidLine))
            painter.setBrush(QBrush(QColor(fillcolor), fillstyle))
        else:
            painter.setPen(QPen(getattr(Qt, color), 1, Qt.SolidLine))
            painter.setBrush(QBrush(getattr(Qt, fillcolor), fillstyle))
        f = getattr(self, '_' + marker)
        for xc, yc in self.scaled:
            f(painter, xc, yc, size)
    
    def _circle(self, painter, xc, yc, size):
        size *= 5
        painter.drawEllipse(xc-0.5*size, yc-0.5*size, size, size)

    def _dot(self, painter, xc, yc, size=1):
        painter.drawEllipse(xc-0.5*size, yc-0.5*size, size, size)

    def _square(self, painter, xc, yc, size):
        size *= 5
        painter.drawRect(xc-0.5*size, yc-0.5*size, size, size)
    
    def _triangle(self, painter, xc, yc, size):
        size *= 5
        points = QPointArray(3)
        points.setPoint(0, xc-0.5*size, yc+0.288675134595*size)
        points.setPoint(1, xc+0.5*size, yc+0.288675134595*size)
        points.setPoint(2, xc, yc-0.577350269189*size)
        painter.drawPolygon(points)

    def _triangle_down(self, painter, xc, yc, size):
        size *= 5
        points = QPointArray(3)
        points.setPoint(0, xc-0.5*size, yc-0.288675134595*size)
        points.setPoint(1, xc+0.5*size, yc-0.288675134595*size)
        points.setPoint(2, xc, yc+0.577350269189*size)
        painter.drawPolygon(points)

    def _cross(self, painter, xc, yc, size):
        size *= 3
        painter.drawLine(xc-size+1, yc-size+1, xc+size, yc+size)
        painter.drawLine(xc-size+1, yc+size-1, xc+size, yc-size)

    def _plus(self, painter, xc, yc, size):
        size *= 3
        painter.drawLine(xc-size+1, yc, xc+size, yc)
        painter.drawLine(xc, yc+size, xc, yc-size+1)

class PlotGraphics:

    """Compound graphics object

    Constructor: PlotGraphics(|objects|)

    Arguments:

    |objects| -- a list whose elements can be instances of the classes
                 PolyLine, PolyMarker, and PlotGraphics.
    """
    
    def __init__(self, objects):
        self.objects = objects

    def boundingBox(self):
        p1, p2 = self.objects[0].boundingBox()
        for o in self.objects[1:]:
            p1o, p2o = o.boundingBox()
            p1 = Numeric.minimum(p1, p1o)
            p2 = Numeric.maximum(p2, p2o)
        return p1, p2

    def scaleAndShift(self, scale=1, shift=0):
        for o in self.objects:
            o.scaleAndShift(scale, shift)

    def draw(self, painter, bbox):
        for o in self.objects:
            o.draw(painter, bbox)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, item):
        return self.objects[item]

    def writeToFile(self, file, separator):
        data = 0
        for o in self.objects:
            if data:
                file.write(separator)
            data = o.writeToFile(file, separator)


class PlotCanvas(QWidget):

    """Qt plot widget

    Constructor: PlotCanvas(|parent|=None, |background|='white',
                            |font|=None, |zoom|=0, |select|=None).

    The default background color is white and the default font is
    Helvetica at 10 points.

    Arguments:

    |parent| -- the parent widget, default: None

    |background| -- the background color, default: 'white'

    |font| -- a QFont object defining the font for axis labels,
              default: 10 point Helevetica

    |zoom| -- a logical variable that indicates whether interactive
              zooming (using the left mouse button) is enabled; the
              default is 0 (no zoom)

    |select| -- enables the user to select a range along the x axis
                by dragging the mouse (with the left button pressed)
                in the area *under* the x axis. If |select| is 0,
                no selection is possible. Otherwise the value of |select|
                must be a callable object that is called whenever the
                selection changes, with a single argument that can be
                None (no selection) or a tuple containing two x values.
    """
    
    def __init__(self, parent=None, background='white',
                 font=None, zoom=0, select=None):
        self.zoom = zoom
        self.selectfn = select
        if font is None:
            font = QFont('Helvetica', 10)
        QWidget.__init__(self, parent)
        if colors_by_name:
            self.background_color = QColor(background)
        else:
            self.background_color = getattr(Qt, background)
        self.setFont(font)
        self.border = (1, 1)
        self.mouse_state = 0
        self.value_label = QLabel(self)
        self.value_label.hide()
        self.popup_menu = QPopupMenu(self)
        self.popup_menu.insertItem('Auto Scale', self._autoScale)
        self.popup_menu.insertItem('Run Xmgrace', self._xmgr)
        self._setsize()
        self.current_plot = None
        self.selected_range = None

    def resizeEvent(self, event):
        self._setsize()
        self.update()

    def _setsize(self):
        self.plotbox_size = 0.97*Numeric.array([self.width(), -self.height()])
        xo = 0.5*(self.width()-self.plotbox_size[0])
        yo = self.height()-0.5*(self.height()+self.plotbox_size[1])
        self.plotbox_origin = Numeric.array([xo, yo])

    def draw(self, graphics, xaxis = None, yaxis = None):
        """Draws the graphics object |graphics|, which can be
        a PolyLine, PolyMarker, or PlotGraphics object. The
        arguments |xaxis| and |yaxis| specify how axes are
        drawn: 'None' means that no axis is drawn and the graphics
        objects are scaled to fill the canvas optimally. '"automatic"'
        means that the axis is drawn and a suitable value range is
        determined automatically. A sequence of two numbers means
        that the axis is drawn and the value range is the interval
        specified by the two numbers.
        """
        self.current_plot = (graphics, xaxis, yaxis)
        self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        p.fillRect(self.rect(), QBrush(self.background_color))
        graphics, xaxis, yaxis = self.current_plot
        p1, p2 = graphics.boundingBox()
        xaxis = self._axisInterval(xaxis, p1[0], p2[0])
        yaxis = self._axisInterval(yaxis, p1[1], p2[1])
        text_width = [0., 0.]
        text_height = [0., 0.]
        if xaxis is not None:
            p1[0] = xaxis[0]
            p2[0] = xaxis[1]
            xticks = self._ticks(xaxis[0], xaxis[1])
            w, h = self._textBoundingBox(p, xticks[0][1])
            text_height[1] = h+2
            text_width[0] = 0.5*w
            w, h = self._textBoundingBox(p, xticks[-1][1])
            text_width[1] = 0.5*w
        else:
            xticks = None
        if yaxis is not None:
            p1[1] = yaxis[0]
            p2[1] = yaxis[1]
            yticks = self._ticks(yaxis[0], yaxis[1])
            for y in yticks:
                w, h = self._textBoundingBox(p, y[1])
                text_width[0] = max(text_width[0], w+2)
            h = 0.5*h
            text_height[0] = h
            text_height[1] = max(text_height[1], h)
        else:
            yticks = None
        text1 = Numeric.array([text_width[0], -text_height[1]])
        text2 = Numeric.array([text_width[1], -text_height[0]])
        scale = (self.plotbox_size-text1-text2) / (p2-p1)
        shift = -p1*scale + self.plotbox_origin + text1
        self.transformation = (scale, shift)
        self.bbox = (p1, p2)
        if self.selected_range is not None:
            x1 = scale[0]*self.selected_range[0]+shift[0]
            x2 = scale[0]*self.selected_range[1]+shift[0]
            p.setPen(QPen(Qt.NoPen))
            p.setBrush(QBrush(Qt.gray, Qt.Dense5Pattern))
            p.drawRect(x1, 0, x2-x1, self.height())
        self._drawAxes(p, xaxis, yaxis, p1, p2, scale, shift, xticks, yticks)
        graphics.scaleAndShift(scale, shift)
        graphics.draw(p, (scale*p1+shift, scale*p2+shift))
        p.end()

    def _axisInterval(self, spec, lower, upper):
        if spec is None:
            return None
        if spec == 'minimal':
            if lower == upper:
                return lower-0.5, upper+0.5
            else:
                return lower, upper
        if spec == 'automatic':
            range = upper-lower
            if range == 0.:
                return lower-0.5, upper+0.5
            log = Numeric.log10(range)
            power = Numeric.floor(log)
            fraction = log-power
            if fraction <= 0.05:
                power = power-1
            grid = 10.**power
            lower = lower - lower % grid
            mod = upper % grid
            if mod != 0:
                upper = upper - mod + grid
            return lower, upper
        if type(spec) == type(()):
            lower, upper = spec
            if lower <= upper:
                return lower, upper
            else:
                return upper, lower
        raise ValueError, str(spec) + ': illegal axis specification'

    def _drawAxes(self, painter, xaxis, yaxis,
                  bb1, bb2, scale, shift, xticks, yticks):
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        ww = self.width()
        wh = self.height()
        if xaxis is not None:
            lower, upper = xaxis
            text = 1
            for y, d in [(bb1[1], -4), (bb2[1], 4)]:
                p1 = scale*Numeric.array([lower, y])+shift
                p2 = scale*Numeric.array([upper, y])+shift
                painter.drawLine(p1[0], p1[1], p2[0], p2[1])
                for x, label in xticks:
                    p = scale*Numeric.array([x, y])+shift
                    painter.drawLine(p[0], p[1], p[0], p[1]+d)
                    if text:
                        rect = painter.boundingRect(0, wh, ww, wh,
                                 Qt.AlignLeft|Qt.AlignBottom, label)
                        w = rect.width()
                        h = rect.height()
                        painter.drawText(p[0]-w/2, p[1]+2, w, h,
                                         Qt.AlignLeft|Qt.AlignBottom, label)
                text = 0

        if yaxis is not None:
            lower, upper = yaxis
            text = 1
            for x, d in [(bb1[0], -4), (bb2[0], 4)]:
                p1 = scale*Numeric.array([x, lower])+shift
                p2 = scale*Numeric.array([x, upper])+shift
                painter.drawLine(p1[0], p1[1], p2[0], p2[1])
                for y, label in yticks:
                    p = scale*Numeric.array([x, y])+shift
                    painter.drawLine(p[0], p[1], p[0]-d, p[1])
                    if text:
                        rect = painter.boundingRect(0, wh, ww, wh,
                                 Qt.AlignLeft|Qt.AlignBottom, label)
                        w = rect.width()
                        h = rect.height()
                        painter.drawText(p[0]-w-2, p[1]-h/2, w, h,
                                         Qt.AlignLeft|Qt.AlignBottom, label)
                text = 0

    def _ticks(self, lower, upper):
        ideal = (upper-lower)/7.
        if ideal == 0.:
            ideal = 1./7.
        log = Numeric.log10(ideal)
        power = Numeric.floor(log)
        fraction = log-power
        factor = 1.
        error = fraction
        for f, lf in self._multiples:
            e = Numeric.fabs(fraction-lf)
            if e < error:
                error = e
                factor = f
        grid = factor * 10.**power
        if power > 3 or power < -3:
            format = '%+7.0e'
        elif power >= 0:
            digits = max(1, int(power))
            format = '%' + `digits`+'.0f'
        else:
            digits = -int(power)
            format = '%'+`digits+2`+'.'+`digits`+'f'
        ticks = []
        t = -grid*Numeric.floor(-lower/grid)
        while t <= upper and len(ticks) < 200:
            ticks.append((t, format % (t,)))
            t = t + grid
        return ticks

    _multiples = [(2., Numeric.log10(2.)), (5., Numeric.log10(5.))]

    def _textBoundingBox(self, painter, text):
        w = self.width()
        h = self.height()
        rect = painter.boundingRect(0, h, w, h, Qt.AlignLeft|Qt.AlignBottom,
                                    text)
        return rect.width(), rect.height()

    def clear(self):
        "Clears the canvas."
        self.current_plot = None
        self.selected_range = None
        self.update()

    def redraw(self):
        "Redraws the last canvas contents."
        self.update()

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.LeftButton:
            self.startx = event.x()
            self.starty = event.y()
            self.painter = QPainter()
            self.painter.begin(self)
            self.painter.setRasterOp(Qt.XorROP)
            self.mouse_state = 0
        elif button == Qt.MidButton:
            self._showValue(event.x(), event.y())
            self.mouse_state = 3
        else:
            self.popup_menu.move(event.x(), event.y())
            self.popup_menu.show()

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        if self.mouse_state == 0:
            scale, shift = self.transformation
            p = (Numeric.array([self.startx, self.starty])-shift)/scale
            bb1, bb2 = self.bbox
            if self.selectfn is not None and p[1] < bb1[1]:
                self.painter.setPen(QPen(Qt.NoPen))
                self.painter.setBrush(QBrush(Qt.blue, Qt.Dense5Pattern))
                self.rectangle = (self.startx, 0, x-self.startx, self.height())
                self.painter.drawRect(*self.rectangle)
                self.mouse_state = 2
            elif self.zoom:
                self.painter.setPen(QPen(Qt.white, 1, Qt.DotLine))
                self.painter.setBrush(QBrush(Qt.NoBrush))
                self.rectangle = (self.startx, self.starty,
                                  x-self.startx, y-self.starty)
                self.painter.drawRect(*self.rectangle)
                self.mouse_state = 1
        elif self.mouse_state == 1 or self.mouse_state == 2:
            self.painter.drawRect(*self.rectangle)
            if self.mouse_state == 1:
                self.rectangle = (self.startx, self.starty,
                                  x-self.startx, y-self.starty)
            elif self.mouse_state == 2:
                self.rectangle = (self.startx, 0, x-self.startx, self.height())
            self.painter.drawRect(*self.rectangle)
        elif self.mouse_state == 3:
            scale, shift = self.transformation
            point = Numeric.array([x, y])
            point = (point-shift)/scale
            self.value_label.setText(" x = %f\n y = %f" % tuple(point))

    def mouseReleaseEvent(self, event):
        button = event.button()
        if button == Qt.LeftButton:
            if self.mouse_state != 0:
                self.painter.drawRect(*self.rectangle)
            self.painter.end()
            if self.mouse_state == 1:
                x = event.x()
                y = event.y()
                p1 = Numeric.array([self.startx, self.starty])
                p2 = Numeric.array([event.x(), event.y()])
                if Numeric.minimum.reduce(Numeric.fabs(p1-p2)) > 5:
                    scale, shift = self.transformation
                    p1 = (p1-shift)/scale
                    p2 = (p2-shift)/scale
                    graphics, xaxis, yaxis = self.current_plot
                    if xaxis is not None:
                        xaxis = (p1[0], p2[0])
                    if yaxis is not None:
                        yaxis = (p2[1], p1[1])
                    self.clear()
                    self.draw(graphics, xaxis, yaxis)
            elif self.mouse_state == 2:
                scale, shift = self.transformation
                x1 = (self.startx-shift[0])/scale[0]
                x2 = (event.x()-shift[0])/scale[0]
                if x1 < x2:
                    self.selected_range = (x1, x2)
                else:
                    self.selected_range = (x2, x1)
                if self.selectfn is not None:
                    self.selectfn(self.selected_range)
            self.mouse_state = 0
        elif button == Qt.MidButton:
            self._hideValue()
        else:
            pass

    def select(self, range):
        """Shows the given |range| as highlighted. |range| can be
        None (no selection) or a sequence of two values on the
        x-axis."""
        if range is None:
            self.selected_range = None
        else:
            self.selected_range = range
        self.update()

    def _popupMenu(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def _autoScale(self):
        if self.current_plot is not None:
            graphics, xaxis, yaxis = self.current_plot
            if xaxis is not None:
                xaxis = 'automatic'
            if yaxis is not None:
                yaxis = 'automatic'
            self.clear()
            self.draw(graphics, xaxis, yaxis)

    def _xmgr(self):
        if self.current_plot is not None:
            import os, tempfile
            filename = tempfile.mktemp()
            file = open(filename, 'w')
            graphics, xaxis, yaxis = self.current_plot
            graphics.writeToFile(file, '!\n')
            file.close()
            os.system('xmgrace ' + filename + ' &')
            os.unlink(filename)

    def _showValue(self, x, y):
        scale, shift = self.transformation
        point = Numeric.array([x, y])
        point = (point-shift)/scale
        self.value_label.setText(" x = %f\n y = %f" % tuple(point))
        self.value_label.show()

    def _hideValue(self):
        self.value_label.hide()


if __name__ == '__main__':

    data1 = 2.*Numeric.pi*Numeric.arange(200)/200.
    data1.shape = (100, 2)
    data1[:,1] = Numeric.sin(data1[:,0])
    lines1 = PolyLine(data1, color='green')

    pi = Numeric.pi
    lines2 = PolyLine([(0., 0.), (pi/2., 1.), (pi, 0.), (3.*pi/2., -1),
                       (2.*pi, 0.)], color='red')

    markers = PolyMarker([(0., 0.), (pi/2., 1.), (pi, 0.), (3.*pi/2., -1),
                          (2.*pi, 0.)], color='blue', fillcolor='blue', 
                         marker='plus')

    object = PlotGraphics([lines1, lines2, markers])

    def display(value):
        c.select(value)
        print value

    import sys
    app = QApplication(sys.argv)

    c = PlotCanvas(zoom=1, select=display)
    c.draw(object, 'automatic', 'automatic')

    app.setMainWidget(c)
    c.show()
    app.exec_loop()
