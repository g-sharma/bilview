#!/bin/python
#***********************************************************************
# Written By Gagan Sharma :
# August 10th 2013, Department of Radiology, The University of Melbourne
# Australia
#***********************************************************************
"""
Read DICOM Images and open it in a viewer.

Usage:  python bilview.py -input directory-name

"""

import numpy as np
import scipy
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import dicom
import os
import sys


# check command line arguments make sense
if not 1 < len(sys.argv) < 4:
    print(__doc__)
    sys.exit()


app = QtGui.QApplication([])

## Create window with two ImageView widgets
win = QtGui.QMainWindow()
win.resize(512,512)
win.setWindowTitle('BILVIEW')
cw = QtGui.QWidget()
win.setCentralWidget(cw)
l = QtGui.QGridLayout()
cw.setLayout(l)
imv1 = pg.ImageView()
l.addWidget(imv1, 0, 0)
win.show()

roi = pg.LineSegmentROI([[10, 64], [120,64]], pen='r')

fileList=[]
rootdir= sys.argv[1]

if os.path.isdir(rootdir):
	for root,dir,files in os.walk(rootdir):
    		for ieach in files:
        		fileList.append(os.path.join(rootdir,ieach))
	ds=dicom.read_file(fileList[0])
	imagedata=np.zeros((ds.pixel_array.shape[0],ds.pixel_array.shape[1],len(fileList)))
	ipos=np.zeros(len(fileList))

	for each in range(len(fileList)):
    		ds=dicom.read_file(fileList[each])
    		imagedata[:,:,each]=ds.pixel_array
		ipos[each]=ds.InstanceNumber 
else:	
	print "Please provide directory path...."
	exit(1)

# This is the key. Got it from Brad and Soren's code.Pretty Kewl..
ipos=ipos.argsort()
imagedata=imagedata[:,:,ipos]
#############################################################

data=(imagedata.transpose())

def update():
    global data, imv1#, imv2
    d2 = roi.getArrayRegion(data, imv1.imageItem, axes=(1,2))
    
roi.sigRegionChanged.connect(update)


## Display the data
imv1.setImage(data)
imv1.setHistogramRange(-0.01, 0.01)
imv1.setLevels(-0.003, 0.003)

update()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
