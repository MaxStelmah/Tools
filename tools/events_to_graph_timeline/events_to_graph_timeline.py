"""---------------------------------------------------------------------------------------------

    Using Matplotlib this program creates a Graphic timeline to compare and inspect some algorithms results.
    For instance, I use it to inspect new versions of computer vision algorithms. 
    To compare two algorithms, you need to specify two folders wich contains results with file log and images on lines 511 and 523.

--------------------------------------------------------------------------------------------"""


import matplotlib.pyplot as plt
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox, AnchoredText)
from matplotlib.cbook import get_sample_data
from random import choice
import easygui

import sys
from pathlib import Path
# Get the project root directory
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from libs.images import images
from libs.logs import parsing_logs

"""----------------------------------------------------------------------------------------

Class PlotViewer for creating a window with mathplot objects. 
The class contains methods for render windows and managing it with a keyboard and a mouse.

-------------------------------------------------------------------------------------------"""

class PlotViewer:
    def __init__(self,left_edge_of_view, right_edge_of_view, plt):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.grid_visible = 2
        self.help_visible = False
        self.first_click = True
        self.plotObjects =[]
        self.plt = plt
        self.fig = self.plt.figure()
        self.ax = self.fig.add_subplot(111)
        # Set the display limits default
        self.ax.set_ylim(0, 2)
        self.ax.set_xlim(left_edge_of_view, right_edge_of_view)  #track1.getFirstElementX() - 20, track1.getFirstElementX() + track1.getMinDeltaX() * 2
        # Naming the x axis
        self.plt.xlabel('x - time')
        self.plt.title('Timeline')
        self.scale = 1.5

    def show(self):
        self.plt.legend()
        self.plt.minorticks_on()
        self.ax.xaxis.grid()
        self.ax.yaxis.grid(False)
        self.plt.show()

    def ax(self):
        return self.ax

    def zoom_factory(self, base_scale = 1.5):
        def zoom(event):
            if base_scale != 1.5 :
                self.scale == base_scale
            cur_xlim = self.ax.get_xlim()
            # cur_ylim = self.ax.get_ylim()

            xdata = event.xdata # get event x location
            # ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / self.scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = self.scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            # new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            # rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            self.ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            # self.ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            self.ax.figure.canvas.draw()

        fig = self.ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def shift_factory(self, shiftDelta = 10):
        def shift(event):
            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()

            if event.key == 'left':
                # deal with shift left
                self.ax.set_xlim(cur_xlim[0] - shiftDelta, cur_xlim[1] - shiftDelta)
            elif event.key == 'right':
                # deal with shift right
                self.ax.set_xlim(cur_xlim[0] + shiftDelta, cur_xlim[1] + shiftDelta)

            # self.ax.set_ylim()
            self.ax.figure.canvas.draw()

        fig = self.ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('key_press_event', shift)

        return shift

    def pan_factory(self):
        def onPress(event):
            if event.inaxes != self.ax: return
            self.cur_xlim = self.ax.get_xlim()
            self.cur_ylim = self.ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            self.ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != self.ax: return
            dx = event.xdata - self.xpress
            # dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            # self.cur_ylim -= dy
            self.ax.set_xlim(self.cur_xlim)
            # self.ax.set_ylim(self.cur_ylim)

            self.ax.figure.canvas.draw()

        fig = self.ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion

    def createPlotLinks(self):
        def onRightClick(event):
            if event.button == 3:
                if event.inaxes != self.ax: return
                pLink = plotLine()
                numberObj = 0
                if self.first_click == True:
                    self.first_click = False
                    pLink.appendPoint(self.press[2],self.press[3])
                    self.plotObjects.append(pLink)
                    numberObj = len(self.plotObjects)
                    self.plotObjects[numberObj - 1].draw(self.ax)

                elif self.first_click == False:
                    self.first_click = True
                    self.plotObjects[numberObj-1].appendPoint(self.press[2],self.press[3])
                    self.plotObjects[numberObj-1].draw(self.ax)

        # attach the call back
        self.fig.canvas.mpl_connect('button_press_event', onRightClick)

        #return the function
        return onRightClick

    def keyboardProcessing(self):
        def ifKeyboardSent(event):
            if event.key == 'g' or event.key == 'п':
                if self.grid_visible == 2:
                    self.ax.xaxis.grid(False, which='minor')
                    self.ax.xaxis.grid(False, which='major')
                    self.ax.yaxis.grid(False)
                    self.grid_visible = 0
                elif self.grid_visible == 1:
                    self.ax.xaxis.grid(True, which='minor', linestyle = ':')
                    self.ax.yaxis.grid(False)
                    self.grid_visible = 2
                elif self.grid_visible == 0:
                    self.ax.xaxis.grid(True, which='major')
                    self.ax.yaxis.grid(False)
                    self.grid_visible = 1
            if event.key == 'h' or event.key == 'р':
                    # pymsgbox.alert('But does not support russian language', 'Simple alert')
                    str1 = 'Arrows or left m. button - panning the Timeline\n\nScroll - scaling the Timeline\n\n"G" - show/hide grids\n\nDrawing lines: click right m. button to drawing start point of the line and click right m. button again to finish the line\n\n'
                    str2 = 'Ctrl+Z - cancel the last drawn line\n\nIf there are the same events between timetracks, you will see a green line between them.\nIf the time of events is the same, but the pictures(or rects on them) are different - you will see a red line'
                    str = str1 + str2  #' -*- coding: utf-8 -*- '
                    easygui.msgbox(str, "Help", 'Close', "D:/MyScripts/ico.png")
            if event.key == 'ctrl+z':
                self.plotObjects[-1].hide(self.ax)
                self.ax.figure.canvas.draw()

        fig = self.ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('key_press_event', ifKeyboardSent)

        return ifKeyboardSent

    def findMatches(self, trackXY1, trackXY2, listImg1, listImg2):
        listX1, listY1, label1 = trackXY1
        listX2, listY2, label2 = trackXY2
        numElementsList1 = len(listX1)
        numElementsList2 = len(listX2)
        timeMatchedButDifFrame = 0
        fullMatched = 0

        for i in range(0, numElementsList1):
            for j in range(0, numElementsList2):
                if listX1[i] == listX2[j]:
                    diff = images.compareTwoImages(listImg1[i], listImg2[j]) # compare images
                    if diff == 0:                                     # if match than draw a green line between them
                        pLink = plotLine('g',5)
                        pLink.appendPoint(listX1[i], listY1[i])
                        pLink.appendPoint(listX2[j], listY2[j])
                        pLink.draw(self.ax)
                        fullMatched += 1
                    else:                                             # if images don't match than draw a red line
                        pLink = plotLine('r', 5)
                        pLink.appendPoint(listX1[i], listY1[i])
                        pLink.appendPoint(listX2[j], listY2[j])
                        pLink.draw(self.ax)
                        timeMatchedButDifFrame += 1
        return timeMatchedButDifFrame, fullMatched

    def showDescription(self, str):
        at = AnchoredText(
            str,
            prop=dict(size=15), frameon=True,
            loc='upper left',
            )
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        self.ax.add_artist(at)

