#-----------------------------------------------------------------------------
# Name:        c2DataManager.py
#
# Purpose:     Data manager class used to manage all the linked program process 
#              the data submitted from the malware.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.2.2
# Created:     2023/01/11
# Copyright:   Copyright (c) 2022 LiuYuancheng
# License:     MIT License   
#-----------------------------------------------------------------------------

from collections import OrderedDict

import c2HubGlobal as gv
import c2MwUtils

# Import all the task state flag
from c2Constants import TASK_P_FLG, TASK_F_FLG, TASK_A_FLG, TASK_E_FLG, TASK_R_FLG
# Import the action constents
from c2Constants import ACT_KEY, ACT_GET_TASK, ACT_ACCEPT_FLG, ACT_REJECT_FLG
# Import the task type
from c2Constants import TSK_TYEP_RIG, TSK_TYPE_RPT, TSK_TYPE_UPLOAD, TSK_TYPE_DOWNLOAD, TSK_TYPE_CMD

SCH_ID_PREFIX = 'Emu'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(object):
    """ The data manager is the module contents all the malware record obj and 
        control all the data display on the web.
    """
    def __init__(self, parent) -> None:
        self.parent = parent
        self.idCount = 0
        # malware data record dict.
        self.malwareRcdDict = OrderedDict()
        
    #-----------------------------------------------------------------------------
    def addMalware(self, malwareID, ipaddres, taskList=[]):
        """ Add a new malware record in the list."""
        if str(malwareID) in self.malwareRcdDict.keys():
            gv.gDebugPrint("Malware ID: %s is already in record" %str(malwareID), 
                           prt=True, logType=gv.LOG_INFO)
            self.malwareRcdDict[malwareID].updateRegisterT()
            return False
        else:
            self.malwareRcdDict[str(malwareID)] = c2MwUtils.mwServerRcd(self.idCount, malwareID, ipaddres, 
                                                                 taskList=taskList)
            self.idCount += 1
            gv.gDebugPrint("Added Malware ID: %s in data manager." %str(malwareID), 
                           prt=True, logType=gv.LOG_INFO)
            self.broadcast2SioClients('pagerefersh', {'data': 'malwaremgmt'})
            return True 

    #-----------------------------------------------------------------------------
    def addTaskToMalware(self, malwareIdx, taskJson):
        """ Add a new task to the malware assignment task queue
            Args:
                malwareIdx (int): malware idx in the manager.
                taskJson (dict): task json example: 
                {
                    'taskType': c2Constants.TSK_TYPE_DOWNLOAD
                    'startT': None,
                    'repeat': 1,
                    'exePreT': 0,
                    'state' : c2Constants.TASK_A_FLG,
                    'taskData': ['2023-12-13_100327.png','NCL_SGX Service.docx']
                }
        """
        malwareIdx = int(malwareIdx)
        malwareIdList = list(self.malwareRcdDict.keys())
        if 0 <= malwareIdx <= len(malwareIdList):
            malwareID = malwareIdList[malwareIdx]
            return self.addTaskToRcdDict(malwareID, taskJson)
        else:
            return False

    #-----------------------------------------------------------------------------
    def addTaskToRcdDict(self, malwareID, taskJson):
        """ Add a new task to malware based on the malware ID.
            Args:
                malwareID (str):  malware's unique ID.
                taskJson (dict): refer to function <addTaskToMalware> input para taskJson.
            Returns:
                _type_: _description_
        """
        if malwareID in self.malwareRcdDict.keys():
            return self.malwareRcdDict[malwareID].addNewTask(taskJson)
        else: 
            gv.gDebugPrint("Malware ID: %s not exist." %str(malwareID), 
                prt=True, logType=gv.LOG_INFO)
            return False

    #-----------------------------------------------------------------------------
    def getMwLastTaskRst(self, malwareID):
        """ Return the malware's last tasks execution result.
            Args:
                malwareID (str): malware's unique ID.
        """
        if malwareID in self.malwareRcdDict.keys():
            return self.malwareRcdDict[malwareID].getLastTaskRst()
        else: 
            gv.gDebugPrint("Malware ID: %s not exist." %str(malwareID), 
                prt=True, logType=gv.LOG_INFO)
            return None
    
    #-----------------------------------------------------------------------------
    def buildPeerInfoDict(self, peerIdx):
        """ Build the peer all information dictionary based on the input peer index.
            Args:
                peerId (int): malware index in data manager.
            Returns:
                None - if the malware idx is not exist
                peerInfoDict = {
                    "idx"       : peerIdx,
                    "name"      : peerId,
                    "connected" : recordData['connected'],
                    "updateT"   : recordData['updateT'],
                    "tasks"     : tasksData,
                }
        """
        peerIdx = int(peerIdx)
        if peerIdx >= len(self.malwareRcdDict.keys()): return None
        peerId = list(self.malwareRcdDict.keys())[peerIdx]
        recordObj = self.malwareRcdDict[peerId]
        recordData = recordObj.getRcdInfo()
        tasksData = recordObj.getTaskList()
        lastTaskRst = recordObj.getLastTaskRst()
        peerInfoDict = {
            "idx"       : peerIdx,
            "name"      : peerId,
            "connected" : recordData['connected'],
            "updateT"   : recordData['updateT'],
            "tasks"     : tasksData,
            "result"    : lastTaskRst,
        }
        return peerInfoDict

    #-----------------------------------------------------------------------------
    def handleRequest(self, reqDict):
        """ Handle all the GET/POST requests data flask-app got."""
        reqDict = dict(reqDict)
        id = reqDict['id']
        data = reqDict['data']
        # malware register request  
        if reqDict[ACT_KEY] == TSK_TYEP_RIG:
            ipaddr = data['ipaddr']
            taskList = data['tasks']
            self.addMalware(id, ipaddr, taskList=taskList)
            return {ACT_KEY: TSK_TYEP_RIG,'state': TASK_F_FLG}
        # file upload request
        elif reqDict['action'] == TSK_TYPE_UPLOAD:
            # send the upload file request accept flag
            return {TSK_TYPE_UPLOAD: ACT_ACCEPT_FLG}
        # file download request
        elif reqDict['action'] == TSK_TYPE_DOWNLOAD:
            return { TSK_TYPE_DOWNLOAD: ACT_ACCEPT_FLG}
        # state report request
        elif reqDict['action'] == TSK_TYPE_RPT:
            self.updateTaskState(id, data)
            return { TSK_TYPE_RPT: ACT_ACCEPT_FLG}
        # malware task fetch request
        elif reqDict['action'] == ACT_GET_TASK:
            if id in self.malwareRcdDict.keys():
                mvObj = self.malwareRcdDict[id]
                taskList = mvObj.getTaskList(taskState=TASK_P_FLG)
                if len(taskList) > 0:
                    task = taskList[0]
                    tskId = task['taskID']
                    rst = mvObj.setTaskState(tskId, state=TASK_A_FLG)
                    if rst : self.broadcast2SioClients('pagerefersh', {'data': 'peerstate', 'malwareID':id})
                    return {'task': task}
            return None
        else:
            return None 
    #-----------------------------------------------------------------------------
    def getMalwaresInfo(self, malwareIDList=None):
        """ Return a list of malware summary information."""
        if malwareIDList is None: malwareIDList = self.malwareRcdDict.keys() 
        return [self.getMalwareDetail(pName) for pName in malwareIDList] 

    def getMalwareDetail(self, peerName):
        if peerName in self.malwareRcdDict.keys():
            return self.malwareRcdDict[peerName].getRcdInfo()
        return {}

    def updateTaskState(self, malId, reportInfo):
        if malId in self.malwareRcdDict.keys():
            self.malwareRcdDict[malId].updateTaskRcd(reportInfo)
            self.broadcast2SioClients('pagerefersh', {'data': 'peerstate', 'malwareID':malId})
    
    #-----------------------------------------------------------------------------
    def broadcast2SioClients(self, msgTag, dataJson):
        """ Broadcast the control data Json to all the connected socketIO client."""
        if gv.iSocketIO:
            try:
                gv.iSocketIO.emit(str(msgTag), dict(dataJson))
                return True
            except Exception as err: 
                gv.gDebugPrint("Sio broadcast Error: %s" %str(err))
                return False 