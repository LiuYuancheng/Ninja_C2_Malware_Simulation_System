
#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        mouseEventActor.py
#
# Purpose:     This module will provide function to record and playback user's 
#              mouse action and use CV to detect the match area in the screen and 
#              move mouse to the position to click. 
# 
# Author:      Yuancheng Liu
#
# Version:     v_0.0.2
# Created:     2022/01/11
# Copyright:   Copyright (c) 2022 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
"""
    This simple module is used to turn off the firewall and windefender in LS2022:
    1. Use "win32gui" (input the app name/filename)  to make the app window show in the front ground above all other windows. 
    2. Use "pyscreenshot" capture the screen shot. 
    3. Use the "openCV cv2" to find the screen shot position(x, y) which matches the text field/button template we want to find. 
    4. Use the "mouse" to move the mouse cursor to the position(x,y) and click. 
    5. Use the "keyboard" to input the pre-setup text.
"""
import os 
import cv2
import time
from datetime import datetime
import threading

import mouse
import pyscreenshot

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)

DEF_DATA_DIR = 'data'
DEF_SS_NAME = 'screenshot.png' # default screenshot name 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class mouseRecorder(threading.Thread):
    """ Module used to record the user's mouse trace and click actions and play 
        back in background thread. 
    """
    def __init__(self, threadID=None) -> None:
        """ Init example: 
                recorder = mouseRecorder()
                recorder.start()
            Args:
                threadID (int, optional): thread ID for multi-threading managment. 
                    Defaults to None.
        """
        threading.Thread.__init__(self)
        self.threadID = 0 if not threadID else threadID
        self.eventList = [] # list to record the mouse event
        self.recordingFlg = False
        self.playingFlg = False
        self.terminate = False 

    #-----------------------------------------------------------------------------
    def clearRecord(self):
        self.eventList = []

    def getthreadID(self):
        return self.threadID

    def getRecord(self):
        return self.eventList

    #-----------------------------------------------------------------------------
    def run(self):
        """ Thread running background loop to playback mouse trace. """
        while(not self.terminate):
            if self.playingFlg:
                if len(self.eventList):
                    print("Start to playback the record.")
                    mouse.play(self.eventList)
                else:
                    print("Warning: the mouse event list is empty. Please record it first.")
            else:
                time.sleep(1)
    
    #-----------------------------------------------------------------------------
    def startNewRecord(self):
        """ Start a new mouse event recording."""
        if self.recordingFlg:
            print("Warning: the mouse event is already recording. Please stop it first.")
            return False
        else:
            self.clearRecord()
            mouse.hook(self.eventList.append)
            self.recordingFlg = True
            return True

    #-----------------------------------------------------------------------------
    def stopRecord(self):
        if self.recordingFlg:
            mouse.unhook(self.eventList.append)
            self.recordingFlg = False
            return True
        else:
            print("Warning: the mouse event is not recording. Please start it first.")
            return False

    #-----------------------------------------------------------------------------
    def startPlayback(self):
        if self.playingFlg:
            print("Warning: the mouse event is already playing. Please stop it first.")
            return False
        else:
            if self.recordingFlg: self.stopRecord() # stop record before playback
            self.playingFlg = True

    def stop(self):
        self.terminate = True 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class screenPosClicker(object):
    def __init__(self) -> None:
        self.dataDir = os.path.join(dirpath, 'data')
        if not os.path.isdir(self.dataDir): os.mkdir(self.dataDir)
        self.clickTemplatePath = None 

    #-----------------------------------------------------------------------------
    def findTemplatePos(self, srcImgPath, templatePath, recordRst=False):
        """ Find the template image center position in the source image.
            Args:
                srcImgPath (str): source image path
                templatePath (str): template need to find image path.
                recordRst (bool, optional): flag to identify whether mark result on 
                    source file. Defaults to False.
            Returns:
                (int, int): center position (x, y) to find the template image. if any 
                    x or y < 0, it means the template image is not found in the source.
        """
        srcImg = cv2.imread(srcImgPath)
        srcGray = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)

        tmpImg = cv2.imread(templatePath, 0)

        result = cv2.matchTemplate(srcGray, tmpImg, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        height, width = tmpImg.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)
        pos_XY = (int((top_left[0]+bottom_right[0])/2),
                  int((top_left[1]+bottom_right[1])/2))
        # Draw detection result on the src image
        if recordRst:
            print("Draw detection result on the src image")
            cv2.rectangle(srcImg, top_left, bottom_right, (0, 0, 255), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.7
            org = (top_left[0], top_left[1]-10)
            rstImage = cv2.putText(srcImg, 'find match: at %s' % str(pos_XY), org, font,
                                fontScale, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite(srcImgPath, rstImage)

        return pos_XY

    #-----------------------------------------------------------------------------
    def setClickTemplate(self, templatePath):
        if os.path.exists(templatePath):
            self.clickTemplatePath = templatePath
        else:
            print("Error, the click template image file is not exist")

    #-----------------------------------------------------------------------------
    def findAndClick(self, recordRst=False):
        """ Find the template image center position in the source image and click 
            the position.
        """
        # screen short current desktop
        screenshot = pyscreenshot.grab()
        filename = 'screenshot_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.png' if recordRst else DEF_SS_NAME
        filePath = os.path.join(self.dataDir, filename)
        screenshot.save(filePath)
        if self.clickTemplatePath: 
            pos_XY = self.findTemplatePos(filePath, self.clickTemplatePath, recordRst=recordRst)
            if pos_XY[0] >=0 and pos_XY[1] >=0:
                print("Find matched click position: %s" % str(pos_XY))
                mouse.move(pos_XY[0], pos_XY[1])
                time.sleep(0.2)
                mouse.click()
            else:
                print("Warning: didn't find match click position")
        else:
            print("Warning: didn't set click template image")

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode):
    templateFile = os.path.join(dirpath, 'template.png')
    clicker = screenPosClicker()
    recorder = mouseRecorder()
    recorder.start()
    clicker.setClickTemplate(templateFile)
    if mode == 0:
        print("Test case 0: test click without recording detection result")
        clicker.findAndClick(recordRst=False)
    elif mode == 1:
        print("Test case 1: test click with recording detection result in data folder.")
        clicker.findAndClick(recordRst=True)
    elif mode == 2:
        print("Test case 2: test record and play back mouse trace for 10 sec")
        recorder.startNewRecord()
        for i in range(10):
            time.sleep(1)
            print("record end in %s sec." % str(10-i))
        recorder.stopRecord()
        recorder.startPlayback()
        for i in range(12):
            time.sleep(1)
            print("playback end in %s sec." % str(12-i))
        recorder.stop()
    else:
        print("Error: unknown test case: %s" %str(mode))
        pass
    recorder.stop()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    print("Input the test mode:")
    print("0: test click without recording detection result")
    print("1: test click with recording detection result in data folder.")
    print("2: test record and play back mouse trace for 10 sec")
    mode = int(input())
    testCase(mode)