"""---------------------------------------------------------------------------------------------------------------

Class plotPoint uses MathPlot lib for drawing points and Offsetboxes with Images or Titles on the matplot axes

----------------------------------------------------------------------------------------------------------------"""
class plotPoint(object):
    def __init__(self , x = 0., y = 0., offsetBoxTitle = '' ,offsetboxImage = '' ,**kw ):
        super(plotPoint, self).__init__(**kw)
        self.x = x
        self.y = y
        self.offsetboxTitle = offsetBoxTitle
        self.fileOffsetboxImage = offsetboxImage


    def drawPoint(self, ax):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.x, self.y, ls="", marker="o")

    def drawOffsetbox(self, type, ax):
        if type == 'txt':
            offsetbox = TextArea(self.offsetboxTitle, minimumdescent=False)
            xy = [self.x, self.y]
            ab = AnnotationBbox(offsetbox, xy,
                                xybox=(-20, 40),
                                xycoords='data',
                                boxcoords="offset points",
                                arrowprops=dict(arrowstyle="->"))
            ax.add_artist(ab)

        elif type == 'img':
            with get_sample_data(self.fileOffsetboxImage) as file:
                arr_img = plt.imread(file, format='png')
            imagebox = OffsetImage(arr_img, zoom=0.1)
            xy = [self.x, self.y]               # coordinates to position this image
            ab = AnnotationBbox(imagebox, xy,
                xybox=(30., -30.),
                xycoords='data',
                boxcoords="offset points")
            ax.add_artist(ab)

    def getX(self):
        return int(self.x)

    def getY(self):
        return  int(self.y)

"""-----------------------------------------------------------------------------------------------

Class plotLine uses MathPlot lib for drawing lines on the matplot axes

-----------------------------------------------------------------------------------------------"""

