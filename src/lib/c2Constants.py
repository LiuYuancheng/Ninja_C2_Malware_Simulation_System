#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        c2Constants.py [python3]
#
# Purpose:     This module is used to define all the used constants in the c2
#              malware project which used by <c2Client.py> and <c2MwUtils.py>
#              modules.
#  
# Author:      Yuancheng Liu
#
# Created:     2024/05/17
# version:     v0.2.3
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
""" For one type of state flag, the value should be unique.
    - FLG : Flag can be int or str. 
    - KEY : Key must be str type. 
    - TYPE: type must be str type.
"""

#-----------------------------------------------------------------------------
# Define all the task state here : 
TASK_P_FLG = 0  # task pending flag (Task is enqueued in the RTC2-Hub task manager's sending queue.)
TASK_F_FLG = 1  # task finish flag (Task information has been sent to related the Red-Teaming-Malicious-Action-Program.)
TASK_A_FLG = 2  # task accept flag (Task execution finished and state updated in the RTC2-Hub.)
TASK_E_FLG = 3  # task error flag (Tasks execution got error.)
TASK_R_FLG = 4  # task running flag (Tasks executing.)

#-----------------------------------------------------------------------------
# Define all the action flag here:
ACT_KEY = 'action'
ACT_GET_TASK = 'getTask'
ACT_ACCEPT_FLG = 'ok'
ACT_REJECT_FLG = 'no'

#-----------------------------------------------------------------------------
# Define all the task type here:
TSK_TYEP_RIG    = 'register'    # Task type : register agent to C2  
TSK_TYPE_CMD    = 'command'     # Task type : execute command on victim
TSK_TYPE_PING   = 'ping'      # Task type : ping the victim
TSK_TYPE_RPT    = 'report'      # Task type : report task execution result to C2
TSK_TYPE_SSH    = 'sshRun'      # Task type : use victim to ssh another victim and run cmd. 
TSK_TYPE_SCP    = 'scpFile'     # Task type : scp the victim file to another victim.
TSK_TYPE_UPLOAD = 'upload'      # Task type : upload a victim file to C2
TSK_TYPE_DOWNLOAD = 'download'  # Task type : download a file from C2 to victim
TSK_TYPE_SCANNET = 'scanSubnet'     # Task type : scan victim's subnet
TSK_TYPE_KEYBD = 'keyEvent'         # Task type : record keyboard and generate keyboard event on victim.
TSK_TYPE_SCREENST = 'screenShot'    # Task type : capture the victim screen shot.
TSK_TYPE_EAVESDP = 'eavesDrop'      # Task type : eavesDrop victim network traffic. 