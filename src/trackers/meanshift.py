import numpy as np
import cv2 as cv
class Meanshift:

    def init (self, frame, box):
        # Set Region of interest
        self.box = box
        x,y,w,h = self.box
        self.roi = frame[y:y+h, x:x+w]
        self.hsv_roi = cv.cvtColor(self.roi, cv.COLOR_BGR2HSV)
        self.mask = cv.inRange(self.hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        self.roi_hist = cv.calcHist([self.hsv_roi],[0],self.mask,[180],[0,180])
        cv.normalize(self.roi_hist,self.roi_hist,0,255,cv.NORM_MINMAX)
        #Set up the termination criteria
        self.term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

    def update(self, frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],self.roi_hist,[0,180],1)
        #Application of CamShift
        ret, self.box = cv.meanShift(dst, self.box, self.term_crit)
        return (ret, self.box)
    
def create(config):
    return Meanshift()