class plotLine(object):
    def __init__(self, color = '', linewidth = 1, style = '-', **kw):
        super(plotLine, self).__init__(**kw)
        link_line = None
        self.x_array = []
        self.y_array = []
        if color == '':
            self.color = choice(['b','c','y','m'])
        else:
            self.color = color
        self.style = style
        self.linewidth = linewidth

    def hide(self, ax):

        try:
            self.link_line = ax.plot(self.x_array, self.y_array, ls=self.style, marker="o", linewidth=3,
                                     color='w')
            return 0
        except:
            print("Error during hiding"+ self.link_line)

    def appendPoint(self, x, y):
        self.x_array.append(x)
        self.y_array.append(y)

    def getplotLine(self):
        return self.x_array, self.y_array

    def draw(self, ax):
        try:
            self.link_line = ax.plot(self.x_array, self.y_array, ls=self.style, marker="o", linewidth=self.linewidth, color = self.color)
            return 0
        except:
            print("Error while drawing "+ self.link_line)

"""-----------------------------------------------------------------------------------------------

Class for drawing progressions of Events - TimeTracks on the mathplot axes. 

-----------------------------------------------------------------------------------------------"""
class TimeTrack(plotPoint, plotLine):

    def __init__(self, x = 0., y = 0., offsetBoxTitle = '' , offsetboxImage = '', color = '', linewidth = 2, style = '-'):
        super(TimeTrack, self).__init__(x = x, y = y, offsetBoxTitle = offsetBoxTitle , offsetboxImage = offsetboxImage, color = color, linewidth = linewidth, style = style )
        self.Track_line = None
        self.label = ''
        self.xPointsInsideWindow_array = []
        self.minDeltaX = 0
        self.maxDeltaX = 0
        self.medDeltaX = 0
        self.numPoints = 0
        self.offsetboxTitle_array = []
        self.lenTitles = 0
        self.fileOffsetboxImage_array = []
        self.lenImages = 0
        self.pathVideoFile = ''
        self.ax = None

    def appendPoint(self, x, y, title = '', img = ''):
        self.x_array.append(x)
        self.y_array.append(y)
        self.offsetboxTitle_array.append(title)
        self.fileOffsetboxImage_array.append(img)
        self.numPoints +=1

    def setListXPoints(self, listXPoints):
        self.x_array = listXPoints

        # calculate minimum delta X between 2 points
        self.numPoints = len(self.x_array)
        for i in range(0, self.numPoints-2):
            if self.x_array[i+1]-self.x_array[i] <=  self.x_array[i+2]-self.x_array[i+1]:
                self.minDeltaX = self.x_array[i+1]-self.x_array[i]
            else:
                self.minDeltaX = self.x_array[i + 2] - self.x_array[i+1]

        # calculate maximum delta X between 2 points
        self.numPoints = len(self.x_array)
        for i in range(0, self.numPoints-2):
            if self.x_array[i+1]-self.x_array[i] >=  self.x_array[i+2]-self.x_array[i+1]:
                self.maxDeltaX = self.x_array[i+1]-self.x_array[i]
            else:
                self.maxDeltaX = self.x_array[i + 2] - self.x_array[i+1]

        # calculate medium delta X between 2 points
        self.medDeltaX = int((self.x_array[-1]-self.x_array[0])/self.numPoints)

        #if there is no specific array of Y than every Y is default self.y
        if self.y_array == []:
            for i in self.x_array:
                self.y_array.append(self.y)

    def setListYPointsByTrackY(self):
        if self.y_array == []:
            for i in self.x_array:
                self.y_array.append(self.y)


    def setListTitles(self, listTitles):
        self.offsetboxTitle_array = listTitles
        self.lenTitles = len(self.offsetboxTitle_array)

    def setListImages(self, listImages):
            self.fileOffsetboxImage_array = listImages

    def getListImages(self):
            return self.fileOffsetboxImage_array

    def getTrack(self):
        return self.x_array, self.y_array, self.label

    def getNumPooints(self):
        return self.numPoints

    def getTitles(self):
        return self.offsetboxTitle_array

    def getLenTitiles(self):
        return self.lenTitles

    def getMinDeltaX(self):
        return self.minDeltaX

    def getFirstElementX(self):
        return self.x_array[0]

    def createLabel(self, firstStr = '', lastStr = ''):
        self.label = firstStr + '\nEvents: ' + str(self.numPoints) + '\n' \
                     + 'Minimum delta time between events: ' + str(self.minDeltaX) + 'sec.\n' \
                     + 'Medium delta time between events: ' + str(self.medDeltaX) + 'sec.\n' \
                     + 'Maximum delta time between events: ' + str(self.maxDeltaX) + 'sec.\n' \
                     + lastStr
        return self.label

    def calcPointsInsideWindow(self, ax, gap):
        cur_xlim = ax.get_xlim()
        # cur_ylim = ax.get_ylim()

        for x in self.x_array:
            if x > cur_xlim[0]-gap and x < cur_xlim[1]+gap:
                self.xPointsInsideWindow_array.append(x)
        print(self.xPointsInsideWindow_array)
        return self.xPointsInsideWindow_array

    def drawOffsetboxes(self, type, ax, state = 'all', part_array = None):

        if state == 'in_window':
            X_array = self.xPointsInsideWindow_array
        elif state != 'all':
            X_array = part_array
        else:
            X_array = self.x_array


        if type == 'txt':
            for x, title in zip(X_array, self.offsetboxTitle_array):
                offsetbox = TextArea(title)
                xy = [x, self.y]
                ab = AnnotationBbox(offsetbox, xy,
                                    xybox=(0, 15),
                                    xycoords='data',
                                    boxcoords="offset points",
                                    arrowprops=dict(arrowstyle="->"))
                ax.add_artist(ab)

        elif type == 'img':
            for x, img in zip(X_array, self.fileOffsetboxImage_array):
                with get_sample_data(img) as file:
                    arr_img = plt.imread(file, format='png')
                imagebox = OffsetImage(arr_img, zoom=0.18)       # image size
                xy = [x, self.y]                                # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy,
                                    xybox=(0., 85),
                                    xycoords='data',
                                    boxcoords="offset points"
                                    )
                ax.add_artist(ab)

        elif type == 'time':
            for x, tstamp in zip(X_array, self.x_array):
                offsetbox = TextArea(tstamp)
                xy = [x, self.y]
                ab = AnnotationBbox(offsetbox, xy,
                                    xybox=(0, -15),
                                    xycoords='data',
                                    boxcoords="offset points",
                                    arrowprops=dict(arrowstyle="->"))
                ax.add_artist(ab)

    def draw(self, ax):
        try:
            self.Track_line = ax.plot(self.x_array, self.y_array, ls="-", marker="o", linewidth=2, label=self.label)
            return self.x_array, self.y_array, self.label
        except:
            print('Err during drawing track ' + self.Track_line)

    def drawTrackWithData(self, ax):
        try:
            self.Track_line = ax.plot(self.x_array, self.y_array, ls="-", marker="o", linewidth=2, label=self.label)
            self.drawOffsetboxes('txt', ax)
            self.drawOffsetboxes('img', ax)
            self.drawOffsetboxes('time', ax)
            return self.x_array, self.y_array, self.label
        except:
            print('Err during drawing track ' + str(self.Track_line))


# ------------ Code of Timeline app ---------------------------------------------------------------------------------------

timestamps = []
titles = []
images = []

#--- add a track 1------------------------------
folderForScanningImages = "D:/Documents/GitHub/Tools/tools/events_to_graph_timeline/assets/autovision_v1/"            # 1 Address of the first TimeTrack

track1 = TimeTrack(1, 0.2)
pLog1 = parsing_logs.ParsedLog()
pLog1.fillParsedLogFromFolder(folderForScanningImages,'Rects:','INFO: Recognized:')
track1.setListXPoints(pLog1.getTimestamps())
track1.setListTitles(pLog1.getData0_list())
track1.createLabel('Track 1')
track1.setListImages(pLog1.getListImages(folderForScanningImages,'.png'))

#----add a track 2----------------------------------

folderForScanningImages = "D:/Documents/GitHub/Tools/tools/events_to_graph_timeline/assets/autovision_v2/"            # 2 Addres of the second TimeTrack

track2 = TimeTrack(1, 1.2)
pLog2 = parsing_logs.ParsedLog()
pLog2.fillParsedLogFromFolder(folderForScanningImages,'Rects:','INFO: Recognized:')
track2.setListXPoints(pLog2.getTimestamps())
track2.setListTitles(pLog2.getData0_list())
track2.createLabel('Track 2')
track2.setListImages(pLog2.getListImages(folderForScanningImages,'.png'))


#---- create plot window viewer object-------------------------------------------

pltViewer = PlotViewer(track1.getFirstElementX() - 20, track1.getFirstElementX() + track1.getMinDeltaX() * 2, plt)
figZoom = pltViewer.zoom_factory(1.5)
figShift = pltViewer.shift_factory( track1.getMinDeltaX()/2)
figPan = pltViewer.pan_factory()
figGrid = pltViewer.keyboardProcessing()
figLinks= pltViewer.createPlotLinks()



#--------draw tracks        ----------------------------------

track1.drawTrackWithData(pltViewer.ax)
track2.drawTrackWithData(pltViewer.ax)

#-------- print match statistics  ----------------------------------
matchedDiff, fullmatched = pltViewer.findMatches(track1.getTrack(),track2.getTrack(),track1.getListImages(),track2.getListImages())
pltViewer.showDescription("Same timestamp, but different rects: " + str(matchedDiff) + "\nSame recognition events: " + str(fullmatched))
#------- show all at the screen----------------------------
pltViewer.show()

